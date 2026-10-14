# HunterChain — Anteproyecto técnico v1.0

**Fecha:** 2026-10-13  
**Versión:** 1.0 (línea base de diseño, no release de software)  
**Estado:** Aprobación conceptual; implementación condicionada a hitos de validación.  
**Público:** estudiantes, docente, revisores y colaboradores de la red.

## 1. Resumen ejecutivo

HunterChain es una red privada Ethereum/EVM orientada a la enseñanza práctica de sistemas distribuidos, Proof of Stake (PoS) y finanzas descentralizadas. Opera sobre la red local de un aula con 24 alumnos y un docente, mediante una computadora física por participante. Se planea una moneda nativa ficticia —Hunts (HNT)— cuyo gas, validación y transferencia funcionen en una cadena propia. HNT no representa dinero, inversión ni derecho de redención; no se conecta con Ethereum Mainnet.

Este texto establece requisitos, componentes, economía inicial, criterios de aceptación, riesgo y secuencia de ejecución. **No afirma que HunterChain esté desplegada, probada o auditada.**

## 2. Alcance

### Incluido

- Red EVM privada con Execution Layer (EL) y Consensus Layer (CL) separadas.
- Besu como execution client; Teku como beacon/consensus client, con validator client cuando se participe en staking.
- Despliegue por Docker en 25 computadoras reales; comunicación P2P de ambas capas por LAN Wi-Fi escolar.
- Siete validadores de génesis (docente y seis alumnos); 18 participantes adicionales como nodos no validadores inicialmente, con incorporación voluntaria mediante depósito.
- HNT nativo con gas de valor positivo, EIP-1559, recompensas y penalizaciones del protocolo cuando corresponda.
- Airdrop solicitado por el alumno, aprobado y transmitido manualmente por el docente, con transacción trazable.
- Portal de administración HTTPS (React + Quarkus + PostgreSQL), servicio de descubrimiento LAN, agente de métricas, explorador EVM Blockscout.
- Laboratorios de pagos, smart contracts, tokens, exchange, garantías y experimentación adversarial aislada.
- Repositorio público y memoria técnica: ADR, runbooks, manifiestos, criterios de prueba y reproducibilidad.

### Excluido

- Dinero fiduciario, valor económico externo, comercio real, recaudación, intercambios públicos y custodia de fondos ajenos.
- Gestión de identidades gubernamentales o PKI institucional.
- Exposición P2P/RPC a Internet; uso de puentes entre HunterChain y cadenas públicas.
- Consola con capacidad de modificar el consenso o corregir arbitrariamente balances.
- Promesa de disponibilidad permanente 24/7, seguridad de nivel producción o validación automática de cualquier despliegue.

## 3. Identidad, participantes y recursos

| Identificador | Valor aprobado |
|---|---|
| Red | HunterChain |
| Activo nativo | Hunts |
| Ticker | HNT |
| Unidad mínima pedagógica | Peas (PEAS), equivalente a 10^-18 HNT |
| Usuarios | 25 (24 alumnos + docente) |
| Equipos | 25 hosts físicos, acceso administrador, al menos 4 cores y 8 GB RAM |
| SO | Predominio Windows 11; aproximadamente cuatro Linux y dos macOS |
| Conectividad | Wi-Fi con tráfico cliente-cliente comprobado; DHCP para todos |
| Internet | Permitido para descargar herramientas; la cadena opera exclusivamente en LAN |
| Disponibilidad | Encendido durante clase; sin obligación de operar fuera del aula |
| Horario | Lunes 17–19; martes 18–20; miércoles 22–23; jueves 19–20 |
| Preparación | Prerrequisitos instalados fuera de la sesión guiada |
| Primera implantación en clase | Objetivo de 4–6 horas, condicionado a validaciones |

## 4. Arquitectura lógica

Cada equipo aloja:
1. Un contenedor Besu, con estado EVM, P2P de ejecución y JSON-RPC unido al loopback del host.
2. Un contenedor Teku, con beacon node/CL y, opcionalmente, validator client.
3. Engine API privada Besu↔Teku autenticada con secreto JWT **propio de ese equipo**.
4. Wallet EVM, clave pública del validador (si aplica), almacenamiento persistente y agente local de telemetría limitada.

El equipo del profesor aloja adicionalmente servicios *no consensuales*: portal React, API Quarkus, PostgreSQL administrativo, aprobador de airdrops, directorio de bootnodes y QR de incorporación, Blockscout, Caddy y step-ca. Su condición de bootnode o proveedor de interfaz **no le concede privilegios de validación**.

