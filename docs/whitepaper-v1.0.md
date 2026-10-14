# HunterChain — Whitepaper v1.0

**A private Ethereum-compatible classroom economy**  
**Fecha:** 13 de octubre de 2026 · **Idioma:** español · **Estado:** diseño/hipótesis, no red lanzada.

## Resumen

HunterChain es una propuesta de infraestructura blockchain educativa: 25 personas operarán 25 nodos físicos en una red Wi-Fi local y estudiarán el funcionamiento de Ethereum Proof of Stake desde sus fundamentos, sin especulación, valor fiduciario ni dependencia de una blockchain pública. La red incorpora moneda nativa, gas, firmas, transacciones, staking, validadores, bloques, finalidad y contratos ejecutados por la EVM. Al separar las funciones de ejecución, consenso, administración y exploración, el proyecto permite experimentar con una microeconomía ficticia y observar sus fallas reales.

Este whitepaper presenta los principios y reglas objetivos del sistema; los aspectos que dependen de un prototipo o de versiones concretas del protocolo no se consideran implementados hasta superar pruebas de aceptación. El anteproyecto técnico describe la ruta de construcción.

## 1. Motivación: ¿para qué otra blockchain?

La hipótesis de HunterChain no es que una blockchain distribuida supere siempre a una base de datos. Un registro central con PostgreSQL suele ser más simple y económico cuando existe una autoridad única confiable. Lo distintivo de blockchain es la **máquina de estados replicada**: participantes independientes validan un historial ordenado de transacciones y acuerdan sus efectos sobre un estado común.

El ejercicio didáctico debe permitir al estudiante responder con evidencia:
- Qué es un bloque; cómo se vincula con el anterior; qué transacciones incluye y cómo compromete criptográficamente el estado resultante.
- Por qué un usuario necesita moneda nativa para pagar gas y cuál es la diferencia entre el gas consumido, base fee y priority fee.
- Cuándo una transacción queda incluida y cuándo alcanza finalidad.
- Qué ocurre cuando los validadores abandonan la red, se concentran o colaboran para impedir la finalización.
- Por qué no basta modificar una base de datos local para alterar el balance global.
- Qué mecanismos ofrecen los contratos y qué límites mantienen al tratar con activos externos.

La red es un instrumento para observar, comparar y refutar hipótesis; **no un producto financiero para comercializar**.

## 2. Objetivos técnicos

1. Desplegar 25 parejas EL/CL independientes, distribuidas por 25 máquinas reales.
2. Mantener las dos redes P2P (Execution y Consensus) comunicadas sólo a través de la LAN.
3. Crear un génesis de red PoS privada consistente entre Besu y Teku.
4. Ejecutar depósitos de validadores y transacciones de HNT con tarifas distintas de cero.
5. Registrar y consultar bloques, contratos, receipts, balances, logs y eventos.
6. Ofrecer herramientas visuales que no sustituyan la interacción local mediante CLI.
7. Aislar las prácticas ofensivas en cadenas de prueba y preservar la integridad del historial definitivo.
8. Publicar el diseño y documentar cada decisión reproducible mediante ADR, versiones fijas, hashes y runbooks.

## 3. Modelo de la red

**HunterChain** es una cadena EVM independiente; no utiliza el estado de Ethereum Mainnet y no requiere el activo ETH para operar. Su moneda nativa se denomina **Hunts (HNT)** y la unidad atómica definida pedagógicamente **Peas (PEAS)**. La relación es 1 HNT = 10^18 PEAS. El símbolo HNT también lo usa Helium en otra red: **no existe afiliación ni equivalencia**.

Cada nodo lógico contiene:
- **Execution Client (Besu):** mempool, ejecución EVM, cuentas, storage, gas, JSON-RPC, state root y cadena de bloques de ejecución.
- **Consensus Client (Teku):** beacon chain, slots, epochs, fork choice, sincronización, attestations y finalidad.
- **Validator Client (Teku, opcional):** firma tareas de consenso con clave BLS del titular y participa en propuestas/attestations.
- **Engine API:** canal autenticado con JWT local entre EL y CL, no expuesto a terceros.

El nodo de un estudiante puede participar en las redes EL/CL sin operar un validador; **25 nodos no implica 25 validadores**. Al nacimiento se planean siete validadores, cada uno con una clave distinta; otros 18 alumnos podrán activar validadores por voluntad propia, sujeto al mecanismo de depósitos y activación.

