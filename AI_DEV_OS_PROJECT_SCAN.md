# AI DEV OS PROJECT SCAN — MELOMANOS MARKETPLACE

**Scan date:** 2026-06-17  
**Scanner:** Cursor AI Dev OS Scanner (read-only inspection)  
**Root:** `C:\melomanos`  
**Scope:** `backend/`, `frontend/`, `workspace/` — no code changes, no dependency installs, no test execution in this scan.

---

## 1. Project Structure

Árbol resumido (excluye `node_modules`, `.git`, `__pycache__`, `.venv`/`venv`, `dist`, `build`, `.next`, y contenido profundo de virtualenv).

### backend/

```
backend/
├── .cursor/rules/           # ai-operating-system.mdc, release-process.mdc
├── alembic/
│   ├── versions/            # 27 migraciones
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── ai_bridge/           # repo analyzer + /ai-bridge endpoints
│   ├── catalog/             # normalize.py
│   ├── core/                # config, database, security, request_correlation
│   ├── dependencies/        # auth.py, admin.py
│   ├── models/              # 10 modelos ORM
│   ├── routers/             # 9 routers (admin, auth, favorites, listings, messages, orders, disputes, reviews, users)
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # escrow, dispute, subscription, NL search, etc.
│   └── main.py
├── docs/                    # api_overview.md, architecture.md
├── scripts/                 # seed_local.py
├── tests/                   # 21 archivos de test (pytest)
├── AGENT_RULES.md
├── AI_OS_OVERVIEW.md
├── ARCHITECTURE.md
├── BUSINESS_RULES.md
├── CHANGELOG.md
├── Dockerfile
├── MVP_ROADMAP.md
├── PROJECT_STATUS.md
├── QUALITY_GATE.md
├── README.md
├── TESTING_STRATEGY.md
├── alembic.ini
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── run.py
```

### frontend/

```
frontend/
├── e2e/
│   ├── helpers/             # api, auth, listing, order, setup-users
│   ├── global-setup.ts
│   └── melomanos.spec.ts    # 20 tests E2E
├── public/                  # SVG assets
├── src/
│   ├── app/                 # App Router (Next.js)
│   │   ├── admin/page.tsx
│   │   ├── favorites/page.tsx
│   │   ├── listings/[id]/page.tsx
│   │   ├── login/page.tsx
│   │   ├── messages/page.tsx
│   │   ├── orders/page.tsx
│   │   ├── orders/[id]/page.tsx
│   │   ├── profile/page.tsx
│   │   ├── sell/page.tsx
│   │   ├── page.tsx         # marketplace home
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── components/          # 18 componentes UI
│   ├── lib/                 # api, auth, orders, messages, disputes, etc.
│   └── types/index.ts
├── AGENTS.md
├── CLAUDE.md
├── eslint.config.mjs
├── next.config.ts
├── package.json
├── playwright.config.ts
├── run_frontend.py
└── tsconfig.json
```

### workspace/

```
workspace/
├── finish_task.py           # Quality Gate + commit/push workflow
├── melomanos_paths.py       # Resolución de rutas backend/frontend/workspace
├── project_status.py        # Actualiza PROJECT_STATUS.md por markers
├── roadmap_advance.py       # Avanza MVP_ROADMAP.md
├── run_audit.py             # pytest + build + e2e
├── run_melomanos.py         # Launcher dev backend+frontend
├── MIGRATION_TO_STANDARD_LAYOUT.md
├── PROJECT_STATUS.md
├── QUALITY_GATE.md
├── README_AUDIT.md
├── README_FINISH_TASK.md
├── README_LOCAL_RUN.md
├── README_PROJECT_LAYOUT.md
├── README_RUN_MELOMANOS.md
└── README_STATUS.md
```

**Notas de layout:**

- Existen **3 repos git separados**: `backend/.git`, `frontend/.git`, `workspace/.git`.
- El código vive en `C:\melomanos\{backend,frontend,workspace}` pero `melomanos_paths.py` **por defecto** apunta a rutas legacy (`C:\melomanos_market`, `C:\melomanos-frontend`, `C:\melomanos_workspace`) salvo que se definan variables de entorno `MELOMANOS_*_DIR`.

---

## 2. AI Dev OS Artifacts Found

