# BuildFolio

BuildFolio helps you build, track, understand, and showcase technical projects.

> Give BuildFolio your project information → AI understands it → generates an editable portfolio → publish it as a shareable link.

**[🚀 Live Demo](https://projectpulse-1-mjqh.onrender.com)**

> [!IMPORTANT]
> **AI portfolio generation runs locally using Ollama.**
>
> The public Render deployment provides the full application — project workspace, task tracking, component management, portfolio editor, and public portfolio experience — but Ollama is **not** running on Render.
>
> To use the AI generation feature, run Ollama on the same machine as the BuildFolio backend and pull the model before starting. See [AI Setup](#7-ai-setup) for details.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Features](#2-features)
3. [How It Works](#3-how-it-works)
4. [Architecture](#4-architecture)
5. [Tech Stack](#5-tech-stack)
6. [Local Setup](#6-local-setup)
7. [AI Setup](#7-ai-setup)
8. [Using BuildFolio](#8-using-buildfolio)
9. [Project Structure](#9-project-structure)
10. [Deployment](#10-deployment)
11. [Testing](#11-testing)
12. [Contributing](#12-contributing)
13. [Future Ideas](#13-future-ideas)
14. [License](#14-license)

---

## 1. Overview

BuildFolio combines four things that engineers typically manage in separate tools:

| Layer | What it does |
|---|---|
| **Project tracker** | Source of truth for your actual engineering work — description, status, deadlines, links, notes |
| **Task tracking** | Granular task list with status tracking and automatic progress calculation |
| **Component / BOM** | Parts list with quantity, unit cost, total cost, and budget tracking |
| **Portfolio** | AI-generated and user-edited showcase that can be published as a public, shareable page |

**The distinction matters:**

- The **project tracker** stores your real engineering data. It does not depend on AI.
- **AI** reads that data and generates a draft portfolio. It does not modify your project data.
- The **portfolio** is the presentation layer. It can be edited freely before publishing.
- The **public portfolio** is accessible to anyone via a unique URL — no login required.

AI-generated content does not replace or overwrite your underlying project, task, or component data.

---

## 2. Features

### Project Management

- Create projects with name, description, status, technologies, deadline, and budget
- Add project links: GitHub, KiCad, Fusion 360, Arduino, docs, and demo URLs
- Edit and update project information
- Track overall project progress driven by task completion

### Task Tracking

- Create tasks with name, description, and status
- Update task status: `Pending`, `In Progress`, `Completed`
- Delete tasks
- Automatic progress calculation based on completed vs. total tasks

### Components / Bill of Materials

- Add components with name, category, quantity, and unit price
- Total price is calculated automatically (`quantity × unit_price`)
- Edit and delete components
- Budget utilization summary with remaining budget and over-budget detection

### Costs

- Per-project cost summary: total spent, remaining budget, percentage used
- Over-budget warning when component costs exceed the project budget

### Portfolio

- Every project has an associated portfolio created automatically
- Generate portfolio content with AI (requires Ollama locally)
- AI populates structured sections: Summary, Problem, Solution, Hardware, Software, Architecture, Challenges, and Future Improvements
- Edit any generated section before publishing
- Add, remove, and reorder portfolio sections manually
- Attach media URLs to the portfolio
- Publish the portfolio with a unique slug-based URL
- Custom slug support (must be unique)
- Published portfolios are publicly accessible without authentication

### AI

- Local inference via Ollama
- Configurable model (recommended: `gemma3:1b`)
- Structured JSON output — the AI produces data, not raw HTML
- Each fact is tagged with a confidence status: `confirmed`, `inferred`, or `unknown`
- Up to 3 automatic retries on invalid or empty AI output

---

## 3. How It Works

```
Project information (name, description, tasks, components, notes)
       ↓
FastAPI backend assembles a context string
       ↓
AI service sends the context to Ollama
       ↓
Ollama runs the local model
       ↓
Model returns structured JSON (ProjectKnowledge)
       ↓
Backend validates and maps the output to portfolio sections
       ↓
User reviews and edits each section in the portfolio editor
       ↓
User publishes the portfolio
       ↓
Public portfolio page is accessible via a shareable URL
```

BuildFolio does **not** ask the model to generate HTML. The AI returns a structured JSON object; the React frontend handles all rendering and presentation.

---

## 4. Architecture

### Application Layer

```
Browser
   ↓
React + Vite  (port 5173 in development)
   ↓  (API calls proxied to /api)
FastAPI  (port 8000)
   ↓
SQLAlchemy ORM
   ↓
SQLite (local development) / PostgreSQL (production)
```

### AI Layer

```
FastAPI  (/api/projects/{id}/generate)
   ↓
AI service  (backend/ai/service.py)
   ↓
Provider abstraction  (backend/ai/providers.py)
   ↓
Ollama HTTP API  (http://localhost:11434)
   ↓
Local model  (e.g. gemma3:1b)
   ↓
Structured JSON — validated by Pydantic (ProjectKnowledge)
   ↓
Portfolio sections written to the database
```

**Component responsibilities:**

- **React** handles the user interface, routing, and all content rendering.
- **FastAPI** handles authentication, business logic, database writes, and API routes.
- **SQLAlchemy** manages all database access through ORM models.
- **SQLite** is used for local development (default, no setup required).
- **PostgreSQL** is used in production via the `DATABASE_URL` environment variable.
- **Ollama** provides local model inference — no cloud dependency for AI.
- The **React app** renders structured portfolio content from the database; it does not interpret raw AI text as markup.

---

## 5. Tech Stack

| Layer | Technology |
|---|---|
| Frontend framework | React 19 + Vite |
| Frontend routing | React Router v7 |
| Frontend icons | Lucide React |
| Backend framework | FastAPI |
| Backend language | Python |
| Database ORM | SQLAlchemy 2 |
| Authentication | JWT via `httpOnly` cookies |
| Local database | SQLite |
| Production database | PostgreSQL (psycopg v3) |
| AI runtime | Ollama |
| AI model | Configurable — `gemma3:1b` recommended |
| HTTP client (AI) | httpx |
| Data validation | Pydantic v2 |
| Production hosting | Render |

---

## 6. Local Setup

### Prerequisites

- Python 3.10 or later
- Node.js 18 or later and npm
- Git
- [Ollama](https://ollama.com) — required only for AI generation

### Clone

```bash
git clone <repository-url>
cd ProjectPulse
```

### Backend

```bash
cd backend
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the FastAPI server (run from the **repository root**, not from inside `backend/`):
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Interactive API documentation is available at `http://localhost:8000/docs`.

### Frontend

```bash
# From the repository root:
cd frontend
npm install
npm run dev
```

Open your browser at `http://localhost:5173`.

Vite automatically proxies all `/api` requests to the FastAPI backend at `http://127.0.0.1:8000`. Credentials (cookies) are forwarded correctly.

---

## 7. AI Setup

> [!IMPORTANT]
> AI generation requires Ollama to be installed and running **on the same machine as the BuildFolio backend**. The Render deployment does not include Ollama.

### Install and configure Ollama

1. Download and install Ollama from [https://ollama.com](https://ollama.com).

2. Pull the recommended model:
   ```bash
   ollama pull gemma3:1b
   ```

3. Ensure Ollama is running (it starts automatically after installation on most platforms, or run `ollama serve`).

4. Start the BuildFolio backend with the model configured:

   **Windows PowerShell:**
   ```powershell
   $env:AI_PROVIDER="ollama"
   $env:AI_MODEL="gemma3:1b"
   python -m uvicorn backend.main:app --reload --port 8000
   ```

   **Linux / macOS:**
   ```bash
   AI_PROVIDER=ollama AI_MODEL=gemma3:1b python -m uvicorn backend.main:app --reload --port 8000
   ```

5. Open a project in BuildFolio and use **Generate with AI**.

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `AI_PROVIDER` | `ollama` | Inference provider |
| `AI_MODEL` | `gemma3:1b` | Model name passed to Ollama |
| `AI_BASE_URL` | `http://localhost:11434` | Ollama API base URL |
| `AI_API_KEY` | _(empty)_ | API key for non-Ollama providers |

> [!NOTE]
> The AI layer is separated from the application logic so the inference provider can be extended. The primary supported setup is **Ollama running locally**. The provider abstraction also accepts an OpenAI-compatible endpoint via `AI_BASE_URL` and `AI_API_KEY`, but this is not the primary tested configuration.

---

## 8. Using BuildFolio

### Typical workflow

1. **Create an account** — sign up with email, username, and password.
2. **Sign in** — authentication uses secure `httpOnly` cookies.
3. **Create a project** — fill in name, description, technologies, deadline, budget, and optional links.
4. **Add tasks** — break the project into tasks and track their status.
5. **Add components** — list parts with quantity and unit price for BOM and cost tracking.
6. **Track progress** — the dashboard shows completion percentage driven by task status.
7. **Open the Portfolio tab** — every project has a portfolio workspace.
8. **Generate with AI** — the backend sends your project data to Ollama, which returns structured portfolio content.
9. **Review the generated content** — check each section (Summary, Problem, Solution, Hardware, Software, Architecture, Challenges, Future Improvements).
10. **Edit freely** — modify any section, add or remove sections, attach media.
11. **Publish** — toggle the portfolio to published and optionally set a custom slug.
12. **Share** — copy the public URL and share it. Viewers do not need an account.

> [!NOTE]
> AI generates a first draft based only on the information you have provided. You should review generated content before publishing. Facts are tagged as `confirmed`, `inferred`, or `unknown` to help you identify what to verify.

---

## 9. Project Structure

```
ProjectPulse/
├── backend/
│   ├── ai/
│   │   ├── providers.py        # Ollama / OpenAI-compatible HTTP client
│   │   ├── schema.py           # Pydantic model for AI output (ProjectKnowledge)
│   │   └── service.py          # Context builder and generation logic
│   ├── middleware/
│   │   └── auth.py             # JWT cookie authentication dependency
│   ├── models/
│   │   ├── component.py        # Component (BOM) ORM model
│   │   ├── portfolio.py        # Portfolio ORM model
│   │   ├── portfolio_media.py  # Portfolio media ORM model
│   │   ├── portfolio_section.py # Portfolio section ORM model
│   │   ├── project.py          # Project ORM model
│   │   ├── task.py             # Task ORM model
│   │   └── user.py             # User ORM model
│   ├── routes/
│   │   ├── auth.py             # Registration, login, logout, current user
│   │   ├── components.py       # Component CRUD and cost summary
│   │   ├── portfolio.py        # Portfolio CRUD, AI generation, sections, media
│   │   ├── projects.py         # Project CRUD
│   │   ├── public.py           # Unauthenticated public portfolio endpoint
│   │   └── tasks.py            # Task CRUD
│   ├── schemas/
│   │   ├── auth.py             # Auth request/response schemas
│   │   ├── component.py        # Component and cost summary schemas
│   │   ├── portfolio.py        # Portfolio schemas including PublicPortfolioOut
│   │   ├── project.py          # Project schemas
│   │   └── task.py             # Task schemas
│   ├── services/
│   │   ├── auth_service.py     # Password hashing and JWT generation
│   │   ├── cost_service.py     # Budget and cost calculation
│   │   ├── portfolio_service.py # Portfolio query helpers
│   │   ├── progress_service.py  # Task-based progress calculation
│   │   └── project_service.py   # Project query helpers and slug generation
│   ├── tests/
│   │   └── test_backend_api.py  # End-to-end backend API test
│   ├── config.py               # Environment variable loading and defaults
│   ├── database.py             # SQLAlchemy engine and session setup
│   └── main.py                 # FastAPI application entry point
├── frontend/
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── api/                # API client functions
│   │   ├── assets/             # Images and static resources
│   │   ├── components/         # Reusable UI components
│   │   ├── context/            # React context (authentication state)
│   │   ├── pages/
│   │   │   ├── CreateProject.jsx    # New project form
│   │   │   ├── Dashboard.jsx        # Project list and overview
│   │   │   ├── Landing.jsx          # Public landing page
│   │   │   ├── Login.jsx            # Sign in page
│   │   │   ├── ProjectWorkspace.jsx # Project detail, tasks, BOM, portfolio editor
│   │   │   ├── PublicPortfolio.jsx  # Public portfolio view (no auth required)
│   │   │   └── Signup.jsx           # Registration page
│   │   ├── styles/             # CSS modules and global styles
│   │   ├── App.jsx             # Root component and route definitions
│   │   └── main.jsx            # React entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js          # Vite config with API proxy to port 8000
├── .gitignore
└── README.md

```

---

## 10. Deployment

BuildFolio is deployed on [Render](https://render.com).

### Public deployment

```
Browser
   ↓
Render — React/Vite static build (frontend)
   ↓
Render — FastAPI backend
   ↓
Production PostgreSQL database
```

The deployed application handles all project management, task tracking, component tracking, portfolio editing, and public portfolio viewing.

**Ollama does not run on Render.** The AI generation endpoint returns a service-unavailable error on the live deployment because no Ollama instance is reachable. All other features work fully on the deployed version.

### Local AI development

```
Local browser
   ↓
Local React dev server  (port 5173)
   ↓
Local FastAPI backend  (port 8000)
   ↓
Ollama  (port 11434)
   ↓
Local model  (e.g. gemma3:1b)
```

### Environment variables for production

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (`postgresql://...`) |
| `SECRET_KEY` | Secret for JWT signing — use a long random value |
| `AI_PROVIDER` | `ollama` |
| `AI_MODEL` | Model name |
| `AI_BASE_URL` | Ollama API URL |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins |
| `COOKIE_SECURE` | Set to `true` in production (HTTPS only) |

**Live demo:** [https://projectpulse-1-mjqh.onrender.com](https://projectpulse-1-mjqh.onrender.com)

---

## 11. Testing

### Backend API test

The repository includes an end-to-end backend verification script that exercises the full request pipeline against a live FastAPI instance using `TestClient`.

The test covers:

- Health check
- User registration and authentication
- Project creation and retrieval
- Task creation, status update, and progress calculation
- Component creation and cost summary
- Portfolio retrieval, editing, and publishing
- Portfolio section and media management
- Public portfolio access (unauthenticated)

```bash
# From the repository root:
python backend/tests/test_backend_api.py
```

### Frontend build check

To verify the frontend compiles without errors:

```bash
cd frontend
npm run build
```

---

## 12. Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Make your changes.
4. Run the backend test: `python backend/tests/test_backend_api.py`
5. Verify the frontend builds: `cd frontend && npm run build`
6. Open a pull request with a clear description of what changed and why.

Use GitHub Issues to report bugs or propose features.

---

## 13. Future Ideas

These are directions that have been discussed but are **not currently implemented**:

- **Document ingestion** — allow users to upload project documentation and include extracted text as context for AI generation
- **GitHub / README integration** — pull project description and context directly from a GitHub repository
- **Project image understanding** — use a vision-capable model to analyse photos of hardware builds
- **Additional AI providers** — first-class support for OpenAI, Anthropic, or other OpenAI-compatible services
- **Richer portfolio customization** — themes, custom sections, drag-and-drop reordering
- **Project-specific AI Q&A** — answer questions about a project based on its stored information

---

## 14. License

BuildFolio is released under the **MIT License**.
