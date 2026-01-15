# AiVRIC Solution Configurator

Local Next.js (App Router) + TypeScript app to build a rules-based security solution recommendation.

Setup

1. Install dependencies

```bash
cd "aivric-solution-configurator"
npm install
```

2. Run dev

```bash
npm run dev
```

Environment

- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM` — for sending email. If `SMTP_HOST` is not set the app will log payload and return success in dev mode.

Notes

- PDF generation uses `pdfkit` in `/app/api/pdf/route.ts`.
- State persists to `localStorage` via `zustand` persist middleware (key: `aivric-wizard`).
- Forms use `react-hook-form` + `zod` validation per step (`/data/schemas.ts`).
 - Persona presets: choose a persona at the start to reprioritize steps and influence recommendations (`/data/personas.ts`).
 - Transparent scoring: download a JSON scoring breakdown from the results page or export it via PDF. The recommender returns a `rationale` array with rule matches and per-rule scores.
 - Rule metadata: each rule now includes `severity` (low|medium|high) and `category`; scoring applies a severity multiplier so high-severity rules contribute more. See `/data/rules.ts`.
 - Rule metadata: each rule now includes `severity` (low|medium|high) and `category`; scoring applies a severity multiplier so high-severity rules contribute more. See `/data/rules.ts`.
 - Expanded ruleset: the ruleset now includes additional domain rules (MFA for admins, IaC scanning, vuln scanning, log retention, multi-cloud, pentest cadence, backups, and common compliance flags) to improve recommendations.

Rule Editor

You can edit rule overrides in the browser via the in-app Rule Editor at `/admin/rules`. Changes are saved to `localStorage` under the key `aivric-rules-override` and affect recommendations immediately in the browser (they do not modify repository files).

Testing

Run unit tests with Vitest:

```bash
npm run test
```

The tests cover the recommender scoring logic in `test/recommender.test.ts`.

Continuous Integration

The repository includes a GitHub Actions workflow that runs tests on push and pull requests. Workflow file:
`.github/workflows/ci.yml` (configured to run `npm run test` in the `aivric-solution-configurator` folder).
# AiVRIC Solution Configurator

Local development:

1. cd aivric-solution-configurator
2. npm install
3. npm run dev

API endpoints:
- `POST /api/pdf` — generate PDF from results (placeholder in dev)
- `POST /api/email` — send results via SMTP; if `SMTP_HOST` not set, returns success and logs payload in dev.

Environment variables for email:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASS`
- `SMTP_FROM`