| Archivo esperado | Estado | Resumen |
|------------------|--------|---------|
| `workspace/AI_CONTEXT.md` | **NO EXISTE** | — |
| `workspace/PROJECT_STATUS.md` | **EXISTE** | Snapshot vivo: último Quality Gate 2026-06-05 (backend tests, frontend build, E2E, audit PASSED). Release: Admin Panel MVP. Lista ~20 features MVP completadas. Próximo trabajo: WebPay, notificaciones, deploy, beta, launch. |
| `workspace/TASKS.md` | **NO EXISTE** | — |
| `workspace/ROADMAP.md` | **NO EXISTE** en workspace | Roadmap vive en `backend/MVP_ROADMAP.md` |
| `workspace/SPEC.md` | **NO EXISTE** | — |
| `workspace/DESIGN.md` | **NO EXISTE** | — |
| `workspace/RELEASE_NOTES.md` | **NO EXISTE** | — |

### Otros artefactos relevantes encontrados

| Ubicación | Propósito |
|-----------|-----------|
| `backend/AI_OS_OVERVIEW.md` | Filosofía AI OS, mapa de documentos core, workflow doc→código→validación→release |
| `backend/AGENT_RULES.md` | Reglas para agentes AI (prioridades, scope, quality gate) |
| `backend/ARCHITECTURE.md` | Stack, módulos, flujos escrow/disputes, capas API→services→DB |
| `backend/BUSINESS_RULES.md` | Reglas de negocio (grading Discogs, Compra Segura, anti-desintermediación, planes) |
| `backend/MVP_ROADMAP.md` | **13 milestones COMPLETED**, cola de 5 (WebPay, Notifications, Deploy, Beta, Launch). Active task: Payment Provider Integration — **READY** |
| `backend/PROJECT_STATUS.md` | Estado detallado backend (180 pytest, 20 E2E según docs) |
| `backend/TESTING_STRATEGY.md` | Pirámide de tests, DoD |
| `backend/QUALITY_GATE.md` | Mismo contenido que `workspace/QUALITY_GATE.md` |
| `workspace/QUALITY_GATE.md` | DoD: pytest, build, e2e, run_audit, commit, push, PROJECT_STATUS |
| `workspace/README_*.md` | Run local, audit, finish_task, layout, migración |
| `workspace/finish_task.py` | Orquesta quality gate + commits en 3 repos |
| `workspace/run_melomanos.py` | Launcher con `--check`, `--no-wait`, `--kill-stale` |
| `backend/.cursor/rules/*.mdc` | Reglas Cursor always-on (AI OS + release process) |
| `backend/docs/api_overview.md` | Tabla de endpoints (parcialmente desactualizada vs código) |
| `frontend/AGENTS.md`, `frontend/CLAUDE.md` | Guías para agentes en frontend |

**Brecha AI Dev OS:** El workspace no tiene el set estándar (`AI_CONTEXT`, `TASKS`, `SPEC`, `DESIGN`, `RELEASE_NOTES`). La gobernanza está **dispersa** entre `backend/*.md` y scripts en `workspace/`.

---

## 3. Backend State

### Framework

- **FastAPI** + **Uvicorn** (`run.py`)
- **SQLAlchemy** ORM + **Alembic** migraciones
- **Pydantic v2** + **pydantic-settings**
- **JWT** (python-jose) + **bcrypt** (passlib)
- Tests: **pytest** + FastAPI TestClient

### Estructura de carpetas

Ver sección 1. Patrón: `routers/` (HTTP) → `services/` (reglas) → `models/` (persistencia).

### Archivos principales

| Archivo | Rol |
|---------|-----|
| `app/main.py` | App FastAPI, CORS localhost:3000, registra 9 routers + ai_bridge |
| `app/core/config.py` | Settings desde `.env.local` o `.env` |
| `app/core/database.py` | Engine, pool PostgreSQL, get_db |
| `app/core/security.py` | JWT + password hashing |
| `run.py` | Servidor dev (APP_HOST/PORT/RELOAD) |
| `docker-compose.yml` | API + PostgreSQL 15 |
| `Dockerfile` | Imagen API |

### Modelos existentes (`app/models/`)

