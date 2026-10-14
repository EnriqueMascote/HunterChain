# Architecture Decision Records — HunterChain

Cada ADR documenta una decisión relevante. Estados válidos: **Aceptado**, **Propuesto**, **En validación**, **Rechazado** y **Sustituido**. Aceptado expresa acuerdo arquitectónico, **no que el software haya pasado pruebas**.

| ADR | Asunto | Estado |
|---|---|---|
| [0001](ADR-0001.md) | Ethereum PoS y pila Besu/Teku | Aceptado, condicionado a piloto |
| [0002](ADR-0002.md) | Nodo físico por participante + Docker | Aceptado, performance pendiente |
| [0003](ADR-0003.md) | LAN DHCP y doble descubrimiento P2P | Aceptado, validación pendiente |
| [0004](ADR-0004.md) | Economía HNT/PEAS y oferta de génesis | Aceptado en diseño, contabilidad técnica pendiente |
| [0005](ADR-0005.md) | Siete validadores de génesis y staking opcional | Aceptado, compatibilidad del génesis pendiente |
| [0006](ADR-0006.md) | Airdrop manual autorizado con gas | Aceptado |
| [0007](ADR-0007.md) | Portal administrativo separado del consenso | Aceptado |
| [0008](ADR-0008.md) | Custodia individual y seudonimato | Aceptado |
| [0009](ADR-0009.md) | step-ca / Caddy / ACME | Aceptado |
| [0010](ADR-0010.md) | Pausa interclases y recuperación PoS | En validación; variante condicional |
| [0011](ADR-0011.md) | Blockscout y observabilidad CL | Aceptado, dimensión pendiente |
| [0012](ADR-0012.md) | Repositorio público, AGPLv3 y secretos | Aceptado |
| [0013](ADR-0013.md) | Ensayos adversariales en redes desechables | Aceptado |
| [0014](ADR-0014.md) | Perfil de forks/génesis y entrada real al staking | Propuesto; prueba bloqueante |
| [0015](ADR-0015.md) | Wallet ligera si el equipo no soporta Besu+Teku | Aceptado, recursos por medir |
| [0016](ADR-0016.md) | Piloto Kurtosis desechable y despliegue persistente separado | Aceptado, piloto no ejecutado |

## Flujo de decisión

1. Registrar necesidad, alternativas, riesgos y resultados observables.
2. Declarar **Aceptado** sólo el principio consensuado; marcar parámetros ejecutables como pendientes.
3. Construir experimento en devnet; guardar evidencia con hash de versión, build y logs saneados.
4. Si la decisión cambia, redactar nuevo ADR y marcar el previo **Sustituido por ADR-XXXX**.
5. No versionar wallets, JWT, claves de CA, volúmenes del consenso, datos privados del alumnado ni contraseñas.

[Plantilla](TEMPLATE.md) · [Anteproyecto](../anteproyecto-v1.0.md) · [Whitepaper](../whitepaper-v1.0.md).
