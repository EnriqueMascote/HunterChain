#!/usr/bin/env python3
"""HunterChain G0 health probe. Python >=3.10, standard library only.

Use only against a disposable Ethereum-package/Kurtosis devnet.
EL and CL URLs are host-forwarded LOCAL endpoints (never Engine API 8551).
"""
import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request


def request_json(url, body=None):
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        url, data=json.dumps(body).encode() if body is not None else None,
        headers=headers, method="POST" if body is not None else "GET"
    )
    with urllib.request.urlopen(req, timeout=12) as response:
        return json.load(response)


def rpc(url, method):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": []}
    result = request_json(url, payload)
    if "error" in result:
        raise RuntimeError(f"{method}: {result['error']}")
    return result["result"]


def beacon(url, path):
    result = request_json(url.rstrip("/") + path)
    return result["data"]


def snapshot(el, cl):
    el_height = int(rpc(el, "eth_blockNumber"), 16)
    chain_id = int(rpc(el, "eth_chainId"), 16)
    latest_header = request_json(el, {
        "jsonrpc": "2.0", "id": 2, "method": "eth_getBlockByNumber",
        "params": ["latest", False]
    })["result"]
    genesis = beacon(cl, "/eth/v1/beacon/genesis")
    head = beacon(cl, "/eth/v1/beacon/headers/head")
    checkpoints = beacon(cl, "/eth/v1/beacon/states/head/finality_checkpoints")
    active = beacon(cl, "/eth/v1/beacon/states/head/validators?status=active_ongoing")
    return {
        "observed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "chain_id": chain_id,
        "execution_block_number": el_height,
        "execution_block_hash": latest_header["hash"],
        "base_fee_per_gas_wei": int(latest_header.get("baseFeePerGas", "0x0"), 16),
        "beacon_head_slot": int(head["header"]["message"]["slot"]),
        "beacon_genesis_time": int(genesis["genesis_time"]),
        "genesis_validators_root": genesis["genesis_validators_root"],
        "justified_epoch": int(checkpoints["current_justified"]["epoch"]),
        "finalized_epoch": int(checkpoints["finalized"]["epoch"]),
        "active_validators": len(active),
    }


def main():
    p = argparse.ArgumentParser(description="Probe Besu EL and Teku CL for G0 acceptance")
    p.add_argument("--el", required=True, help="Host-mapped Besu JSON-RPC URL")
    p.add_argument("--cl", required=True, help="Host-mapped Teku Beacon REST URL")
    p.add_argument("--validators", type=int, default=7, help="Expected active genesis validators")
    p.add_argument("--wait", type=int, default=1100, help="Max seconds waiting for finality")
    p.add_argument("--interval", type=int, default=15)
    p.add_argument("--output", default="", help="Save last probe result to JSON file")
    args = p.parse_args()

    deadline = time.monotonic() + args.wait
    while True:
        try:
            record = snapshot(args.el.rstrip("/"), args.cl.rstrip("/"))
            passed = (record["execution_block_number"] > 0
                      and record["active_validators"] == args.validators
                      and record["finalized_epoch"] > 0)
            record["g0_pass"] = passed
            print(json.dumps(record, ensure_ascii=False), flush=True)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(record, f, ensure_ascii=False, indent=2)
                    f.write("\n")
            if passed:
                return 0
        except (ValueError, KeyError, RuntimeError, urllib.error.URLError,
                OSError, TypeError) as ex:
            print(f"not ready: {ex}", file=sys.stderr, flush=True)
        if time.monotonic() >= deadline:
            print("G0 did not achieve observed finality before deadline", file=sys.stderr)
            return 1
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