| Modelo | Tabla / dominio |
|--------|-----------------|
| `User` | users — email, password_hash, plan_type (free/pack/pro), city |
| `VinylListing` | vinyl_listings — marketplace, grading, reserva, sold, video_url |
| `Favorite` | listing_favorites |
| `Message` | messages — hilos por listing |
| `Order` | orders — lifecycle compra, escrow, payment_status |
| `OrderDispute` | order_disputes |
| `DisputeEvidence` | dispute_evidence — URLs foto/video |
| `Review` | reviews |
| `SellerShippingProfile` | seller_shipping_profiles |
| `SellerPayoutProfile` | seller_payout_profiles |

**Nota:** Migraciones referencian `vinyl_releases` (catálogo), pero **no hay modelo ni router `releases` en el código actual** de `app/`. Documentación README/api_overview aún describe endpoints `/releases/*` que **no están registrados** en `main.py`.

### Endpoints existentes (routers registrados)

**Raíz:** `GET /` — health message

**Auth** (`/auth`): `POST /register`, `POST /login`, `GET /me`

**Listings** (`/listings`):
- `POST /`, `GET /` (filtros, paginación, sort)
- `POST /search/nl` — búsqueda en lenguaje natural
- `GET /mine`
- `POST /{id}/reserve`, `POST /{id}/cancel-reservation`
- `PATCH /{id}/sold`, `PATCH /{id}/status`
- `GET /{id}`, `PUT /{id}`, `DELETE /{id}`

**Favorites** (`/favorites`): `POST /{listing_id}`, `DELETE /{listing_id}`, `GET /me`

**Messages** (`/messages`): `POST /`, `GET /conversations`, `GET /listing/{id}`, `PATCH /{id}/read`

**Orders** (`/orders`):
- `POST /from-listing/{id}` (reserva atómica + crea order)
- `GET /me/buying`, `GET /me/selling`, `GET /{id}`
- `PATCH /{id}/simulate-payment`, `/shipping`, `/complete`, `/cancel`
- `POST /{id}/dispute`, `GET /{id}/dispute`

**Disputes** (`/disputes`): evidence CRUD + `under-review`, `resolve-buyer`, `resolve-seller` (admin key)

**Reviews** (`/reviews`): `POST /`, `GET /seller/{id}`, `GET /seller/{id}/summary`

**Users** (`/users`):
- `GET /me/purchases`, `/me/sales`, `/me/subscription`
- `GET/PATCH /me/shipping-profile`
- `GET/POST/PUT /me/payout-profile`
- `GET /{user_id}`, `/reputation`, `/reviews`, `/digging-score`

**Admin** (`/admin`): `GET /summary`, `/disputes`, `/orders`, `/users` (requiere `x-admin-key`)

**AI Bridge** (`/ai-bridge`): `GET /repo-summary`, `POST /task`

### Sistema de auth

- Registro con email + password hasheado
- Login OAuth2 password form → JWT Bearer
- `get_current_user` dependency — valida JWT, usuario activo
- Admin separado: header `x-admin-key` vs `ADMIN_KEY` env (`dependencies/admin.py`)

### Listings / publicaciones

- CRUD completo en backend
- Filtros: search, city, genre, price, status, sort
- Discogs grading (record/cover M–G)
- `listing_type` new/used — video obligatorio para used (validación backend)
- Reserva atómica vía `UPDATE` condicional
- Límites por plan (`subscription` service en create)

### Reservas

- `POST /listings/{id}/reserve` — reserva standalone
- `POST /orders/from-listing/{id}` — reserva + crea order en una transacción (flujo principal del frontend)

### Mensajes

- Por listing, entre buyer/seller
- `message_safety.py` — bloqueo teléfonos, emails, redes, frases bypass

### Favoritos

- CRUD en `/favorites`

### Pagos / WebPay

- **NO hay integración WebPay real**
- Escrow MVP: `simulate-payment` → `payment_status` held
- `Order.payment_status`: pending, paid, held, released, refunded
- Dispute resolution actualiza payment_status
- Roadmap item #1 activo: `PaymentProvider` abstraction, checkout, webhook — **TODO**

### Notificaciones

- **NO EXISTEN** (sin tabla, sin endpoints, sin emisión de eventos)

### Migraciones / Alembic

- **27 revisiones** en `alembic/versions/`
- Comando documentado: `alembic upgrade head`
- `alembic.ini` presente

### Variables de entorno requeridas

Desde `.env.example` y `config.py`:

