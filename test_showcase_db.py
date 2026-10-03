"""
test_showcase_db.py — Tests the new Showcase database tables and CRUD functions.
"""

import os
import sys

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

print("\n" + "=" * 60)
print("Stage 1 — Project Showcase Database Tests")
print("=" * 60)

# Create a project
pid = db.create_project(name="Showcase Test Project")
check("Project created", pid > 0)

# 1. Test upserting a showcase
db.upsert_showcase(
    project_id=pid,
    showcase_slug="showcase-test-project",
    problem_statement="Test Problem",
    solution_description="Test Solution",
    technologies="Python, SQLite",
    architecture_data='{"nodes":[], "edges":[]}',
    github_url="https://github.com/test",
    is_published=True
)

showcase = db.get_showcase(pid)
check("Showcase created and fetched", showcase is not None)
check("Slug is correct", showcase["showcase_slug"] == "showcase-test-project")
check("Problem is correct", showcase["problem_statement"] == "Test Problem")
check("Technologies correct", showcase["technologies"] == "Python, SQLite")
check("is_published is True (1)", showcase["is_published"] == 1)

# 2. Test updating an existing showcase
db.upsert_showcase(
    project_id=pid,
    showcase_slug="showcase-test-project-updated",
    problem_statement="Updated Problem",
    solution_description="Updated Solution",
    technologies="Python, SQLite, Streamlit",
    architecture_data='{"nodes":[{"id":"n1"}], "edges":[]}',
    github_url="https://github.com/test-updated",
    is_published=False
)

showcase_updated = db.get_showcase(pid)
check("Showcase updated", showcase_updated["showcase_slug"] == "showcase-test-project-updated")
check("Technologies updated", showcase_updated["technologies"] == "Python, SQLite, Streamlit")
check("is_published is False (0)", showcase_updated["is_published"] == 0)

# 3. Test showcase media CRUD
m1_id = db.add_showcase_media(
    project_id=pid,
    file_path="uploads/projects/1/cover.jpg",
    media_type="cover",
    title="Cover Image",
    display_order=1
)
check("Media 1 (cover) added", m1_id > 0)

m2_id = db.add_showcase_media(
    project_id=pid,
    file_path="https://youtube.com/watch?v=123",
    media_type="demo_video",
    title="Demo Video",
    display_order=2
)
check("Media 2 (video) added", m2_id > 0)

media_list = db.get_showcase_media(pid)
check("Both media files retrieved", len(media_list) == 2)
check("Media order is correct", media_list[0]["media_type"] == "cover" and media_list[1]["media_type"] == "demo_video")

# Delete media
db.delete_showcase_media(m1_id)
media_list_after_del = db.get_showcase_media(pid)
check("Media 1 deleted", len(media_list_after_del) == 1)
check("Remaining media is video", media_list_after_del[0]["id"] == m2_id)

# 4. Test cascade deletion
db.delete_project(pid)
showcase_after_delete = db.get_showcase(pid)
media_after_delete = db.get_showcase_media(pid)
check("Showcase deleted on project cascade", showcase_after_delete is None)
check("Media deleted on project cascade", len(media_after_delete) == 0)

print("\n" + "=" * 60)
if not errors:
    print("ALL TESTS PASSED! (Stage 1 Showcase DB is fully verified)")
else:
    print(f"FAILED: {len(errors)} test(s) failed:")
    for err in errors:
        print(f"  - {err}")
print("=" * 60 + "\n")

sys.exit(0 if not errors else 1)
