MELÓMANOS QUALITY GATE

Una funcionalidad NO está terminada hasta cumplir el nivel de gate que corresponda.

## Gate tiers

| Tier | Cuándo | Comando |
|------|--------|---------|
| **Fast Gate** | Cambios backend, iteración rápida | `py run_audit.py --backend-only` |
| **Quality Gate** | Feature completa sin E2E aún, o pre-merge sin stack | `py run_audit.py --skip-e2e` |
| **Full audit** | Antes de release con flujos UI | `py run_audit.py` (auto-inicia stack local si hace falta) |
| **Release Gate** | Cierre de milestone / roadmap | `py finish_task.py` |

Ejecutar desde `C:\melomanos\workspace` (o `MELOMANOS_WORKSPACE_DIR`).

### Fast Gate

- ✓ `py -m pytest` (vía `run_audit.py --backend-only`)
- No inicia backend ni frontend
- **No valida** migraciones Alembic en PostgreSQL local (pytest usa SQLite + `create_all`)

### Quality Gate

- ✓ Backend: `py -m pytest`
- ✓ Frontend: `npm run build`
- (E2E omitido; no inicia stack local)
- **Recomendado** antes de E2E manual: `cd backend && py scripts/migration_status.py --check`

### Full audit / Release Gate

El **Full audit** verifica backend y frontend antes de Playwright. Si no están listos, ejecuta automáticamente:

```powershell
py run_melomanos.py --kill-stale --no-wait
```

`run_melomanos.py` compara `alembic current` vs `alembic heads` y **aborta** si la base local está atrasada (salvo `--skip-migration-check`). Usa `--auto-migrate` para aplicar `alembic upgrade head` antes de arrancar.

Si ya están corriendo, no los reinicia.

Definition of Done (DoD) completo:

Backend:
✓ py -m pytest

Frontend:
✓ npm run build

E2E:
✓ npm run test:e2e

Full Audit:
✓ py run_audit.py

Git (Release Gate vía finish_task.py):
✓ commit realizado
✓ push realizado

Documentation:
✓ PROJECT_STATUS.md actualizado si aplica

Release Rule:
✓ Ninguna funcionalidad se considera completada hasta pasar todas las validaciones del tier aplicable (Full audit + git para release).

Si cualquiera falla:
La tarea vuelve a estado "En desarrollo".

Ver [`README_AUDIT.md`](./README_AUDIT.md) y [`../backend/TESTING_STRATEGY.md`](../backend/TESTING_STRATEGY.md).