| Variable | Requerida | Notas |
|----------|-----------|-------|
| `DATABASE_URL` | Sí | SQLite o PostgreSQL |
| `SECRET_KEY` | Sí | JWT |
| `ALGORITHM` | Sí | ej. HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Sí | |
| `ADMIN_KEY` | Opcional | Requerida para admin/dispute resolution |
| `OPENAI_API_KEY` | Opcional | NL search |
| `OPENAI_MODEL` | Opcional | default gpt-4o-mini |
| `OPENAI_NL_SEARCH_ENABLED` | Opcional | default false |
| `OPENAI_NL_MAX_REQUESTS_PER_DAY` | Opcional | |
| `OPENAI_NL_CACHE_TTL_HOURS` | Opcional | |
| `DB_POOL_*` | Opcional | Solo PostgreSQL |
| `APP_HOST`, `APP_PORT`, `APP_RELOAD` | Opcional | Solo `run.py` |

Archivos: `.env.local` (dev), `.env.docker` (compose). **No commitear** secretos.

### Tests existentes

21 archivos en `backend/tests/` cubriendo: admin, ai_bridge, database, digging_score, disputes, favorites, listings (grading, reservations, search, NL), messages, message_safety, orders, reviews, seller profiles, subscription, request_correlation.

**Documentado:** 180 tests pytest (último quality gate 2026-06-05). **No re-ejecutado en este scan.**

### Comandos disponibles (backend)

| Acción | Comando |
|--------|---------|
| Instalar deps | `pip install -r requirements.txt` (dev: `requirements-dev.txt`) |
| Servidor dev | `py run.py` |
| Tests | `py -m pytest` |
| Migraciones | `alembic upgrade head` |
| Health check | `GET http://127.0.0.1:8000/` o `GET /listings?limit=1` |
| Docker | `docker compose up --build` |
| Seed local | `py scripts/seed_local.py` (si configurado) |

---

## 4. Frontend State

### Framework

- **Next.js 16.2.6** (App Router)
- **React 19**
- **TypeScript 5**
- **Tailwind CSS 4**
- **Playwright** E2E (20 tests documentados)

### Estructura

Ver sección 1. Patrón: `src/app/` páginas, `src/components/` UI, `src/lib/` cliente API.

### Rutas / páginas

| Ruta | Página | Auth |
|------|--------|------|
| `/` | Marketplace + filtros | Público |
| `/login` | Login | Público |
| `/sell` | Crear listing | Requiere token |
| `/listings/[id]` | Detalle listing | Público (SSR fetch) |
| `/favorites` | Favoritos | Requiere token |
| `/messages` | Mensajería | Requiere token |
| `/orders` | Lista pedidos | Requiere token |
| `/orders/[id]` | Detalle pedido, escrow, dispute | Requiere token |
| `/profile` | Panel usuario (ventas, compras, favoritos, mensajes, reputación) | Requiere token |
| `/admin` | Panel admin read-only | Admin key en UI |

**No existe:** `/register`, `/terms`, `/privacy`, páginas de catálogo `/releases`.

### Componentes principales

`Marketplace`, `ListingCard`, `ListingDetailActions`, `VinylCover` (placeholder visual), `MessageForm`, `OrderEscrowCard`, `OrderDisputeSection`, `SellerReputationPanel`, `DiggingScorePanel`, `SubscriptionCard`, `Navbar`, etc.

### Flujo login / registro

- **Login:** `/login` → `POST /auth/login` → token en localStorage → `GET /auth/me` → redirect
- **Registro UI:** **NO EXISTE** — solo vía API (E2E `setup-users.ts` llama `POST /auth/register`)
- Session expiry handling en `auth-session.ts`

### Flujo publicaciones / listings

- **Crear:** `/sell` → `createListing()` → redirect a listing
- **Listar/filtrar:** `/` Marketplace con filtros
- **Detalle:** `/listings/[id]` server component
- **Editar / eliminar:** **NO en frontend** (backend tiene PUT/DELETE; `api.ts` no expone funciones)
- **Reservar directo:** frontend usa **Comprar** → `createOrderFromListing` (no llama `/reserve` standalone)

### Flujo reservas / compra

1. Buyer: Comprar → `POST /orders/from-listing/{id}` → `/orders/{id}`
2. Buyer: simulate payment → escrow held
3. Seller: shipping info → complete
4. Disputes + evidence + admin resolution

### Flujo mensajes

