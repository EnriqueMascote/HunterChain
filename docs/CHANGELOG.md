# Registro de evolución arquitectónica

## 2026-10-13 — Inicio de implementación G0

**Estado:** devnet piloto configurada, no ejecutada.

Se incorporan decisiones posteriores a los documentos v1.0 sin reescribir retrospectivamente las entrevistas:

- [ADR-0015](adr/ADR-0015.md): los equipos que no soporten Besu+Teku podrán participar usando wallet y explorer; por tanto **25 participantes no implica necesariamente 25 nodos**, aunque siguen previstos siete validadores de génesis y se promoverá que haya más nodos cuando el hardware lo permita.
- [ADR-0016](adr/ADR-0016.md): ethPandaOps ethereum-package/Kurtosis se utiliza únicamente para validar una devnet **desechable**; la red definitiva con apagados intermitentes requerirá otra estrategia probada de persistencia mediante Docker.
- [devnet/g0/](../devnet/g0/README.md): primera configuración ejecutable y probe para comprobar número de validadores, altura de ejecución y finalized epoch.
- [Pipeline CI](../.github/workflows/g0-static.yml): sólo realiza verificación de sintaxis e invariantes de la configuración. No acredita que el PoS haya arrancado.

**Pendientes obligatorios:** medición en un equipo de 8 GB; arranque/finalidad con siete validadores; recuperación tras apagados 20/26/93/168 h; diseño verificable de génesis EL/CL con oferta total 2,500 HNT; depósitos y activaciones de nuevos validadores.

Hasta que G0 se ejecute, ninguna de esas capacidades debe calificarse de comprobada.