Las redes P2P EL y CL son independientes. La caída del portal o explorador no debe detener la producción y validación de bloques si suficientes validadores y peers siguen operando.

### Interfaces y exposición

| Servicio | Alcance planeado |
|---|---|
| Besu P2P TCP/UDP 30303 (referencia) | LAN entre hosts |
| Teku P2P TCP/UDP 9000 y QUIC UDP 9001 (referencia) | LAN entre hosts; confirmar imagen/versión |
| JSON-RPC Besu TCP 8545 | localhost de cada host |
| Engine API 8551 | sólo red Docker local, nunca LAN |
| Teku REST 5051 | sólo localhost/agente autorizado |
| Portal, explorador y bootstrap | HTTPS LAN sobre Caddy |
| Base de datos, CA interna y APIs privadas | redes Docker internas/host restringido |

Los puertos son valores de diseño propuestos y deben probarse frente a Firewalls de Windows/macOS/Linux, FortiGate y redes Docker. No se asumirán DNS, IP estáticas ni alcance de un nombre mDNS en todas las plataformas.

## 5. Identidades y custodia

Se distinguen: (a) estudiante registrado administrativamente, (b) identificador público seudónimo, (c) wallet secp256k1 para HNT/operaciones, (d) claves BLS para validador PoS, (e) claves P2P de los clientes y (f) JWT local para Engine API. El estudiante genera y custodia localmente las claves privadas de wallet y validador. El portal recibe sólo direcciones y claves públicas necesarias.

El vínculo nombre real↔identificador se guarda fuera de la cadena y sólo el docente lo consulta. Los alumnos ven seudónimos, direcciones, hashes, bloques y balances; esto no garantiza anonimato: la observación de transacciones puede permitir correlaciones.

Pérdida de clave = consecuencias reales de acceso/validación. No se habilita sustitución secreta de credenciales, emisión arbitraria o reversión administrativa. El respaldo personal y cifrado, cuando exista, será responsabilidad de su titular.

## 6. Economía y contabilidad del génesis

**Aprobado:** 2,500 HNT como oferta económica inicial total; 32 HNT por validador inicial; siete validadores génesis; recompensa PoS según reglas de red; slots de 12 s, epochs de 32 slots; transferencias con gas positivo.

La contabilidad inicial objetivo será:

| Concepto | HNT |
|---|---:|
| Stake de génesis: 7 × 32 | 224.00 |
| Saldos líquidos disponibles en EL, incluyendo distribuidor | 2,276.00 |
| **Suma inicial** | **2,500.00** |

La distribución equitativa de referencia es **99.96 HNT por participante** (total stake + líquido), dejando 1 HNT en distribuidor para gas. Para los siete validadores de génesis corresponderían 32 HNT comprometidos más 67.96 HNT líquidos; para los 18 restantes, 99.96 HNT líquidos hasta depositar voluntariamente 32. El distribuidor debe tener inicialmente 2,276 HNT y enviar 25 transferencias según su calendario. El remanente de gas no gastado no desaparecerá automáticamente y debe contabilizarse y declararse terminado el reparto.

**Advertencia técnica vinculante:** las convenciones de depósitos génesis, estado CL y preasignación EL deben compatibilizarse con el generador y versión seleccionados. Un saldo del estado de consenso no puede contarse otra vez como saldo líquido EL. El informe de balance del génesis y su test de reconciliación son bloqueantes para pasar a G1.

El gas representa cómputo y se paga en HNT; EIP-1559 divide base fee (quema) y priority fee (proponente), mientras que la emisión de recompensas de consenso sigue la especificación elegida. No hay minería PoW ni mint administrativo posterior. El ticker HNT también está en uso por Helium, sin relación con HunterChain.

La **entrada voluntaria al staking** debe recorrer depósito, inclusión en la cadena, reconocimiento en CL, cola y activación; no se obtiene por cambiar una columna en PostgreSQL. El mecanismo y las transiciones exactas dependen de la versión de forks y generador de red: pendientes de prueba.

## 7. Operación intermitente y riesgo crítico

