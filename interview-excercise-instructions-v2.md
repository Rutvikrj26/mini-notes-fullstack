# Full-Stack Mini Exercise (45 minutes) — Example 2: “Notes + Search”

## Objective

Create a **decoupled** full-stack app from scratch:

- **Frontend:** React + Redux (Redux Toolkit) + Vite
- **Backend:** Python 3.13 using **FastAPI** (preferred) or **aiohttp**
- **Storage:** **in-memory only** (no DB)

AI assistants (Copilot / Claude Code / etc.) are allowed and encouraged.

---

## What you’ll build: “Mini Notes”

A tiny notes app that supports:

- Creating notes
- Listing notes
- Searching notes by keyword (server-side)

No styling required.

---

## Constraints

- **Timebox:** 45 minutes total
- Start from scratch (new folders/projects).
- You do **not** need to modify any existing code.
- Keep backend and frontend in separate folders.
- Keep it small and focused: a working vertical slice beats polish.

---

## Repo layout (required)

At the end you should have:

- `backend/`
- `frontend/`
- `README.md` at the repo root with:
  - how to run backend
  - how to run frontend
  - ports used
  - how the frontend discovers the backend URL (env var or config)

---

## Backend requirements

Implement a JSON API with these endpoints:

### 1) Health

- `GET /health`
- Returns: `{ "status": "ok" }`

### 2) List notes (with optional search)

- `GET /notes`
- Optional query param: `q` (string)
  - If `q` is present, return only notes whose `title` or `content` contains `q` (case-insensitive is fine).

- Returns: an array of notes

### 3) Create note

- `POST /notes`
- Request body:
  - `{ "title": "string", "content": "string" }`

- Returns the created note

### Note model (minimum)

Each note should include at least:

- `id` (string or int)
- `title` (string)
- `content` (string)
- `created_at` (string timestamp or ISO-like string)

### Must-haves

- **CORS configured** so the Vite frontend can call the API during local dev.
- Basic validation:
  - title required
  - content required

- Clear run instructions (e.g., how to start the server).

### Nice-to-have (only if time)

- Consistent error shape (e.g., `{ "error": { "message": "...", "details": ... } }`)
- Simple logging for create/search actions

---

## Frontend requirements

Create a Vite React app that uses **Redux Toolkit**.

### State management (required)

Use a slice called `notes` (or similar) that tracks:

- `items` (array)
- `loading` (boolean)
- `error` (string/null)
- `query` (string) — current search text (optional but recommended)

### Async flows (required)

You must implement:

1. Fetch notes:
   - `GET /notes` (optionally with `?q=...`)

2. Create note:
   - `POST /notes`

You can use `createAsyncThunk`, thunks, or another RTK-compatible approach.

### UI (required)

A single page is enough. It must include:

- A search input + “Search” button (or search on Enter)
- A list of notes showing at least title + a preview of content
- A “Create note” form:
  - title input
  - content textarea
  - submit button

- Visible loading and error states for:
  - fetching notes
  - creating notes

---

## API base URL requirement

The frontend must get the backend URL via either:

- `VITE_API_BASE_URL` env variable, **or**
- a single documented config constant (e.g., `src/config.ts`)

Document your approach in the root `README.md`.

---

## AI assistant usage expectations

You may use AI tools freely, but we’ll evaluate how you use them:

- Briefly narrate what you asked the assistant for and why.
- Review generated code before accepting it:
  - correctness
  - unnecessary complexity
  - dependency choices
  - edge cases (empty search, empty form submission, etc.)

- If you changed the assistant’s output, explain the reasoning.

We’re looking for **strong judgment and workflow**, not just speed.

---

## Suggested time plan (recommended)

- **0–5 min:** Plan and scaffold folders; decide ports and API base URL strategy
- **5–18 min:** Backend endpoints + in-memory storage + CORS
- **18–38 min:** Frontend scaffold + Redux slice + fetch/create + UI
- **38–45 min:** Demo + quick “production next steps” discussion

---

## Acceptance checklist

You should be able to demonstrate:

- [ ] Backend runs and responds to `GET /health`
- [ ] `POST /notes` creates a note with `id` and `created_at`
- [ ] `GET /notes` lists notes
- [ ] `GET /notes?q=...` filters notes correctly
- [ ] Frontend runs and calls backend successfully (CORS OK)
- [ ] Notes list updates after creating a note (re-fetch or optimistic update)
- [ ] Searching updates the list based on the query
- [ ] Loading and error states are visible and sensible
- [ ] Root `README.md` explains how to run both services

---

## Stretch goals (pick one if time)

- Add `DELETE /notes/{id}`
- Add “Clear search” behavior
- Add a minimal test (backend or frontend)
- Add a short “Productionization notes” section in README:
  - validation hardening
  - lint/format/type-check
  - CI pipeline
  - containerization
  - observability (logs/metrics/tracing)
  - security considerations (CORS restrictions, input validation)

---

## Post-demo discussion (2–3 minutes)

Be ready to briefly explain:

- Why you chose your structure (folders/modules/state shape)
- How you’d evolve this from prototype to production (top 3–5 steps)
- How the AI assistant helped and how you verified the result
