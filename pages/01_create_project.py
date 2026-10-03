"""
pages/01_create_project.py — Create a New Project
─────────────────────────────────────────────────────────────────
This page lets the user fill in all project details and save them
to the SQLite database.

Key concepts used here:
  - st.form(): Groups inputs so the page doesn't re-run on every
    keystroke — only re-runs when the form is submitted.
  - st.session_state: Streamlit's "memory" between re-runs.
    We use it to store the dynamic task list (add/remove rows).
  - st.columns(): Places widgets side by side.
  - Validation: We check required fields before saving to DB.
─────────────────────────────────────────────────────────────────
"""

import streamlit as st
import os
import database as db

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="New Project — ProjectPulse",
    page_icon="➕",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────
# LOAD CUSTOM CSS
# ─────────────────────────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

db.init_db()

# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ ProjectPulse")
    st.markdown("*Your ECE Project Tracker*")
    st.divider()
    st.page_link("app.py",                     label="🏠 Dashboard")
    st.page_link("pages/01_create_project.py", label="➕ New Project")
    st.page_link("pages/03_cost_tracker.py",   label="💰 Cost Tracker")
    st.page_link("pages/04_showcase_editor.py",label="🎨 Showcase Editor")
    st.page_link("pages/05_showcase_viewer.py",label="🚀 Showcase")
    st.divider()
    st.markdown(
        "<small style='color:#5050A0'>Milestone 5 — Cost & Component Tracker ✅</small>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────
st.markdown('<p class="page-title">➕ Create New Project</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-subheader">Fill in your ECE project details below. '
    'All fields except Project Name are optional.</p>',
    unsafe_allow_html=True,
)

col_back, _ = st.columns([1, 9])
with col_back:
    if st.button("← Dashboard"):
        st.switch_page("app.py")

st.divider()

# ─────────────────────────────────────────────────────────────────
# SESSION STATE — Dynamic Task List
# ─────────────────────────────────────────────────────────────────
# What is session_state?
#   Every time a user clicks a button, Streamlit re-runs the whole
#   script from top to bottom. session_state lets us REMEMBER values
#   across these re-runs — like a notepad that persists.
#
# Here we use it to store a list of task dictionaries.
# Each task dict looks like: {"name": "", "description": "", "status": "Pending"}

if "task_list" not in st.session_state:
    # First visit: start with 3 common ECE task templates
    st.session_state.task_list = [
        {"name": "Schematic Design",      "description": "", "status": "Pending"},
        {"name": "PCB Layout",             "description": "", "status": "Pending"},
        {"name": "Component Procurement",  "description": "", "status": "Pending"},
    ]

# ─────────────────────────────────────────────────────────────────
# HELPER: Reset the task list (used after successful form submit)
# ─────────────────────────────────────────────────────────────────
def reset_task_list():
    st.session_state.task_list = [
        {"name": "Schematic Design",     "description": "", "status": "Pending"},
        {"name": "PCB Layout",           "description": "", "status": "Pending"},
        {"name": "Component Procurement","description": "", "status": "Pending"},
    ]

# ─────────────────────────────────────────────────────────────────
# SECTION 1 — PROJECT INFORMATION
# ─────────────────────────────────────────────────────────────────
st.markdown("### 📋 Project Information")

with st.form("project_form", clear_on_submit=False):

    # Row 1: Project Name (full width — the most important field)
    project_name = st.text_input(
        "Project Name *",
        placeholder="e.g., ESP32 Smart Home Controller",
        help="This is the only required field.",
    )

    # Row 2: Description (multi-line text box)
    project_desc = st.text_area(
        "Project Description",
        placeholder="Briefly describe what this project does, its goals, and key components...",
        height=100,
    )

    # Row 3: Deadline and Budget side by side
    col1, col2 = st.columns(2)
    with col1:
        project_deadline = st.date_input(
            "Project Deadline",
            value=None,                   # No default date selected
            format="YYYY-MM-DD",
            help="When do you need this project completed?",
        )
    with col2:
        project_budget = st.number_input(
            "Total Budget (₹)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            format="%.2f",
            help="Your total planned spending for this project.",
        )

    st.divider()

    # ─────────────────────────────────────────────────────────────
    # SECTION 2 — PROJECT LINKS
    # ─────────────────────────────────────────────────────────────
    st.markdown("### 🔗 Project Links")
    st.caption("Add links to external tools. You can update these later too.")

    link_col1, link_col2 = st.columns(2)

    with link_col1:
        github_url = st.text_input(
            "🐙 GitHub Repository",
            placeholder="https://github.com/username/project",
        )
        kicad_url = st.text_input(
            "📐 KiCad / PCB Files",
            placeholder="https://github.com/username/project/tree/main/pcb",
        )
        fusion_url = st.text_input(
            "⚙️ Fusion 360 / CAD",
            placeholder="https://a360.co/xxxxxxx",
        )

    with link_col2:
        arduino_url = st.text_input(
            "💾 Arduino / PlatformIO",
            placeholder="https://github.com/username/project/tree/main/firmware",
        )
        docs_url = st.text_input(
            "📄 Documentation",
            placeholder="https://docs.google.com/... or Notion link",
        )
        demo_url = st.text_input(
            "🎥 Demo Video",
            placeholder="https://youtube.com/watch?v=...",
        )

    st.divider()

    # ─────────────────────────────────────────────────────────────
    # SECTION 3 — TASKS (shown inside form but managed via session_state)
    # ─────────────────────────────────────────────────────────────
    st.markdown("### ✅ Project Tasks / Stages")
    st.caption(
        "Define the stages of your project. You can add, edit, or remove tasks "
        "here, and update statuses later from the Project Detail page."
    )

    # Display each task as an editable row
    # We loop over a copy index so edits go back to session_state correctly
    STATUS_OPTIONS = ["Pending", "In Progress", "Completed"]

    for i, task in enumerate(st.session_state.task_list):
        t_col1, t_col2, t_col3 = st.columns([4, 3, 2])

        with t_col1:
            # text_input key must be unique — we use f"task_name_{i}"
            new_name = st.text_input(
                f"Task {i+1} Name",
                value=task["name"],
                key=f"task_name_{i}",
                placeholder="e.g., PCB Layout, Firmware, Testing...",
            )
            st.session_state.task_list[i]["name"] = new_name

        with t_col2:
            new_desc = st.text_input(
                f"Task {i+1} Notes (optional)",
                value=task["description"],
                key=f"task_desc_{i}",
                placeholder="Short note about this task",
            )
            st.session_state.task_list[i]["description"] = new_desc

        with t_col3:
            new_status = st.selectbox(
                f"Task {i+1} Status",
                options=STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(task["status"]),
                key=f"task_status_{i}",
            )
            st.session_state.task_list[i]["status"] = new_status

    # ── Task action buttons (outside columns, inside form) ────────
    btn_add, btn_remove, _ = st.columns([2, 2, 6])
    with btn_add:
        add_task = st.form_submit_button("＋ Add Task Row", type="secondary")
    with btn_remove:
        remove_task = st.form_submit_button(
            "－ Remove Last Task",
            type="secondary",
            disabled=(len(st.session_state.task_list) <= 1),
            # Can't go below 1 task
        )

    st.divider()

    # ── Main Submit button ────────────────────────────────────────
    submitted = st.form_submit_button(
        "💾 Save Project",
        type="primary",
        use_container_width=True,
    )

# ─────────────────────────────────────────────────────────────────
# HANDLE FORM ACTIONS
# (These run AFTER the form block — Streamlit executes them on re-run
#  after the user clicks a submit button inside the form)
# ─────────────────────────────────────────────────────────────────

# ── Add a blank task row ──────────────────────────────────────────
if add_task:
    st.session_state.task_list.append(
        {"name": "", "description": "", "status": "Pending"}
    )
    st.rerun()  # Re-run the page so the new row appears

# ── Remove the last task row ──────────────────────────────────────
if remove_task and len(st.session_state.task_list) > 1:
    st.session_state.task_list.pop()
    st.rerun()

# ── Save the project to the database ─────────────────────────────
if submitted:
    # Validation: project name is required
    if not project_name.strip():
        st.error("❌ Project Name is required. Please enter a name.")
    else:
        # Filter out tasks with empty names (user may have left blank rows)
        valid_tasks = [
            t for t in st.session_state.task_list
            if t["name"].strip()
        ]

        # Convert date object to string (SQLite stores dates as text)
        deadline_str = str(project_deadline) if project_deadline else None

        # ── Save project to DB ────────────────────────────────────
        project_id = db.create_project(
            name=project_name.strip(),
            description=project_desc.strip(),
            deadline=deadline_str,
            budget=project_budget,
            github_url=github_url.strip(),
            kicad_url=kicad_url.strip(),
            fusion_url=fusion_url.strip(),
            arduino_url=arduino_url.strip(),
            docs_url=docs_url.strip(),
            demo_url=demo_url.strip(),
        )

        # ── Save tasks to DB ──────────────────────────────────────
        for idx, task in enumerate(valid_tasks):
            db.create_task(
                project_id=project_id,
                name=task["name"].strip(),
                description=task["description"].strip(),
                status=task["status"],
                order_index=idx,
            )

        # ── Success feedback ──────────────────────────────────────
        st.success(
            f"Project **'{project_name}'** created successfully with "
            f"{len(valid_tasks)} task(s)! Redirecting to dashboard..."
        )

        # Reset task list for next project creation
        reset_task_list()

        # Store the new project ID so the detail page knows which to load
        st.session_state["selected_project_id"] = project_id
        st.session_state["new_project_created"] = project_name

        # Navigate back to dashboard after a moment
        import time
        time.sleep(1.2)
        st.switch_page("app.py")

# ─────────────────────────────────────────────────────────────────
# QUICK REFERENCE — Common ECE Tasks
# A helpful cheat-sheet for beginners so they know what tasks to add
# ─────────────────────────────────────────────────────────────────
with st.expander("💡 Common ECE Project Tasks — Quick Reference"):
    st.markdown("""
    Copy any of these into your task list above:

    | Stage | Task Name | Notes |
    |---|---|---|
    | **Planning** | Requirements & Spec | Define inputs, outputs, power, constraints |
    | **Schematic** | Schematic Design | Draw circuit in KiCad / EasyEDA |
    | **PCB** | PCB Layout | Route traces, set clearances |
    | **PCB** | Gerber Export & Fab Order | Send to JLCPCB / PCBWay |
    | **Procurement** | Component Procurement | Order from Robu, LCSC, Amazon |
    | **Assembly** | PCB Soldering & Assembly | SMD / THT soldering |
    | **Firmware** | Firmware Development | Arduino / ESP-IDF / PlatformIO |
    | **Firmware** | UART / I2C / SPI Debug | Verify peripheral communication |
    | **Testing** | Functional Testing | Test core features |
    | **Testing** | Power Consumption Test | Measure idle & active current |
    | **Enclosure** | Enclosure Design | Fusion 360 / FreeCAD |
    | **Enclosure** | 3D Printing / Fabrication | Print and fit-check |
    | **Docs** | Schematic Documentation | Annotate and export PDF |
    | **Docs** | Project Report / README | Write final report |
    | **Demo** | Demo Video Recording | Record working demo |
    """)
