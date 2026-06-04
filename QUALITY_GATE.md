MELÓMANOS QUALITY GATE

Una funcionalidad NO está terminada hasta:

Definition of Done (DoD)

Backend:
✓ py -m pytest

Frontend:
✓ npm run build

E2E:
✓ npm run test:e2e

Full Audit:
✓ py run_audit.py

Git:
✓ commit realizado
✓ push realizado

Documentation:
✓ PROJECT_STATUS.md actualizado si aplica

Release Rule:
✓ Ninguna funcionalidad se considera completada hasta pasar todas las validaciones anteriores.

Si cualquiera falla:
La tarea vuelve a estado "En desarrollo".
