"""
app.py — ProjectPulse Dashboard (Home Page)
─────────────────────────────────────────────────────────────────
This is the MAIN file of the app. When you run:

    streamlit run app.py

Streamlit starts a local web server and opens this page in your browser.
This page acts as the Dashboard — it lists all your projects.

How Streamlit multi-page apps work:
  Any Python file you put inside the 'pages/' folder automatically
  becomes a separate page in the sidebar. No routing code needed!
─────────────────────────────────────────────────────────────────
"""

import streamlit as st      # The web framework
import os                   # For file path operations
from datetime import date   # To work with dates
import database as db       # Our custom database module

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# Must be the FIRST Streamlit command in the script.
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ProjectPulse",          # Browser tab title
    page_icon="⚡",                      # Browser tab icon
    layout="wide",                      # Use full browser width
    initial_sidebar_state="expanded",   # Sidebar open by default
)

# ─────────────────────────────────────────────────────────────────
# INITIALIZE DATABASE
# This runs every time the page loads, but thanks to
# "CREATE TABLE IF NOT EXISTS", it only creates tables once.
# ─────────────────────────────────────────────────────────────────
db.init_db()

# ─────────────────────────────────────────────────────────────────
# LOAD CUSTOM CSS
# We read our style.css file and inject it into the page.
# st.markdown() with unsafe_allow_html=True allows raw HTML/CSS.
# ─────────────────────────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ ProjectPulse")
    st.markdown("*Your ECE Project Tracker*")
    st.divider()
    st.markdown("**Navigation**")
    st.page_link("app.py",                          label="🏠 Dashboard",       icon=None)
    st.page_link("pages/01_create_project.py",      label="➕ New Project",      icon=None)
    st.page_link("pages/03_cost_tracker.py",        label="💰 Cost Tracker",    icon=None)
    st.page_link("pages/04_showcase_editor.py",     label="🎨 Showcase Editor", icon=None)
    st.page_link("pages/05_showcase_viewer.py",     label="🚀 Showcase",        icon=None)
    st.divider()
    st.markdown(
        "<small style='color:#5050A0'>Milestone 5 — Cost & Component Tracker ✅</small>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────
# DASHBOARD HEADER
# ─────────────────────────────────────────────────────────────────
st.markdown('<p class="page-title">⚡ ProjectPulse</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-subheader">ECE & Hardware Engineering Project Tracker</p>',
    unsafe_allow_html=True
)

# Show a success banner if we just redirected from the create-project page
if "new_project_created" in st.session_state:
    st.success(
        f"Project **'{st.session_state['new_project_created']}'** was created successfully!",
        icon="",
    )
    del st.session_state["new_project_created"]

# Show a deletion banner if we just deleted a project from the detail page
if "project_deleted" in st.session_state:
    st.error(
        f"Project **'{st.session_state['project_deleted']}'** was permanently deleted.",
        icon="",
    )
    del st.session_state["project_deleted"]

# ─────────────────────────────────────────────────────────────────
# TOP METRICS ROW
# Shows aggregate stats across all projects.
# ─────────────────────────────────────────────────────────────────
projects = db.get_all_projects()

total_projects = len(projects)
# Count projects where every task is Completed
completed_projects = 0
in_progress_projects = 0

for p in projects:
    progress = db.calculate_progress(p["id"])
    if progress == 100.0:
        completed_projects += 1
    elif progress > 0:
        in_progress_projects += 1

# Display 4 metric boxes side by side using st.columns
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📁 Total Projects",     total_projects)
with col2:
    st.metric("🔄 In Progress",        in_progress_projects)
with col3:
    st.metric("✅ Completed",          completed_projects)
with col4:
    pending = total_projects - in_progress_projects - completed_projects
    st.metric("⏳ Not Started",        pending)

st.divider()

# ─────────────────────────────────────────────────────────────────
# ACTION BUTTON — Create New Project
# ─────────────────────────────────────────────────────────────────
col_btn, col_spacer = st.columns([2, 8])
with col_btn:
    if st.button("➕ New Project", use_container_width=True, type="primary"):
        # st.switch_page navigates to another page file
        st.switch_page("pages/01_create_project.py")

# ─────────────────────────────────────────────────────────────────
# PROJECT CARDS
# ─────────────────────────────────────────────────────────────────
if not projects:
    # Show a friendly empty state when no projects exist yet
    st.markdown("""
        <div class="empty-state">
            <h2>🛠️ No projects yet!</h2>
            <p>Click "New Project" above to create your first ECE project.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f'<p class="section-header">All Projects ({total_projects})</p>',
                unsafe_allow_html=True)

    for project in projects:
        pid       = project["id"]
        name      = project["name"]
        desc      = project["description"] or "No description provided."
        deadline  = project["deadline"]
        budget    = project["budget"] or 0.0
        progress  = db.calculate_progress(pid)
        spent     = db.get_total_spent(pid)
        tasks     = db.get_tasks(pid)

        # ── Determine deadline display ────────────────────────────
        deadline_html = "<span style='color:#5050A0'>No deadline set</span>"
        if deadline:
            try:
                dl_date = date.fromisoformat(deadline)
                days_left = (dl_date - date.today()).days
                if days_left < 0:
                    deadline_html = f'<span class="deadline-past">🔴 Overdue by {abs(days_left)} days</span>'
                elif days_left <= 7:
                    deadline_html = f'<span class="deadline-near">🟡 {days_left} days left</span>'
                else:
                    deadline_html = f'<span class="deadline-ok">🟢 {days_left} days left</span>'
            except ValueError:
                deadline_html = deadline

        # ── Determine status badge ────────────────────────────────
        if progress == 100.0:
            badge_html = '<span class="badge badge-completed">✅ Completed</span>'
        elif progress > 0:
            badge_html = '<span class="badge badge-inprogress">🔄 In Progress</span>'
        else:
            badge_html = '<span class="badge badge-pending">⏳ Pending</span>'

        # ── Render card ───────────────────────────────────────────
        st.markdown(f"""
        <div class="project-card">
            <div style="display:flex; align-items:center; margin-bottom:8px;">
                <span class="card-title">{name}</span>
                {badge_html}
            </div>
            <p style="color:#8080A0; font-size:0.9rem; margin:0 0 12px 12px;">
                {desc[:120]}{"..." if len(desc) > 120 else ""}
            </p>
            <div class="stat-row" style="margin-left:12px;">
                <div class="stat-box">
                    <div class="stat-label">Progress</div>
                    <div class="stat-value">{progress}%</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Tasks</div>
                    <div class="stat-value">{len(tasks)}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Deadline</div>
                    <div class="stat-value" style="font-size:0.85rem;">{deadline_html}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Budget</div>
                    <div class="stat-value">₹{budget:,.0f}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Spent</div>
                    <div class="stat-value" style="color:{'#F87171' if spent > budget and budget > 0 else '#34D399'}">
                        ₹{spent:,.0f}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar below the card
        st.progress(progress / 100,
                    text=f"**{name}** — {progress}% complete")

        # Buttons: View, Costs, Edit Showcase, View Showcase, Delete
        btn_col1, btn_col2, btn_col3, btn_col4, btn_col5, _ = st.columns([1, 1, 1.3, 1.3, 1, 4.4])
        with btn_col1:
            if st.button(f"👁 View", key=f"view_{pid}", use_container_width=True):
                st.session_state["selected_project_id"] = pid
                st.switch_page("pages/02_project_detail.py")
        with btn_col2:
            if st.button(f"💰 Costs", key=f"cost_{pid}", use_container_width=True):
                st.session_state["selected_project_id"] = pid
                st.switch_page("pages/03_cost_tracker.py")
        with btn_col3:
            if st.button(f"🎨 Edit Showcase", key=f"showcase_edit_{pid}", use_container_width=True):
                st.session_state["selected_project_id"] = pid
                st.switch_page("pages/04_showcase_editor.py")
        with btn_col4:
            if st.button(f"🚀 View Showcase", key=f"showcase_view_{pid}", use_container_width=True):
                st.session_state["selected_project_id"] = pid
                st.switch_page("pages/05_showcase_viewer.py")
        with btn_col5:
            if st.button(f"🗑 Delete", key=f"del_{pid}", use_container_width=True):
                st.session_state[f"confirm_delete_{pid}"] = True
                st.rerun()

        # Confirmation popup before deleting
        if st.session_state.get(f"confirm_delete_{pid}"):
            st.warning(f"⚠️ Are you sure you want to delete **{name}**? This cannot be undone.")
            c1, c2, c3 = st.columns([1, 1, 8])
            with c1:
                if st.button("Yes, Delete", key=f"yes_del_{pid}", type="primary"):
                    db.delete_project(pid)
                    st.session_state.pop(f"confirm_delete_{pid}", None)
                    st.success(f"Project '{name}' deleted.")
                    st.rerun()
            with c2:
                if st.button("Cancel", key=f"cancel_del_{pid}"):
                    st.session_state.pop(f"confirm_delete_{pid}", None)
                    st.rerun()

        st.markdown("---")