- Desde listing: toggle MessageForm
- `/messages`: conversaciones, hilos, reply, mark read/unread, delete

### Favoritos

- ListingCard + `/favorites` + tab en profile
- `addFavorite`, `removeFavorite`, `getMyFavorites`

### Pagos / WebPay

- UI: botón confirmar pago → `simulatePayment()` 
- **Sin WebPay, sin redirect checkout**

### Notificaciones

- **NO EXISTEN** en frontend

### Variables de entorno

| Variable | Uso |
|----------|-----|
| `API_BASE` | **Hardcoded** en `src/lib/api.ts` como `http://127.0.0.1:8000` — no usa `NEXT_PUBLIC_*` |
| E2E: `E2E_BASE_URL`, `E2E_API_URL`, `E2E_BUYER_EMAIL`, `E2E_SELLER_EMAIL`, `E2E_PASSWORD` | Playwright |
| `MELOMANOS_MARKET_ROOT` | E2E seller setup (legacy path) |

### Tests existentes

- **E2E:** `e2e/melomanos.spec.ts` — 20 tests (homepage, admin, auth redirect, sell, buy flow, escrow, disputes, reviews, etc.)
- **Unit/component tests:** **NO encontrados** (solo lint + build + e2e)

### Comandos disponibles (frontend)

| Acción | Comando |
|--------|---------|
| Instalar deps | `npm install` |
| Dev server | `npm run dev` o `py run_frontend.py` |
| Build | `npm run build` |
| Lint | `npm run lint` |
| E2E | `npm run test:e2e` |
| E2E UI | `npm run test:e2e:ui` |

---

## 5. Current MVP Features

Clasificación basada en inspección de código y documentos. Donde no hay evidencia clara: **UNKNOWN**.

| Feature | Estado | Evidencia |
|---------|--------|-----------|
| Registro / login | **PARTIAL** | Login UI + API register; sin página de registro |
| Perfil de usuario | **PARTIAL** | `/profile` con ventas/compras/favoritos/mensajes/reputación; sin edición de perfil |
| Crear publicación de vinilo | **DONE** | `/sell` + `POST /listings` |
| Editar publicación | **PARTIAL** | Backend `PUT /listings/{id}`; sin UI ni client API |
| Eliminar publicación | **PARTIAL** | Backend `DELETE /listings/{id}`; sin UI |
| Listar publicaciones | **DONE** | Marketplace + API |
| Filtros / búsqueda | **DONE** | Filtros UI; backend NL search sin UI dedicada |
| Favoritos | **DONE** | Backend + frontend |
| Reserva atómica | **DONE** | Backend conditional UPDATE; orders flow en frontend |
| Estado vendido / reservado / disponible | **DONE** | Modelo + UI badges |
| Mensajería comprador / vendedor | **DONE** | Con filtros anti-leak |
| Checkout / pagos | **PARTIAL** | Flujo order + simulate payment; sin gateway real |
| WebPay | **MISSING** | Solo en roadmap como próxima tarea |
| Notificaciones | **MISSING** | Sin implementación |
| Panel usuario | **DONE** | `/profile` |
| Panel admin | **DONE** | `/admin` read-only + backend summary |
| Moderación / reportes | **PARTIAL** | Disputes en orders; sin reportes de listings/usuarios |
| Imágenes de productos | **PARTIAL** | `VinylCover` decorativo; `video_url` para used; sin upload de fotos de producto |
| Seguridad básica | **PARTIAL** | JWT, bcrypt, message safety, admin key; CORS solo localhost; sin rate limiting visible |
| Testing | **DONE** | 180 pytest + 20 e2e documentados; quality gate PASSED 2026-06-05 |
| Deploy | **PARTIAL** | Docker compose local; sin CI/CD ni deploy prod documentado ejecutado |
| Documentación comercial | **PARTIAL** | BUSINESS_RULES, planes en docs; sin pitch deck / docs comerciales en repo |
| Términos / privacidad | **MISSING** | Sin páginas ni contenido legal en frontend |

---

## 6. Risks and Technical Debt

### Archivos / documentación incompletos o desalineados

