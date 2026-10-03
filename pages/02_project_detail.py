"""
pages/02_project_detail.py — Project Detail Page
─────────────────────────────────────────────────────────────────
This page shows everything about ONE project:
  • Header: name, deadline status, progress bar
  • Task list: update statuses, add new tasks, delete tasks
  • Project links: clickable buttons for GitHub, KiCad, etc.
  • Edit project: expandable form to update all project fields
  • Quick stats: budget, spent, tasks breakdown

How does this page know WHICH project to show?
  When the user clicks "View" on the dashboard, we store the
  project ID in st.session_state["selected_project_id"].
  This page reads that value. We also support st.query_params
  as a fallback (for direct URL access like ?pid=2).
─────────────────────────────────────────────────────────────────
"""

import streamlit as st
import os
from datetime import date
import database as db

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Project Detail — ProjectPulse",
    page_icon="📋",
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
# RESOLVE WHICH PROJECT TO SHOW
# Priority: query_params (?pid=X) > session_state
# ─────────────────────────────────────────────────────────────────
params = st.query_params
if "pid" in params:
    try:
        project_id = int(params["pid"])
        st.session_state["selected_project_id"] = project_id
    except ValueError:
        pass

project_id = st.session_state.get("selected_project_id", None)

# ─────────────────────────────────────────────────────────────────
# GUARD: No project selected — show a helpful message
# ─────────────────────────────────────────────────────────────────
if project_id is None:
    st.markdown("## 📋 Project Detail")
    st.warning("No project selected. Please go to the dashboard and click 'View' on a project.")
    if st.button("← Go to Dashboard"):
        st.switch_page("app.py")
    st.stop()  # Stop rendering the rest of the page

# ─────────────────────────────────────────────────────────────────
# LOAD PROJECT DATA
# ─────────────────────────────────────────────────────────────────
project = db.get_project(project_id)

if project is None:
    st.error("Project not found. It may have been deleted.")
    if st.button("← Back to Dashboard"):
        st.switch_page("app.py")
    st.stop()