La cadena sólo se ejecutará durante las clases; las PCs estarán apagadas fuera de horario. Los intervalos normales incluyen ~20 h, 23 h, 26 h y hasta **93 h** de jueves a lunes (sin contar asuetos). Esto contradice las expectativas de disponibilidad de validadores de Ethereum PoS: los slots avanzan con el reloj real y la falta de participación puede disparar penalizaciones e inactivity leak después de cuatro epochs sin finalizar.

**Plan obligatorio G0:** probar suspensión y recuperación con 7 validadores, en 20 h, 26 h, 93 h y al menos un intervalo mayor; medir cabeza/finalidad, penalizaciones, sincronización y posibilidad de recuperar consenso. No se autoriza presentar una pausa de Docker como “pausa del tiempo Ethereum”.

Si las pruebas fallan, se podrá diseñar una **variante experimental** de tiempo lógico/PoS, documentada como desviación relevante respecto a Ethereum; no se promete que exista sin modificar clientes. La definición operativa requiere una nueva decisión ADR, prototipo y pruebas cruzadas antes del génesis definitivo.

## 8. Bootstrap e incorporación de estudiantes

Secuencia objetivo:
1. Instalador guiado y diagnóstico local Docker/CPU/RAM/puertos (preparación previa).
2. QR o URL HTTPS de incorporación en LAN; resolución mediante IP/host actual, mDNS opcional.
3. Descarga de manifiestos públicos, chain ID, hashes génesis y bootnodes EL/CL actualizados.
4. Generación local de wallet, P2P y clave de validador si el alumno lo solicita.
5. Arranque EL+CL, descubrimiento de peers, validación de cabeza y hashes comunes.
6. Registro administrativo de seudónimo, direcciones públicas y estado del nodo.
7. Solicitud manual de airdrop; aprobación docente; envío on-chain desde distribuidor y verificación de hash/recibo.
8. Opción de depositar 32 HNT, esperar activación y ejercer funciones de validador.

Primeros ingresos secuenciales y documentados; posteriormente concurrencia voluntaria. Se requiere una máquina de estados idempotente para airdrops: solicitado→aprobado→emitido→confirmado, con tratamiento de errores, reintentos y transacciones reemplazadas. Ningún alumno debe entregar secretos al servicio central.

## 9. Portal, explorer y TLS

El portal (Quarkus/React/PostgreSQL) gestiona usuarios locales con roles, registro seudónimo, solicitudes y autorizaciones, nodos y evidencias. Un agente de sólo lectura, ejecutado localmente, informa estado de Docker, versiones, salud EL/CL, peers y estatus de validadores; nunca conoce ni reporta claves privadas. Las operaciones locales se harán por CLI, reflejando sus efectos en la GUI.

Blockscout indexa transacciones, bloques, balances, fees, contratos y logs desde un endpoint JSON-RPC de referencia. El estado de consenso/validadores requiere consultas adicionales a Teku o herramienta CL; Blockscout por sí solo no lo resuelve. Los recursos de Blockscout se hospedan centralmente y deben dimensionarse.

HTTPS interno: una CA privada step-ca con un Caddy que termina TLS y utiliza ACME para emitir/renovar certificados; distribución verificada del root CA a clientes. No se utilizará GnuPG como CA TLS (podrá utilizarse para firmar artefactos si se aprueba). Nombre DNS local estable por decidir; no exponer Engine API ni las claves de step-ca a clientes.

## 10. Estrategia de implementación y puertas de aceptación

| Puerta | Trabajo | Entregable | Salida/criterio |
|---|---|---|---|
| G0 | Piloto técnico | Informe de 8 GB RAM, puertos, tiempo y suspensión PoS | Aprobación de continuidad o ADR de desviación |
| G1 | Génesis EL/CL | Configuración, manifiesto, hashes, 7 validator keys locales | Auditoría supply 2,500 HNT, bloque génesis reproducible |
| G2 | Nodos físicos | Compose versionado y runbooks Windows/Linux/macOS | EL/CL emparejados, 2 redes P2P sobre LAN con DHCP |
| G3 | UX operativa | Portal, bootstrap, Caddy/step-ca, Blockscout | Solicitar/aprobar/ver TX y errores sin secretos centralizados |
| G4 | Incorporación | Secuencia de altas, claves y stake | Depósito, reconocimiento CL, activación y estado verificables |
| G5 | Economía | ERC-20, mercados, escrow, DEX y lending **educativos** | Pruebas funcionales, balances, gas y límites documentados |
| G6 | Resiliencia | Red de ataques desechable | Evidencia de pérdida de finalidad, fallas, censura, recuperación |
| G7 | Transferencia | Runbooks, ADR y BOM | Reinstalación documentada por grupo independiente |

