"""
test_db.py — Quick verification that the database layer works correctly.
Run with:  python test_db.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import database as db

print("=" * 50)
print("BuildFolio — Database Verification Test")
print("=" * 50)

# 1. Init DB
db.init_db()

# 2. Create a sample project
pid = db.create_project(
    name="ESP32 Weather Station",
    description="Weather station using ESP32 + BME280 sensor with OLED display.",
    deadline="2026-12-31",
    budget=1500.0,
    github_url="https://github.com/example/esp32-weather",
)
print(f"\n[1] Created project with ID: {pid}")

# 3. Add tasks
db.create_task(pid, "Schematic Design",      status="Completed",   order_index=1)
db.create_task(pid, "PCB Layout (KiCad)",    status="In Progress", order_index=2)
db.create_task(pid, "Component Procurement", status="Pending",     order_index=3)
db.create_task(pid, "Firmware (ESP-IDF)",    status="Pending",     order_index=4)
db.create_task(pid, "Testing & Debugging",   status="Pending",     order_index=5)
print("[2] Tasks created: 5 tasks (1 Completed, 1 In Progress, 3 Pending)")

# 4. Add components
db.create_component(pid, "ESP32-WROOM-32",  quantity=1, unit_price=350.0)
db.create_component(pid, "BME280 Sensor",   quantity=1, unit_price=180.0)
db.create_component(pid, "0.96in OLED",     quantity=1, unit_price=120.0)
db.create_component(pid, "PCB Fabrication", quantity=5, unit_price=85.0)
print("[3] Components created: 4 components")

# 5. Check progress
progress = db.calculate_progress(pid)
expected_progress = 20.0
assert progress == expected_progress, f"Expected {expected_progress}%, got {progress}%"
print(f"[4] Progress calculation: {progress}%  (Expected 20.0%) -> PASS")

# 6. Check total cost
spent = db.get_total_spent(pid)
expected_spent = 350 + 180 + 120 + (5 * 85)   # = 1075.0
assert spent == expected_spent, f"Expected Rs.{expected_spent}, got Rs.{spent}"
print(f"[5] Total spent: Rs.{spent}  (Expected Rs.{expected_spent}) -> PASS")

# 7. Check budget remaining
project = db.get_project(pid)
budget = project["budget"]
remaining = budget - spent
print(f"[6] Budget: Rs.{budget}  |  Spent: Rs.{spent}  |  Remaining: Rs.{remaining}")

# 8. Fetch all projects
projects = db.get_all_projects()
print(f"[7] Projects in DB: {len(projects)}")
for p in projects:
    print(f"     -> [{p['id']}] {p['name']}  deadline={p['deadline']}")

# 9. Update a task status
tasks = db.get_tasks(pid)
db.update_task_status(tasks[1]["id"], "Completed")
new_progress = db.calculate_progress(pid)
print(f"[8] After marking task 2 Completed -> Progress: {new_progress}%  (Expected 40.0%)")
assert new_progress == 40.0

print()
print("=" * 50)
print("ALL TESTS PASSED! Database is working correctly.")
print(f"DB file location: {db.DB_PATH}")
print("=" * 50)