El servidor del docente actuará como un peer más y alojará servicios auxiliares. Ni el portal administrativo ni el explorador son árbitros de la validez del ledger.

## 4. Estado, transacciones y bloques

La EVM procesa una secuencia ordenada de transacciones para transformar el estado de una altura a la siguiente. Los bloques conservan transacciones y compromisos criptográficos sobre el resultado, y contienen, entre otros datos, referencias al parent hash, raíces de estado/transacciones/receipts, timestamp, gas usado y base fee cuando corresponda. El estado completo de cuentas y storage no se replica íntegramente dentro de cada header.

El alumno podrá observar que:
- Una transferencia de HNT afecta saldos y nonces, y consume gas.
- Una llamada a contrato puede modificar storage, emitir eventos o revertir.
- El orden de transacciones importa, incluso si llegaron a nodos distintos en órdenes diferentes.
- Una transacción incluida en un bloque todavía debe distinguirse de un checkpoint finalizado.
- Las afirmaciones del mundo externo no se vuelven ciertas sólo por quedar almacenadas en la cadena.

HunterChain no almacenará nombres reales de los alumnos ni materiales personales directamente en la blockchain.

## 5. Modelo monetario

### Oferta génesis

La oferta inicial total objetivo es **2,500 HNT**, no 2,500 HNT líquidos más los depósitos de staking. Siete validadores tendrán **32 HNT comprometidos cada uno** (224 HNT en CL, a reconciliar con su génesis). Quedarán **2,276 HNT líquidos** asignados inicialmente al distribuidor para realizar pagos rastreables.

Se busca una participación económica inicial equitativa de **99.96 HNT por titular**, incluyendo stake de génesis cuando exista:
- 7 validadores: 32 HNT comprometidos + 67.96 HNT líquidos cada uno.
- 18 participantes inicialmente no validadores: 99.96 HNT líquidos cada uno.
- 1 HNT se mantiene temporalmente para gas de distribución (remanente sujeto a publicación y disposición posterior).

Comprobación aritmética: (7 × 32) + (7 × 67.96) + (18 × 99.96) + 1 = **2,500 HNT**.

Esta asignación es **un presupuesto de diseño**, no instrucciones de preminado listas para ejecutar. Deben resolverse depósitos génesis/estado CL, direcciones, generación de genesis.ssz y genesis.json y soporte de las versiones elegidas. Los fees pagados y quemados cambiarán la oferta real con el tiempo; no prometer una oferta constante.

### Emisión y tarifas

Los HNT nuevos se acreditarán exclusivamente por el mecanismo de recompensas de consenso que soporte el fork de PoS elegido. Los proponentes podrán percibir priority fees. La base fee EIP-1559 se quema; las penalizaciones e inactivity leak afectan a los validadores según las reglas configuradas. No existe minado PoW ni privilegio administrativo para incrementar saldos.

Para diferenciar mecanismos, cada alumno deberá consultar:
- Importe transferido, gas limit, gas used, baseFeePerGas, priority fee efectiva y balance final.
- Posición económica del validador antes/después de recompensas o penalizaciones.
- Oferta inicial, variación por emisión y destrucción y lo que puede/no puede observarse desde EL.

### Airdrop didáctico

Cada alumno genera una wallet propia, solicita HNT en el portal y el docente revisa manualmente. Tras aprobar, se firma y emite una transacción de HNT desde el distribuidor, se registra el hash y se exige confirmación on-chain. Una solicitud puede fallar, expirar o reintentarse; la operación debe ser idempotente para prevenir pagos dobles.

El distribuidor no actuará como tesorería permanente ni como autoridad de consenso.

## 6. Proof of Stake, depósitos y finalización

La configuración prioriza el comportamiento de Ethereum PoS, no un consenso Proof of Authority. Se establece un **stake mínimo didáctico de 32 HNT** por validador y **siete validadores de génesis**. La compatibilidad del perfil de forks y los parámetros de devnet mínima deberán verificarse: los parámetros predeterminados de Mainnet no permiten asumir un génesis de siete validadores.

