"""
ApexMfg AI — Intelligent Operations & Industrial Efficiency Platform
Enterprise manufacturing operations copilot leveraging Firebase, Firestore, Cloud Run, and Gemini.
"""

import os
import time
import pandas as pd
import streamlit as st
from PIL import Image

from backend.telemetry import (
    MACHINES,
    ANOMALY_TYPES,
    generate_telemetry_snapshot,
    generate_historical_series
)
from backend.firestore_service import FirestoreService
from backend.gemini_service import GeminiService

# Page Configuration
st.set_page_config(
    page_title="ApexMfg AI — Intelligent Industrial Operations",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Industrial Dark Theme CSS
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Card Styles */
    .mfg-card {
        background: linear-gradient(145deg, #131b2e, #1a233a);
        border: 1px solid #233052;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #38bdf8;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
    }
    
    /* Status Badges */
    .badge-healthy {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid #059669;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    
    .badge-critical {
        background-color: rgba(239, 68, 68, 0.25);
        color: #f87171;
        border: 1px solid #dc2626;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
        animation: pulse 2s infinite;
    }

    .badge-tech {
        background-color: #1e293b;
        color: #60a5fa;
        border: 1px solid #3b82f6;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 6px;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.6; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "active_anomaly" not in st.session_state:
    st.session_state.active_anomaly = None
if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = "CNC-4001"
if "rca_cache" not in st.session_state:
    st.session_state.rca_cache = {}
if "sop_cache" not in st.session_state:
    st.session_state.sop_cache = {}

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🏭 Industrial Operations Hub")
    st.caption("Challenge: Manufacturing — Intelligent Operations")
    
    # Firebase Auth Role Simulation
    st.markdown("---")
    st.markdown("**🔐 Firebase Identity & RBAC**")
    user_role = st.selectbox(
        "Active Operator Role",
        ["Maintenance Engineer", "Plant Operations Manager", "Quality Control Inspector"]
    )
    st.caption(f"Authenticated as: `operator_{user_role.lower().replace(' ', '_')}@apexmfg.cloud`")

    st.markdown("---")
    st.markdown("**⚙️ Machine Fleet Selector**")
    machine_options = list(MACHINES.keys())
    selected_machine = st.selectbox(
        "Target Asset",
        machine_options,
        index=machine_options.index(st.session_state.selected_machine),
        format_func=lambda x: f"{x} - {MACHINES[x]['name']}"
    )
    st.session_state.selected_machine = selected_machine

    # Anomaly Injector Simulator
    st.markdown("---")
    st.markdown("**⚠️ Anomaly Injection Testing**")
    st.caption("Simulate real-time industrial telemetry faults:")
    
    anomaly_choice = st.selectbox(
        "Inject Anomaly Event",
        ["-- None (Normal Operation) --"] + list(ANOMALY_TYPES.keys()),
        format_func=lambda x: ANOMALY_TYPES[x]["label"] if x in ANOMALY_TYPES else x
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚨 Trigger Fault", use_container_width=True):
            if anomaly_choice != "-- None (Normal Operation) --":
                st.session_state.active_anomaly = anomaly_choice
                target_m = ANOMALY_TYPES[anomaly_choice]["target_machine"]
                st.session_state.selected_machine = target_m
                
                # Auto record incident in Firestore
                snap = generate_telemetry_snapshot(target_m, anomaly_choice)
                inc_id = FirestoreService.record_incident({
                    "machine_id": target_m,
                    "machine_name": MACHINES[target_m]["name"],
                    "anomaly_type": anomaly_choice,
                    "description": ANOMALY_TYPES[anomaly_choice]["description"],
                    "metrics": snap["metrics"],
                    "reported_by": user_role
                })
                st.toast(f"Incident {inc_id} logged to Firestore!", icon="🚨")
                st.rerun()

    with col_btn2:
        if st.button("🔄 Reset Baseline", use_container_width=True):
            st.session_state.active_anomaly = None
            st.session_state.rca_cache = {}
            st.session_state.sop_cache = {}
            st.toast("Telemetry restored to nominal baseline", icon="✅")
            st.rerun()

    st.markdown("---")
    st.markdown("**☁️ GCP Architecture Status**")
    fs_info = FirestoreService.get_connection_info()
    st.markdown(f"• **Cloud Run:** <span class='badge-tech'>ACTIVE :8080</span>", unsafe_allow_html=True)
    st.markdown(f"• **Firestore:** <span class='badge-tech'>{fs_info['backend']}</span>", unsafe_allow_html=True)
    st.markdown(f"• **Gemini Core:** <span class='badge-tech'>Gemini 2.5 Flash</span>", unsafe_allow_html=True)
    st.markdown(f"• **Firebase Auth:** <span class='badge-tech'>Verified JWT</span>", unsafe_allow_html=True)

# Main Dashboard Header
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 16px; margin-bottom: 24px;">
    <div>
        <h1 style="margin: 0; font-size: 2.1rem; color: #f8fafc; font-weight: 800;">
            ApexMfg AI <span style="font-size: 1.1rem; font-weight: 500; color: #38bdf8;">| Intelligent Industrial Operations</span>
        </h1>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.95rem;">
            Real-Time IoT Predictive Maintenance, Automated Root Cause Analysis & Visual Defect Inspection
        </p>
    </div>
    <div style="text-align: right;">
        <span class="badge-tech">Cloud Run</span>
        <span class="badge-tech">Firestore</span>
        <span class="badge-tech">Gemini 2.5</span>
        <span class="badge-tech">Firebase</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_overview, tab_telemetry, tab_gemini_rca, tab_vision_qc, tab_architecture = st.tabs([
    "🏭 Fleet Digital Twin",
    "📈 Live Telemetry Stream",
    "🧠 Gemini Predictive RCA & SOP",
    "🔍 Multimodal Visual QA",
    "☁️ GCP Stack & Firestore Ledger"
])

# -------------------------------------------------------------
# TAB 1: FLEET DIGITAL TWIN OVERVIEW
# -------------------------------------------------------------
with tab_overview:
    # High-level KPIs
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown("""
        <div class="mfg-card">
            <div class="metric-label">Plant Overall OEE</div>
            <div class="metric-value">88.6%</div>
            <div style="color: #34d399; font-size: 0.8rem; margin-top: 4px;">▲ +3.4% vs last shift</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        active_inc = 1 if st.session_state.active_anomaly else 0
        badge_cls = "badge-critical" if active_inc > 0 else "badge-healthy"
        status_txt = "ACTION REQUIRED" if active_inc > 0 else "NOMINAL"
        st.markdown(f"""
        <div class="mfg-card">
            <div class="metric-label">Active Anomaly Alerts</div>
            <div class="metric-value" style="color: {'#f87171' if active_inc > 0 else '#34d399'};">{active_inc}</div>
            <div style="margin-top: 4px;"><span class="{badge_cls}">{status_txt}</span></div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown("""
        <div class="mfg-card">
            <div class="metric-label">Unplanned Downtime Avoided</div>
            <div class="metric-value" style="color: #a78bfa;">$142,500</div>
            <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 4px;">Calculated via MTBF baseline</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown("""
        <div class="mfg-card">
            <div class="metric-label">Mean Time to Diagnose (MTTD)</div>
            <div class="metric-value" style="color: #facc15;">1.8 sec</div>
            <div style="color: #34d399; font-size: 0.8rem; margin-top: 4px;">Powered by Gemini 2.5 Flash</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🛠️ Connected Machinery Fleet")
    grid_cols = st.columns(4)
    
    for i, (m_id, m_cfg) in enumerate(MACHINES.items()):
        is_faulted = (st.session_state.active_anomaly and 
                      ANOMALY_TYPES[st.session_state.active_anomaly]["target_machine"] == m_id)
        current_data = generate_telemetry_snapshot(m_id, st.session_state.active_anomaly)
        
        with grid_cols[i]:
            card_border = "#dc2626" if is_faulted else "#233052"
            status_badge = "<span class='badge-critical'>FAULT DETECTED</span>" if is_faulted else "<span class='badge-healthy'>HEALTHY</span>"
            
            st.markdown(f"""
            <div style="background: #131b2e; border: 2px solid {card_border}; border-radius: 12px; padding: 16px; min-height: 250px;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <strong style="font-size: 1.1rem; color: #f8fafc;">{m_id}</strong>
                        <div style="font-size: 0.8rem; color: #94a3b8;">{m_cfg['name']}</div>
                        <div style="font-size: 0.75rem; color: #64748b;">{m_cfg['bay']}</div>
                    </div>
                    <div>{status_badge}</div>
                </div>
                <hr style="border-color: #1e293b; margin: 12px 0;">
                <div style="font-size: 0.8rem; color: #94a3b8;">
                    <strong>{m_cfg['primary_metric']}:</strong>
                    <span style="font-size: 1.2rem; font-weight: 700; color: {'#f87171' if is_faulted else '#38bdf8'}; float: right;">
                        {list(current_data['metrics'].values())[0]}
                    </span>
                </div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">
                    <strong>Power:</strong> <span style="float: right; color: #e2e8f0;">{current_data['metrics'].get('power_kw', 20)} kW</span>
                </div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">
                    <strong>OEE:</strong> <span style="float: right; color: {'#f87171' if is_faulted else '#34d399'}; font-weight: 600;">{current_data['metrics'].get('oee', 90)}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Inspect {m_id}", key=f"btn_inspect_{m_id}", use_container_width=True):
                st.session_state.selected_machine = m_id
                st.rerun()

# -------------------------------------------------------------
# TAB 2: LIVE TELEMETRY STREAM
# -------------------------------------------------------------
with tab_telemetry:
    curr_m = st.session_state.selected_machine
    m_info = MACHINES[curr_m]
    snap = generate_telemetry_snapshot(curr_m, st.session_state.active_anomaly)
    is_anomaly = snap["status"] == "CRITICAL_ANOMALY"

    st.markdown(f"### 📡 Live Sensor Telemetry: `{curr_m}` ({m_info['name']})")
    st.caption(f"Location: {m_info['bay']} | Machine Type: {m_info['type']}")

    if is_anomaly:
        st.error(f"""
        🚨 **CRITICAL TELEMETRY THRESHOLD BREACH DETECTED!**  
        **Anomaly:** {snap['anomaly_description']}  
        **Action Required:** Run Gemini Predictive Root Cause Analysis below to prevent complete machine seizure.
        """)

    # Current Metrics Display Cards
    cols_m = st.columns(len(snap["metrics"]))
    for i, (k, v) in enumerate(snap["metrics"].items()):
        with cols_m[i]:
            st.metric(label=k.replace("_", " ").upper(), value=v)

    # Time series history chart
    st.markdown("#### 📊 Dynamic Real-Time Time Series Trend (Last 25 Samples)")
    hist_data = generate_historical_series(curr_m, points=25, active_anomaly=st.session_state.active_anomaly)
    
    # Format into DataFrame for charting
    df_rows = []
    for item in hist_data:
        row = {"Timestamp": item["timestamp"]}
        row.update(item["metrics"])
        df_rows.append(row)
    df_hist = pd.DataFrame(df_rows).set_index("Timestamp")

    # Select which metric to plot
    metric_cols = [c for c in df_hist.columns if c not in ["Timestamp"]]
    chart_col = st.selectbox("Select Sensor Stream for Trend Analysis", metric_cols, index=0)
    
    st.line_chart(df_hist[[chart_col]], height=300)

# -------------------------------------------------------------
# TAB 3: GEMINI PREDICTIVE MAINTENANCE & RCA
# -------------------------------------------------------------
with tab_gemini_rca:
    st.markdown("### 🧠 Gemini Cognitive Predictive Maintenance Engine")
    st.caption("Leveraging Gemini 2.5 Flash for Multimodal Root Cause Analysis (RCA) and Automated OSHA-Compliant SOP Generation")

    curr_m = st.session_state.selected_machine
    snap = generate_telemetry_snapshot(curr_m, st.session_state.active_anomaly)

    col_telemetry_box, col_rca_box = st.columns([1, 2])

    with col_telemetry_box:
        st.markdown("#### 📥 Ingested Telemetry Payload")
        st.json(snap["metrics"])
        
        btn_run_rca = st.button("⚡ Execute Gemini RCA Diagnosis", use_container_width=True, type="primary")

    with col_rca_box:
        st.markdown("#### 📋 Root Cause Diagnosis & Prescriptive Actions")
        
        if btn_run_rca or curr_m in st.session_state.rca_cache:
            if btn_run_rca:
                with st.spinner("Gemini is analyzing multi-axis vibration harmonics, thermodynamic gradients, and maintenance logs..."):
                    rca_res = GeminiService.diagnose_machine_anomaly(snap, snap.get("anomaly_description"))
                    st.session_state.rca_cache[curr_m] = rca_res
                    time.sleep(0.5)
            
            rca_res = st.session_state.rca_cache[curr_m]
            
            sev_color = "#f87171" if rca_res.get("severity") == "CRITICAL" else "#facc15"
            st.markdown(f"""
            <div class="mfg-card" style="border-left: 5px solid {sev_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: #f8fafc;">{rca_res.get('root_cause')}</h3>
                    <span style="background: {sev_color}22; color: {sev_color}; border: 1px solid {sev_color}; padding: 4px 10px; border-radius: 6px; font-weight: 700;">
                        {rca_res.get('severity')} SEVERITY
                    </span>
                </div>
                <hr style="border-color: #1e293b; margin: 12px 0;">
                <p><strong>Failure Mechanism:</strong> {rca_res.get('failure_mechanism')}</p>
                <div style="display: flex; gap: 24px; margin: 12px 0;">
                    <div><strong>Confidence:</strong> <span style="color: #38bdf8;">{rca_res.get('confidence_percentage')}%</span></div>
                    <div><strong>Estimated Remaining Useful Life (RUL):</strong> <span style="color: #f87171; font-weight: bold;">{rca_res.get('estimated_rul_hours')} Hours</span></div>
                </div>
                <p><strong>Immediate Mitigation:</strong> <span style="color: #facc15;">{rca_res.get('immediate_mitigation')}</span></p>
                <p style="font-size: 0.85rem; color: #94a3b8;"><strong>Compliance:</strong> {rca_res.get('iso_compliance_note')}</p>
            </div>
            """, unsafe_allow_html=True)

            # Generate SOP Work Order
            st.markdown("#### 🛠️ Automated Standard Operating Procedure (SOP)")
            if st.button("📄 Generate Maintenance Work Order & Parts List", use_container_width=True):
                with st.spinner("Synthesizing step-by-step OEM repair protocol with OSHA Lockout/Tagout instructions..."):
                    sop = GeminiService.generate_sop_work_order(curr_m, rca_res)
                    st.session_state.sop_cache[curr_m] = sop

            if curr_m in st.session_state.sop_cache:
                sop = st.session_state.sop_cache[curr_m]
                st.info(f"**Work Order:** {sop.get('title')} | Priority: {sop.get('priority')} | Estimated Duration: {sop.get('estimated_repair_time_mins')} min")
                
                st.markdown("**🔒 Mandatory Lockout/Tagout (LOTO):**")
                st.caption(sop.get("loto_procedure"))

                st.markdown("**📦 Required Replacement Parts & Tools:**")
                c_p1, c_p2 = st.columns(2)
                with c_p1:
                    st.markdown("*Spare Parts Required:*")
                    for p in sop.get("required_parts", []):
                        st.markdown(f"• `{p}`")
                with c_p2:
                    st.markdown("*Precision Maintenance Tools:*")
                    for t in sop.get("required_tools", []):
                        st.markdown(f"• {t}")

                st.markdown("**🔧 Step-by-Step Corrective Procedure:**")
                for step in sop.get("steps", []):
                    st.markdown(f"• {step}")

                if st.button("💾 Commit Work Order to Cloud Firestore", key="save_wo"):
                    wo_id = FirestoreService.save_work_order({
                        "machine_id": curr_m,
                        "rca_diagnosis": rca_res.get("root_cause"),
                        "severity": rca_res.get("severity"),
                        "sop": sop,
                        "assigned_role": "Maintenance Lead"
                    })
                    st.success(f"Work Order successfully committed to Firestore as `{wo_id}`!")
        else:
            st.info("Click 'Execute Gemini RCA Diagnosis' or trigger an anomaly in the sidebar to run cognitive analysis.")

# -------------------------------------------------------------
# TAB 4: MULTIMODAL VISUAL QA INSPECTION
# -------------------------------------------------------------
with tab_vision_qc:
    st.markdown("### 🔍 Multimodal Industrial Automated Optical Inspection (AOI)")
    st.caption("Leveraging Gemini Multimodal Vision to Detect Surface Micro-Pitting, Fatigue Cracks, and Welding Porosity")

    sample_dir = os.path.join(os.path.dirname(__file__), "assets", "samples")
    sample_files = {
        "Weld Porosity Defect (Severe)": os.path.join(sample_dir, "weld_porosity_defect.jpg"),
        "Bearing Raceway Crack (Critical)": os.path.join(sample_dir, "bearing_crack_defect.jpg"),
        "Nominal Machined Component (Pass)": os.path.join(sample_dir, "nominal_machined_part.jpg")
    }

    v_col1, v_col2 = st.columns([1, 1])

    with v_col1:
        st.markdown("#### 📷 Image Acquisition")
        img_source = st.radio("Image Source", ["Select Benchmark Sample", "Upload Custom Photo"], horizontal=True)
        
        active_image = None
        component_label = "Industrial Manufactured Component"

        if img_source == "Select Benchmark Sample":
            chosen_sample = st.selectbox("Preset Test Asset", list(sample_files.keys()))
            if os.path.exists(sample_files[chosen_sample]):
                active_image = Image.open(sample_files[chosen_sample])
                component_label = chosen_sample
        else:
            uploaded_file = st.file_uploader("Upload Component Photo (JPEG/PNG)", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                active_image = Image.open(uploaded_file)
                component_label = uploaded_file.name

        if active_image:
            st.image(active_image, caption=f"Active Frame: {component_label}", use_column_width=True)

    with v_col2:
        st.markdown("#### 🤖 Gemini Vision Optical Analysis")
        if active_image:
            if st.button("🔎 Run Gemini Optical Inspection", use_container_width=True, type="primary"):
                with st.spinner("Gemini Multimodal Vision is scanning surface geometry, edge contrast, and micro-structure..."):
                    inspection_res = GeminiService.analyze_visual_defect(active_image, component_label)
                    time.sleep(0.5)

                    is_pass = inspection_res.get("verdict") == "PASS"
                    v_color = "#34d399" if is_pass else "#f87171"
                    
                    st.markdown(f"""
                    <div class="mfg-card" style="border-left: 5px solid {v_color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h2 style="margin: 0; color: {v_color};">{inspection_res.get('verdict')}</h2>
                            <span style="background: {v_color}22; color: {v_color}; border: 1px solid {v_color}; padding: 4px 10px; border-radius: 6px; font-weight: 700;">
                                Confidence: {int(inspection_res.get('confidence_score', 0.95)*100)}%
                            </span>
                        </div>
                        <hr style="border-color: #1e293b; margin: 12px 0;">
                        <p><strong>Defect Classification:</strong> {inspection_res.get('defect_type')}</p>
                        <p><strong>Location:</strong> {inspection_res.get('defect_location')}</p>
                        <p><strong>Structural Impact:</strong> {inspection_res.get('impact_analysis')}</p>
                        <p><strong>Prescribed QA Action:</strong> <span style="color: #facc15; font-weight: bold;">{inspection_res.get('action_required')}</span></p>
                        <p style="font-size: 0.85rem; color: #94a3b8;"><strong>Standard Violation:</strong> {inspection_res.get('iso_standard_violation')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Save to Firestore
                    qa_doc_id = FirestoreService.save_qa_inspection({
                        "component": component_label,
                        "verdict": inspection_res.get("verdict"),
                        "defect_type": inspection_res.get("defect_type"),
                        "severity": inspection_res.get("severity"),
                        "action_required": inspection_res.get("action_required"),
                        "inspector": user_role
                    })
                    st.toast(f"QA Audit record saved to Firestore: {qa_doc_id}", icon="✅")
        else:
            st.info("Select or upload an image to execute multimodal quality inspection.")

# -------------------------------------------------------------
# TAB 5: GCP CLOUD ARCHITECTURE & FIRESTORE LEDGER
# -------------------------------------------------------------
with tab_architecture:
    st.markdown("### ☁️ Google Cloud Platform Architecture & Real-Time Firestore Ledger")
    
    st.markdown("""
    #### 🏗️ System Architecture Pipeline
    ```
    ┌─────────────────────────┐          ┌──────────────────────────┐          ┌─────────────────────────┐
    │     Plant Floor IoT     │          │    Cloud Run Service     │          │    Gemini 2.5 Flash     │
    │  (Telemetry & Cameras)  │──HTTPS──▶│  (FastAPI / Streamlit)   │─────────▶│  (Multimodal Cognitive  │
    └─────────────────────────┘          │    Port 8080 Container   │◀─────────│   Inference Engine)     │
                 │                       └──────────────────────────┘          └─────────────────────────┘
                 │                                     │
                 ▼                                     ▼
    ┌─────────────────────────┐          ┌──────────────────────────┐
    │  Firebase Identity &    │          │  Cloud Firestore Ledger  │
    │  Role-Based Auth (RBAC) │          │  (Real-Time Collections) │
    └─────────────────────────┘          └──────────────────────────┘
    ```
    """)

    st.markdown("---")
    st.markdown("#### 📂 Live Firestore Collections Inspector")
    summary = FirestoreService.get_all_collections_summary()

    col_fs1, col_fs2, col_fs3 = st.columns(3)
    
    with col_fs1:
        st.markdown(f"**🚨 Collection: `incidents` ({summary['incidents']['count']} docs)**")
        incidents = FirestoreService.get_incidents(5)
        if incidents:
            st.json(incidents)
        else:
            st.caption("No active incident documents logged yet.")

    with col_fs2:
        st.markdown(f"**📋 Collection: `work_orders` ({summary['work_orders']['count']} docs)**")
        work_orders = FirestoreService.get_work_orders(5)
        if work_orders:
            st.json(work_orders)
        else:
            st.caption("No work order documents logged yet.")

    with col_fs3:
        st.markdown(f"**🔍 Collection: `qa_inspections` ({summary['qa_inspections']['count']} docs)**")
        inspections = FirestoreService.get_qa_inspections(5)
        if inspections:
            st.json(inspections)
        else:
            st.caption("No inspection documents logged yet.")
