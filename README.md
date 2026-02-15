# Mini Notes — Full-Stack App

A decoupled full-stack notes application with create, list, and search functionality.

- **Backend:** Python 3.13 + FastAPI + Pydantic v2 (in-memory storage)
- **Frontend:** React 19 + TypeScript + Vite + Redux Toolkit + Material UI
- **Package Management:** `uv` (backend), `npm` (frontend)

---

## Architecture

```
.
├── backend/          # FastAPI API — port 8000
├── frontend/         # React Vite SPA — port 5173
└── README.md         # This file
```

| Service  | Port   | URL                        |
|----------|--------|----------------------------|
| Backend  | `8000` | http://localhost:8000       |
| Frontend | `5173` | http://localhost:5173       |

---

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Node.js 22 LTS+
- npm

### 1. Run the Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify: http://localhost:8000/health → `{"status": "ok"}`

### 2. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open: http://localhost:5173

---

## API Endpoints

| Method | Path        | Description                       |
|--------|-------------|-----------------------------------|
| GET    | `/health`   | Health check                      |
| GET    | `/notes`    | List all notes                    |
| GET    | `/notes?q=` | Search notes by keyword           |
| POST   | `/notes`    | Create a note (`title`, `content`)|

### Example: Create a note

```bash
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "content": "World"}'
```

### Example: Search notes

```bash
curl "http://localhost:8000/notes?q=hello"
```

---

## How the Frontend Discovers the Backend

The frontend uses the `VITE_API_BASE_URL` environment variable, defined in `frontend/.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

This is read at build time via `import.meta.env.VITE_API_BASE_URL` in `src/api/client.ts`. A `.env.example` file is committed to the repo as a template.

---

## CORS

The FastAPI backend includes `CORSMiddleware` configured to allow requests from `http://localhost:5173` (the Vite dev server). This is handled automatically — no proxy configuration needed.

---

## Running Backend Tests

```bash
cd backend
uv run pytest
```

Runs 20 tests with coverage report (89% coverage).

---

## Quality Gates (Backend)

```bash
cd backend
uv run ruff check --fix .    # Lint
uv run ruff format .          # Format
uv run pyright                # Type checking (strict mode)
uv run pytest                 # Tests with coverage
```

---

## Productionization Notes

To evolve this prototype into production:

1. **Persistent storage** — Replace in-memory list with PostgreSQL + SQLAlchemy/SQLModel async.
2. **Validation hardening** — Add rate limiting, input sanitization, max payload sizes.
3. **Lint/format/type-check** — Already configured with ruff + pyright (strict). Add ESLint flat config for frontend.
4. **CI pipeline** — GitHub Actions with lint → type-check → test → build stages for both services.
5. **Containerization** — Dockerfiles for both services + docker-compose for local dev.
6. **Observability** — Structured JSON logging, OpenTelemetry traces, Prometheus metrics.
7. **Security** — Restrict CORS origins per environment, add authentication (JWT/OAuth2), HTTPS.
8. **Testing** — Add frontend component tests with Vitest + React Testing Library.
