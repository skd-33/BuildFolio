"""
database.py — All database logic for ProjectPulse.

What is SQLite?
  SQLite is a lightweight database that stores everything in a single file
  (projectpulse.db). Python has built-in support for it — no extra install!

What does this file do?
  It contains functions to:
  - Create the database tables (if they don't exist yet)
  - Add, read, update, and delete projects, tasks, and components.
  These operations are called CRUD: Create, Read, Update, Delete.
"""

import sqlite3  # Built into Python — no install needed
import os

# --------------------------------------------------------------------------
# DATABASE FILE PATH
# --------------------------------------------------------------------------
# This makes the DB file sit next to this script, no matter where you run it.
DB_PATH = os.path.join(os.path.dirname(__file__), "projectpulse.db")


# --------------------------------------------------------------------------
# HELPER: Get a database connection
# --------------------------------------------------------------------------
def get_connection():
    """
    Opens a connection to the SQLite database file.
    detect_types lets SQLite understand Python datetime objects.
    """
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row  # Lets us access columns by name (row["name"])
    return conn


# --------------------------------------------------------------------------
# INITIALIZE DATABASE — Create tables if they don't exist
# --------------------------------------------------------------------------
def init_db():
    """
    Creates all three tables on first launch.
    'IF NOT EXISTS' means this is safe to call every time — it won't
    overwrite existing data.
    """
    conn = get_connection()
    cursor = conn.cursor()  # A cursor is like a pen that writes SQL queries

    # ── Table 1: projects ────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            description TEXT,
            deadline    TEXT,
            budget      REAL    DEFAULT 0.0,
            github_url  TEXT,
            kicad_url   TEXT,
            fusion_url  TEXT,
            arduino_url TEXT,
            docs_url    TEXT,
            demo_url    TEXT,
            created_at  TEXT    DEFAULT (datetime('now', 'localtime'))
        )
    """)

    # ── Table 2: tasks ───────────────────────────────────────────────────
    # 'FOREIGN KEY' links each task back to its parent project.
    # ON DELETE CASCADE means: if a project is deleted, its tasks are too.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id  INTEGER NOT NULL,
            name        TEXT    NOT NULL,
            description TEXT,
            status      TEXT    DEFAULT 'Pending',
            order_index INTEGER DEFAULT 0,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    """)

    # ── Table 3: components ──────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS components (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id     INTEGER NOT NULL,
            name           TEXT    NOT NULL,
            quantity       INTEGER DEFAULT 1,
            unit_price     REAL    DEFAULT 0.0,
            total_price    REAL    DEFAULT 0.0,
            purchase_link  TEXT,
            notes          TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    """)

    # ── Table 4: showcases ──────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS showcases (
            project_id           INTEGER PRIMARY KEY,
            showcase_slug        TEXT UNIQUE,
            problem_statement    TEXT,
            solution_description TEXT,
            technologies         TEXT,
            architecture_data    TEXT,
            github_url           TEXT,
            is_published         BOOLEAN DEFAULT 0,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    """)

    # ── Table 5: showcase_media ──────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS showcase_media (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id    INTEGER NOT NULL,
            file_path     TEXT NOT NULL,
            media_type    TEXT NOT NULL,
            title         TEXT,
            description   TEXT,
            display_order INTEGER DEFAULT 0,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    """)

    # Enable foreign key enforcement (SQLite has it off by default)
    cursor.execute("PRAGMA foreign_keys = ON")

    conn.commit()   # Save all the changes
    conn.close()    # Close the connection
    print(f"[OK] Database ready at: {DB_PATH}")


# ============================================================================
# PROJECT CRUD FUNCTIONS
# ============================================================================

def create_project(name, description="", deadline=None, budget=0.0,
                   github_url="", kicad_url="", fusion_url="",
                   arduino_url="", docs_url="", demo_url=""):
    """
    Inserts a new project row into the 'projects' table.
    Returns the ID of the newly created project.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projects
            (name, description, deadline, budget,
             github_url, kicad_url, fusion_url, arduino_url, docs_url, demo_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, description, deadline, budget,
          github_url, kicad_url, fusion_url, arduino_url, docs_url, demo_url))
    # '?' placeholders prevent SQL Injection attacks — never use f-strings in SQL!
    project_id = cursor.lastrowid  # The ID the database assigned to the new row
    conn.commit()
    conn.close()
    return project_id


def get_all_projects():
    """
    Fetches every project from the database.
    Returns a list of Row objects (access values like row["name"]).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_project(project_id):
    """
    Fetches a single project by its ID.
    Returns one Row object, or None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_project(project_id, name, description, deadline, budget,
                   github_url, kicad_url, fusion_url,
                   arduino_url, docs_url, demo_url):
    """Updates all fields of an existing project."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projects
        SET name=?, description=?, deadline=?, budget=?,
            github_url=?, kicad_url=?, fusion_url=?,
            arduino_url=?, docs_url=?, demo_url=?
        WHERE id=?
    """, (name, description, deadline, budget,
          github_url, kicad_url, fusion_url,
          arduino_url, docs_url, demo_url,
          project_id))
    conn.commit()
    conn.close()


