# Melómanos Visual System V1 — UX & Brand Polish Implementation Plan

**Status:** Planning only (no code changes in this document)  
**Scope:** Frontend visual system, UX copy, trust presentation, responsive polish  
**Out of scope:** Backend business logic, payment/order/auth/dispute flows, architecture changes  
**Reference:** Daniela’s UX direction + editorial marketplace reference image (warm ivory, black/gold, collector culture — directional, not pixel-perfect)

---

## Executive summary

Melómanos is functionally complete but reads as a **dark SaaS dashboard** (purple/fuchsia gradients, glass panels, mono labels, glow hovers). The target is a **premium electronic vinyl marketplace** with editorial warmth, collector credibility, and Chilean music culture.

This plan delivers Visual System V1 through **five incremental frontend phases**, preserving all flows and E2E selectors unless explicitly migrated with test updates in the same PR.

---

## 1. Visual audit of current UI

### 1.1 Global patterns that feel too technical / dashboard-like

| Pattern | Where | Why it conflicts |
|--------|--------|------------------|
| Near-black base `#08060d` + zinc text | `layout.tsx`, all pages | Reads as dev tool / admin UI, not editorial print |
| Violet → fuchsia gradients on CTAs | Navbar, ListingCard, login, sell | “Neon club UI”; dominates over music/content |
| `font-mono` uppercase micro-labels everywhere | Navbar, Marketplace, stats, badges | Feels like analytics dashboard, not culture magazine |
| `border-white/10` + `bg-white/[0.03]` cards | Most surfaces | Generic dark-glass pattern; no material warmth |
| Glow hovers (`shadow-violet`, `-translate-y`) | ListingCard, profile chip | Gaming/SaaS affordance, not premium catalog |
| Gradient price text | ListingCard, listing detail | Loud promo styling vs. restrained editorial pricing |
| “Filter crate” as primary home interaction | `Marketplace.tsx` | Tool-first; reference direction leads with story + trust |
| English nav labels mixed with Spanish UI | Navbar (`Orders`, `Messages`, `Sell Vinyl`) | Breaks local collector voice |
| Stats row as compact KPI tiles | `MarketplaceStats.tsx` | Dashboard metric strip vs. editorial trust/metrics |
| Trust as purple badge grid | `TrustBadgesPanel.tsx` | Seller gamification, not buyer-safe marketplace messaging |

### 1.2 Components that conflict most with editorial direction

**Priority redesign (highest visual impact):**

1. **`layout.tsx` + `globals.css`** — entire app tone
2. **`Navbar.tsx`** — first impression; currently gradient CTA + purple chip
3. **`Marketplace.tsx` + `page.tsx`** — no hero, no trust, filter-first
4. **`ListingCard.tsx` + `VinylCover.tsx`** — should become “collector fiche” cards
5. **`listings/[id]/page.tsx`** — product editorial layout + trust placement

**Secondary (logged-in polish):**

6. `login/page.tsx`  
7. `orders/page.tsx`, `orders/[id]/page.tsx`, `OrderEscrowCard.tsx`  
8. `favorites/page.tsx`  
9. `messages/page.tsx`, `MessageBubble.tsx`, `MessageForm.tsx`  
10. `profile/page.tsx`, `DiggingScorePanel.tsx` → Reputación Melómanos  
11. `NotificationBell.tsx`, `notifications/page.tsx`  
12. `sell/page.tsx`, `SellerShippingProfileSection.tsx`  

**Lower priority (admin / edge):**

13. `admin/page.tsx` — can lag V1 or get token-only refresh  
14. `ListingVideoSection.tsx`, dispute sections — functional copy/styling pass only  

### 1.3 What already aligns (keep behavior, restyle)

- Demo SVG covers via `VinylCover` / `listing-cover` (safe, owned assets)
- Trust *concepts* in messaging (`MessageForm` leak warning, escrow cards)
- Information architecture (home → listing → order → messages)
- `data-testid` hooks on sell, orders, digging score, admin

