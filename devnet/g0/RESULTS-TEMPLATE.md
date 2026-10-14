# HunterChain G0 — Plantilla de evidencia

**Estado:** PENDIENTE DE MEDICIÓN. No publicar datos simulados.

## Identificación

- Fecha, operador y zona horaria:
- Commit HunterChain:
- Revisión ethPandaOps: 69dcfbbcbde1ce91a6d0790c8150c84de55e3b2b
- SO; versiones Docker y Kurtosis:
- CPU, RAM física y RAM libre previa:
- Imágenes Besu y Teku (tag y digest):
- Génesis EL, Genesis Validators Root CL:
- Chain ID observado:

## G0.1 — Arranque y finalidad

| Indicador | Resultado observado |
|---|---|
| Siete pares Besu/Teku | |
| Altura EL mayor que cero | |
| Siete validadores activos en CL | |
| Epoch finalizado >0 | |
| Tiempo hasta primera finalidad | |
| Memoria y CPU máxima por cliente | |
| Errores relevantes | |

Adjuntar salida JSON de devnet/g0/probe.py sin claves, tokens ni datos personales.

## G0.2 — Equipo de 8 GB

- SO y hardware:
- RAM antes del arranque:
- Uso máximo de RAM Besu:
- Uso máximo de RAM Teku:
- Swap/OOM/errores:
- EL/CL peers, sincronización, estabilidad:
- Dictamen: nodo completo viable / wallet ligera / inconcluso.

## G0.3 — Suspensión/reanudación en entorno persistente

| Horas sin nodos | Epoch finalizado antes | Epoch finalizado después | Penalización medida | Tiempo de recuperación | Dictamen |
|---|---|---|---|---|---|
| 20 | | | | | No ejecutado |
| 26 | | | | | No ejecutado |
| 93 | | | | | No ejecutado |
| 168 | | | | | No ejecutado |

La devnet desechable de Kurtosis no basta para validar persistencia. Se necesita Compose con volúmenes y un plan de apagado/reinicio controlado.

## Decisión de cierre de G0

- [ ] Siete validadores y finalidad confirmados.
- [ ] Modalidad wallet ligera validada.
- [ ] Viabilidad del nodo con 8 GB medida.
- [ ] Recuperación del PoS estándar confirmada o ADR de desviación abierto.
- [ ] Génesis definitivo G1 autorizado.

- Responsable y revisión:
- Referencia a pruebas y ADR:
