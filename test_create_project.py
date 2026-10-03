"""
test_create_project.py — Tests the full Create Project workflow.

This simulates exactly what happens when a user fills in the form
and clicks "Save Project":
  1. Create a project with all fields
  2. Add tasks with different statuses
  3. Verify everything is saved and retrieved correctly
  4. Verify progress calculation is accurate
  5. Test edge cases: empty task names, no deadline, zero budget

Run with:  python test_create_project.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Clean up any old test DB so we start fresh
DB_FILE = os.path.join(os.path.dirname(__file__), "projectpulse.db")
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("[INFO] Removed old database for a clean test.")

import database as db

db.init_db()

PASS = "[PASS]"
FAIL = "[FAIL]"

errors = []

def check(label, condition, got=None, expected=None):
    if condition:
        print(f"  {PASS}  {label}")
    else:
        msg = f"  {FAIL}  {label}"
        if got is not None:
            msg += f" | got={got!r} expected={expected!r}"
        print(msg)
        errors.append(label)

print()
print("=" * 60)
print("Milestone 3 — Create Project Workflow Tests")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────
# TEST 1: Create a project with all fields
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 1] Create a full project with all fields")

pid = db.create_project(
    name="Smart Irrigation System",
    description="ESP32-based automated plant watering system with soil moisture sensors.",
    deadline="2026-11-30",
    budget=3500.0,
    github_url="https://github.com/user/irrigation",
    kicad_url="https://github.com/user/irrigation/tree/main/pcb",
    fusion_url="https://a360.co/abc123",
    arduino_url="https://github.com/user/irrigation/tree/main/firmware",
    docs_url="https://notion.so/smart-irrigation",
    demo_url="https://youtube.com/watch?v=demo",
)
check("Project created (ID > 0)", pid > 0, got=pid, expected=">0")

# Retrieve and verify
p = db.get_project(pid)
check("Name saved correctly",        p["name"]        == "Smart Irrigation System")
check("Description saved correctly", "ESP32" in p["description"])
check("Deadline saved correctly",    p["deadline"]    == "2026-11-30")
check("Budget saved correctly",      p["budget"]      == 3500.0, got=p["budget"], expected=3500.0)
check("GitHub URL saved",            p["github_url"]  == "https://github.com/user/irrigation")
check("KiCad URL saved",             p["kicad_url"]   != "")
check("Fusion URL saved",            p["fusion_url"]  != "")
check("Arduino URL saved",           p["arduino_url"] != "")
check("Docs URL saved",              p["docs_url"]    != "")
check("Demo URL saved",              p["demo_url"]    != "")

# ─────────────────────────────────────────────────────────────────
# TEST 2: Add tasks (simulating the form's task list)
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 2] Add tasks with various statuses")

tasks_data = [
    ("Requirements & Spec",   "",                     "Completed",   0),
    ("Schematic Design",      "Use KiCad 8",          "Completed",   1),
    ("PCB Layout",            "2-layer, JLCPCB fab",  "In Progress", 2),
    ("Component Procurement", "Order from Robu.in",   "Pending",     3),
    ("Firmware Development",  "ESP-IDF + MQTT",       "Pending",     4),
    ("Functional Testing",    "",                     "Pending",     5),
]
for name, desc, status, idx in tasks_data:
    db.create_task(pid, name, description=desc, status=status, order_index=idx)

tasks = db.get_tasks(pid)
check("Correct number of tasks saved", len(tasks) == 6, got=len(tasks), expected=6)
check("Tasks ordered by order_index",  tasks[0]["name"] == "Requirements & Spec")
check("Last task is Functional Testing", tasks[-1]["name"] == "Functional Testing")

# Verify statuses
statuses = [t["status"] for t in tasks]
check("Completed tasks count",   statuses.count("Completed")   == 2)
check("In Progress tasks count", statuses.count("In Progress") == 1)
check("Pending tasks count",     statuses.count("Pending")     == 3)

# ─────────────────────────────────────────────────────────────────
# TEST 3: Progress calculation
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 3] Progress calculation")

progress = db.calculate_progress(pid)
expected_progress = round((2 / 6) * 100, 1)  # 33.3%
check("Progress is 33.3%", progress == expected_progress,
      got=progress, expected=expected_progress)

# Update one more task and re-check
db.update_task_status(tasks[2]["id"], "Completed")  # PCB Layout -> Completed
progress2 = db.calculate_progress(pid)
expected2 = round((3 / 6) * 100, 1)  # 50.0%
check("After update: Progress is 50.0%", progress2 == expected2,
      got=progress2, expected=expected2)

# ─────────────────────────────────────────────────────────────────
# TEST 4: Edge case — project with NO deadline and ZERO budget
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 4] Edge case — minimal project (no deadline, no budget)")

pid2 = db.create_project(name="Quick LED Blink Test")
p2 = db.get_project(pid2)
check("Minimal project created", pid2 > 0)
check("Deadline is None",        p2["deadline"] is None, got=p2["deadline"], expected=None)
check("Budget defaults to 0.0",  p2["budget"] == 0.0,    got=p2["budget"], expected=0.0)
check("Empty URLs are empty strings or None",
      p2["github_url"] in (None, ""))

# Progress on project with NO tasks = 0%
check("Progress with 0 tasks = 0.0%",
      db.calculate_progress(pid2) == 0.0,
      got=db.calculate_progress(pid2), expected=0.0)

# ─────────────────────────────────────────────────────────────────
# TEST 5: get_all_projects returns both projects
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 5] Fetch all projects")
all_projects = db.get_all_projects()
check("Two projects in DB", len(all_projects) == 2, got=len(all_projects), expected=2)
# get_all_projects returns newest first (ORDER BY created_at DESC)
names = [p["name"] for p in all_projects]
check("Both project names present",
      "Smart Irrigation System" in names and "Quick LED Blink Test" in names)

# ─────────────────────────────────────────────────────────────────
# TEST 6: Update a project (simulate editing)
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 6] Update a project")
db.update_project(
    project_id=pid2,
    name="Quick LED Blink Test (Updated)",
    description="A simple LED blink project.",
    deadline="2026-12-01",
    budget=200.0,
    github_url="https://github.com/user/led-blink",
    kicad_url="", fusion_url="", arduino_url="", docs_url="", demo_url=""
)
p2_updated = db.get_project(pid2)
check("Name updated", p2_updated["name"] == "Quick LED Blink Test (Updated)")
check("Budget updated", p2_updated["budget"] == 200.0)
check("Deadline updated", p2_updated["deadline"] == "2026-12-01")

# ─────────────────────────────────────────────────────────────────
# TEST 7: Delete a project (cascade deletes tasks too)
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 7] Delete project and verify cascade")

# Add a task to pid2 first
db.create_task(pid2, "Blink LED Task", status="Pending")
tasks_before = db.get_tasks(pid2)
check("Task added before delete", len(tasks_before) == 1)

db.delete_project(pid2)
check("Project deleted",          db.get_project(pid2) is None)
tasks_after = db.get_tasks(pid2)
check("Tasks cascade-deleted",    len(tasks_after) == 0,
      got=len(tasks_after), expected=0)

# ─────────────────────────────────────────────────────────────────
# RESULTS SUMMARY
# ─────────────────────────────────────────────────────────────────
print()
print("=" * 60)
if errors:
    print(f"FAILED — {len(errors)} test(s) failed:")
    for e in errors:
        print(f"  - {e}")
else:
    print("ALL TESTS PASSED! Create Project workflow is working correctly.")
    print(f"DB file: {db.DB_PATH}")
print("=" * 60)
print()