---

## 2. Design tokens

Implement as **CSS custom properties** in `globals.css` + Tailwind v4 `@theme inline` extension. Avoid hard-coded hex in components after Phase 1.

### 2.1 Color tokens (Daniela palette)

| Token | Hex | Usage |
|-------|-----|--------|
| `--color-bg-primary` | `#F7F3EA` | Page background (warm ivory) |
| `--color-bg-elevated` | `#FFFDF8` | Cards, modals, dropdowns |
| `--color-bg-inverse` | `#0B0B0B` | Navbar, footer bands, hero text panels |
| `--color-bg-inverse-deep` | `#080808` | Hero overlays, featured vinyl stage |
| `--color-surface-muted` | `#E4DED3` | Secondary panels, filter bar, stat strips |
| `--color-text-primary` | `#0B0B0B` | Headlines, body on light surfaces |
| `--color-text-muted` | `#6F6A61` | Secondary copy, metadata, hints |
| `--color-text-on-inverse` | `#FFFDF8` | Nav links on dark bar |
| `--color-border` | `#E4DED3` | Default borders |
| `--color-border-strong` | `#6F6A61` | Dividers, fiche rules |
| `--color-accent-gold` | `#B68A2E` | Primary CTA accent, highlights, active nav |
| `--color-accent-gold-hover` | `#9A7426` | Hover (derive ~15% darker) |
| `--color-success` | `#2F7D55` | Available, paid, completed |
| `--color-danger` | `#8A2D2D` | Errors, disputes, destructive |

**Semantic aliases (use in components):**

```css
--background: var(--color-bg-primary);
--foreground: var(--color-text-primary);
--surface: var(--color-bg-elevated);
--surface-muted: var(--color-surface-muted);
--muted-foreground: var(--color-text-muted);
--border: var(--color-border);
--accent: var(--color-accent-gold);
--accent-foreground: var(--color-bg-elevated);
--primary: var(--color-bg-inverse);
--primary-foreground: var(--color-text-on-inverse);
--success: var(--color-success);
--destructive: var(--color-danger);
```

### 2.2 Typography tokens

| Token | Proposal |
|-------|----------|
| `--font-display` | Keep Geist Sans initially; evaluate editorial serif in V1.1 |
| `--font-body` | Geist Sans |
| `--font-mono` | Geist Mono — **reduce usage** to SKU/grade/price CLP only |
| `--text-xs` … `--text-4xl` | Tailwind defaults |
| `--tracking-editorial` | `0.04em` for small caps section labels |
| `--leading-relaxed` | Body copy on listing descriptions |

### 2.3 Spacing, radius, shadow

| Token | Value | Usage |
|-------|-------|--------|
| `--space-section-y` | `3rem` / `4rem` (sm/lg) | Section vertical rhythm |
| `--space-card-p` | `1.25rem` | Fiche internal padding |
| `--radius-sm` | `0.375rem` | Inputs, pills |
| `--radius-md` | `0.75rem` | Buttons |
| `--radius-lg` | `1rem` | Cards |
| `--radius-xl` | `1.25rem` | Hero media |
| `--shadow-card` | `0 1px 3px rgb(11 11 11 / 6%)` | Subtle elevation on ivory |
| `--shadow-card-hover` | `0 8px 24px rgb(11 11 11 / 8%)` | Catalog hover (no glow) |
| `--shadow-nav` | `0 1px 0 var(--color-border)` | Navbar separation |

### 2.4 Tailwind integration plan

1. Define tokens in `:root` in `globals.css`.  
2. Map to `@theme inline` for utilities: `bg-background`, `text-muted-foreground`, `border-border`, `text-accent`, etc.  
3. Add component utility classes (optional Phase 1):  
   - `.btn-primary` — black fill, gold focus ring  
   - `.btn-accent` — gold fill, dark text  
   - `.btn-ghost` — transparent on ivory  
   - `.fiche-card` — elevated surface + border  
   - `.editorial-label` — small caps muted (not mono-by-default)  
