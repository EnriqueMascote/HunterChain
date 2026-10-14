# HunterChain — G0: Devnet PoS desechable

**Estado:** scaffold publicado / ejecución pendiente. **No se ha arrancado ni validado aún.**

Esta carpeta pone a prueba una red EVM PoS con **siete parejas Besu + Teku**, una clave de validador de prueba por participante, slots de 12 s y epoch normal de 32 slots (sujeto a verificación por la CL). El objetivo NO es crear todavía los 2,500 HNT definitivos, ni generar secretos de alumnos, ni preservar la red entre clases.

## 1. Requisitos

**Equipo piloto:** computadora del profesor con RAM suficiente para siete clientes EL y siete CL; no se debe ejecutar esta topología en un host de 8 GB. Requiere Docker Engine/Desktop activo, [Kurtosis CLI](https://docs.kurtosis.com/install/), Git, Python >= 3.10.

Los 8 GB se medirán **por pareja Besu+Teku en el equipo más modesto**, no levantando siete parejas en él. Quien no supere la prueba participará mediante **wallet ligera y portal**, sin validador local.

Clonar el repositorio:
```bash
git clone https://github.com/EnriqueMascote/HunterChain.git
cd HunterChain
docker version
kurtosis version
python3 --version
```

En Windows se puede utilizar PowerShell para Kurtosis y Docker Desktop; para los scripts Python usar `py -3` en lugar de `python3` si procede.

## 2. Levantar siete nodos Besu/Teku (G0.1)

Se fija una revisión específica del paquete Ethereum de ethPandaOps para reproducir su esquema. El contenido del archivo `kurtosis.yaml` usa los campos documentados `participants.count`, `validator_count`, `network_params.num_validator_keys_per_node` y `preregistered_validator_count`. Si el paquete informa que siete validadores son insuficientes para el perfil elegido, **no aumentarlos silenciosamente**; documentar la incompatibilidad y abrir un ADR de preset/forks.

```bash
kurtosis engine start
kurtosis run github.com/ethpandaops/ethereum-package@69dcfbbcbde1ce91a6d0790c8150c84de55e3b2b \
  --enclave hunterchain-g0 \
  --args-file devnet/g0/kurtosis.yaml
```

El arranque puede descargar varias imágenes grandes y tardar minutos. Por defecto, Kurtosis genera **claves de prueba derivadas de material conocido**. Nunca llevarlas a HunterChain definitiva. No se incluyen semillas privadas en este repositorio.

Observar servicios, direcciones HTTP/puertos locales y logs:
```bash
kurtosis enclave inspect hunterchain-g0
kurtosis enclave ls
kurtosis service logs hunterchain-g0 <nombre-de-servicio-teku>
kurtosis service logs hunterchain-g0 <nombre-de-servicio-besu>
```

**Nota:** los nombres reales de servicio, endpoints y puertos los asigna Kurtosis; leerlos de `enclave inspect`. No asumir que `8545` y `5051` están expuestos en el host directamente: pueden mapearse a puertos efímeros.

## 3. Comprobación G0.1: bloques + validadores + finalidad

Identificar en `kurtosis enclave inspect hunterchain-g0`:
- **EL:** URL HTTP local del JSON-RPC de un servicio Besu (NO la Engine API 8551).
- **CL:** URL HTTP local de REST Beacon API de un servicio Teku.

Con ambas URL, correr:
```bash
python3 devnet/g0/probe.py \
  --el http://127.0.0.1:<PUERTO_EL> \
  --cl http://127.0.0.1:<PUERTO_CL> \
  --validators 7 \
  --wait 1100 \
  --output g0-probe-local.json
```

En Windows:
```powershell
py -3 devnet/g0/probe.py --el http://127.0.0.1:<PUERTO_EL> --cl http://127.0.0.1:<PUERTO_CL> --validators 7 --wait 1100 --output g0-probe-local.json
```

**Éxito observable (por ahora):**
1. `eth_blockNumber > 0`.
2. `eth_chainId` responde y se registra.
3. Beacon REST responde con `genesis_validators_root` y `head slot`.
4. Hay exactamente 7 validadores `active_ongoing`.
5. `finalized_epoch > 0`.

**Nota:** una epoch tiene 32 slots de 12 s = 384 s. La finalidad normal tarda múltiples epochs; esperar al menos 13–18 minutos antes de clasificar como falla definitiva.

**Si falla:** conservar salidas de consola (sin secretos), nombres/versiones/digests de imágenes, errores de génesis, archivos de configuración y resultado del probe. Cambios en fork, número de validadores o tiempo de slot deben quedar en nuevo ADR.

## 4. Métricas de memoria para el piloto

En otra terminal del profesor:
```bash
docker stats --no-stream
```

Guardar evidencia local al inicio, tras alcanzar finalidad y tras 30 minutos. Registrar *host total* y consumo *por contenedor* (RSS, CPU, Docker + otros procesos), junto con OS y RAM. Estas mediciones del host grande no demuestran que la pareja EL/CL quepa en un alumno de 8 GB.

**G0.2, por ejecutar después:** probar **una pareja EL/CL en un equipo de 8 GB** como participante nuevo en la LAN, midiendo swaps, consumo RAM, peering EL/CL, sincronización y rendimiento. La activación del validador será opcional.

## 5. Borrado y límites de persistencia

```bash
kurtosis enclave rm hunterchain-g0 --force
```

Esto elimina la devnet de laboratorio, incluidos sus datos. **No** usar para nodos definitivos. Según el README de ethereum-package, la persistencia en Docker de Besu/Teku con su modalidad `persistent: true` no está soportada; por ello los ensayos de 20/26/93/168 h deben migrar a un **Docker Compose persistente con volúmenes por host**, que aún hay que implementar y verificar.

En particular, **no** se debe confundir `docker stop` con “pausar el tiempo de Ethereum”: el reloj del protocolo sigue avanzando y la red puede aplicar penalizaciones por inactividad al recuperarse.

## 6. Notas de alcance

- G0 usa una cadena y un chain ID de prueba (`network_id: "717071"`); **no fijan el chain ID definitivo de HunterChain**.
- La red de prueba de Kurtosis corre en **un host de laboratorio**, no representa todavía la LAN de 25 equipos.
- La economía de HNT (2,500 en génesis, 224 staked y 2,276 líquidos, gastos de airdrop) es parte de **G1**, no una característica probada por este archivo.
- Las claves generadas por Kurtosis no se deben compartir como identidades finales: cada alumno generará material propio en su equipo.
- Se usará la wallet sobre JSON-RPC para alumnos sin nodo completo; el portal Blockscout será servicio compartido.
- Una cadena Ethereum plenamente descentralizada no se obtiene por el simple hecho de tener 25 cuentas: importa quién posee el stake y opera los validadores.

## 7. Próximos checkpoints

| Hito | ¿Implementado? | Evidencia requerida |
|---|---|---|
| G0.1: siete Besu/Teku, genesis, bloques y finalidad | **Configurado, no ejecutado** | Salida exitosa `probe.py` y logs |
| G0.2: un host de 8 GB | Pendiente | RAM/CPU + peering EL/CL |
| G0.3: reinicio tras 20/26/93/168 h | Pendiente | Histórico continuo, epochs finalizados, penalizaciones |
| G0.4: airdrop en devnet | Pendiente | transacción, receipt, gas positivo |
| G1: génesis HNT definitivo | Bloqueado por G0 | coherencia EL/CL y 2,500 HNT reconciliados |

Fuentes: [ethereum-package](https://github.com/ethpandaops/ethereum-package), [Kurtosis](https://docs.kurtosis.com/run/), [Especificación Ethereum](https://ethereum.github.io/consensus-specs/), [ADR-0010](../../docs/adr/ADR-0010.md).

> Licencia: software original HunterChain bajo AGPL-3.0-only; herramientas de terceros conservan su licencia.