- **`/releases` catálogo:** Documentado en `README.md`, `docs/api_overview.md`, migraciones Alembic — **sin router ni modelo en `app/`**.
- **`docs/api_overview.md`:** No lista orders, disputes, admin, ai-bridge, NL search.
- **AI Dev OS estándar en workspace:** Faltan `AI_CONTEXT.md`, `TASKS.md`, `SPEC.md`, `DESIGN.md`, `RELEASE_NOTES.md`.
- **Dos `PROJECT_STATUS.md`:** `workspace/` y `backend/` — riesgo de divergencia.

### TODO / FIXME en código

- No se encontraron `TODO`/`FIXME` críticos en código fuente (solo estados TODO en `MVP_ROADMAP.md` para items de cola).
- Cola explícita: WebPay, Notifications, Deploy, Beta, Launch — todos **TODO**.

### Endpoints sin frontend

- `PUT/DELETE /listings/{id}`
- `POST /listings/{id}/reserve`, `cancel-reservation` (frontend usa orders)
- `POST /listings/search/nl`
- `POST /reviews` (UNKNOWN si hay UI — no encontrada en páginas; posible gap)
- `/releases/*` (documentados pero no implementados)
- Payout profile endpoints (backend sí; UI en profile **UNKNOWN** — no visto en scan de profile tabs)

### Frontend sin backend completo

- WebPay checkout (frontend esperaría endpoints no existentes)
- Notificaciones bell
- Registro UI
- Edición/eliminación listings
- Términos legales

### Código duplicado / paths

- `QUALITY_GATE.md` duplicado backend/workspace
- `PROJECT_STATUS.md` duplicado
- Paths legacy en `melomanos_paths.py`, `README_LOCAL_RUN.md`, E2E helpers vs layout `C:\melomanos`

### Tests faltantes

- Sin unit tests frontend (solo E2E)
- WebPay y notifications sin tests (features no implementadas)
- Coverage reports marcados "Planned" en TESTING_STRATEGY

### Deuda de seguridad

- `API_BASE` y CORS hardcoded a localhost
- `ADMIN_KEY` shared secret (MVP)
- Sin rate limiting / CSRF visible
- Evidence/dispute usa URLs externas sin validación de hosting
- Secretos en `.env` locales (correctamente gitignored)

### Deuda de configuración

- **Crítico:** `MELOMANOS_*_DIR` no apunta por defecto a `C:\melomanos\*` — scripts workspace pueden fallar sin env vars
- Frontend sin `NEXT_PUBLIC_API_URL` para producción
- Tres repos git con branches distintos documentados (`main` backend, `master` frontend)
- Sin `.github/workflows` encontrado

### Deuda de documentación

- Catálogo releases obsoleto en docs
- README frontend genérico create-next-app
- Migración a layout estándar "prepared" pero no completada en paths default

---

## 7. Commands Executed or Recommended

**Comandos ejecutados en este scan:** solo inspección de filesystem y lectura de archivos. **No** se ejecutaron pytest, build, ni installs.

### Backend (seguros)

```powershell
cd C:\melomanos\backend
pip install -r requirements.txt
py run.py
py -m pytest
alembic upgrade head
# Health: curl http://127.0.0.1:8000/  o  http://127.0.0.1:8000/listings?limit=1
```

### Frontend (seguros)

```powershell
cd C:\melomanos\frontend
npm install
npm run dev
npm run build
npm run lint
npm run test:e2e
```

### Workspace (seguros — configurar env primero)

```powershell
$env:MELOMANOS_BACKEND_DIR = "C:\melomanos\backend"
$env:MELOMANOS_FRONTEND_DIR = "C:\melomanos\frontend"
$env:MELOMANOS_WORKSPACE_DIR = "C:\melomanos\workspace"

cd C:\melomanos\workspace
py project_status.py --help
py finish_task.py --dry-run
py run_melomanos.py --check
py run_audit.py
```

---

## 8. Recommended Next Phase

### **Implementation**

**Por qué:**

- El núcleo MVP marketplace está **implementado y validado** (13 milestones, quality gate PASSED).
- La tarea activa en `MVP_ROADMAP.md` es **Payment Provider Integration (WebPay placeholder)** con status **READY**.
- Las brechas restantes (WebPay, notificaciones, deploy, legal) son trabajo de **implementación**, no de discovery o diseño desde cero.
- Testing y audit son **continuos** (ya integrados en quality gate), no la fase dominante actual.

La fase **Audit** aplica al ejercicio que estás haciendo ahora con ChatGPT; la fase operativa del proyecto para avanzar al MVP completo es **Implementation**.