4. **Deprecate** direct `violet-*`, `fuchsia-*`, `#08060d`, `#0d0a14` in phases; grep CI check optional later.

### 2.5 Dark mode

**V1:** Light editorial default only (matches reference). Do not ship dual themes in Phase 1–3 unless required for contrast testing.

---

## 3. Component impact map

| Component / page | Current role | V1 changes | E2E risk |
|------------------|-------------|------------|----------|
| `layout.tsx` | Root shell | Background, metadata title | Low |
| `globals.css` | 2 vars | Full token system | Low |
| `Navbar.tsx` | Nav + auth | Ivory/black bar, gold accent, Spanish labels | **High** — link text `Orders`, `Sell Vinyl` |
| `Marketplace.tsx` | Home catalog + filters | Hero, trust, sections; filters secondary | **Medium** — heading “Filter crate” |
| `MarketplaceStats.tsx` | KPI strip | Editorial metrics styling | Low |
| `ListingCard.tsx` | Grid item | Fiche layout, gold/black CTAs | Low (testids unchanged) |
| `VinylCover.tsx` | Cover image | Square fiche frame, drop violet ring | Low — keep `listing-cover-image` |
| `VinylCoverPlaceholder.tsx` | Fallback art | Ivory-safe placeholder palette | Low |
| `listings/[id]/page.tsx` | PDP | Editorial hero, trust row | Medium — heading structure |
| `login/page.tsx` | Auth | Warm card on ivory, gold CTA | Medium — button “Sign in” |
| `favorites/page.tsx` | Saved listings | Fiche grid + copy | Low |
| `orders/page.tsx` | Tabs compras/ventas | Copy + table/card polish | Medium — tab labels |
| `orders/[id]/page.tsx` | Order detail | Trust blocks, tracking copy | **High** — many testids |
| `OrderEscrowCard.tsx` | Payment state | Trust styling | Medium |
| `OrderDisputeSection.tsx` | Disputes | Danger token usage | Medium |
| `NotificationBell.tsx` | Dropdown | Light dropdown on ivory | Low |
| `notifications/page.tsx` | Inbox | List polish | Low |
| `messages/page.tsx` | Inbox | Conversation UI warmth | Low |
| `MessageForm.tsx` | Compose | In-platform trust reminder | Low — testid preserved |
| `profile/page.tsx` | Account | Reputación section rename | Medium — digging score testids |
| `DiggingScorePanel.tsx` | Score UI | Rename display → Reputación Melómanos | **Medium** — keep testids |
| `SellerShippingProfileSection.tsx` | Seller settings | Form tokens | Low — testids preserved |
| `sell/page.tsx` | Create listing | Form + CTA polish | **High** — sell-* testids |
| `SubscriptionCard.tsx` | Plan display | Card tokens | Low |
| `TrustBadgesPanel.tsx` | Seller badges | Visual only | Low |
| **New:** `TrustStrip.tsx` | Buyer trust | Compra segura, etc. | New component |
| **New:** `HomeHero.tsx` | Marketing hero | Featured vinyl, CTAs | New component |
| **New:** `SectionHeader.tsx` | Editorial titles | Reusable | New component |

---

## 4. Phase plan

### Phase 1 — Design tokens + global visual reset

**Goal:** Swap palette and base typography without layout changes.

**Work:**

- Implement tokens in `globals.css` + `@theme inline`
- Update `layout.tsx` body classes to token utilities
- Replace global violet/fuchsia in shared patterns (buttons, inputs, borders) via token aliases
- Add `frontend/src/styles/` or document token usage in README snippet
- No route or data changes

**Do not yet:** Hero, navbar structure, card layout changes

---

### Phase 2 — Home redesign (editorial shell)

