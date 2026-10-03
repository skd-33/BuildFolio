"""
pages/05_showcase_viewer.py — Project Showcase Viewer (Stage 3)
─────────────────────────────────────────────────────────────────
A read-only, portfolio-style page that presents a completed ECE
project as a polished showcase — no forms, no edit controls.

Sections:
  1. Hero — project name, status badge, technologies, GitHub link
  2. Problem & Solution — two-column narrative cards
  3. Progress & Stats — visual progress, budget, task counts
  4. Media Gallery — cover image, circuit/PCB/CAD images, video
  5. System Architecture — structured node/edge visualization
  6. Hardware & Components — component table from cost tracker
  7. Project Links — GitHub, KiCad, Firmware, Docs, Demo
─────────────────────────────────────────────────────────────────
"""

import streamlit as st
import os
import json
import database as db

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Project Showcase — ProjectPulse",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────
# LOAD BASE CSS + VIEWER-SPECIFIC STYLES
# ─────────────────────────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
/* ── Hero section ──────────────────────────────────────────────── */
.sv-hero {
    background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 40%, #16213E 100%);
    border: 1px solid #2D2D54;
    border-radius: 20px;
    padding: 52px 48px 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.sv-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #6C63FF, #A78BFA, #6C63FF);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
.sv-hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E0E0F0 0%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 12px;
}
.sv-hero-desc {
    font-size: 1.05rem;
    color: #9090B0;
    line-height: 1.65;
    max-width: 780px;
    margin-bottom: 24px;
}
.sv-published-badge {
    display: inline-block;
    padding: 5px 16px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.sv-published { background: rgba(52,211,153,0.15); border: 1px solid rgba(52,211,153,0.4); color: #34D399; }
.sv-draft     { background: rgba(251,191,36,0.12);  border: 1px solid rgba(251,191,36,0.4);  color: #FBBF24; }

/* ── Technology pills ──────────────────────────────────────────── */
.sv-tech-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
.sv-tech-pill {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    background: rgba(108,99,255,0.15);
    border: 1px solid rgba(108,99,255,0.4);
    color: #A78BFA;
    font-size: 0.82rem;
    font-weight: 500;
}

/* ── Section labels ────────────────────────────────────────────── */
.sv-section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6C63FF;
    margin-bottom: 10px;
}
.sv-section-title {
    font-size: 1.55rem;
    font-weight: 700;
    color: #E0E0F0;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #2D2D54;
}

/* ── Problem / Solution cards ──────────────────────────────────── */
.sv-narrative-card {
    background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
    border: 1px solid #2D2D54;
    border-radius: 16px;
    padding: 28px;
    height: 100%;
    min-height: 160px;
}
.sv-narrative-card h4 {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.sv-narrative-card p {
    font-size: 0.97rem;
    color: #B0B0D0;
    line-height: 1.75;
    margin: 0;
}
.sv-problem-card h4 { color: #F87171; }
.sv-solution-card h4 { color: #34D399; }

/* ── Stats cards ───────────────────────────────────────────────── */
.sv-stat-card {
    background: rgba(108,99,255,0.08);
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    margin-bottom: 8px;
}
.sv-stat-num {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sv-stat-lbl {
    font-size: 0.72rem;
    color: #8080A0;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 4px;
}

/* ── Media label ───────────────────────────────────────────────── */
.sv-media-label {
    font-size: 0.72rem;
    color: #8080A0;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    text-align: center;
    margin-top: 6px;
}

/* ── Architecture canvas ───────────────────────────────────────── */
.sv-arch-canvas {
    background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 100%);
    border: 1px solid #2D2D54;
    border-radius: 16px;
    padding: 28px;
}
.sv-node {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 130px;
    min-height: 72px;
    border-radius: 12px;
    padding: 10px 12px;
    text-align: center;
    font-size: 0.82rem;
    font-weight: 600;
    border: 1.5px solid;
    margin: 6px;
    transition: transform 0.15s;
    cursor: default;
}
.sv-node:hover { transform: translateY(-2px); }
.sv-node-type {
    font-size: 0.64rem;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    opacity: 0.7;
    margin-top: 3px;
}
.svn-processing { background: rgba(108,99,255,0.18); border-color: rgba(108,99,255,0.6); color: #A78BFA; }
.svn-input      { background: rgba(52,211,153,0.12);  border-color: rgba(52,211,153,0.5);  color: #34D399; }
.svn-output     { background: rgba(96,165,250,0.12);  border-color: rgba(96,165,250,0.5);  color: #60A5FA; }
.svn-power      { background: rgba(251,191,36,0.12);  border-color: rgba(251,191,36,0.5);  color: #FBBF24; }
.svn-storage    { background: rgba(248,113,113,0.12); border-color: rgba(248,113,113,0.5); color: #F87171; }
.svn-cloud      { background: rgba(167,139,250,0.12); border-color: rgba(167,139,250,0.5); color: #C4B5FD; }

/* ── Edge rows ─────────────────────────────────────────────────── */
.sv-edge-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 16px;
    background: rgba(108,99,255,0.06);
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 0.88rem;
}
.sv-edge-src  { color: #A78BFA; font-weight: 600; font-family: monospace; }
.sv-edge-arr  { color: #5050A0; }
.sv-edge-tgt  { color: #A78BFA; font-weight: 600; font-family: monospace; }
.sv-edge-lbl  { color: #8080A0; font-style: italic; margin-left: auto; }

/* ── Component table ───────────────────────────────────────────── */
.sv-comp-row {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 12px;
    padding: 10px 16px;
    border-radius: 8px;
    align-items: center;
    font-size: 0.88rem;
}
.sv-comp-header {
    background: rgba(108,99,255,0.12);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #8080A0;
    border-radius: 8px;
    margin-bottom: 4px;
}
.sv-comp-data       { color: #C0C0E0; }
.sv-comp-data:hover { background: rgba(108,99,255,0.06); }
.sv-comp-name       { font-weight: 500; color: #E0E0F0; }
.sv-comp-price      { color: #34D399; font-weight: 600; }

/* ── GitHub / resource buttons ─────────────────────────────────── */
.sv-gh-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 22px;
    border-radius: 10px;
    background: rgba(108,99,255,0.15);
    border: 1px solid rgba(108,99,255,0.4);
    color: #A78BFA;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 600;
    transition: background 0.2s, transform 0.15s;
    margin: 4px;
}
.sv-gh-btn:hover {
    background: rgba(108,99,255,0.3);
    color: #C4B5FD;
    transform: translateY(-2px);
}

/* ── Empty showcase placeholder ────────────────────────────────── */
.sv-no-showcase {
    text-align: center;
    padding: 80px 20px;
    color: #5050A0;
}
.sv-no-showcase h2 { font-size: 1.6rem; color: #8080A0; margin-bottom: 12px; }
.sv-no-showcase p  { font-size: 0.95rem; color: #5050A0; }

/* ── Video embed wrapper ────────────────────────────────────────── */
.sv-video-wrapper {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #2D2D54;
    background: #0A0A14;
}
</style>
""", unsafe_allow_html=True)

db.init_db()

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
NODE_CSS = {
    "processing": "svn-processing",
    "input":      "svn-input",
    "output":     "svn-output",
    "power":      "svn-power",
    "storage":    "svn-storage",
    "cloud":      "svn-cloud",
}
NODE_ICON = {
    "processing": "⚙️",
    "input":      "📥",
    "output":     "📤",
    "power":      "🔋",
    "storage":    "💾",
    "cloud":      "☁️",
}
MEDIA_LABEL = {
    "cover":         "Cover Image",
    "circuit":       "Circuit Schematic",
    "pcb":           "PCB Layout",
    "cad":           "CAD / 3D Model",
    "gallery_image": "Gallery",
    "demo_video":    "Demo Video",
}


def is_video_url(path):
    low = path.lower()
    return any(s in low for s in ["youtube.com", "youtu.be", "vimeo.com", "drive.google.com"])


def is_local_video(path):
    return path.lower().endswith((".mp4", ".webm"))


def make_embed_url(url):
    """Convert a YouTube/Vimeo watch URL to an embeddable URL."""
    if "youtube.com/watch?v=" in url:
        vid = url.split("v=")[-1].split("&")[0]
        return f"https://www.youtube.com/embed/{vid}"
    if "youtu.be/" in url:
        vid = url.rstrip("/").split("youtu.be/")[-1].split("?")[0]
        return f"https://www.youtube.com/embed/{vid}"
    if "vimeo.com/" in url:
        vid = url.rstrip("/").split("/")[-1]
        return f"https://player.vimeo.com/video/{vid}"
    return None


def tech_pills_html(tech_str):
    if not tech_str or not tech_str.strip():
        return "<span style='color:#5050A0;font-size:0.85rem'>No technologies listed.</span>"
    pills = "".join(
        f'<span class="sv-tech-pill">{t.strip()}</span>'
        for t in tech_str.split(",") if t.strip()
    )
    return f'<div class="sv-tech-row">{pills}</div>'


# ─────────────────────────────────────────────────────────────────
# RESOLVE PROJECT
# ─────────────────────────────────────────────────────────────────
all_projects = db.get_all_projects()

if not all_projects:
    st.markdown('<div class="sv-no-showcase"><h2>🛠️ No projects yet</h2>'
                '<p>Create a project first, then build its showcase.</p></div>',
                unsafe_allow_html=True)
    if st.button("← Dashboard"):
        st.switch_page("app.py")
    st.stop()

query_pid = st.query_params.get("pid")
selected_id = None
if query_pid:
    try:
        qid = int(query_pid)
        if any(p["id"] == qid for p in all_projects):
            selected_id = qid
    except (ValueError, TypeError):
        pass

if selected_id is None:
    sid = st.session_state.get("selected_project_id")
    if sid and any(p["id"] == sid for p in all_projects):
        selected_id = sid
    else:
        selected_id = all_projects[0]["id"]

st.session_state["selected_project_id"] = selected_id
project    = next(p for p in all_projects if p["id"] == selected_id)
project_id = project["id"]

# ─────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────
showcase    = db.get_showcase(project_id)
media_items = db.get_showcase_media(project_id)
components  = db.get_components(project_id)
tasks       = db.get_tasks(project_id)
progress    = db.calculate_progress(project_id)
spent       = db.get_total_spent(project_id)
budget      = float(project["budget"] or 0.0)

arch_data = {"nodes": [], "edges": []}
if showcase and showcase["architecture_data"]:
    try:
        arch_data = json.loads(showcase["architecture_data"])
    except json.JSONDecodeError:
        pass

# ─────────────────────────────────────────────────────────────────
# SIDEBAR — navigation only, no editing controls
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ ProjectPulse")
    st.markdown("*Your ECE Project Tracker*")
    st.divider()
    st.page_link("app.py",                      label="🏠 Dashboard")
    st.page_link("pages/01_create_project.py",  label="➕ New Project")
    st.page_link("pages/02_project_detail.py",  label="📋 Project Detail")
    st.page_link("pages/03_cost_tracker.py",    label="💰 Cost Tracker")
    st.page_link("pages/04_showcase_editor.py", label="🎨 Showcase Editor")
    st.page_link("pages/05_showcase_viewer.py", label="🚀 Showcase")
    st.divider()
    project_options = {p["id"]: p["name"] for p in all_projects}
    sel_dd = st.selectbox(
        "Project",
        options=list(project_options.keys()),
        format_func=lambda x: project_options[x],
        index=list(project_options.keys()).index(project_id),
    )
    if sel_dd != project_id:
        st.session_state["selected_project_id"] = sel_dd
        st.query_params["pid"] = str(sel_dd)
        st.rerun()

# ─────────────────────────────────────────────────────────────────
# TOP NAV
# ─────────────────────────────────────────────────────────────────
nc1, nc2, nc3, _ = st.columns([1.2, 1.4, 1.8, 5.6])
with nc1:
    if st.button("← Dashboard", use_container_width=True):
        st.switch_page("app.py")
with nc2:
    if st.button("📋 Detail", use_container_width=True):
        st.switch_page("pages/02_project_detail.py")
with nc3:
    if st.button("🎨 Edit Showcase", use_container_width=True):
        st.switch_page("pages/04_showcase_editor.py")

# ─────────────────────────────────────────────────────────────────
# ❶  HERO
# ─────────────────────────────────────────────────────────────────
is_published = bool(showcase["is_published"]) if showcase else False
pub_badge = (
    '<span class="sv-published-badge sv-published">● Published</span>'
    if is_published else
    '<span class="sv-published-badge sv-draft">◐ Draft</span>'
)

if progress == 100.0:
    status_html = '<span class="badge badge-completed">✅ Completed</span>'
elif progress > 0:
    status_html = '<span class="badge badge-inprogress">🔄 In Progress</span>'
else:
    status_html = '<span class="badge badge-pending">⏳ Not Started</span>'

desc_text = project["description"] or ""
tech_str  = (showcase["technologies"] if showcase else "") or ""
gh_url    = ((showcase["github_url"] if showcase else "") or project["github_url"] or "")

gh_btn_html = ""
if gh_url:
    gh_btn_html = (f'<a href="{gh_url}" target="_blank" class="sv-gh-btn">'
                   f'🐙 View on GitHub</a>')

st.markdown(f"""
<div class="sv-hero">
    {pub_badge}
    <div class="sv-hero-title">{project["name"]}</div>
    <p class="sv-hero-desc">{desc_text}</p>
    {status_html}
    <div style="margin-top:20px;">
        <div class="sv-section-label" style="margin-top:12px">Technologies</div>
        {tech_pills_html(tech_str)}
    </div>
    <div style="margin-top:16px">{gh_btn_html}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ❷  PROBLEM & SOLUTION
# ─────────────────────────────────────────────────────────────────
prob_text = ((showcase["problem_statement"]    if showcase else "") or "")
sol_text  = ((showcase["solution_description"] if showcase else "") or "")

if prob_text or sol_text:
    st.markdown('<p class="sv-section-label">Narrative</p>', unsafe_allow_html=True)
    st.markdown('<p class="sv-section-title">🧩 Problem &amp; Solution</p>', unsafe_allow_html=True)

    p_col, s_col = st.columns(2, gap="large")
    with p_col:
        body = prob_text.replace("\n", "<br>") if prob_text else (
            "<em style='color:#5050A0'>Not yet described in the Showcase Editor.</em>")
        st.markdown(f"""
        <div class="sv-narrative-card sv-problem-card">
            <h4>🔴 The Problem</h4>
            <p>{body}</p>
        </div>""", unsafe_allow_html=True)
    with s_col:
        body = sol_text.replace("\n", "<br>") if sol_text else (
            "<em style='color:#5050A0'>Not yet described in the Showcase Editor.</em>")
        st.markdown(f"""
        <div class="sv-narrative-card sv-solution-card">
            <h4>🟢 The Solution</h4>
            <p>{body}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ❸  PROGRESS & PROJECT STATS
# ─────────────────────────────────────────────────────────────────
st.markdown('<p class="sv-section-label">At a Glance</p>', unsafe_allow_html=True)
st.markdown('<p class="sv-section-title">📊 Project Stats</p>', unsafe_allow_html=True)

total_tasks     = len(tasks)
completed_tasks = sum(1 for t in tasks if t["status"] == "Completed")
inprog_tasks    = sum(1 for t in tasks if t["status"] == "In Progress")

sc1, sc2, sc3, sc4, sc5 = st.columns(5)
for col, num, lbl in [
    (sc1, f"{progress}%",  "Progress"),
    (sc2, total_tasks,      "Tasks Total"),
    (sc3, completed_tasks,  "Completed"),
    (sc4, inprog_tasks,     "In Progress"),
    (sc5, f"₹{spent:,.0f}", "Total Spent"),
]:
    col.markdown(
        f'<div class="sv-stat-card">'
        f'<div class="sv-stat-num">{num}</div>'
        f'<div class="sv-stat-lbl">{lbl}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
st.progress(
    progress / 100,
    text=f"**{project['name']}** — {progress}% complete  "
         f"({completed_tasks}/{total_tasks} tasks done)",
)
if budget > 0:
    pct   = min(spent / budget, 1.0)
    over  = spent > budget
    label = (
        f"₹{spent:,.0f} spent of ₹{budget:,.0f} budget — "
        + ("⚠️ Over budget!" if over else f"₹{budget - spent:,.0f} remaining")
    )
    st.progress(pct, text=label)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ❹  MEDIA GALLERY
# ─────────────────────────────────────────────────────────────────
if media_items:
    st.markdown('<p class="sv-section-label">Media</p>', unsafe_allow_html=True)
    st.markdown('<p class="sv-section-title">🖼️ Images &amp; Video</p>', unsafe_allow_html=True)

    cover_items  = [m for m in media_items if m["media_type"] == "cover"]
    video_items  = [m for m in media_items if m["media_type"] == "demo_video"]
    image_items  = [m for m in media_items if m["media_type"] not in ("cover", "demo_video")]
    IMAGE_EXTS   = (".jpg", ".jpeg", ".png", ".gif", ".webp")

    # ── Cover (full-width) ───────────────────────────────────────
    for m in cover_items[:1]:
        fp  = m["file_path"]
        cap = m["title"] or "Cover Image"
        if fp.startswith("http"):
            if fp.lower().endswith(IMAGE_EXTS):
                st.image(fp, caption=cap, use_container_width=True)
            else:
                st.markdown(f'<a href="{fp}" target="_blank" class="sv-gh-btn">🖼️ View Cover</a>',
                            unsafe_allow_html=True)
        else:
            abs_p = os.path.join(os.path.dirname(__file__), "..", fp)
            if os.path.exists(abs_p):
                st.image(abs_p, caption=cap, use_container_width=True)
        st.markdown('<p class="sv-media-label">COVER</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Technical images grid ────────────────────────────────────
    if image_items:
        for row_start in range(0, len(image_items), 3):
            row  = image_items[row_start:row_start + 3]
            cols = st.columns(len(row), gap="medium")
            for col, m in zip(cols, row):
                fp    = m["file_path"]
                lbl   = MEDIA_LABEL.get(m["media_type"], m["media_type"].replace("_", " ").title())
                cap   = m["title"] or lbl
                with col:
                    if fp.startswith("http"):
                        if fp.lower().endswith(IMAGE_EXTS):
                            st.image(fp, caption=cap, use_container_width=True)
                        else:
                            st.markdown(f'<a href="{fp}" target="_blank" class="link-btn">🔗 {cap}</a>',
                                        unsafe_allow_html=True)
                    else:
                        abs_p = os.path.join(os.path.dirname(__file__), "..", fp)
                        if os.path.exists(abs_p):
                            st.image(abs_p, caption=cap, use_container_width=True)
                    st.markdown(f'<p class="sv-media-label">{lbl.upper()}</p>',
                                unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Demo video ───────────────────────────────────────────────
    for m in video_items[:1]:
        st.markdown("**🎬 Demo Video**")
        fp = m["file_path"]

        if is_video_url(fp):
            embed = make_embed_url(fp)
            if embed:
                st.markdown(
                    f'<div class="sv-video-wrapper">'
                    f'<iframe width="100%" height="480" src="{embed}" '
                    f'frameborder="0" allow="accelerometer; autoplay; '
                    f'clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
                    f'allowfullscreen></iframe></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f'<a href="{fp}" target="_blank" class="sv-gh-btn">▶ Watch Demo</a>',
                            unsafe_allow_html=True)
        elif is_local_video(fp):
            abs_p = os.path.join(os.path.dirname(__file__), "..", fp)
            if os.path.exists(abs_p):
                st.video(abs_p)
            else:
                st.caption("Video file not found on this server.")
        else:
            st.markdown(f'<a href="{fp}" target="_blank" class="sv-gh-btn">▶ Watch Demo</a>',
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ❺  SYSTEM ARCHITECTURE
# ─────────────────────────────────────────────────────────────────
nodes = arch_data.get("nodes", [])
edges = arch_data.get("edges", [])

if nodes:
    st.markdown('<p class="sv-section-label">System Design</p>', unsafe_allow_html=True)
    st.markdown('<p class="sv-section-title">🧩 System Architecture</p>', unsafe_allow_html=True)

    st.markdown('<div class="sv-arch-canvas">', unsafe_allow_html=True)
    st.markdown("**Components**")

    nodes_per_row = 5
    for row_start in range(0, len(nodes), nodes_per_row):
        row_nodes  = nodes[row_start:row_start + nodes_per_row]
        node_html  = '<div style="display:flex; flex-wrap:wrap; gap:12px; margin-bottom:8px;">'
        for n in row_nodes:
            css_cls  = NODE_CSS.get(n.get("type", "processing"), "svn-processing")
            icon     = NODE_ICON.get(n.get("type", "processing"), "⚙️")
            proto    = n.get("protocol", "")
            proto_h  = f'<div class="sv-node-type">{proto}</div>' if proto else ""
            node_html += (
                f'<div class="sv-node {css_cls}">'
                f'{icon} {n.get("label", n.get("id", "?"))}'
                f'<div class="sv-node-type">{n.get("type","").upper()}</div>'
                f'{proto_h}</div>'
            )
        node_html += "</div>"
        st.markdown(node_html, unsafe_allow_html=True)

    if edges:
        st.markdown("<br>**Connections**", unsafe_allow_html=True)
        for e in edges:
            lbl     = e.get("label", "")
            lbl_h   = f'<span class="sv-edge-lbl">{lbl}</span>' if lbl else ""
            st.markdown(
                f'<div class="sv-edge-row">'
                f'<span class="sv-edge-src">{e.get("source","?")}</span>'
                f'<span class="sv-edge-arr">──▶</span>'
                f'<span class="sv-edge-tgt">{e.get("target","?")}</span>'
                f'{lbl_h}</div>',
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)  # .sv-arch-canvas
    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ❻  HARDWARE & COMPONENTS (from Cost Tracker)
# ─────────────────────────────────────────────────────────────────
if components:
    st.markdown('<p class="sv-section-label">Hardware</p>', unsafe_allow_html=True)
    st.markdown('<p class="sv-section-title">🔩 Components &amp; Bill of Materials</p>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="sv-comp-row sv-comp-header">
        <span>Component</span><span>Qty</span>
        <span>Unit Price</span><span>Total</span>
    </div>""", unsafe_allow_html=True)

    for comp in components:
        link_h  = ""
        if comp["purchase_link"]:
            link_h = (f' <a href="{comp["purchase_link"]}" target="_blank" '
                      f'style="color:#6C63FF;font-size:0.75rem;margin-left:6px;">🔗 Buy</a>')
        notes_h = (f'<br><span style="font-size:0.75rem;color:#8080A0">{comp["notes"]}</span>'
                   if comp["notes"] else "")
        st.markdown(f"""
        <div class="sv-comp-row sv-comp-data">
            <span class="sv-comp-name">{comp["name"]}{link_h}{notes_h}</span>
            <span>{comp["quantity"]}</span>
            <span>₹{comp["unit_price"]:,.2f}</span>
            <span class="sv-comp-price">₹{comp["total_price"]:,.2f}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sv-comp-row" style="
        border-top:1px solid #2D2D54; margin-top:8px;
        padding-top:12px; font-weight:700; color:#E0E0F0;">
        <span>Total Spent</span><span></span><span></span>
        <span class="sv-comp-price" style="font-size:1.05rem">₹{spent:,.2f}</span>
    </div>""", unsafe_allow_html=True)

    if budget > 0:
        remaining = budget - spent
        colour    = "#F87171" if spent > budget else "#34D399"
        sign      = "over"    if spent > budget else "remaining"
        st.markdown(
            f'<div style="text-align:right;margin-top:6px;font-size:0.82rem;color:{colour}">'
            f'Budget: ₹{budget:,.2f} — ₹{abs(remaining):,.2f} {sign}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ❼  PROJECT LINKS
# ─────────────────────────────────────────────────────────────────
link_defs = [
    ("github_url",  "🐙 GitHub"),
    ("kicad_url",   "📐 KiCad / PCB"),
    ("fusion_url",  "⚙️ Fusion 360"),
    ("arduino_url", "💾 Firmware"),
    ("docs_url",    "📄 Docs"),
    ("demo_url",    "🎥 Demo Video"),
]
active_links = [(lbl, project[field]) for field, lbl in link_defs if project[field]]

if active_links:
    st.markdown('<p class="sv-section-label">Resources</p>', unsafe_allow_html=True)
    st.markdown('<p class="sv-section-title">🔗 Project Links</p>', unsafe_allow_html=True)
    html = '<div style="display:flex;flex-wrap:wrap;gap:10px;">'
    for lbl, url in active_links:
        html += f'<a href="{url}" target="_blank" class="sv-gh-btn">{lbl}</a>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# ❽  EMPTY STATE
# ─────────────────────────────────────────────────────────────────
has_content = any([prob_text, sol_text, tech_str, media_items, nodes, components, active_links])
if not has_content:
    st.markdown("""
    <div class="sv-no-showcase">
        <h2>🎨 Showcase not built yet</h2>
        <p>Open the <strong>Showcase Editor</strong> to add your problem statement,
        solution, technologies, images, and architecture diagram.</p>
    </div>""", unsafe_allow_html=True)
    if st.button("🎨 Open Showcase Editor", type="primary"):
        st.switch_page("pages/04_showcase_editor.py")

# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    f'<p style="text-align:center;color:#3030A0;font-size:0.78rem;">'
    f'⚡ ProjectPulse — {project["name"]} — ECE Project Showcase</p>',
    unsafe_allow_html=True,
)