Los participantes adicionales seguirán una incorporación observable: obtener HNT, generar clave BLS y withdrawal credentials según el fork, depositar en un mecanismo en cadena, esperar reconocimiento del depósito por el consenso y pasar por estados de activación. La API del portal sólo presenta dichos estados; no los decreta.

La finalidad de Ethereum requiere una supermayoría de al menos dos tercios del stake participante conforme al protocolo. Con siete validadores equivalentes, cinco representan ~71.43 %; cuatro sólo ~57.14 %. El manejo de fork choice, penalizaciones, salidas y actualizaciones depende de la versión de especificación seleccionada.

Un “ataque del 51 %” no debe reducirse a apagar equipos. Una mayoría de stake no puede hacer válidas transacciones EVM inválidas, pero puede alterar disponibilidad, selección de cadena y censura bajo condiciones concretas. Los laboratorios maliciosos se harán **sólo en redes desechables aisladas**, evaluando pérdida de finalidad, conflictos y recuperación. No se inducirá equivocadamente a pensar que 51 % equivale a dos tercios.

## 7. Operación intermitente como problema de investigación

El salón opera lunes (2 h), martes (2 h), miércoles (1 h) y jueves (1 h). Ningún estudiante estará obligado a mantener encendida su máquina fuera de clase; el mayor apagado típico es de ~93 h entre jueves y lunes.

**Ethereum PoS no pausa los slots por detener Docker.** El reloj real sigue avanzando; los validadores dejan de votar y pueden recibir penalizaciones por inactividad, incluso durante periodos largos sin finalidad. Por eso no se afirma que la red definitiva podrá conservar de manera sostenible sus balances y finalidad con una disponibilidad semanal aproximada del 3.6 %.

Se exige primero una devnet piloto y pruebas controladas de apagado de 20, 26, 93 y 168 h, seguidas de recuperación. Si el protocolo original no satisface los criterios, sólo podrá usarse una **variante experimental de tiempo lógico** con ADR explícito, diferencias documentadas y demostración de interoperabilidad. Tal variante podría requerir mantener cambios propios en cliente CL o rediseñar la práctica; su factibilidad aún no está establecida.

Esta limitación no se ocultará a los alumnos: constituye una de las hipótesis centrales del proyecto.

## 8. Interfaz administrativa y observabilidad

El docente aloja un portal local con:
- Frontend React y backend Java/Quarkus.
- PostgreSQL para cuentas locales, roles, identidad administrativa, solicitudes, evidencias y estado de incorporación.
- Descubrimiento de bootnodes actualizados mediante QR/URL HTTPS; no se depende de IP fija. mDNS es opcional y habrá alternativa mediante IP.
- Agente ligero de sólo lectura que reporta salud de Docker, peers, EL/CL y validator, sin extraer archivos secretos.
- Blockscout para consultar bloques EVM, transacciones, contratos, direcciones y sus balances.
- Consultas CL adicionales para epochs, validators, attestations y finalidad.
- Caddy + step-ca para HTTPS privado y renovación ACME, con root CA instalado tras verificar su fingerprint.

La información de identidad personal estará separada de lo publicado. Alumnos ven seudónimos y direcciones, docente conoce la relación de identidades; blockchain y explorer exponen datos públicos y no garantizan privacidad por sí solos.

## 9. Microeconomía y contratos planeados

**Iteración A — pagos:** transferencias nativas HNT, gas y transacciones fallidas.

**Iteración B — activos programables:** token ERC-20 pedagógico (por definir nombre y reglas), contratos con events/roles y comparación con moneda nativa.

**Iteración C — mercado:** compraventa de activos ficticios, escrow y liquidación atómica.

**Iteración D — exchange:** AMM/líquidez simulada con análisis de slippage y profundidad.

**Iteración E — crédito:** depósitos, colateral, intereses y liquidaciones experimentales, sin valor real.

**Iteración F — gobernanza y resiliencia:** propuestas y decisiones consensuales/sociales; concentración del stake; experimentos aislados sobre censura, disponibilidad y finalización.

El uso de “finanzas descentralizadas” designa **protocolos experimentales**, no operaciones con fondos de estudiantes ni asesoría de inversión. Cada contrato se someterá a pruebas unitarias y de integración; no se presume seguro por ejecutarse en una blockchain.

## 10. Seguridad y límites de confianza