**Goal:** Home feels like a marketplace magazine, not a filter dashboard.

**Work:**

- **`Navbar` V1:** Fixed/sticky black bar (`--color-bg-inverse`), ivory logo mark, gold active state, Spanish primary labels
- **`HomeHero`:** Headline, subcopy (Chile electronic vinyl), featured listing or rotating demo cover (safe SVG), primary CTA “Explorar catálogo”, secondary “Publicar vinilo”
- **Trust strip** below hero (5 trust messages — see §6)
- **Metrics band:** Listings / ciudades / artistas on `--color-surface-muted` (reuse `MarketplaceStats` data)
- **“Novedades” section:** Existing grid, renamed heading
- **Filter crate:** Move visually below fold or collapse into “Refinar búsqueda” accordion — keep same API/filter logic
- Update `metadata` title/description to Spanish brand voice

**Preserve:** `getListings`, filter behavior, `buildMarketplaceApiFilters`

---

### Phase 3 — Listing cards & catalog polish

**Goal:** Product cards read as collector fiches.

**Work:**

- `ListingCard`: ivory surface, hairline border, typographic hierarchy (artist small caps, title serif/sans bold), price in black not gradient
- Status badges: success/amber/danger tokens (no neon rings)
- `VinylCover`: remove violet top accent bar or replace with gold hairline
- Listing detail: hero cover left, editorial spec table (`DetailField`), trust strip near buy CTA
- Related listings: smaller fiche variant
- Empty states: editorial illustration tone (text-only OK for V1)

---

### Phase 4 — Logged-in experience polish

**Goal:** Consistent voice and trust across account flows.

**Work:**

- Copy map (§5) applied across Navbar, page titles, headings
- `favorites` → “Colección” / “Favoritos”
- `orders` → “Compras y ventas”
- `DiggingScorePanel` display label → “Reputación Melómanos” (**keep** `data-testid="digging-score-*"`)
- Messages: reinforce “Mantén la conversación dentro de Melómanos”
- Order detail: trust blocks near payment/shipping/dispute
- Login: Spanish-first form labels; optional keep English button text until E2E batch update
- Notifications bell dropdown: light surface, gold unread dot

---

### Phase 5 — Mobile-first polish & responsive pass

**Goal:** Editorial layout holds on small screens.

**Work:**

- Navbar: hamburger or condensed links; CTA “Publicar” always visible
- Hero: stack copy above cover; trust strip horizontal scroll or 2×2 grid
- Fiche grid: 1 col → 2 → 3
- Order detail: sticky CTA bottom bar (visual only)
- Touch targets ≥ 44px; filter form single column
- Audit contrast on ivory (gold on ivory, muted text)

---

## 5. Copy changes

Apply incrementally; **update E2E in the same PR** when changing user-visible strings relied on by tests.

| Old (EN / mixed) | New (ES — V1) | Notes |
|------------------|---------------|--------|
| Orders | Compras y ventas | Navbar + page `<h1>`; E2E: update `getByRole('link', { name: 'Orders' })` |
| Listing | Publicación | Seller-facing (“Tu publicación” already partial) |
| Listings (stats) | Publicaciones | Home metrics |
| Tracking | Seguimiento | Order detail shipping block |
| Digging Score | Reputación Melómanos | Profile + seller card; keep API field name |
| Favorites | Favoritos / Colección | Nav: “Colección”; page title can use “Tu colección” |
| Sell Vinyl / + Sell Vinyl | Publicar vinilo / Vender vinilo | Nav CTA vs page title |
| Messages | Mensajes | Navbar |
| Login | Iniciar sesión | Nav + page |
| Filter crate | Refinar búsqueda | Home section heading; E2E update |
| Vinyl & electronic marketplace | Mercado de vinilo electrónico | Hero H1 variant |
| Trust badges | Insignias de confianza | Seller profile |
| Collector | Coleccionista | Profile chip subtitle |
| Welcome back | Bienvenido de nuevo | Login |
| Sign in | Iniciar sesión | Login button — E2E update |

