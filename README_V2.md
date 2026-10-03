# ProjectPulse 2.0

> Modern Technical Project Workspace & Portfolio Platform for Engineering Students and Makers.

---

## Architecture Overview

ProjectPulse 2.0 provides a modern full-stack decoupled architecture:

- **Frontend:** React + Vite + Vanilla CSS Modern Engineering Studio design system (Manrope headings, Plus Jakarta Sans body, warm amber accents, and persistent Light / Dark mode toggle)
- **Backend:** FastAPI with modular routers, schemas, and services
- **Database:** SQLite with SQLAlchemy ORM (isolated `projectpulse_v2.db` preventing collision with MVP)
- **Authentication:** Secure `httpOnly` cookie JWT authentication
- **Milestone & Progress Engine:** Formula-driven task tracking with live progress calculations
- **Hardware Cost Tracker & BOM:** Dynamic unit price × quantity calculation, budget threshold alerts (>=80% and over-budget warnings), and CSV BOM export
- **Engineering Portfolio Showcase:** Problem statement, solution highlights, system architecture, and public shareable URLs (`/p/{slug}`) accessible without authentication

---

## Running the Application

### 1. Run the FastAPI Backend (Port 8000)

```bash
# From the repository root:
python -m uvicorn backend.main:app --reload --port 8000
```
Interactive API documentation will be available at:
`http://localhost:8000/docs`

### 2. Run the React Frontend (Port 5173)

```bash
# From the repository root:
cd frontend
npm run dev
```
Open your browser at:
`http://localhost:5173`

*(Vite dev server automatically proxies `/api` calls to the FastAPI backend at `http://127.0.0.1:8000` with credential support).*

---

## Running the Existing Streamlit MVP

The original Streamlit MVP has been preserved 100% intact in the repository root:

```bash
# Run Streamlit app:
python -m streamlit run app.py

# Run Streamlit test suite:
python test_db.py
python test_create_project.py
python test_project_detail.py
python test_cost_tracker.py
python test_showcase_db.py
```

---

## Running ProjectPulse 2.0 Automated Tests

```bash
# Comprehensive end-to-end verification of all ProjectPulse 2.0 backend endpoints:
python backend/tests/test_backend_api.py
```
