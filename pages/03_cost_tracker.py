"""
pages/03_cost_tracker.py — Cost & Component Tracker Page
─────────────────────────────────────────────────────────────────
Milestone 5 — Cost & Component Tracker
Features:
  • Select any project or default to the active project
  • Add components with quantity, unit price, link, and notes
  • Auto-calculate component total price (qty × unit_price)
  • Real-time project spending calculation
  • Project spending vs. budget comparison:
      - Budget, Total Spent, Remaining Budget, % Budget Used
      - Color-coded status banners: Within Budget / Warning / Over Budget
      - Visual budget progress bar
  • Edit component details (name, qty, unit price, link, notes)
  • Delete components with confirmation
  • Interactive visual cost breakdown (Plotly donut chart)
  • Export Bill of Materials (BOM) as CSV
─────────────────────────────────────────────────────────────────
"""

import streamlit as st
import os
import pandas as pd
import plotly.express as px
import database as db

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cost Tracker — ProjectPulse",
    page_icon="💰",
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
    st.markdown('<p class="page-title">💰 Cost & Component Tracker</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-subheader">Track components, parts, and hardware budget</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="empty-state">
            <h2>No Projects Found</h2>
            <p>You haven't created any projects yet. Create your first ECE project to start tracking components and costs!</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("➕ Create First Project", type="primary"):
        st.switch_page("pages/01_create_project.py")
    st.stop()

# Determine initial project ID: query params > session_state > first project
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

# Find active project object
project = next((p for p in all_projects if p["id"] == selected_id), all_projects[0])
project_id = project["id"]

# ─────────────────────────────────────────────────────────────────
# TOP NAVIGATION & PROJECT SELECTOR
# ─────────────────────────────────────────────────────────────────
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1.5, 1.5, 1.5, 1.5, 4.0])
with nav_col1:
    if st.button("← Dashboard", use_container_width=True):
        st.switch_page("app.py")
with nav_col2:
    if st.button("📋 Project Detail", use_container_width=True):
        st.session_state["selected_project_id"] = project_id
        st.switch_page("pages/02_project_detail.py")
with nav_col3:
    if st.button("🎨 Showcase Editor", use_container_width=True):
        st.session_state["selected_project_id"] = project_id
        st.switch_page("pages/04_showcase_editor.py")
with nav_col4:
    if st.button("➕ New Project", use_container_width=True):
        st.switch_page("pages/01_create_project.py")
with nav_col5:
    # Project switcher dropdown
    project_options = {p["id"]: f"{p['name']} (Budget: ₹{float(p['budget'] or 0):,.0f})" for p in all_projects}
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
# CALCULATE COSTS & BUDGET STATS
# ─────────────────────────────────────────────────────────────────
budget = float(project["budget"] or 0.0)
components = db.get_components(project_id)
spent = float(db.get_total_spent(project_id))
remaining = budget - spent
budget_pct = (spent / budget * 100.0) if budget > 0 else 0.0
total_quantity = sum(c["quantity"] for c in components)
progress = db.calculate_progress(project_id)

# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ ProjectPulse")
    st.markdown("*Your ECE Project Tracker*")
    st.divider()
    st.page_link("app.py",                     label="🏠 Dashboard")
    st.page_link("pages/01_create_project.py", label="➕ New Project")
    st.page_link("pages/02_project_detail.py", label="📋 Project Detail")
    st.page_link("pages/03_cost_tracker.py",   label="💰 Cost Tracker")
    st.page_link("pages/04_showcase_editor.py",label="🎨 Showcase Editor")
    st.divider()
    st.markdown(f"**Active Project:**")
    st.markdown(f"📋 **{project['name']}**")
    st.markdown(f"**Task Progress:** {progress}%")
    st.progress(progress / 100)
    st.markdown(f"**Budget:** ₹{budget:,.2f}")
    st.markdown(f"**Total Spent:** ₹{spent:,.2f}")
    if budget > 0:
        if spent > budget:
            st.markdown(f"**Status:** <span style='color:#F87171;'>Over Budget by ₹{abs(remaining):,.2f}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**Remaining:** <span style='color:#34D399;'>₹{remaining:,.2f}</span>", unsafe_allow_html=True)
    st.divider()
    st.markdown(
        "<small style='color:#5050A0'>Milestone 5 — Cost & Component Tracker ✅</small>",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────
st.markdown('<p class="page-title">💰 Cost & Component Tracker</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="section-subheader">Hardware Bill of Materials (BOM) & Budget for <strong>{project["name"]}</strong></p>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────
# BUDGET OVERVIEW CARDS
# ─────────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        label="🎯 Project Budget",
        value=f"₹{budget:,.2f}",
        help="Allocated budget for this project",
    )

with m2:
    st.metric(
        label="💸 Total Spent",
        value=f"₹{spent:,.2f}",
        delta=f"{budget_pct:.1f}% of budget" if budget > 0 else f"{len(components)} components",
        delta_color="off",
        help="Sum of all component costs",
    )

with m3:
    if budget > 0:
        st.metric(
            label="⚖️ Remaining Budget",
            value=f"₹{remaining:,.2f}",
            delta=f"{'-' if remaining < 0 else '+'}{abs(remaining):,.2f}",
            delta_color="normal" if remaining >= 0 else "inverse",
            help="Total Budget minus Total Spent",
        )
    else:
        st.metric(
            label="⚖️ Remaining Budget",
            value="No limit set",
            help="Set a budget in Project Detail to enable limits",
        )

with m4:
    st.metric(
        label="📦 Components Count",
        value=f"{len(components)} items",
        delta=f"{total_quantity} total units",
        delta_color="off",
        help="Number of unique parts and total units",
    )

# ─────────────────────────────────────────────────────────────────
# BUDGET VISUAL STATUS & PROGRESS BAR
# ─────────────────────────────────────────────────────────────────
if budget > 0:
    if spent > budget:
        over_amt = spent - budget
        st.markdown(
            f"""
            <div class="budget-banner budget-banner-danger">
                <span>🚨</span>
                <div>
                    <strong>OVER BUDGET!</strong> You have exceeded the allocated budget by 
                    <strong>₹{over_amt:,.2f}</strong> ({budget_pct:.1f}% of budget consumed).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(1.0, text=f"Budget Exceeded: ₹{spent:,.2f} spent of ₹{budget:,.2f} ({budget_pct:.1f}%)")
    elif budget_pct >= 80:
        st.markdown(
            f"""
            <div class="budget-banner budget-banner-warn">
                <span>⚠️</span>
                <div>
                    <strong>Budget Warning:</strong> You have used <strong>{budget_pct:.1f}%</strong> of your budget. 
                    Only <strong>₹{remaining:,.2f}</strong> remaining.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(spent / budget, 1.0), text=f"Budget Usage: ₹{spent:,.2f} of ₹{budget:,.2f} ({budget_pct:.1f}%)")
    else:
        st.markdown(
            f"""
            <div class="budget-banner budget-banner-ok">
                <span>✅</span>
                <div>
                    <strong>Within Budget:</strong> <strong>{budget_pct:.1f}%</strong> of budget used. 
                    <strong>₹{remaining:,.2f}</strong> remaining for remaining parts.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(spent / budget, 1.0), text=f"Budget Usage: ₹{spent:,.2f} of ₹{budget:,.2f} ({budget_pct:.1f}%)")
else:
    st.info("💡 **No budget set for this project.** You can set a budget on the Project Detail page under 'Edit Project' to track spending limits.")

# ─────────────────────────────────────────────────────────────────
# VISUAL BREAKDOWN (CHARTS)
# ─────────────────────────────────────────────────────────────────
if components:
    with st.expander("📊 Cost Breakdown & Analysis", expanded=False):
        chart_col1, chart_col2 = st.columns([1, 1])

        df_components = pd.DataFrame([
            {
                "Component": c["name"],
                "Quantity": c["quantity"],
                "Unit Price (₹)": c["unit_price"],
                "Total Cost (₹)": c["total_price"],
            }
            for c in components
        ])

        with chart_col1:
            fig_pie = px.pie(
                df_components,
                names="Component",
                values="Total Cost (₹)",
                title="Spending Distribution by Component",
                hole=0.45,
                color_discrete_sequence=px.colors.sequential.Purp,
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E0F0"),
                margin=dict(t=40, b=20, l=20, r=20),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with chart_col2:
            fig_bar = px.bar(
                df_components.sort_values(by="Total Cost (₹)", ascending=True),
                x="Total Cost (₹)",
                y="Component",
                orientation="h",
                title="Component Cost Ranking",
                color="Total Cost (₹)",
                color_continuous_scale="Purples",
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E0F0"),
                margin=dict(t=40, b=20, l=20, r=20),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────
# ADD COMPONENT SECTION
# ─────────────────────────────────────────────────────────────────
st.markdown("### ➕ Add Component / Hardware Part")

with st.expander("Click to add a new part or component", expanded=(len(components) == 0)):
    with st.form(key="add_component_form", clear_on_submit=True):
        c_name = st.text_input(
            "Component Name *",
            placeholder="e.g. ESP32-WROOM-32, L298N Motor Driver, HC-SR04, 10k Resistor (Pack)",
            help="Name or part number of the hardware component",
        )

        col_q, col_p, col_preview = st.columns([1, 1, 1.5])
        with col_q:
            c_qty = st.number_input("Quantity *", min_value=1, value=1, step=1)
        with col_p:
            c_price = st.number_input("Unit Price (₹) *", min_value=0.0, value=0.0, step=10.0, format="%.2f")
        with col_preview:
            st.markdown("<p style='font-size:0.8rem; color:#8080A0; margin-bottom:4px;'>Subtotal (Auto-Calculated):</p>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='background:#1A1A2E; border:1px solid #2D2D54; border-radius:8px; padding:8px 12px; font-size:1.1rem; font-weight:600; color:#34D399;'>"
                f"₹{c_qty * c_price:,.2f}"
                f"</div>",
                unsafe_allow_html=True,
            )

        col_link, col_notes = st.columns([1, 1])
        with col_link:
            c_link = st.text_input(
                "Purchase Link / Store (Optional)",
                placeholder="https://robu.in/... or Amazon / Mouser URL",
                help="Store URL where the part was bought or is planned to be ordered",
            )
        with col_notes:
            c_notes = st.text_input(
                "Notes / Specifications (Optional)",
                placeholder="e.g. 3.3V logic, dual H-bridge, SMD 0805",
                help="Extra notes, specifications, package type, or vendor info",
            )

        submitted = st.form_submit_button("➕ Add Component", use_container_width=True, type="primary")

        if submitted:
            if not c_name.strip():
                st.error("Please provide a component name.")
            else:
                db.create_component(
                    project_id=project_id,
                    name=c_name.strip(),
                    quantity=int(c_qty),
                    unit_price=float(c_price),
                    purchase_link=c_link.strip(),
                    notes=c_notes.strip(),
                )
                st.success(f"Added component: **{c_name.strip()}** (Total: ₹{c_qty * c_price:,.2f})")
                st.rerun()

st.markdown("---")

# ─────────────────────────────────────────────────────────────────
# BILL OF MATERIALS (BOM) & COMPONENT LIST
# ─────────────────────────────────────────────────────────────────
header_col1, header_col2 = st.columns([6, 4])
with header_col1:
    st.markdown(f"### 📦 Bill of Materials ({len(components)} items)")
with header_col2:
    if components:
        # Download BOM as CSV
        df_export = pd.DataFrame([
            {
                "Component Name": c["name"],
                "Quantity": c["quantity"],
                "Unit Price (INR)": f"{c['unit_price']:.2f}",
                "Total Price (INR)": f"{c['total_price']:.2f}",
                "Purchase Link": c["purchase_link"] or "",
                "Notes": c["notes"] or "",
            }
            for c in components
        ])
        csv_data = df_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download BOM (CSV)",
            data=csv_data,
            file_name=f"{project['name'].lower().replace(' ', '_')}_bom.csv",
            mime="text/csv",
            use_container_width=True,
        )

if not components:
    st.markdown("""
        <div class="empty-state">
            <h2>No components recorded yet</h2>
            <p>Add components using the form above to begin tracking parts, prices, and your project's total spend.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for comp in components:
        cid = comp["id"]
        c_name = comp["name"]
        c_qty = comp["quantity"]
        c_unit = comp["unit_price"]
        c_total = comp["total_price"]
        c_link = comp["purchase_link"]
        c_notes = comp["notes"]

        # Component Card Container
        with st.container():
            st.markdown("""<div class="cost-card">""", unsafe_allow_html=True)
            col_info, col_qty, col_unit, col_total, col_actions = st.columns([3.5, 1, 1.2, 1.5, 1.8])

            with col_info:
                st.markdown(f"**{c_name}**")
                extra_details = []
                if c_notes:
                    extra_details.append(f"📝 {c_notes}")
                if c_link:
                    url = c_link if c_link.startswith(("http://", "https://")) else f"https://{c_link}"
                    extra_details.append(f'<a href="{url}" target="_blank" style="color:#A78BFA; text-decoration:none;">🔗 Store Link</a>')
                if extra_details:
                    st.markdown(f"<small style='color:#A0A0C0;'>{' &nbsp;|&nbsp; '.join(extra_details)}</small>", unsafe_allow_html=True)

            with col_qty:
                st.markdown(f"<span style='color:#8080A0; font-size:0.8rem;'>QTY</span><br><strong>{c_qty}</strong>", unsafe_allow_html=True)

            with col_unit:
                st.markdown(f"<span style='color:#8080A0; font-size:0.8rem;'>UNIT</span><br>₹{c_unit:,.2f}", unsafe_allow_html=True)

            with col_total:
                st.markdown(f"<span style='color:#8080A0; font-size:0.8rem;'>TOTAL</span><br><strong style='color:#34D399;'>₹{c_total:,.2f}</strong>", unsafe_allow_html=True)

            with col_actions:
                act1, act2 = st.columns(2)
                with act1:
                    edit_clicked = st.button("✏️", key=f"edit_btn_{cid}", help="Edit this component")
                    if edit_clicked:
                        st.session_state[f"editing_{cid}"] = not st.session_state.get(f"editing_{cid}", False)
                with act2:
                    del_clicked = st.button("🗑️", key=f"del_btn_{cid}", help="Delete this component")
                    if del_clicked:
                        st.session_state[f"confirm_delete_comp_{cid}"] = True

            st.markdown("</div>", unsafe_allow_html=True)

        # ── Edit Component Form (Collapsible/Conditional) ────────────────
        if st.session_state.get(f"editing_{cid}", False):
            with st.form(key=f"edit_comp_form_{cid}"):
                st.markdown(f"#### ✏️ Edit Component: {c_name}")
                e_name = st.text_input("Component Name", value=c_name)
                eq_col, ep_col, ep_preview = st.columns([1, 1, 1.5])
                with eq_col:
                    e_qty = st.number_input("Quantity", min_value=1, value=int(c_qty), step=1, key=f"e_qty_{cid}")
                with ep_col:
                    e_price = st.number_input("Unit Price (₹)", min_value=0.0, value=float(c_unit), step=10.0, format="%.2f", key=f"e_price_{cid}")
                with ep_preview:
                    st.markdown("<p style='font-size:0.8rem; color:#8080A0; margin-bottom:4px;'>Updated Total:</p>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='background:#1A1A2E; border:1px solid #2D2D54; border-radius:8px; padding:8px 12px; font-size:1.1rem; font-weight:600; color:#34D399;'>"
                        f"₹{e_qty * e_price:,.2f}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                el_col, en_col = st.columns([1, 1])
                with el_col:
                    e_link = st.text_input("Purchase Link", value=c_link or "", key=f"e_link_{cid}")
                with en_col:
                    e_notes = st.text_input("Notes / Specifications", value=c_notes or "", key=f"e_notes_{cid}")

                btn_save_col, btn_cancel_col, _ = st.columns([1.5, 1.5, 7])
                with btn_save_col:
                    save_clicked = st.form_submit_button("💾 Save Changes", type="primary")
                with btn_cancel_col:
                    cancel_clicked = st.form_submit_button("Cancel")

                if save_clicked:
                    if not e_name.strip():
                        st.error("Component name cannot be empty.")
                    else:
                        db.update_component(
                            comp_id=cid,
                            name=e_name.strip(),
                            quantity=int(e_qty),
                            unit_price=float(e_price),
                            purchase_link=e_link.strip(),
                            notes=e_notes.strip(),
                        )
                        st.session_state[f"editing_{cid}"] = False
                        st.success(f"Updated **{e_name.strip()}** successfully!")
                        st.rerun()

                if cancel_clicked:
                    st.session_state[f"editing_{cid}"] = False
                    st.rerun()

        # ── Delete Component Confirmation ────────────────────────────────
        if st.session_state.get(f"confirm_delete_comp_{cid}", False):
            st.warning(f"⚠️ Are you sure you want to delete **{c_name}**? Total ₹{c_total:,.2f} will be deducted from project spending.")
            d_yes, d_no, _ = st.columns([1, 1, 8])
            with d_yes:
                if st.button("Yes, Delete", key=f"yes_delete_comp_{cid}", type="primary"):
                    db.delete_component(cid)
                    st.session_state.pop(f"confirm_delete_comp_{cid}", None)
                    st.success(f"Component '{c_name}' removed.")
                    st.rerun()
            with d_no:
                if st.button("Cancel", key=f"cancel_delete_comp_{cid}"):
                    st.session_state.pop(f"confirm_delete_comp_{cid}", None)
                    st.rerun()

    # Grand Total Summary Box
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg, #1A1A2E 0%, #16213E 100%); border:1px solid #6C63FF; border-radius:12px; padding:18px 24px; margin-top:20px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="color:#A78BFA; font-weight:600; font-size:1.1rem;">Bill of Materials Grand Total</span><br>
                <small style="color:#8080A0;">{len(components)} components | {total_quantity} total units</small>
            </div>
            <div style="text-align:right;">
                <span style="font-size:1.6rem; font-weight:700; color:{'#F87171' if budget > 0 and spent > budget else '#34D399'};">
                    ₹{spent:,.2f}
                </span><br>
                <small style="color:#8080A0;">{'Over budget by ₹' + f'{spent - budget:,.2f}' if budget > 0 and spent > budget else ('Remaining: ₹' + f'{remaining:,.2f}' if budget > 0 else 'No budget limit')}</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