**E2E strategy for copy:** Prefer `data-testid` for stability (`nav-orders`, `nav-sell`) in Phase 2 PR, then migrate tests off English literals.

---

## 6. Trust system

### 6.1 Reusable trust components (new)

| Component | Message | Icon tone |
|-----------|---------|-----------|
| `TrustStrip` | Compra segura Melómanos | Shield |
| `TrustStrip` | Pago protegido | Lock |
| `TrustStrip` | Mantén la conversación dentro de Melómanos | Chat |
| `TrustStrip` | Envíos con seguimiento | Package |
| `TrustStrip` | Comunidad real de coleccionistas | Users |

Implement as compact horizontal strip (home), stacked cards (PDP/order), or inline banner (messages).

### 6.2 Placement map

| Surface | Trust elements |
|---------|----------------|
| **Home** | Full `TrustStrip` under hero; repeat “Compra segura” near first CTA |
| **Listing detail** | Strip above `ListingDetailActions`; “Pago protegido” near Comprar |
| **Order detail** | `OrderEscrowCard` + strip; “Envíos con seguimiento” near shipping |
| **Checkout / pay return** | “Pago protegido” (WebPay return banners) |
| **Messages** | Banner above thread; `MessageForm` existing leak warning styled to match |
| **Orders list** | Subtle footer note on first visit (optional tooltip) |

**Do not duplicate** backend escrow logic — presentation only.

---

## 7. Acceptance criteria

### Phase 1 — Tokens + global reset

| Category | Criteria |
|----------|----------|
| Visual | No `#08060d`, `violet-600`, `fuchsia-600` in `layout.tsx` / `globals.css`; ivory page bg visible |
| Responsive | N/A (no layout change) |
| Tests | `npm run test:unit`, `npm run build`, `npm run test:e2e` — **37/37 pass** |
| Screenshots | Full-page home + login + listing detail @ 1440px and 390px |

### Phase 2 — Home + Navbar

| Category | Criteria |
|----------|----------|
| Visual | Black navbar, gold accent, hero with headline + featured cover, trust strip visible without scroll (desktop) |
| Responsive | Hero stacks on mobile; nav usable at 390px |
| Tests | Update E2E for renamed headings/links; `demo-daniela-login`, `melomanos.spec` green |
| Screenshots | Before/after home; navbar logged-in/out |

### Phase 3 — Catalog fiches

| Category | Criteria |
|----------|----------|
| Visual | Cards on ivory; no glow hover; price readable; cover aspect consistent |
| Responsive | Grid 1/2/3 columns |
| Tests | `listing-cover.spec.ts` pass; listing buy/favorite flows pass |
| Screenshots | Grid + PDP |

### Phase 4 — Logged-in polish

| Category | Criteria |
|----------|----------|
| Visual | Spanish primary labels; Reputación Melómanos visible on profile |
| Responsive | Orders tabs, messages split view |
| Tests | Orders, disputes, notifications, webpay E2E pass |
| Screenshots | Profile, order detail, messages |

### Phase 5 — Mobile pass

| Category | Criteria |
|----------|----------|
| Visual | No horizontal overflow; contrast WCAG AA for body text on ivory |
| Responsive | 390px, 768px, 1280px breakpoints signed off |
| Tests | Full E2E suite + manual Daniela login smoke |
| Screenshots | Mobile home, PDP, order |

---

## 8. Risk analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Large visual rewrite breaks layout | Medium | High | Phase boundaries; one surface per PR |
| E2E failures on copy/nav changes | High | Medium | Add `data-testid` before renaming; update tests same PR |
| Mobile regressions (nav, hero) | Medium | Medium | Phase 5 dedicated pass; test 390px early |
| Contrast failures (gold/-muted on ivory) | Medium | Medium | Check with axe or Lighthouse; document min sizes |
| Loss of functional clarity (orders/disputes) | Low | High | Do not change order status logic/colors mapping semantics |
| Copyrighted album art | Low | Legal | Keep demo SVGs; no Discogs/real covers |
| Performance (hero images) | Low | Low | Use existing static demo assets; lazy load grids |
| Scope creep into backend | Medium | High | Explicit frontend-only PR template |
| Admin panel inconsistency | Low | Low | Token-only refresh or defer |

