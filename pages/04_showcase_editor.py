"""
pages/04_showcase_editor.py — Showcase Editor Page (Stage 2)
─────────────────────────────────────────────────────────────────
Allows users to build their project showcase page by:
  • Editing problem/solution text, technologies, and GitHub URL
  • Configuring a custom shareable slug
  • Uploading multiple media files (cover, CAD, PCB, video)
  • Building a structured architecture diagram (nodes/edges)
  • Saving as a Draft or Publishing
─────────────────────────────────────────────────────────────────
"""

import streamlit as st
import os
import json
import database as db
from utils.file_manager import save_uploaded_file

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Showcase Editor — BuildFolio",
    page_icon="🎨",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────
# LOAD CUSTOM CSS
# ─────────────────────────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

db.init_db()

# ─────────────────────────────────────────────────────────────────
# RESOLVE PROJECT SELECTION
# ─────────────────────────────────────────────────────────────────
all_projects = db.get_all_projects()

if not all_projects:
    st.markdown('<p class="page-title">🎨 Showcase Editor</p>', unsafe_allow_html=True)
    st.warning("No projects found. Create a project first to build a showcase.")
    if st.button("➕ Create Project"):
        st.switch_page("pages/01_create_project.py")
    st.stop()

query_pid = st.query_params.get("pid")
selected_id = None

if query_pid:
    try:
        query_pid_int = int(query_pid)
        if any(p["id"] == query_pid_int for p in all_projects):
            selected_id = query_pid_int
    except (ValueError, TypeError):
        pass

if selected_id is None:
    session_id = st.session_state.get("selected_project_id")
    if session_id and any(p["id"] == session_id for p in all_projects):
        selected_id = session_id
    else:
        selected_id = all_projects[0]["id"]

st.session_state["selected_project_id"] = selected_id
project = next(p for p in all_projects if p["id"] == selected_id)
project_id = project["id"]

# ─────────────────────────────────────────────────────────────────
# TOP NAVIGATION & PROJECT SELECTOR
# ─────────────────────────────────────────────────────────────────
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1.5, 1.5, 1.5, 5.5])
with nav_col1:
    if st.button("← Dashboard", use_container_width=True):
        st.switch_page("app.py")
with nav_col2:
    if st.button("📋 Project Detail", use_container_width=True):
        st.switch_page("pages/02_project_detail.py")
with nav_col3:
    if st.button("💰 Cost Tracker", use_container_width=True):
        st.switch_page("pages/03_cost_tracker.py")
with nav_col4:
    project_options = {p["id"]: p["name"] for p in all_projects}
    selected_from_dropdown = st.selectbox(
        "Switch Project",
        options=list(project_options.keys()),
        format_func=lambda x: project_options[x],
        index=list(project_options.keys()).index(project_id),
        label_visibility="collapsed",
    )
    if selected_from_dropdown != project_id:
        st.session_state["selected_project_id"] = selected_from_dropdown
        st.query_params["pid"] = str(selected_from_dropdown)
        st.rerun()

st.divider()

# ─────────────────────────────────────────────────────────────────
# LOAD EXISTING SHOWCASE DATA
# ─────────────────────────────────────────────────────────────────
showcase = db.get_showcase(project_id)
if not showcase:
    showcase = {
        "showcase_slug": f"project-{project_id}",
        "problem_statement": "",
        "solution_description": "",
        "technologies": "",
        "architecture_data": '{"nodes": [], "edges": []}',
        "github_url": project["github_url"] or "",
        "is_published": 0
    }

arch_data = {"nodes": [], "edges": []}
if showcase["architecture_data"]:
    try:
        arch_data = json.loads(showcase["architecture_data"])
    except json.JSONDecodeError:
        pass

# Initialize session state for architecture if not present for this project
arch_state_key = f"arch_{project_id}"
if arch_state_key not in st.session_state:
    st.session_state[arch_state_key] = arch_data

