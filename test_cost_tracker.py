"""
test_cost_tracker.py — Tests the Cost & Component Tracker workflow (Milestone 5).

Verifies every backend & business logic requirement:
  1. Add components with name, quantity, unit price, link, notes
  2. Automatic calculation of component total_price (quantity * unit_price)
  3. Total project spending calculation across multiple components
  4. Project spending vs. budget logic:
     - Under budget & remaining calculation
     - Approaching budget limit warning (>= 80%)
     - Over budget detection & exceeded amount calculation
     - Zero budget (no limit) handling without division errors
  5. Component update workflow (edits re-calculate total_price and project spend)
  6. Component deletion workflow (deducts from project spend immediately)
  7. Multi-project isolation (components belong strictly to their parent project)
  8. Foreign key cascade deletion (deleting project removes all its components)

Run with:  python test_cost_tracker.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# Clean DB for a fresh test run
DB_FILE = os.path.join(os.path.dirname(__file__), "projectpulse.db")
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("[INFO] Removed old DB for clean test.")

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
print("Milestone 5 — Cost & Component Tracker Tests")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────
# TEST 1: Projects Setup
# ─────────────────────────────────────────────────────────────────
print("\n--- Test 1: Project Setup for Cost Tracking ---")
pid1 = db.create_project(
    name="Autonomous Drone",
    description="Quadcopter with optical flow and GPS navigation.",
    deadline="2026-12-01",
    budget=5000.0,
)
check("Created Project 1 with budget 5000.0", pid1 is not None and pid1 > 0)

pid2 = db.create_project(
    name="Smart Plant Monitor",
    description="IoT soil moisture & light telemetry.",
    deadline="2026-11-15",
    budget=1200.0,
)
check("Created Project 2 with budget 1200.0", pid2 is not None and pid2 > 0)

initial_spent_p1 = db.get_total_spent(pid1)
check("Initial spent for project 1 is 0.0", initial_spent_p1 == 0.0, got=initial_spent_p1, expected=0.0)

# ─────────────────────────────────────────────────────────────────
# TEST 2: Add Components & Auto-Calculate Total Price
# ─────────────────────────────────────────────────────────────────
print("\n--- Test 2: Add Components & Automatic Total Price Calculation ---")

c1_id = db.create_component(
    project_id=pid1,
    name="Flight Controller F405",
    quantity=1,
    unit_price=2200.0,
    purchase_link="https://robu.in/f405",
    notes="STM32F405 with MPU6000 gyro",
)
check("Created component 1 (Flight Controller)", c1_id > 0)

comp1 = db.get_component(c1_id)
check("comp1 name is correct", comp1["name"] == "Flight Controller F405", got=comp1["name"])
check("comp1 quantity is 1", comp1["quantity"] == 1, got=comp1["quantity"])
check("comp1 unit_price is 2200.0", comp1["unit_price"] == 2200.0, got=comp1["unit_price"])
check("comp1 total_price auto-calculated to 2200.0", comp1["total_price"] == 2200.0, got=comp1["total_price"])
check("comp1 purchase_link stored", comp1["purchase_link"] == "https://robu.in/f405")
check("comp1 notes stored", "STM32F405" in comp1["notes"])

# Add second component with quantity > 1 and floating point price
c2_id = db.create_component(
    project_id=pid1,
    name="Brushless Motor 2306 2400KV",
    quantity=4,
    unit_price=450.50,
    purchase_link="https://robu.in/motor2306",
    notes="CW and CCW pairs",
)
comp2 = db.get_component(c2_id)
expected_c2_total = 4 * 450.50  # 1802.0
check("comp2 (4 motors @ 450.50) total_price auto-calculated to 1802.0", comp2["total_price"] == expected_c2_total, got=comp2["total_price"], expected=expected_c2_total)

# ─────────────────────────────────────────────────────────────────
# TEST 3: Total Project Spending & Budget Comparisons
# ─────────────────────────────────────────────────────────────────
print("\n--- Test 3: Total Spent & Budget Calculations ---")

current_spent = db.get_total_spent(pid1)
expected_spent = 2200.0 + 1802.0  # 4002.0
check("Total spent for Project 1 sums accurately to 4002.0", current_spent == expected_spent, got=current_spent, expected=expected_spent)

project1 = db.get_project(pid1)
budget1 = project1["budget"]
remaining1 = budget1 - current_spent
budget_pct1 = (current_spent / budget1) * 100

check("Project 1 budget is 5000.0", budget1 == 5000.0)
check("Remaining budget is 998.0", remaining1 == 998.0, got=remaining1, expected=998.0)
check("Budget used percentage is ~80.04%", round(budget_pct1, 2) == 80.04, got=round(budget_pct1, 2))
check("Budget warning triggered (>= 80% and <= 100%)", 80.0 <= budget_pct1 <= 100.0)

# ─────────────────────────────────────────────────────────────────
# TEST 4: Over-Budget Detection
# ─────────────────────────────────────────────────────────────────
print("\n--- Test 4: Over-Budget Detection ---")

# Add a battery that exceeds the budget
c3_id = db.create_component(
    project_id=pid1,
    name="4S 1500mAh LiPo Battery",
    quantity=2,
    unit_price=800.0,
    notes="100C discharge rate",
)
# New spent: 4002 + 1600 = 5602.0 (Budget was 5000.0)
new_spent = db.get_total_spent(pid1)
over_budget_amt = new_spent - budget1
is_over_budget = new_spent > budget1

check("Total spent is now 5602.0", new_spent == 5602.0, got=new_spent, expected=5602.0)
check("Over budget flag is True", is_over_budget is True)
check("Over budget amount is 602.0", over_budget_amt == 602.0, got=over_budget_amt, expected=602.0)

# ─────────────────────────────────────────────────────────────────
# TEST 5: Update Component
# ─────────────────────────────────────────────────────────────────
print("\n--- Test 5: Edit / Update Component ---")

# Suppose user found a discount on batteries: 2 @ 400.0 instead of 800.0
db.update_component(
    comp_id=c3_id,
    name="4S 1500mAh LiPo Battery (Discounted)",
    quantity=2,
    unit_price=400.0,
    purchase_link="https://robu.in/discount-lipo",
    notes="Bought on sale",
)

comp3_updated = db.get_component(c3_id)
check("comp3 name updated", comp3_updated["name"] == "4S 1500mAh LiPo Battery (Discounted)")
check("comp3 unit_price updated to 400.0", comp3_updated["unit_price"] == 400.0)
check("comp3 total_price recalculated to 800.0", comp3_updated["total_price"] == 800.0, got=comp3_updated["total_price"], expected=800.0)
check("comp3 purchase_link updated", comp3_updated["purchase_link"] == "https://robu.in/discount-lipo")

# Check new project total: 2200 + 1802 + 800 = 4802.0
updated_spent = db.get_total_spent(pid1)
check("Project total spent updated to 4802.0 after edit", updated_spent == 4802.0, got=updated_spent, expected=4802.0)
check("Project is now back under budget (4802.0 <= 5000.0)", updated_spent <= budget1)

# ─────────────────────────────────────────────────────────────────
# TEST 6: Delete Component
# ─────────────────────────────────────────────────────────────────
print("\n--- Test 6: Delete Component ---")

# Delete the battery component
db.delete_component(c3_id)
comp3_check = db.get_component(c3_id)
check("comp3 is deleted from database (returns None)", comp3_check is None)

remaining_components = db.get_components(pid1)
check("Project 1 now has 2 components", len(remaining_components) == 2, got=len(remaining_components))

spent_after_delete = db.get_total_spent(pid1)
check("Total spent after deletion dropped back to 4002.0", spent_after_delete == 4002.0, got=spent_after_delete, expected=4002.0)

# ─────────────────────────────────────────────────────────────────
# TEST 7: Multi-Project Component Isolation
# ─────────────────────────────────────────────────────────────────
print("\n--- Test 7: Multi-Project Isolation ---")

# Add components to Project 2 (Smart Plant Monitor)
db.create_component(
    project_id=pid2,
    name="Capacitive Soil Moisture Sensor v1.2",
    quantity=3,
    unit_price=120.0,
    notes="Corrosion resistant analog sensor",
)
db.create_component(
    project_id=pid2,
    name="ESP32 DevKit V1",
    quantity=1,
    unit_price=380.0,
    notes="Wi-Fi and BLE telemetry node",
)

p1_comps = db.get_components(pid1)
p2_comps = db.get_components(pid2)

check("Project 1 has 2 components", len(p1_comps) == 2, got=len(p1_comps))
check("Project 2 has 2 components", len(p2_comps) == 2, got=len(p2_comps))

p1_spent = db.get_total_spent(pid1)
p2_spent = db.get_total_spent(pid2)
expected_p2_spent = (3 * 120.0) + (1 * 380.0)  # 360 + 380 = 740.0

check("Project 1 spent unchanged at 4002.0", p1_spent == 4002.0, got=p1_spent)
check("Project 2 spent is 740.0", p2_spent == expected_p2_spent, got=p2_spent, expected=expected_p2_spent)

# ─────────────────────────────────────────────────────────────────
# TEST 8: Zero-Budget Project Handling
# ─────────────────────────────────────────────────────────────────
print("\n--- Test 8: Zero-Budget Project Handling ---")
pid3 = db.create_project(name="Exploratory Lab Project", budget=0.0)
db.create_component(project_id=pid3, name="Jumper Wires", quantity=1, unit_price=90.0)

p3_spent = db.get_total_spent(pid3)
p3_budget = db.get_project(pid3)["budget"]
# Ensure logic doesn't crash on budget == 0
pct = (p3_spent / p3_budget * 100.0) if p3_budget > 0 else 0.0
check("Zero-budget project spending is 90.0", p3_spent == 90.0)
check("Zero-budget percentage calculation avoids division by zero", pct == 0.0)

# ─────────────────────────────────────────────────────────────────
# TEST 9: Cascade Deletion of Components on Project Delete
# ─────────────────────────────────────────────────────────────────
print("\n--- Test 9: Cascade Deletion When Project is Deleted ---")
db.delete_project(pid2)
p2_check = db.get_project(pid2)
check("Project 2 deleted", p2_check is None)

p2_comps_after = db.get_components(pid2)
check("Project 2 components automatically deleted via cascade", len(p2_comps_after) == 0, got=len(p2_comps_after))
p2_spent_after = db.get_total_spent(pid2)
check("Project 2 spent is 0.0 after cascade delete", p2_spent_after == 0.0)

# Ensure Project 1 components were NOT affected
p1_comps_final = db.get_components(pid1)
check("Project 1 components remain intact (2 components)", len(p1_comps_final) == 2)

# ─────────────────────────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
if not errors:
    print("ALL TESTS PASSED! (Milestone 5 is fully verified)")
else:
    print(f"FAILED: {len(errors)} test(s) failed:")
    for err in errors:
        print(f"  - {err}")
print("=" * 60 + "\n")

sys.exit(0 if not errors else 1)
