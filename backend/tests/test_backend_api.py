import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from fastapi.testclient import TestClient
from backend.main import app
from backend.config import COOKIE_NAME

client = TestClient(app)

def test_full_pipeline():
    print("=" * 60)
    print("Starting ProjectPulse 2.0 Backend Verification")
    print("=" * 60)

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[PASS] 1. Health check OK")

    # 2. Register user
    reg_payload = {
        "email": "maker@example.com",
        "username": "makertest",
        "password": "securepassword123",
        "display_name": "Maker Alex"
    }
    res = client.post("/api/auth/register", json=reg_payload)
    if res.status_code == 400 and "already" in res.text:
        # User already exists from previous run, login instead
        login_res = client.post("/api/auth/login", json={
            "username_or_email": "makertest",
            "password": "securepassword123"
        })
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        token = login_res.json()["access_token"]
        print("[PASS] 2. Logged in existing user, cookie set")
    else:
        assert res.status_code == 201, f"Register failed: {res.text}"
        assert COOKIE_NAME in client.cookies or "access_token" in res.json()
        token = res.json()["access_token"]
        print("[PASS] 2. User registration and cookie auth OK")

    # Verify current user endpoint
    me_res = client.get("/api/auth/me")
    assert me_res.status_code == 200, f"Get /api/auth/me failed: {me_res.text}"
    assert me_res.json()["username"] == "makertest"
    print(f"[PASS] 3. Current user verified: {me_res.json()['username']}")

    # 3. Create Project
    proj_payload = {
        "name": "Smart IoT Plant Monitor",
        "description": "An automated plant monitoring system with soil moisture sensors and ESP32.",
        "technologies": "ESP32, C++, FreeRTOS, MQTT",
        "deadline": "2026-11-30",
        "budget": 2500.0,
        "github_url": "https://github.com/makertest/plant-monitor",
        "initial_tasks": [
            "Schematic Design",
            "Firmware Development",
            "Enclosure 3D Print"
        ]
    }
    proj_res = client.post("/api/projects", json=proj_payload)
    assert proj_res.status_code == 201, f"Create project failed: {proj_res.text}"
    project = proj_res.json()
    project_id = project["id"]
    print(f"[PASS] 4. Project created with ID {project_id}: {project['name']}")
    assert project["task_count"] == 3, f"Expected 3 tasks, got {project['task_count']}"
    assert project["progress"] == 0.0, f"Expected 0.0 progress, got {project['progress']}"

    # 4. Tasks and Progress Verification
    tasks_res = client.get(f"/api/projects/{project_id}/tasks")
    assert tasks_res.status_code == 200
    tasks = tasks_res.json()
    assert len(tasks) == 3
    print(f"[PASS] 5. Fetched {len(tasks)} initial tasks")

    # Mark first task completed
    task1_id = tasks[0]["id"]
    update_task_res = client.put(f"/api/tasks/{task1_id}", json={"status": "Completed"})
    assert update_task_res.status_code == 200
    assert update_task_res.json()["status"] == "Completed"

    # Verify project progress is updated (1/3 = 33.3%)
    proj_detail = client.get(f"/api/projects/{project_id}").json()
    assert proj_detail["progress"] == 33.3, f"Expected 33.3% progress, got {proj_detail['progress']}%"
    print(f"[PASS] 6. Progress calculation verified: {proj_detail['progress']}% (1/3 completed)")

    # 5. Component / Cost Tracker Verification
    comp1 = client.post(f"/api/projects/{project_id}/components", json={
        "name": "ESP32 Development Board",
        "category": "MCU",
        "quantity": 2,
        "unit_price": 450.0,
        "purchase_link": "https://store.example.com/esp32",
        "notes": "NodeMCU-32S"
    }).json()
    assert comp1["total_price"] == 900.0, f"Expected 900.0, got {comp1['total_price']}"

    comp2 = client.post(f"/api/projects/{project_id}/components", json={
        "name": "Capacitive Soil Moisture Sensor",
        "category": "Sensor",
        "quantity": 4,
        "unit_price": 120.0,
        "purchase_link": "https://store.example.com/sensor",
        "notes": "Corrosion resistant"
    }).json()
    assert comp2["total_price"] == 480.0

    costs_res = client.get(f"/api/projects/{project_id}/costs").json()
    assert costs_res["total_spent"] == 1380.0, f"Expected 1380.0, got {costs_res['total_spent']}"
    assert costs_res["remaining_budget"] == 1120.0, f"Expected 1120.0, got {costs_res['remaining_budget']}"
    assert costs_res["budget_used_percentage"] == 55.2
    assert costs_res["is_over_budget"] is False
    print(f"[PASS] 7. Cost Tracker verified: Spent Rs.{costs_res['total_spent']} of Rs.{costs_res['budget']} (55.2% used)")

    # 6. Portfolio & Public Showcase Verification
    port_res = client.get(f"/api/projects/{project_id}/portfolio")
    assert port_res.status_code == 200
    portfolio = port_res.json()
    slug = portfolio["slug"]
    print(f"[PASS] 8. Auto-generated portfolio verified with slug: {slug}")

    # Edit portfolio and publish
    pub_edit = client.put(f"/api/projects/{project_id}/portfolio", json={
        "problem": "Houseplants often die from under-watering or root rot due to manual watering errors.",
        "solution": "Automated telemetry continuously reads soil permittivity and alerts the owner via web dashboard.",
        "is_published": True
    })
    assert pub_edit.status_code == 200
    assert pub_edit.json()["is_published"] is True
    print("[PASS] 9. Portfolio published successfully")

    # Add section and media
    sec_res = client.post(f"/api/projects/{project_id}/portfolio/sections", json={
        "section_type": "architecture",
        "title": "System Architecture",
        "content": "Sensors -> ADC -> ESP32 -> MQTT Broker -> React Dashboard"
    })
    assert sec_res.status_code == 201

    media_res = client.post(f"/api/projects/{project_id}/portfolio/media", json={
        "media_url": "https://images.unsplash.com/photo-1518770660439-4636190af475",
        "media_type": "cover",
        "title": "Hardware Setup"
    })
    assert media_res.status_code == 201
    print("[PASS] 10. Added showcase section and media")

    # Access via public endpoint without any auth
    anon_client = TestClient(app)
    public_res = anon_client.get(f"/api/public/portfolio/{slug}")
    assert public_res.status_code == 200, f"Public portfolio failed: {public_res.text}"
    pub_data = public_res.json()
    assert pub_data["project_name"] == "Smart IoT Plant Monitor"
    assert pub_data["author_username"] == "makertest"
    assert pub_data["progress_percentage"] == 33.3
    assert pub_data["total_spent"] == 1380.0
    assert len(pub_data["sections"]) == 1
    assert len(pub_data["media"]) == 1
    print(f"[PASS] 11. Public Showcase endpoint /api/public/portfolio/{slug} verified!")

    print("=" * 60)
    print("ALL PROJECTPULSE 2.0 BACKEND TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    test_full_pipeline()
