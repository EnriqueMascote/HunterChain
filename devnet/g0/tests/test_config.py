"""Static checks for HunterChain G0 configuration (not a consensus integration test)."""
import pathlib
import unittest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = ROOT / "kurtosis.yaml"


class GenesisPilotConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))

    def test_seven_besu_teku_participants(self):
        entries = self.config["participants"]
        self.assertEqual(len(entries), 1)
        node = entries[0]
        self.assertEqual(node["el_type"], "besu")
        self.assertEqual(node["cl_type"], "teku")
        self.assertEqual(node["count"], 7)
        self.assertEqual(node["validator_count"], 1)

    def test_validator_registration_matches_nodes(self):
        params = self.config["network_params"]
        self.assertEqual(params["preregistered_validator_count"], 7)
        self.assertEqual(params["num_validator_keys_per_node"], 1)
        self.assertEqual(params["seconds_per_slot"], 12)
        self.assertNotEqual(str(params["network_id"]), "1")

    def test_pilot_is_disposable(self):
        self.assertIs(self.config["persistent"], False)
        self.assertIs(self.config["wait_for_finalization"], False)

    def test_no_seed_in_our_configuration(self):
        raw = CONFIG.read_text(encoding="utf-8").lower()
        self.assertNotIn("preregistered_validator_keys_mnemonic:", raw)
        self.assertNotIn("private_key:", raw)
        self.assertNotIn("secretkey:", raw)


if __name__ == "__main__":
    unittest.main()
