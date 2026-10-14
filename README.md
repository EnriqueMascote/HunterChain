# HunterChain

> Red Ethereum PoS privada de aprendizaje y microeconomía ficticia para un grupo de 24 estudiantes y un docente.

**Estado:** anteproyecto v1.0 — **no se ha desplegado la red definitiva**. La documentación distingue decisiones de diseño de características probadas.

- **Cadena:** HunterChain
- **Moneda nativa:** Hunts (**HNT**); subunidad: **Peas (PEAS)**; 1 HNT = 10^18 PEAS.
- **Participantes:** 25 equipos físicos independientes sobre LAN Wi-Fi (DHCP).
- **Clientes propuestos:** Besu (Execution Layer) y Teku (Consensus/Validator Layer).
- **Consenso:** Ethereum Proof of Stake; 7 validadores de génesis (docente + 6 alumnos) y hasta 18 participantes adicionales que pueden optar por hacer staking.
- **Emisión económica inicial:** 2,500 HNT totales, incluyendo 224 HNT de stake génesis; distribución mediante transacciones con gas real.
- **Ciclo de uso:** sólo durante horas de clase, conservando el estado. **Pendiente de probar compatibilidad con penalizaciones y reloj PoS de Ethereum.**
- **Stack auxiliar:** Quarkus, React, PostgreSQL, Blockscout, Docker Compose, Caddy y step-ca.
- **Propósito:** investigación, experimentación y docencia; HNT no tiene valor monetario externo.

## Documentación

| Documento | Contenido |
| --- | --- |
| [Anteproyecto técnico v1.0](docs/anteproyecto-v1.0.md) | Arquitectura, alcance, requisitos, fases, pruebas y riesgos |
| [Whitepaper v1.0](docs/whitepaper-v1.0.md) | Tesis de diseño, modelo de red y economía, límites y aplicaciones |
| [Índice de ADR](docs/adr/README.md) | Decisiones arquitectónicas, estado y criterios |
| [Plantilla ADR](docs/adr/TEMPLATE.md) | Formato estándar para nuevas decisiones |

## Advertencias antes de instalar

1. **No hay aún archivos génesis válidos, compose ni scripts de instalación aprobados.** No debe asumirse que la red ya funciona.
2. Ethereum PoS **no se pausa al detener contenedores**. La viabilidad de apagar *todos* los nodos de jueves a lunes (~93 h) sigue siendo un riesgo crítico; se requiere prueba.
3. El mínimo de 8 GB RAM por equipo es **hipótesis de hardware**, no un requisito validado para Besu+Teku en Windows/macOS/Linux.
4. Los portales de administración y Blockscout no intervienen en el consenso; no guardarán claves privadas. Las claves de validador y wallets se generan localmente.
5. El ticker **HNT** también existe en Helium. HunterChain no está asociada a esa red ni a su token.
6. El repositorio es público para descarga de estudiantes, pero **ningún nombre, credencial, secreto, CA privada ni dato personal** debe publicarse.

## Ruta de trabajo

**G0** validación técnica de devnet pequeña y recursos → **G1** génesis reproducible y supply auditado → **G2** LAN/P2P por equipo → **G3** portal/faucet/aprobación de transferencias/explorer → **G4** depósitos y activación de validadores → **G5** microeconomía y DeFi → **G6** laboratorio adversarial aislado y entrega de memoria técnica.

El plan de despliegue considera una preparación previa no evaluable y una sesión inicial de **4–6 horas**, que sólo será aceptada si las pruebas de referencia confirman su viabilidad.

## Contribución y licencia

Código original del proyecto bajo [GNU AGPL-3.0-only](LICENSE). La licencia del repositorio **no cambia las licencias independientes** de Besu, Teku, Blockscout u otras dependencias. Ante cualquier modificación de la arquitectura, registrar un ADR.

Fuentes técnicas: [Ethereum consensus specs](https://ethereum.github.io/consensus-specs/), [Besu](https://docs.besu-eth.org/), [Teku](https://docs.teku.consensys.com/), [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559), [step-ca](https://smallstep.com/docs/step-ca/).