def delete_project(project_id):
    """
    Deletes a project and — thanks to CASCADE — also deletes
    all its tasks and components automatically.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()


# ============================================================================
# TASK CRUD FUNCTIONS
# ============================================================================

def create_task(project_id, name, description="", status="Pending", order_index=0):
    """Adds a new task (stage) to a project."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (project_id, name, description, status, order_index)
        VALUES (?, ?, ?, ?, ?)
    """, (project_id, name, description, status, order_index))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id


def get_tasks(project_id):
    """Fetches all tasks for a given project, ordered by order_index."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM tasks
        WHERE project_id = ?
        ORDER BY order_index ASC
    """, (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_task_status(task_id, status):
    """Updates only the status of a task (Pending / In Progress / Completed)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()


def update_task(task_id, name, description, status):
    """Updates name, description, and status of a task."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks SET name=?, description=?, status=?
        WHERE id=?
    """, (name, description, status, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    """Deletes a single task by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


def calculate_progress(project_id):
    """
    Calculates the completion percentage for a project.

    Formula:
        progress = (completed tasks / total tasks) * 100

    Returns a float between 0.0 and 100.0.
    Returns 0.0 if there are no tasks yet.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE project_id=?", (project_id,))
    total = cursor.fetchone()[0]  # [0] gets the first column of the result

    cursor.execute("""
        SELECT COUNT(*) FROM tasks
        WHERE project_id=? AND status='Completed'
    """, (project_id,))
    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0.0  # Avoid division by zero
    return round((completed / total) * 100, 1)  # Round to 1 decimal place


# ============================================================================
# COMPONENT CRUD FUNCTIONS
# ============================================================================

def create_component(project_id, name, quantity=1, unit_price=0.0,
                     purchase_link="", notes=""):
    """Adds a component/part to the cost tracker."""
    total_price = quantity * unit_price  # Calculate automatically
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO components
            (project_id, name, quantity, unit_price, total_price, purchase_link, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (project_id, name, quantity, unit_price, total_price, purchase_link, notes))
    comp_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return comp_id


def get_components(project_id):
    """Fetches all components for a given project."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM components WHERE project_id=?", (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_total_spent(project_id):
    """
    Sums up all component costs for a project.
    Returns the total amount spent so far.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(total_price), 0.0)
        FROM components
        WHERE project_id=?
    """, (project_id,))
    # COALESCE returns 0.0 if there are no components (avoids None)
    total = cursor.fetchone()[0]
    conn.close()
    return total


def update_component(comp_id, name, quantity, unit_price, purchase_link, notes):
    """Updates a component's details and recalculates total_price."""
    total_price = quantity * unit_price
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE components
        SET name=?, quantity=?, unit_price=?, total_price=?,
            purchase_link=?, notes=?
        WHERE id=?
    """, (name, quantity, unit_price, total_price, purchase_link, notes, comp_id))
    conn.commit()
    conn.close()


def delete_component(comp_id):
    """Deletes a single component by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM components WHERE id=?", (comp_id,))
    conn.commit()
    conn.close()


def get_component(comp_id):
    """Fetches a single component by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM components WHERE id=?", (comp_id,))
    row = cursor.fetchone()
    conn.close()
    return row


# ============================================================================
# SHOWCASE CRUD FUNCTIONS
# ============================================================================

def upsert_showcase(project_id, showcase_slug=None, problem_statement="",
                    solution_description="", technologies="", architecture_data="",
                    github_url="", is_published=False):
    """Inserts or updates a showcase for a project."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO showcases
            (project_id, showcase_slug, problem_statement, solution_description,
             technologies, architecture_data, github_url, is_published)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (project_id, showcase_slug, problem_statement, solution_description,
          technologies, architecture_data, github_url, 1 if is_published else 0))
    conn.commit()
    conn.close()


def get_showcase(project_id):
    """Fetches the showcase data for a project."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM showcases WHERE project_id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def add_showcase_media(project_id, file_path, media_type, title="", description="", display_order=0):
    """Adds a media record for a showcase."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO showcase_media
            (project_id, file_path, media_type, title, description, display_order)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (project_id, file_path, media_type, title, description, display_order))
    media_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return media_id


def get_showcase_media(project_id):
    """Fetches all media for a showcase, ordered by display_order."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM showcase_media
        WHERE project_id = ?
        ORDER BY display_order ASC, id ASC
    """, (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_showcase_media(media_id):
    """Deletes a specific media record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM showcase_media WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()


