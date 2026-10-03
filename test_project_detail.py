"""
test_project_detail.py — Tests the Project Detail page workflow.

Simulates every action available on the Project Detail page:
  1. Load project by ID
  2. Inline task status update (single task)
  3. Full task update (name + notes + status)
  4. Add a new task from the detail page
  5. Delete a task (cascade check)
  6. Update project info (edit form)
  7. Update project links
  8. Progress recalculates correctly after status changes
  9. Deadline parsing logic
  10. Delete entire project from detail page

Run with:  python test_project_detail.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Clean DB for a fresh test run
DB_FILE = os.path.join(os.path.dirname(__file__), "projectpulse.db")
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("[INFO] Removed old DB for clean test.")

import database as db
from datetime import date, timedelta

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
print("Milestone 4 — Project Detail Page Tests")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────
# SETUP: Create a project with tasks
# ─────────────────────────────────────────────────────────────────
future_deadline = str(date.today() + timedelta(days=30))

pid = db.create_project(
    name="Line Following Robot",
    description="PID-controlled line follower using IR sensors and L298N motor driver.",
    deadline=future_deadline,
    budget=2000.0,
    github_url="https://github.com/user/line-robot",
    kicad_url="https://github.com/user/line-robot/pcb",
)
task_ids = []
tasks_data = [
    ("Chassis Design",       "Fusion 360",       "Completed"),
    ("Motor Driver Circuit", "L298N + flybacks",  "Completed"),
    ("IR Sensor Array",      "8-sensor array",    "In Progress"),
    ("PID Firmware",         "Arduino Mega",      "Pending"),
    ("Tuning & Testing",     "",                  "Pending"),
]
for name, notes, status in tasks_data:
    tid = db.create_task(pid, name, description=notes, status=status)
    task_ids.append(tid)

# ─────────────────────────────────────────────────────────────────
# TEST 1: Load project by ID
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 1] Load project by ID")
p = db.get_project(pid)
check("Project found",           p is not None)
check("Name matches",            p["name"] == "Line Following Robot")
check("Deadline stored",         p["deadline"] == future_deadline)
check("Budget stored",           p["budget"] == 2000.0)
check("GitHub URL stored",       p["github_url"] != "")

# ─────────────────────────────────────────────────────────────────
# TEST 2: Load tasks with correct order
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 2] Load and verify tasks")
tasks = db.get_tasks(pid)
check("5 tasks loaded",          len(tasks) == 5, got=len(tasks), expected=5)
check("First task name correct", tasks[0]["name"] == "Chassis Design")
check("Statuses correct",
      tasks[0]["status"] == "Completed" and
      tasks[2]["status"] == "In Progress" and
      tasks[3]["status"] == "Pending")

# ─────────────────────────────────────────────────────────────────
# TEST 3: Progress calculation with initial statuses
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 3] Initial progress (2/5 = 40.0%)")
progress = db.calculate_progress(pid)
check("Progress = 40.0%", progress == 40.0, got=progress, expected=40.0)

# ─────────────────────────────────────────────────────────────────
# TEST 4: Update single task status (the "Save Status" button)
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 4] Update task status only")
db.update_task_status(task_ids[2], "Completed")  # IR Sensor -> Completed
tasks = db.get_tasks(pid)
check("IR Sensor now Completed",
      tasks[2]["status"] == "Completed", got=tasks[2]["status"])
progress = db.calculate_progress(pid)
check("Progress updated to 60.0%", progress == 60.0, got=progress, expected=60.0)

# ─────────────────────────────────────────────────────────────────
# TEST 5: Full task update (name + notes + status — the "Save" button)
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 5] Full task update (name + notes + status)")
db.update_task(
    task_id=task_ids[3],
    name="PID Firmware v2",
    description="Ported to ESP32 with WiFi telemetry",
    status="In Progress",
)
tasks = db.get_tasks(pid)
check("Name updated",        tasks[3]["name"] == "PID Firmware v2")
check("Notes updated",       "ESP32" in tasks[3]["description"])
check("Status updated",      tasks[3]["status"] == "In Progress")
# Progress unchanged (was Pending, now In Progress — neither was Completed)
progress = db.calculate_progress(pid)
check("Progress unchanged at 60.0%", progress == 60.0, got=progress)

# ─────────────────────────────────────────────────────────────────
# TEST 6: Add a new task from the detail page
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 6] Add new task from detail page")
new_tid = db.create_task(
    project_id=pid,
    name="Documentation",
    description="Write final README and component list",
    status="Pending",
    order_index=5,
)
tasks = db.get_tasks(pid)
check("6 tasks now",         len(tasks) == 6, got=len(tasks), expected=6)
check("New task at end",     tasks[-1]["name"] == "Documentation")
check("New task is Pending", tasks[-1]["status"] == "Pending")
# Progress should be same (new task is Pending)
progress = db.calculate_progress(pid)
check("Progress is 50.0% (3/6)", progress == 50.0, got=progress, expected=50.0)

# ─────────────────────────────────────────────────────────────────
# TEST 7: Delete a single task
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 7] Delete a single task")
db.delete_task(new_tid)
tasks = db.get_tasks(pid)
check("Back to 5 tasks",     len(tasks) == 5, got=len(tasks), expected=5)
check("Documentation gone",  all(t["name"] != "Documentation" for t in tasks))
progress = db.calculate_progress(pid)
check("Progress back to 60.0%", progress == 60.0, got=progress, expected=60.0)

# ─────────────────────────────────────────────────────────────────
# TEST 8: Edit project info (edit form submit)
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 8] Edit project info")
new_deadline = str(date.today() + timedelta(days=60))
db.update_project(
    project_id=pid,
    name="Line Following Robot v2",
    description="Updated with ESP32 and BLE telemetry.",
    deadline=new_deadline,
    budget=3000.0,
    github_url="https://github.com/user/line-robot-v2",
    kicad_url="", fusion_url="", arduino_url="",
    docs_url="https://notion.so/lfr-docs",
    demo_url="https://youtube.com/watch?v=lfr",
)
p = db.get_project(pid)
check("Name updated",        p["name"] == "Line Following Robot v2")
check("Description updated", "ESP32" in p["description"])
check("Deadline updated",    p["deadline"] == new_deadline)
check("Budget updated",      p["budget"] == 3000.0, got=p["budget"], expected=3000.0)
check("GitHub URL updated",  "v2" in p["github_url"])
check("Docs URL set",        p["docs_url"] != "")
check("Demo URL set",        p["demo_url"] != "")

# ─────────────────────────────────────────────────────────────────
# TEST 9: Mark all tasks complete → progress = 100%
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 9] Mark all tasks complete")
tasks = db.get_tasks(pid)
for t in tasks:
    db.update_task_status(t["id"], "Completed")
progress = db.calculate_progress(pid)
check("Progress = 100.0%", progress == 100.0, got=progress, expected=100.0)

# ─────────────────────────────────────────────────────────────────
# TEST 10: Delete entire project from detail page
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 10] Delete project from detail page")
db.delete_project(pid)
check("Project deleted",         db.get_project(pid) is None)
check("All tasks cascade-deleted", len(db.get_tasks(pid)) == 0)
check("No components orphaned",    len(db.get_components(pid)) == 0)

# ─────────────────────────────────────────────────────────────────
# TEST 11: Non-existent project returns None (guard clause test)
# ─────────────────────────────────────────────────────────────────
print("\n[TEST 11] Guard clause — non-existent project ID")
ghost = db.get_project(9999)
check("Returns None for missing project", ghost is None)

# ─────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────
print()
print("=" * 60)
if errors:
    print(f"FAILED — {len(errors)} test(s) failed:")
    for e in errors:
        print(f"  - {e}")
else:
    print("ALL TESTS PASSED! Project Detail workflow is working.")
    print(f"DB: {db.DB_PATH}")
print("=" * 60)
print()