- No publicar claves privadas, seed phrases, archivos JWT, CA keys, contraseñas, bases administrativas con nombres ni volumenes persistentes.
- Separar y restringir Engine API, administración Teku y JSON-RPC; sólo los puertos P2P necesarios podrán anunciarse por LAN.
- No depender del portal para validar bloques: la fuente de verdad financiera es el estado EL/CL consensuado.
- Control de acceso a cuentas locales y evidencias, prevención de solicitudes duplicadas, trazabilidad de aprobaciones y cifrado TLS.
- Red pública GitHub ≠ red blockchain pública: sólo se publica código/documentación, no nodos hacia Internet.
- No conectar wallets reales con activos valiosos ni reutilizar frases semilla en HunterChain.
- No confundir garantía criptográfica de historial con veracidad de un dato capturado fuera de cadena.

## 11. Métricas y evaluación

Criterios técnicos propuestos: EL peers y CL peers por host; porcentaje de slots propuestos; epochs finalizados; block import latency; gasto de memoria/cpu en hosts de 8 GB; tiempos de incorporación y activación; tasa de transacciones aceptadas/revertidas; gas efectivo; continuidad después de 93 h; saldo y recompensas de validadores; disponibilidad del portal/explorer sin afectar consenso.

Criterios pedagógicos: alumnos capaces de explicar diferencias entre EOA y validador, unidad PEAS y HNT, block inclusion vs finality, gas vs fee, EL vs CL, hash/estado y fallo de coordinación. Se documentarán ejercicios guiados y rúbricas después de superar el piloto de infraestructura.

## 12. Gobierno técnico y reproducibilidad

Cada decisión significativa se plasma en ADR numerado con estado, contexto, alternativas, decisión, beneficios, costos, reversibilidad y pruebas. El repositorio incluye BOM y digests de imágenes, manifests EL/CL con hashes, runbooks por SO, criterios de aceptación y bitácoras. Los secretos permanecen fuera de Git.

La red definitiva se “congela” sólo tras las pruebas del génesis, del depósito, de la recuperación de consenso y de equipos de 8 GB. Reiniciar devnets no constituye continuidad de HunterChain definitiva; la reinstalación de la cadena debe conservar su identidad e historial salvo decisión formal de migración.

## 13. Roadmap y riesgos abiertos

- **G0:** prueba de clientes, HW mínimo y tiempo/apagados prolongados.
- **G1:** creación validada de EL genesis + CL genesis y reconciliación del supply.
- **G2:** despliegue de 25 hosts con DHCP y peering EL/CL.
- **G3:** portal, CA, airdrop e indexación.
- **G4:** ingreso voluntario de nuevos validadores.
- **G5:** contratos DeFi y casos de microeconomía.
- **G6:** resiliencia/ataques en redes desechables y documentación replicable.

**Riesgos bloqueantes actuales:** compatibilidad PoS con sólo siete validadores, pausa real del protocolo, memoria de ocho gigabytes en PCs heterogéneas, doble cómputo del stake en génesis y mecanismos de entrada posteriores al staking. Su resolución requiere evidencia y ADR, no afirmaciones del whitepaper.

## 14. Referencias

1. Ethereum Consensus Specifications — https://ethereum.github.io/consensus-specs/
2. Ethereum Proof of Stake — https://ethereum.org/developers/docs/consensus-mechanisms/pos/
3. Ethereum rewards and penalties — https://ethereum.org/developers/docs/consensus-mechanisms/pos/rewards-and-penalties/
4. EIP-1559 — https://eips.ethereum.org/EIPS/eip-1559
5. EIP-7251 (32 mínimo, 2048 máximo efectivo para validators elegibles) — https://eips.ethereum.org/EIPS/eip-7251
6. Besu — https://docs.besu-eth.org/
7. Teku — https://docs.teku.consensys.com/
8. ethPandaOps Ethereum package — https://github.com/ethpandaops/ethereum-package
9. Blockscout — https://github.com/blockscout/blockscout
10. Smallstep ACME — https://smallstep.com/docs/tutorials/acme-protocol-acme-clients/
11. GNU Affero General Public License — https://www.gnu.org/licenses/agpl-3.0.en.html

---

**Nota de transparencia:** v1.0 es un whitepaper de diseño público, no un resultado experimental. Las incertidumbres están descritas deliberadamente para poder someterlas a prueba.