---

## 9. Recommended first implementation phase

### Smallest valuable coding slice: **Phase 1 + Phase 2 shell (tokens, Navbar, Home hero only)**

**Rationale:** Maximum brand perception shift with minimal touch to order/payment/dispute flows.

**First PR scope (suggested):**

1. `globals.css` — full token set  
2. `layout.tsx` — ivory background  
3. `Navbar.tsx` — black bar, gold accent, Spanish labels (+ `data-testid` on nav links)  
4. New `HomeHero.tsx` + `TrustStrip.tsx`  
5. `Marketplace.tsx` — insert hero/trust/metrics; **keep filter + grid logic unchanged**  
6. Update E2E for renamed nav/headings in same PR  
7. No changes to `orders/[id]`, WebPay, disputes, API clients  

**Estimated files:** ~8–12 frontend files, 2–4 E2E files  

**Explicitly defer:** ListingCard fiche redesign (Phase 3), profile/orders (Phase 4)

---

## 10. Validation strategy (ongoing)

```powershell
# Stack up
cd C:\melomanos\workspace
py run_melomanos.py --auto-migrate --kill-stale --no-wait
py run_melomanos.py --check

# Frontend quality gates (every PR)
cd C:\melomanos\frontend
npm run test:unit
npm run build
npm run test:e2e          # target: 37/37

# Manual smoke
# http://localhost:3000 — hero, trust, listings > 0
# http://localhost:3000/login — Daniela demo login
# http://localhost:3000/listings/{id} — cover + buy CTA visible
```

**Screenshot review checklist (Daniela):**

- [ ] Feels warm/editorial, not dashboard  
- [ ] Gold used sparingly as accent, not flood  
- [ ] Navbar confident and premium  
- [ ] Vinyl imagery featured, not buried  
- [ ] Trust visible before scroll (desktop)  
- [ ] Spanish voice consistent  

---

## Appendix A — Reference image translation (directional)

| Reference signal | Melómanos implementation |
|------------------|---------------------------|
| Warm ivory page | `--color-bg-primary` |
| Black header band | Navbar `--color-bg-inverse` |
| Gold rules / accents | CTA borders, active nav, section dividers |
| Featured vinyl hero | `HomeHero` with demo SVG cover |
| Editorial typography | Reduce mono; stronger hierarchy |
| Product fiches | Phase 3 ListingCard |
| Trust/proof blocks | `TrustStrip` + escrow copy styling |

---

## Appendix B — Files likely touched by phase

**Phase 1:** `globals.css`, `layout.tsx`, possibly shared button classes  
**Phase 2:** `Navbar.tsx`, `Marketplace.tsx`, `page.tsx`, `MarketplaceStats.tsx`, new `HomeHero.tsx`, `TrustStrip.tsx`, `e2e/*.spec.ts`  
**Phase 3:** `ListingCard.tsx`, `VinylCover.tsx`, `VinylCoverPlaceholder.tsx`, `listings/[id]/page.tsx`, `DetailField.tsx`  
**Phase 4:** `login/page.tsx`, `favorites/page.tsx`, `orders/*`, `messages/*`, `profile/page.tsx`, `DiggingScorePanel.tsx`, `NotificationBell.tsx`  
**Phase 5:** Responsive tweaks across above + `sell/page.tsx`  

---

*Document owner: Frontend / UX sprint*  
*Last updated: 2026-06-20*  
*Next step: Review with Daniela → approve Phase 1+2 PR scope → implement*