# ─────────────────────────────────────────────────────────────────
# PAGE HEADER & SIDEBAR
# ─────────────────────────────────────────────────────────────────
st.markdown('<p class="page-title">🎨 Showcase Editor</p>', unsafe_allow_html=True)
st.markdown(f'<p class="section-subheader">Build the public showcase page for <strong>{project["name"]}</strong></p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚡ BuildFolio")
    st.markdown("*Your ECE Project Tracker*")
    st.divider()
    st.page_link("app.py",                     label="🏠 Dashboard")
    st.page_link("pages/01_create_project.py", label="➕ New Project")
    st.page_link("pages/02_project_detail.py", label="📋 Project Detail")
    st.page_link("pages/03_cost_tracker.py",   label="💰 Cost Tracker")
    st.page_link("pages/04_showcase_editor.py",label="🎨 Showcase Editor")
    st.page_link("pages/05_showcase_viewer.py",label="🚀 Showcase")
    st.divider()
    st.markdown(f"**Active Project:**")
    st.markdown(f"📋 **{project['name']}**")
    status_color = "#34D399" if showcase['is_published'] else "#FBBF24"
    status_text = "Published" if showcase['is_published'] else "Draft"
    st.markdown(f"**Showcase Status:** <span style='color:{status_color}'>{status_text}</span>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# 1. TEXT DETAILS & META (Form)
# ─────────────────────────────────────────────────────────────────
st.markdown("### 📝 Details & Metadata")
with st.expander("Edit Showcase Details", expanded=True):
    with st.form(key=f"showcase_details_{project_id}"):
        col_slug, col_github = st.columns(2)
        with col_slug:
            s_slug = st.text_input("Showcase Slug (Unique URL Path)", value=showcase["showcase_slug"], help="e.g., smart-plant-v1")
        with col_github:
            s_github = st.text_input("GitHub Repository URL", value=showcase["github_url"])

        s_tech = st.text_input("Technologies Used (Comma separated)", value=showcase["technologies"], placeholder="ESP32, C++, KiCad, MQTT")
        s_prob = st.text_area("Problem Statement", value=showcase["problem_statement"], height=100)
        s_sol = st.text_area("Solution Description", value=showcase["solution_description"], height=150)
        s_published = st.checkbox("Publish this Showcase?", value=bool(showcase["is_published"]), help="If checked, this project will be publicly visible.")

        if st.form_submit_button("💾 Save Details", type="primary"):
            # We also save the current architecture data from session state
            current_arch = json.dumps(st.session_state[arch_state_key])
            try:
                db.upsert_showcase(
                    project_id=project_id,
                    showcase_slug=s_slug.strip(),
                    problem_statement=s_prob.strip(),
                    solution_description=s_sol.strip(),
                    technologies=s_tech.strip(),
                    architecture_data=current_arch,
                    github_url=s_github.strip(),
                    is_published=s_published
                )
                st.success("Showcase details saved successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error saving details: (Check if slug is unique) {e}")

st.divider()

# ─────────────────────────────────────────────────────────────────
# 2. MEDIA UPLOADS
# ─────────────────────────────────────────────────────────────────
st.markdown("### 🖼️ Media & Gallery")

# Show existing media
existing_media = db.get_showcase_media(project_id)
if existing_media:
    for m in existing_media:
        mid = m["id"]
        with st.container():
            mc1, mc2, mc3 = st.columns([2, 5, 1])
            with mc1:
                st.markdown(f"**{m['media_type'].upper()}**")
            with mc2:
                display_path = m['file_path'] if m['file_path'].startswith("http") else f"`{m['file_path']}`"
                st.markdown(f"{m['title'] or 'No title'} — {display_path}")
            with mc3:
                if st.button("🗑️", key=f"del_media_{mid}"):
                    db.delete_showcase_media(mid)
                    st.rerun()
else:
    st.info("No media uploaded yet.")

# Add New Media Form
with st.expander("➕ Upload New Media"):
    with st.form(key=f"upload_media_{project_id}", clear_on_submit=True):
        m_type = st.selectbox("Media Type", options=["cover", "circuit", "pcb", "cad", "demo_video", "gallery_image"])
        m_title = st.text_input("Title (Optional)")
        m_desc = st.text_input("Description (Optional)")
        m_order = st.number_input("Display Order", value=0, step=1)
        
        st.markdown("**File or URL:** Provide an uploaded file OR an external URL (for videos).")
        m_file = st.file_uploader("Upload File", type=['png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm'])
        m_url = st.text_input("External URL (e.g., YouTube link)")

        if st.form_submit_button("📤 Upload Media", type="primary"):
            if m_file:
                # Save locally
                saved_path = save_uploaded_file(project_id, m_file)
                if saved_path:
                    db.add_showcase_media(project_id, saved_path, m_type, m_title, m_desc, m_order)
                    st.success(f"Media '{m_file.name}' uploaded successfully!")
                    st.rerun()
            elif m_url.strip():
                # Save URL
                db.add_showcase_media(project_id, m_url.strip(), m_type, m_title, m_desc, m_order)
                st.success("External media URL saved successfully!")
                st.rerun()
            else:
                st.error("Please provide either a file upload or an external URL.")

st.divider()

# ─────────────────────────────────────────────────────────────────
# 3. STRUCTURED ARCHITECTURE EDITOR
# ─────────────────────────────────────────────────────────────────
st.markdown("### 🧩 System Architecture")
st.markdown("Build your architecture diagram by defining nodes (components) and edges (connections).")

# Display Current Architecture
arch = st.session_state[arch_state_key]

ac1, ac2 = st.columns(2)
with ac1:
    st.markdown("**Nodes**")
    if not arch["nodes"]:
        st.caption("No nodes defined.")
    for i, node in enumerate(arch["nodes"]):
        nc1, nc2 = st.columns([5, 1])
        nc1.markdown(f"`{node['id']}`: **{node['label']}** ({node['type']})")
        if nc2.button("🗑️", key=f"del_node_{i}"):
            arch["nodes"].pop(i)
            # Remove any edges connected to this node
            arch["edges"] = [e for e in arch["edges"] if e["source"] != node["id"] and e["target"] != node["id"]]
            st.rerun()

with ac2:
    st.markdown("**Connections (Edges)**")
    if not arch["edges"]:
        st.caption("No connections defined.")
    for i, edge in enumerate(arch["edges"]):
        ec1, ec2 = st.columns([5, 1])
        ec1.markdown(f"`{edge['source']}` ➔ `{edge['target']}` : *{edge.get('label', '')}*")
        if ec2.button("🗑️", key=f"del_edge_{i}"):
            arch["edges"].pop(i)
            st.rerun()

# Add Node / Edge UI
with st.expander("➕ Add Node or Connection"):
    tab1, tab2 = st.tabs(["Add Node", "Add Connection"])
    
    with tab1:
        n_id = st.text_input("Node ID (unique, e.g., 'mcu', 'sensor1')")
        n_label = st.text_input("Label (e.g., 'ESP32 MCU')")
        n_type = st.selectbox("Type", ["processing", "input", "output", "power", "storage", "cloud"])
        n_proto = st.text_input("Protocol/Details (Optional, e.g., 'I2C')")
        if st.button("Add Node"):
            if n_id and n_label:
                if any(n["id"] == n_id for n in arch["nodes"]):
                    st.error("Node ID already exists.")
                else:
                    arch["nodes"].append({"id": n_id, "label": n_label, "type": n_type, "protocol": n_proto})
                    st.success(f"Added node {n_id}")
                    st.rerun()
            else:
                st.error("Node ID and Label are required.")

    with tab2:
        if len(arch["nodes"]) >= 2:
            node_options = [n["id"] for n in arch["nodes"]]
            e_source = st.selectbox("Source Node", node_options)
            e_target = st.selectbox("Target Node", node_options)
            e_label = st.text_input("Connection Label (e.g., 'Data', '3.3V', 'SPI')")
            if st.button("Add Connection"):
                if e_source != e_target:
                    arch["edges"].append({"source": e_source, "target": e_target, "label": e_label})
                    st.success("Added connection.")
                    st.rerun()
                else:
                    st.error("Source and Target cannot be the same node.")
        else:
            st.info("You need at least 2 nodes to create a connection.")

st.info("💡 **Remember to click 'Save Details' in the top section** to persist your architecture changes to the database!")
