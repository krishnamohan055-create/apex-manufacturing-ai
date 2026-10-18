"""
Generates high-resolution graphical assets for the ApexMfg AI Technical Architecture Document.
All graphics are rendered at 300 DPI with anti-aliasing.
"""

import os
from PIL import Image, ImageDraw

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def generate_system_architecture_diagram():
    """Generates a high-res (1600x920) system architecture graphic."""
    w, h = 1600, 920
    im = Image.new("RGB", (w, h), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)

    # Background subtle grid pattern
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=(18, 24, 38), width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=(18, 24, 38), width=1)

    # Top Title Bar
    draw_rounded_rect(draw, (40, 30, w - 40, 95), 10, fill=(19, 27, 46), outline=(2, 132, 199), width=2)
    draw.text((60, 45), "APEXMFG AI  —  END-TO-END INDUSTRIAL OPERATIONS & GCP ARCHITECTURE", fill=(56, 189, 248))
    draw.text((60, 70), "Production Pipeline: Shop-Floor Edge IoT -> Google Cloud Run -> Cloud Firestore -> Gemini 2.5 Cognitive Engine", fill=(148, 163, 184))

    # Column 1: Shop-Floor Edge IoT
    draw_rounded_rect(draw, (40, 130, 380, 860), 14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    draw_rounded_rect(draw, (55, 145, 365, 195), 8, fill=(30, 41, 59))
    draw.text((70, 160), "1. FACTORY-FLOOR IOT EDGE", fill=(248, 250, 252))

    devices = [
        ("CNC-4001 (5-Axis Mill)", "Spindle vibration (mm/s), motor RPM, spindle load %"),
        ("HYD-1020 (Heavy Press)", "System hydraulic line pressure (bar), oil temp (°C)"),
        ("INJ-880 (Injection Cell)", "Zone 2 barrel temp (°C), injection backpressure"),
        ("ROB-W05 (Welder)", "Shielding argon flow (L/min), arc tip temp (°C)"),
        ("Optical AOI Cameras", "High-res weld bead & bearing surface image capture")
    ]
    for idx, (title, sub) in enumerate(devices):
        top_y = 220 + idx * 125
        draw_rounded_rect(draw, (55, top_y, 365, top_y + 105), 8, fill=(19, 27, 46), outline=(35, 48, 82), width=1)
        draw.text((70, top_y + 15), title, fill=(56, 189, 248))
        draw.text((70, top_y + 40), sub, fill=(148, 163, 184))
        draw.text((70, top_y + 70), "Protocol: MQTT / HTTPS / OPC-UA", fill=(52, 211, 153))

    # Arrows 1 -> 2
    for y_arrow in [300, 500, 700]:
        draw.line([(380, y_arrow), (450, y_arrow)], fill=(2, 132, 199), width=4)
        draw.polygon([(465, y_arrow), (445, y_arrow - 8), (445, y_arrow + 8)], fill=(2, 132, 199))

    # Column 2: Google Cloud Run Core Hub
    draw_rounded_rect(draw, (460, 130, 860, 860), 14, fill=(15, 23, 42), outline=(2, 132, 199), width=3)
    draw_rounded_rect(draw, (475, 145, 845, 195), 8, fill=(2, 132, 199))
    draw.text((490, 160), "2. GOOGLE CLOUD RUN (PORT 8080)", fill=(255, 255, 255))

    run_modules = [
        ("FastAPI / Streamlit Core Hub", "Containerized microservice processing real-time telemetry\nand serving operator UI at low latency."),
        ("Edge Anomaly Detection Engine", "Evaluates multi-axis sensor streams against ISO 10816\nand triggers immediate incident alerts upon breach."),
        ("Cognitive AI Orchestrator", "Constructs prompt context from live telemetry and invokes\nGemini 2.5 Flash with structured Pydantic schemas."),
        ("Zero-Crash Dual Mode Handler", "Automatically negotiates live Google Cloud Firestore vs\nlocal real-time memory fallback sync."),
        ("Healthcheck & Auto-Scaling Probes", "Responds to /_stcore/health probes. Scales from 0 to N\ninstances based on incoming plant telemetry load.")
    ]
    for idx, (title, sub) in enumerate(run_modules):
        top_y = 220 + idx * 125
        draw_rounded_rect(draw, (475, top_y, 845, top_y + 105), 8, fill=(19, 27, 46), outline=(35, 48, 82), width=1)
        draw.text((490, top_y + 15), title, fill=(248, 250, 252))
        draw.text((490, top_y + 40), sub, fill=(148, 163, 184))

    # Arrows 2 -> 3
    draw.line([(860, 320), (940, 320)], fill=(168, 85, 247), width=4)
    draw.polygon([(955, 320), (935, 312), (935, 328)], fill=(168, 85, 247))

    draw.line([(860, 680), (940, 680)], fill=(245, 158, 11), width=4)
    draw.polygon([(955, 680), (935, 672), (935, 688)], fill=(245, 158, 11))

    # Column 3 Top: Gemini 2.5 Cognitive Engine
    draw_rounded_rect(draw, (950, 130, 1560, 480), 14, fill=(15, 23, 42), outline=(168, 85, 247), width=2)
    draw_rounded_rect(draw, (965, 145, 1545, 195), 8, fill=(126, 34, 206))
    draw.text((980, 160), "3A. GOOGLE GEMINI 2.5 COGNITIVE CORE", fill=(255, 255, 255))

    gemini_features = [
        ("Multi-Axis Predictive RCA", "Harmonic vibration + thermodynamics -> Pinpoints spalling raceway (95% confidence)."),
        ("Remaining Useful Life (RUL)", "Physical degradation modeling calculates exact countdown to machine seizure (e.g. 8.5 hrs)."),
        ("OSHA SOP & LOTO Synthesis", "Generates Lockout/Tagout steps, required tools, and exact replacement part SKUs."),
        ("Multimodal Vision AOI", "Analyzes camera feeds to detect weld porosity, micro-cracks, and ISO 5817 non-compliance.")
    ]
    for idx, (title, sub) in enumerate(gemini_features):
        top_y = 215 + idx * 62
        draw_rounded_rect(draw, (965, top_y, 1545, top_y + 54), 6, fill=(19, 27, 46), outline=(45, 35, 75), width=1)
        draw.text((980, top_y + 10), title, fill=(192, 132, 252))
        draw.text((980, top_y + 30), sub, fill=(148, 163, 184))

    # Column 3 Bottom: Cloud Firestore & Firebase Auth
    draw_rounded_rect(draw, (950, 510, 1560, 860), 14, fill=(15, 23, 42), outline=(245, 158, 11), width=2)
    draw_rounded_rect(draw, (965, 525, 1545, 575), 8, fill=(180, 83, 9))
    draw.text((980, 540), "3B. CLOUD FIRESTORE & FIREBASE IDENTITY LAYER", fill=(255, 255, 255))

    fs_features = [
        ("Collection: 'incidents'", "Real-time records of threshold breaches, severity, and active machine alarms."),
        ("Collection: 'work_orders'", "Gemini-synthesized SOPs, LOTO safety checklists, and technician dispatches."),
        ("Collection: 'qa_inspections'", "Multimodal visual audit logs, defect locations, and batch quarantine tags."),
        ("Firebase RBAC Identity", "JWT cryptographically secures roles: Maintenance Lead, Plant Manager, QA Inspector.")
    ]
    for idx, (title, sub) in enumerate(fs_features):
        top_y = 595 + idx * 62
        draw_rounded_rect(draw, (965, top_y, 1545, top_y + 54), 6, fill=(19, 27, 46), outline=(55, 45, 25), width=1)
        draw.text((980, top_y + 10), title, fill=(251, 191, 36))
        draw.text((980, top_y + 30), sub, fill=(148, 163, 184))

    output_path = os.path.join(ASSETS_DIR, "system_architecture_diagram.png")
    im.save(output_path, "PNG", dpi=(300, 300))
    print(f"[Success] Generated high-res architecture diagram at: {output_path}")

def generate_rul_chart():
    """Generates a high-res RUL degradation curve with ISO 10816 zones."""
    w, h = 1200, 600
    im = Image.new("RGB", (w, h), color=(15, 23, 42))
    draw = ImageDraw.Draw(im)

    draw.text((40, 30), "VIBRATION SEVERITY & REMAINING USEFUL LIFE (RUL) DEGRADATION CURVE", fill=(56, 189, 248))
    draw.text((40, 55), "ISO 10816-3 Mechanical Vibration Standards vs Gemini Predictive Anomaly Trigger", fill=(148, 163, 184))

    pad_x, pad_y = 90, 100
    gw, gh = w - 180, h - 200

    y_base = pad_y + gh
    y_zoneA = y_base - (1.8 / 7.0) * gh
    y_zoneB = y_base - (2.8 / 7.0) * gh
    y_zoneC = y_base - (4.5 / 7.0) * gh
    y_zoneD = pad_y

    draw.rectangle([pad_x, y_zoneA, pad_x + gw, y_base], fill=(16, 185, 129), outline=(5, 150, 105))
    draw.text((pad_x + 15, y_base - 35), "ZONE A: GOOD (Nominal Spindle Operation < 1.8 mm/s)", fill=(255, 255, 255))

    draw.rectangle([pad_x, y_zoneB, pad_x + gw, y_zoneA], fill=(37, 99, 235), outline=(29, 78, 216))
    draw.text((pad_x + 15, y_zoneA - 35), "ZONE B: SATISFACTORY (Acceptable Long-Term Run)", fill=(255, 255, 255))

    draw.rectangle([pad_x, y_zoneC, pad_x + gw, y_zoneB], fill=(217, 119, 6), outline=(180, 83, 9))
    draw.text((pad_x + 15, y_zoneB - 35), "ZONE C: RESTRICTED OPERATION (Maintenance Scheduled)", fill=(255, 255, 255))

    draw.rectangle([pad_x, y_zoneD, pad_x + gw, y_zoneC], fill=(220, 38, 38), outline=(185, 28, 28))
    draw.text((pad_x + 15, y_zoneC - 35), "ZONE D: DAMAGE INCURRED (Gemini Predictive Anomaly Trigger > 4.5 mm/s)", fill=(255, 255, 255))

    points = []
    for step in range(101):
        x = pad_x + (step / 100.0) * gw
        progress = step / 100.0
        vib = 1.3 + 0.5 * progress + 4.4 * (progress ** 4.5)
        y = y_base - (vib / 7.0) * gh
        points.append((x, y))

    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(255, 255, 255), width=4)

    trig_x, trig_y = points[75]
    draw.ellipse([trig_x - 10, trig_y - 10, trig_x + 10, trig_y + 10], fill=(239, 68, 68), outline=(255, 255, 255), width=2)
    draw.line([(trig_x, trig_y), (trig_x + 120, trig_y - 40)], fill=(239, 68, 68), width=2)
    draw_rounded_rect(draw, (trig_x + 120, trig_y - 65, trig_x + 380, trig_y - 15), 6, fill=(19, 27, 46), outline=(239, 68, 68), width=2)
    draw.text((trig_x + 130, trig_y - 48), "GEMINI RCA TRIGGER: 8.5h RUL Left", fill=(248, 113, 113))

    draw.text((pad_x, h - 75), "T - 30 Days (Nominal Run)", fill=(148, 163, 184))
    draw.text((pad_x + gw * 0.5, h - 75), "T - 7 Days (Micro-spall Initiation)", fill=(148, 163, 184))
    draw.text((pad_x + gw * 0.85, h - 75), "T = 0 (Total Seizure)", fill=(248, 113, 113))

    output_path = os.path.join(ASSETS_DIR, "rul_degradation_chart.png")
    im.save(output_path, "PNG", dpi=(300, 300))
    print(f"[Success] Generated RUL chart at: {output_path}")