Las 4–6 horas se refieren a la actividad de despliegue en clase tras preparación previa, no a construir todo el portal y el ecosistema DeFi. El desarrollo de software y las pruebas G0–G3 tendrán calendario aparte.

## 11. Estrategia de documentación y control de cambios

- README: orientación, estado real y enlaces.
- Whitepaper: motivación, modelo técnico/económico, supuestos y límites.
- ADR: problema, alternativas, decisión, consecuencias, riesgos, reversibilidad y pruebas.
- BOM: versiones y digests de Besu, Teku, Docker, herramientas de génesis y servicios.
- Network manifest: chain ID, fork schedule, genesis hashes EL/CL, Genesis Validators Root, parámetros de gas, puertos y referencias a artefactos públicos.
- Runbooks: preparación, incorporación, transferencia, staking, stop/restart, recuperación, reset y diagnósticos.
- Evidencias: resultados medidos, capturas no sensibles, transacciones, hashes de bloque y logs saneados.
- Política de secretos: volumenes/keystores fuera de git, sin exportación al portal, nada de claves privadas en imágenes o commits.

Un ADR aceptado no se reescribe silenciosamente: se sustituye mediante otro ADR con referencia explícita. Los parámetros que afecten al consenso o génesis se congelarán antes de la red definitiva.

## 12. Riesgos y supuestos

| Riesgo | Severidad | Mitigación / decisión |
|---|---|---|
| PoS no recupera finalidad tras 93 h offline | Crítica | G0 antes de red definitiva; evaluar bifurcación experimental |
| 8 GB RAM insuficientes para EL+CL + sistema | Alta | Perfil real por SO; límites y prueba en equipo mínimo |
| Configuración de devnet no soporta 7 validadores | Crítica | Preset/chain config custom, test de genesis cross-client |
| Doble cómputo de 224 HNT del génesis | Alta | Auditoría económica EL+CL |
| Errores P2P por DHCP/NAT Docker | Alta | Anuncio IP host, bootnodes dinámicos, puertos LAN y firewall |
| Dependencia del portal/faucet central | Media | Separarlo del consenso; fallback manual de información pública |
| Fuga de claves y datos personales | Crítica | Custodia individual, permisos mínimos, registro off-chain |
| Estudiantes que no hacen stake | Media | Objetivos de consenso expresados en porcentaje de stake, no 25 validadores forzosos |
| Fallos de CA/DNS local | Media | IP y QR alternativos, bootstrap de confianza por fingerprint |
| Ataques afectan historial definitivo | Crítica | Devnets desechables físicamente/lógicamente aisladas |
| Ticker HNT duplicado con Helium | Baja | Aviso visible y chain ID propio |

## 13. Decisiones pendientes antes de G1

El número de chain ID, fork/versiones exactas, mecanismos de depósitos y retiros, validadores génesis (claves públicas obtenidas localmente), bootnode/DNS del aula, intervalo de recuperación aceptable, stop/start de PoS, umbrales de rendimiento, gas target/base fee inicial, remanente de distribuidor, deployment de Blockscout y política final de releases **siguen sin aprobarse en términos ejecutables**. Deben cerrarse por ADR con pruebas, no mediante supuestos en scripts.

## 14. Referencias técnicas

- Ethereum consensus specs: https://ethereum.github.io/consensus-specs/
- Ethereum PoS: https://ethereum.org/developers/docs/consensus-mechanisms/pos/
- Recompensas y penalties: https://ethereum.org/developers/docs/consensus-mechanisms/pos/rewards-and-penalties/
- EIP-1559: https://eips.ethereum.org/EIPS/eip-1559
- Besu/EL-CL: https://docs.besu-eth.org/public-networks/concepts/node-clients/
- Teku: https://docs.teku.consensys.com/concepts/node-types
- Ethereum package: https://github.com/ethpandaops/ethereum-package
- Blockscout: https://github.com/blockscout/blockscout/tree/master/docker-compose
- Smallstep ACME: https://smallstep.com/docs/tutorials/acme-protocol-acme-clients/
- GNU AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.en.html

**Control de versión:** v1.0 consolida siete rondas de entrevista. Las decisiones de infraestructura y proceso están aprobadas; las afirmaciones de funcionamiento técnico exigen evidencia de pruebas.