# Load related data
tasks    = db.get_tasks(project_id)
progress = db.calculate_progress(project_id)
spent    = db.get_total_spent(project_id)

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
    st.divider()
    st.markdown(f"**Current Project:**")
    st.markdown(f"📋 {project['name']}")
    st.markdown(f"**Progress:** {progress}%")
    st.progress(progress / 100)
    st.divider()
    st.markdown(
        "<small style='color:#5050A0'>Milestone 5 — Cost & Component Tracker ✅</small>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS (used throughout this page)
# ─────────────────────────────────────────────────────────────────
def deadline_info(deadline_str):
    """
    Returns (label, css_class) for a deadline string.
    E.g. ("7 days left", "deadline-ok")
    """
    if not deadline_str:
        return "No deadline set", "section-subheader"
    try:
        dl = date.fromisoformat(deadline_str)
        days = (dl - date.today()).days
        if days < 0:
            return f"Overdue by {abs(days)} day(s)", "deadline-past"
        elif days == 0:
            return "Due TODAY!", "deadline-past"
        elif days <= 7:
            return f"{days} day(s) left", "deadline-near"
        else:
            return f"{days} day(s) left  ({dl.strftime('%d %b %Y')})", "deadline-ok"
    except ValueError:
        return deadline_str, "section-subheader"


def status_badge_html(progress_pct):
    """Returns a colored badge based on progress."""
    if progress_pct == 100.0:
        return '<span class="badge badge-completed">Completed</span>'
    elif progress_pct > 0:
        return '<span class="badge badge-inprogress">In Progress</span>'
    else:
        return '<span class="badge badge-pending">Pending</span>'


def task_status_icon(status):
    """Returns an icon for each task status."""
    return {"Pending": "⏳", "In Progress": "🔄", "Completed": "✅"}.get(status, "")


# ─────────────────────────────────────────────────────────────────
# TOP NAVIGATION BAR
# ─────────────────────────────────────────────────────────────────
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([2, 2, 2, 4])
with nav_col1:
    if st.button("← Dashboard", use_container_width=True):
        st.switch_page("app.py")
with nav_col2:
    if st.button("💰 Cost Tracker", use_container_width=True):
        st.session_state["selected_project_id"] = project_id
        st.switch_page("pages/03_cost_tracker.py")
with nav_col3:
    if st.button("🎨 Showcase Editor", use_container_width=True):
        st.session_state["selected_project_id"] = project_id
        st.switch_page("pages/04_showcase_editor.py")

st.divider()

# ─────────────────────────────────────────────────────────────────
# PROJECT HEADER
# ─────────────────────────────────────────────────────────────────
deadline_label, deadline_class = deadline_info(project["deadline"])
badge_html = status_badge_html(progress)

st.markdown(
    f'<p class="page-title">{project["name"]}</p>',
    unsafe_allow_html=True,
)
st.markdown(
    f'{badge_html} &nbsp; <span class="{deadline_class}"> {deadline_label}</span>',
    unsafe_allow_html=True,
)
if project["description"]:
    st.markdown(
        f'<p style="color:#A0A0C0; margin-top:8px;">{project["description"]}</p>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────
# QUICK STATS ROW
# ─────────────────────────────────────────────────────────────────
total_tasks     = len(tasks)
completed_count = sum(1 for t in tasks if t["status"] == "Completed")
inprog_count    = sum(1 for t in tasks if t["status"] == "In Progress")
pending_count   = sum(1 for t in tasks if t["status"] == "Pending")
budget          = project["budget"] or 0.0
remaining       = budget - spent
over_budget     = budget > 0 and spent > budget

s1, s2, s3, s4, s5, s6 = st.columns(6)
s1.metric("Progress",    f"{progress}%")
s2.metric("Tasks Total", total_tasks)
s3.metric("Completed",   completed_count)
s4.metric("In Progress", inprog_count)
s5.metric("Budget",      f"₹{budget:,.0f}")
s6.metric(
    "Spent",
    f"₹{spent:,.0f}",
    delta=f"₹{abs(remaining):,.0f} {'over!' if over_budget else 'left'}",
    delta_color="inverse" if over_budget else "normal",
)

# ─────────────────────────────────────────────────────────────────
# OVERALL PROGRESS BAR
# ─────────────────────────────────────────────────────────────────
st.markdown("#### Overall Progress")
bar_color = (
    "deadline-past"   if progress < 30 else
    "deadline-near"   if progress < 70 else
    "deadline-ok"
)
st.progress(progress / 100,
            text=f"{progress}% complete  —  {completed_count}/{total_tasks} tasks done")

st.divider()

# ─────────────────────────────────────────────────────────────────
# TASK MANAGEMENT SECTION
# ─────────────────────────────────────────────────────────────────
st.markdown("### ✅ Tasks & Stages")
st.caption(
    "Update the status of each task using the dropdown. "
    "Changes are saved immediately when you click **Save Status**."
)

STATUS_OPTIONS = ["Pending", "In Progress", "Completed"]

if not tasks:
    st.info("No tasks yet. Add your first task below.")
else:
    # ── Column headers ────────────────────────────────────────────
    h1, h2, h3, h4, h5 = st.columns([1, 4, 4, 3, 1])
    h1.markdown("<small style='color:#5050A0'>#</small>",       unsafe_allow_html=True)
    h2.markdown("<small style='color:#5050A0'>Task Name</small>", unsafe_allow_html=True)
    h3.markdown("<small style='color:#5050A0'>Notes</small>",    unsafe_allow_html=True)
    h4.markdown("<small style='color:#5050A0'>Status</small>",   unsafe_allow_html=True)
    h5.markdown("<small style='color:#5050A0'>Del</small>",      unsafe_allow_html=True)

    st.markdown("<hr style='margin:4px 0; border-color:#2D2D54'>", unsafe_allow_html=True)

    # ── Render each task row ──────────────────────────────────────
    for i, task in enumerate(tasks):
        tid          = task["id"]
        current_stat = task["status"]
        icon         = task_status_icon(current_stat)

        c_num, c_name, c_notes, c_status, c_del = st.columns([1, 4, 4, 3, 1])

        with c_num:
            st.markdown(
                f"<div style='padding-top:8px; color:#5050A0'>{i+1}</div>",
                unsafe_allow_html=True,
            )

        with c_name:
            # Inline editable task name
            new_name = st.text_input(
                "Name",
                value=task["name"],
                key=f"tname_{tid}",
                label_visibility="collapsed",
            )

        with c_notes:
            new_notes = st.text_input(
                "Notes",
                value=task["description"] or "",
                key=f"tnotes_{tid}",
                label_visibility="collapsed",
                placeholder="Optional note",
            )

        with c_status:
            # Status selectbox + Save button stacked
            new_status = st.selectbox(
                "Status",
                options=STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(current_stat),
                key=f"tstatus_{tid}",
                label_visibility="collapsed",
            )
            if st.button(f"{icon} Save", key=f"tsave_{tid}", use_container_width=True):
                db.update_task(tid, new_name.strip(), new_notes.strip(), new_status)
                st.success(f"Saved: **{new_name}** → {new_status}", icon="✅")
                st.rerun()

        with c_del:
            st.markdown("<div style='padding-top:4px'>", unsafe_allow_html=True)
            if st.button("🗑", key=f"tdel_{tid}", help="Delete this task"):
                st.session_state[f"confirm_task_del_{tid}"] = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # Inline delete confirmation
        if st.session_state.get(f"confirm_task_del_{tid}"):
            st.warning(f"Delete task **{task['name']}**?")
            yes_col, no_col, _ = st.columns([1, 1, 8])
            with yes_col:
                if st.button("Yes", key=f"yes_tdel_{tid}", type="primary"):
                    db.delete_task(tid)
                    st.session_state.pop(f"confirm_task_del_{tid}", None)
                    st.rerun()
            with no_col:
                if st.button("No", key=f"no_tdel_{tid}"):
                    st.session_state.pop(f"confirm_task_del_{tid}", None)
                    st.rerun()

    st.markdown("<hr style='margin:8px 0; border-color:#2D2D54'>", unsafe_allow_html=True)

# ── ADD NEW TASK ──────────────────────────────────────────────────
with st.expander("➕ Add New Task", expanded=(len(tasks) == 0)):
    with st.form("add_task_form", clear_on_submit=True):
        st.markdown("**Add a task to this project:**")
        nt_col1, nt_col2, nt_col3 = st.columns([4, 3, 2])
        with nt_col1:
            new_task_name = st.text_input(
                "Task Name *",
                placeholder="e.g., PCB Layout, Firmware v1, Power Testing...",
            )
        with nt_col2:
            new_task_notes = st.text_input(
                "Notes (optional)",
                placeholder="Brief description",
            )
        with nt_col3:
            new_task_status = st.selectbox("Initial Status", STATUS_OPTIONS)

        add_btn = st.form_submit_button("➕ Add Task", type="primary")

    if add_btn:
        if not new_task_name.strip():
            st.error("Task name cannot be empty.")
        else:
            next_order = len(tasks)  # Put new task at the end
            db.create_task(
                project_id=project_id,
                name=new_task_name.strip(),
                description=new_task_notes.strip(),
                status=new_task_status,
                order_index=next_order,
            )
            st.success(f"Task **'{new_task_name}'** added!")
            st.rerun()

st.divider()

# ─────────────────────────────────────────────────────────────────
# PROJECT LINKS SECTION
# ─────────────────────────────────────────────────────────────────
st.markdown("### 🔗 Project Links")

# Collect all links that have a value
link_definitions = [
    ("github_url",  "🐙 GitHub",       "Source code repository"),
    ("kicad_url",   "📐 KiCad / PCB",  "Schematic & PCB files"),
    ("fusion_url",  "⚙️ Fusion 360",   "3D CAD model"),
    ("arduino_url", "💾 Firmware",     "Arduino / PlatformIO code"),
    ("docs_url",    "📄 Docs",         "Project documentation"),
    ("demo_url",    "🎥 Demo Video",   "Working demo video"),
]

active_links = [
    (label, tooltip, project[field])
    for field, label, tooltip in link_definitions
    if project[field]
]

if active_links:
    # Render links as styled buttons in a horizontal row
    link_html = '<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px;">'
    for label, tooltip, url in active_links:
        link_html += (
            f'<a href="{url}" target="_blank" class="link-btn" title="{tooltip}">'
            f'{label}</a>'
        )
    link_html += "</div>"
    st.markdown(link_html, unsafe_allow_html=True)
else:
    st.caption("No links added yet. Edit the project below to add them.")

st.divider()

# ─────────────────────────────────────────────────────────────────
# EDIT PROJECT SECTION (collapsible)
# ─────────────────────────────────────────────────────────────────
st.markdown("### ✏️ Edit Project")

with st.expander("Click to expand and edit project details", expanded=False):
    with st.form("edit_project_form"):
        st.markdown("**Project Information**")

        edit_name = st.text_input(
            "Project Name *",
            value=project["name"],
        )
        edit_desc = st.text_area(
            "Description",
            value=project["description"] or "",
            height=80,
        )

        e_col1, e_col2 = st.columns(2)
        with e_col1:
            # Parse the stored date string back to a date object for the widget
            existing_date = None
            if project["deadline"]:
                try:
                    existing_date = date.fromisoformat(project["deadline"])
                except ValueError:
                    pass
            edit_deadline = st.date_input(
                "Deadline",
                value=existing_date,
                format="YYYY-MM-DD",
            )
        with e_col2:
            edit_budget = st.number_input(
                "Budget (₹)",
                min_value=0.0,
                value=float(project["budget"] or 0.0),
                step=100.0,
                format="%.2f",
            )

        st.markdown("**Project Links**")
        lc1, lc2 = st.columns(2)
        with lc1:
            edit_github  = st.text_input("🐙 GitHub",     value=project["github_url"]  or "")
            edit_kicad   = st.text_input("📐 KiCad",      value=project["kicad_url"]   or "")
            edit_fusion  = st.text_input("⚙️ Fusion 360", value=project["fusion_url"]  or "")
        with lc2:
            edit_arduino = st.text_input("💾 Firmware",   value=project["arduino_url"] or "")
            edit_docs    = st.text_input("📄 Docs",       value=project["docs_url"]    or "")
            edit_demo    = st.text_input("🎥 Demo Video", value=project["demo_url"]    or "")

        save_edit = st.form_submit_button(
            "💾 Save Changes", type="primary", use_container_width=True
        )

    if save_edit:
        if not edit_name.strip():
            st.error("Project name cannot be empty.")
        else:
            db.update_project(
                project_id=project_id,
                name=edit_name.strip(),
                description=edit_desc.strip(),
                deadline=str(edit_deadline) if edit_deadline else None,
                budget=edit_budget,
                github_url=edit_github.strip(),
                kicad_url=edit_kicad.strip(),
                fusion_url=edit_fusion.strip(),
                arduino_url=edit_arduino.strip(),
                docs_url=edit_docs.strip(),
                demo_url=edit_demo.strip(),
            )
            st.success("Project updated successfully!")
            st.rerun()  # Reload the page so the header reflects the new values

st.divider()

# ─────────────────────────────────────────────────────────────────
# DANGER ZONE — Delete the whole project
# ─────────────────────────────────────────────────────────────────
with st.expander("⚠️ Danger Zone", expanded=False):
    st.warning(
        "Deleting this project will permanently remove it along with "
        "**all its tasks and components**. This cannot be undone."
    )
    if st.button("🗑 Delete This Project", type="primary"):
        st.session_state["confirm_proj_delete"] = True
        st.rerun()

if st.session_state.get("confirm_proj_delete"):
    st.error(
        f"Are you absolutely sure you want to delete **{project['name']}**? "
        "All tasks and cost data will be lost."
    )
    dc1, dc2, _ = st.columns([1, 1, 8])
    with dc1:
        if st.button("Yes, Delete Everything", type="primary"):
            db.delete_project(project_id)
            st.session_state.pop("confirm_proj_delete", None)
            st.session_state.pop("selected_project_id", None)
            st.session_state["project_deleted"] = project["name"]
            st.switch_page("app.py")
    with dc2:
        if st.button("Cancel"):
            st.session_state.pop("confirm_proj_delete", None)
            st.rerun()