def generate_dashboard_preview():
    """Generates a high-res graphic preview of the live Fleet Digital Twin Dashboard UI."""
    w, h = 1400, 750
    im = Image.new("RGB", (w, h), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)

    # Header bar
    draw_rounded_rect(draw, (20, 20, w - 20, 90), 8, fill=(19, 27, 46), outline=(35, 48, 82))
    draw.text((40, 35), "ApexMfg AI | Intelligent Industrial Operations Hub", fill=(248, 250, 252))
    draw.text((40, 60), "Real-Time Digital Twin Fleet  •  Connected to Cloud Run & Cloud Firestore", fill=(56, 189, 248))
    draw.text((w - 380, 48), "STACK: Cloud Run | Firestore | Gemini 2.5", fill=(52, 211, 153))

    # 4 KPI cards
    kpi_titles = ["PLANT OVERALL OEE", "ACTIVE ANOMALY ALERTS", "UNPLANNED DOWNTIME AVOIDED", "MEAN TIME TO DIAGNOSE"]
    kpi_vals = ["88.6%", "1 CRITICAL", "$142,500", "1.8 SEC"]
    kpi_colors = [(52, 211, 153), (248, 113, 113), (167, 139, 250), (250, 204, 21)]

    card_w = (w - 100) // 4
    for i in range(4):
        cx = 20 + i * (card_w + 20)
        draw_rounded_rect(draw, (cx, 110, cx + card_w, 200), 8, fill=(19, 27, 46), outline=(35, 48, 82))
        draw.text((cx + 15, 125), kpi_titles[i], fill=(148, 163, 184))
        draw.text((cx + 15, 150), kpi_vals[i], fill=kpi_colors[i])

    # 4 Machine fleet cards
    m_ids = ["CNC-4001", "HYD-1020", "INJ-880", "ROB-W05"]
    m_names = ["5-Axis CNC Mill", "Hydraulic Stamping", "Injection Molding", "Robotic Seam Welder"]
    m_statuses = ["CRITICAL FAULT", "HEALTHY", "HEALTHY", "HEALTHY"]
    m_colors = [(239, 68, 68), (16, 185, 129), (16, 185, 129), (16, 185, 129)]
    m_metrics = ["Vibration: 5.85 mm/s (Breach)", "Pressure: 210 bar (Nominal)", "Barrel: 220°C (Nominal)", "Tip: 315°C (Nominal)"]

    for i in range(4):
        cx = 20 + i * (card_w + 20)
        border_col = m_colors[i] if i == 0 else (35, 48, 82)
        draw_rounded_rect(draw, (cx, 220, cx + card_w, 420), 10, fill=(15, 23, 42), outline=border_col, width=2)
        draw.text((cx + 15, 235), m_ids[i], fill=(248, 250, 252))
        draw.text((cx + 15, 260), m_names[i], fill=(148, 163, 184))
        draw_rounded_rect(draw, (cx + card_w - 145, 235, cx + card_w - 15, 265), 6, fill=m_colors[i])
        draw.text((cx + card_w - 135, 243), m_statuses[i], fill=(255, 255, 255))
        draw.line([(cx + 15, 290), (cx + card_w - 15, 290)], fill=(30, 41, 59))
        draw.text((cx + 15, 305), m_metrics[i], fill=m_colors[i])
        draw.text((cx + 15, 335), "Power: 28 kW | OEE: 62.4%", fill=(148, 163, 184))
        draw_rounded_rect(draw, (cx + 15, 370, cx + card_w - 15, 405), 6, fill=(2, 132, 199))
        draw.text((cx + 35, 382), "RUN GEMINI DIAGNOSIS", fill=(255, 255, 255))

    # Bottom Gemini RCA output box
    draw_rounded_rect(draw, (20, 440, w - 20, 720), 10, fill=(19, 27, 46), outline=(239, 68, 68), width=2)
    draw.text((40, 455), "GEMINI 2.5 FLASH ROOT CAUSE ANALYSIS & PRESCRIPTIVE SOP (CNC-4001)", fill=(248, 113, 113))
    draw.line([(40, 485), (w - 40, 485)], fill=(35, 48, 82))
    draw.text((40, 500), "DIAGNOSIS: Spindle Bearing Outer Raceway Spalling & Micro-welding  |  CONFIDENCE: 95%  |  ESTIMATED RUL: 8.5 HOURS", fill=(56, 189, 248))
    draw.text((40, 530), "FAILURE DYNAMICS: Micro-fracture in front bearing cage inducing 4.2x harmonic vibration spike across 3.5kHz band.", fill=(226, 232, 240))
    draw.text((40, 560), "IMMEDIATE MITIGATION: Execute controlled tool retract; reduce spindle RPM to 0; initiate LOTO protocol.", fill=(250, 204, 21))
    draw.text((40, 590), "OSHA LOTO PROCEDURE: Engage Main Disconnect 3B. Attach Padlock #M-401. Verify 0V across 480V 3-phase bus.", fill=(148, 163, 184))
    draw.text((40, 620), "PARTS REQUIRED: SKF-7014-CD/P4A Angular Contact Spindle Bearing  |  Klüber NBU 15 High-Speed Grease (50g)", fill=(52, 211, 153))
    draw.text((40, 650), "STATUS: COMMITTED TO CLOUD FIRESTORE AS WORK ORDER 'WO-882194' (DISPATCHED TO MAINTENANCE LEAD)", fill=(167, 139, 250))

    output_path = os.path.join(ASSETS_DIR, "dashboard_preview.png")
    im.save(output_path, "PNG", dpi=(300, 300))
    print(f"[Success] Generated dashboard preview at: {output_path}")

if __name__ == "__main__":
    generate_system_architecture_diagram()
    generate_rul_chart()
    generate_dashboard_preview()