---

## 9. Recommended Next Task

### Nombre

**Payment Provider Integration (WebPay placeholder)**

### Motivo

- Es el **Current Active Task** con status **READY** en `backend/MVP_ROADMAP.md`.
- Bloquea launch público con pagos reales (roadmap indica dependencia explícita o decisión simulate-only).
- Escrow, orders y dispute resolution ya existen — falta el adaptador de pago y checkout UX.
- Es el primer item de "Next Recommended Work" en `workspace/PROJECT_STATUS.md`.

### Archivos afectados probables

**Backend:**
- Nuevo: `app/services/payment_provider.py` (o similar)
- `app/routers/orders.py` — `POST /orders/{id}/checkout`, webhook
- `app/models/order.py`, `app/schemas/order.py`
- `app/core/config.py` — vars WebPay sandbox
- `alembic/versions/*` — si se persisten checkout sessions
- `tests/test_orders.py` o nuevo `tests/test_webpay.py`

**Frontend:**
- `src/lib/api.ts`, `src/lib/orders.ts`
- `src/app/orders/[id]/page.tsx` — botón checkout vs simulate
- `src/types/index.ts`

**Workspace / docs:**
- `backend/MVP_ROADMAP.md`
- `backend/PROJECT_STATUS.md`
- `workspace/PROJECT_STATUS.md`

### Documentos AI Dev OS a actualizar

- `backend/MVP_ROADMAP.md` (mover item a Completed)
- `backend/PROJECT_STATUS.md`
- `workspace/PROJECT_STATUS.md` (vía `finish_task.py` / `project_status.py`)
- `backend/ARCHITECTURE.md` (sección pagos)
- `backend/BUSINESS_RULES.md` (si cambian reglas Compra Segura)
- Considerar crear `workspace/TASKS.md` o `workspace/AI_CONTEXT.md` para centralizar contexto post-scan

---

## 10. Summary for ChatGPT

```
PROYECTO: Melómanos Marketplace — marketplace chileno de vinilos
ROOT: C:\melomanos (backend + frontend + workspace, 3 repos git)

ESTADO ACTUAL:
- MVP core muy avanzado: auth, listings, favorites, messaging, orders/escrow,
  disputes, reviews, reputation, digging score, subscriptions, admin panel.
- Quality Gate PASSED (2026-06-05): 180 pytest, frontend build, 20 E2E.
- Pagos reales (WebPay), notificaciones, deploy prod, páginas legales: NO hechos.
- Pagos actuales: simulate-payment solamente.

FASE ACTUAL: Implementation (tarea activa WebPay en roadmap)

PRINCIPAL BLOQUEO:
- Integración de proveedor de pago (WebPay) pendiente — siguiente milestone READY.
- Secundario: paths workspace apuntan a C:\melomanos_market por defecto;
  requiere MELOMANOS_*_DIR para C:\melomanos.

SIGUIENTE ACCIÓN RECOMENDADA:
Implementar Payment Provider Integration (WebPay placeholder):
PaymentProvider abstraction, POST /orders/{id}/checkout, webhook,
frontend checkout, tests backend + E2E, luego finish_task.py.

ARCHIVOS CLAVE:
- backend/MVP_ROADMAP.md — backlog y tarea activa
- backend/PROJECT_STATUS.md, workspace/PROJECT_STATUS.md — estado
- backend/app/main.py — routers registrados
- backend/app/routers/orders.py — flujo compra/escrow
- frontend/src/lib/api.ts — cliente API (API_BASE hardcoded)
- frontend/src/app/orders/[id]/page.tsx — UX pago simulado
- workspace/melomanos_paths.py — resolución rutas
- workspace/finish_task.py, run_audit.py — quality gate
- backend/BUSINESS_RULES.md, ARCHITECTURE.md — reglas y diseño

BRECHAS AUDITORÍA:
- Sin registro UI, sin editar/eliminar listing en frontend
- Catálogo /releases documentado pero no en código
- Sin imágenes reales de producto (solo VinylCover decorativo)
- Sin términos/privacidad, sin notificaciones, sin CI/CD
- AI Dev OS artifacts estándar (AI_CONTEXT, TASKS, SPEC) ausentes en workspace
```

---

*Fin del scan. Generado para auditoría MVP — no modifica código de aplicación.*
