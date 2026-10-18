# ApexMfg AI — Intelligent Operations & Industrial Efficiency Platform

[![Google Cloud Run](https://img.shields.io/badge/Deployed%20on-Google%20Cloud%20Run-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![Cloud Firestore](https://img.shields.io/badge/Database-Cloud%20Firestore-FFA611?logo=firebase&logoColor=white)](https://firebase.google.com/docs/firestore)
[![Gemini 2.5](https://img.shields.io/badge/AI%20Core-Gemini%202.5%20Flash-8E75C2?logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Firebase Auth](https://img.shields.io/badge/Identity-Firebase%20Auth-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **Submission for Google Cloud & Gemini AI Challenge**  
> **Challenge Track:** *Manufacturing: Intelligent Operations & Industrial Efficiency*  
> **Live Cloud Run Prototype:** `https://apexmfg-ai-<hash>-uc.a.run.app` *(Replace with deployed URL)*  
> **Pitch Deck PDF:** [ApexMfg_AI_Pitch_Deck.pdf](./ApexMfg_AI_Pitch_Deck.pdf) *(< 5 MB)*  

---

## 🏭 Executive Summary

In modern industrial manufacturing, an hour of unplanned machine downtime costs upwards of **$260,000**. Maintenance technicians are bombarded with raw IoT sensor data and forced to manually comb through 500-page OEM manuals while production lines sit idle.

**ApexMfg AI** is an end-to-end intelligent operations platform and industrial copilot engineered to eliminate unplanned downtime, automate root-cause diagnosis on the factory floor, and optimize production throughput in real time.

---

## ⚡ How Google Cloud & Gemini are Leveraged

| Google Cloud Technology | Implementation & Operational Role |
| :--- | :--- |
| **Gemini (Gemini 2.5 Flash / Pro)** | **Cognitive Intelligence Engine:** Performs sub-second Root Cause Analysis (RCA) on multi-axis telemetry anomalies, calculates Remaining Useful Life (RUL), synthesizes OSHA-compliant Lockout/Tagout (LOTO) repair SOPs, and inspects camera feeds using multimodal vision to flag micro-defects and ISO violations. |
| **Google Cloud Run** | **Serverless Container Backend:** Hosts our containerized high-performance industrial copilot on port `8080`. Offers sub-second cold starts, automatic scaling based on IoT telemetry volume, and 99.99% enterprise uptime. |
| **Cloud Firestore** | **Real-Time Operational Ledger:** Serves as the distributed NoSQL database storing live telemetry snapshots, active threshold incidents, Gemini-generated maintenance work orders, and visual optical inspection audit records with sub-second synchronization. |
| **Firebase** | **Application Identity & RBAC:** Enforces Role-Based Access Control (RBAC) across Maintenance Engineers, Plant Operations Managers, and Quality Assurance Inspectors, securing machine write permissions and work order dispatches. |

---

## 🏗️ System Architecture

```
                                      ┌────────────────────────────────┐
                                      │   Gemini 2.5 Flash / Pro AI    │
                                      │  • Multi-Harmonic RCA          │
                                      │  • Remaining Useful Life (RUL) │
                                      │  • Multimodal Optical AOI      │
                                      └────────────────────────────────┘
                                                       ▲
                                                       │ (Multimodal Ingest)
                                                       ▼
┌─────────────────────────┐          ┌─────────────────────────────────┐          ┌─────────────────────────┐
│     Plant Floor IoT     │          │        Google Cloud Run         │          │     Cloud Firestore     │
│   Vibration / Heat /    │──HTTPS──▶│    Serverless Web & API Hub     │─────────▶│    Real-Time NoSQL DB   │
│   Hydraulics / Cameras  │          │   (Containerized Port 8080)     │◀─────────│  • incidents            │
└─────────────────────────┘          └─────────────────────────────────┘          │  • work_orders          │
             │                                         ▲                          │  • qa_inspections       │
             │                                         │                          └─────────────────────────┘
             ▼                                         │
┌─────────────────────────┐                            │
│  Firebase Authentication│────────────────────────────┘
│  • Maintenance Eng      │       (Role-Based Token Verification)
│  • Plant Manager        │
│  • QA Inspector         │
└─────────────────────────┘
```

---

## 🎯 Key Platform Features

1. **Digital Twin Fleet Overview:** Real-time operational monitoring of 4 distinct industrial machines (5-Axis CNC Mill, Hydraulic Stamping Press, Polymer Injection Molding, Robotic Seam Welder).
2. **Interactive Telemetry Anomaly Simulator:** Inject real-world failure modes (Bearing Degradation, Valve Cavitation, Thermal Runaway, Shield Gas Choke) with live sensor threshold tracking.
3. **Gemini Predictive Root Cause Analysis (RCA):** Sub-2 second cognitive analysis pinpointing physical failure mechanisms, ISO 10816 compliance breaches, and estimated hours of Remaining Useful Life (RUL).
4. **Automated SOP & Maintenance Work Orders:** Instant generation of OSHA Lockout/Tagout procedures, required precision tools, and exact replacement part SKUs committed directly to Firestore.
5. **Multimodal Automated Optical Inspection (AOI):** High-precision computer vision inspection detecting weld porosity, surface micro-cracks, and structural fatigue risks.

---

## 🚀 Quickstart & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/apex-manufacturing-ai.git
cd apex-manufacturing-ai
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Generate Benchmark Inspection Images
```bash
python generate_sample_images.py
```

### 4. (Optional) Configure Gemini API Key
```bash
# Windows PowerShell:
$env:GEMINI_API_KEY="your-api-key-here"

# Linux / macOS:
export GEMINI_API_KEY="your-api-key-here"
```
*(Note: If no API key is set, the platform operates in domain-engineered simulation mode ensuring reliable zero-crash evaluation).*

### 5. Launch the Dashboard
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ 1-Command Google Cloud Run Deployment

Deploy directly using **Google Cloud Shell** or your local terminal with `gcloud`:

```bash
# 1. Login to Google Cloud
gcloud auth login

# 2. Set your active GCP project
gcloud config set project YOUR_GCP_PROJECT_ID

# 3. Enable required Google Cloud services
gcloud services enable run.googleapis.com cloudbuild.googleapis.com firestore.googleapis.com

# 4. Deploy containerized service to Cloud Run
gcloud run deploy apexmfg-ai \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1
```

Once deployment completes, Cloud Run outputs your live service URL:
```
Service [apexmfg-ai] revision [apexmfg-ai-00001-abc] has been deployed and is serving 100 percent of traffic.
Service URL: https://apexmfg-ai-xyz-uc.a.run.app
```

---

## ⏱️ Video Demonstration Script (3 to 4 Minutes)

| Time | Phase | On-Screen Action | Script / Voiceover |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:35** | **Problem & Overview** | Show Fleet Digital Twin tab | *"In manufacturing, unplanned downtime costs over $260k per hour. Maintenance teams are overwhelmed with complex telemetry. ApexMfg AI transforms sensor chaos into immediate prescriptive intelligence."* |
| **0:35 - 1:40** | **Telemetry Anomaly & Gemini RCA** | Sidebar: Trigger `Bearing Degradation` on CNC-4001; Open Gemini RCA tab | *"On our dashboard, vibration spikes past ISO 10816 limits. We click 'Execute Gemini RCA'. Gemini analyzes multi-axis harmonics, pinpoints bearing raceway spalling with 95% confidence, and estimates 8.5 hours of Remaining Useful Life before catastrophic lockup."* |
| **1:40 - 2:30** | **Automated SOP & Firestore Commit** | Click 'Generate Work Order' and 'Commit to Cloud Firestore' | *"Instead of searching paper manuals, Gemini instantly generates an OSHA LOTO procedure and exact SKUs. One click commits the work order directly to Cloud Firestore for technician dispatch."* |
| **2:30 - 3:15** | **Multimodal Visual QA** | Tab 4: Select Weld Porosity sample; Click 'Run Gemini Optical Inspection' | *"On the quality line, an optical camera captures a weld bead. Gemini Multimodal Vision identifies cluster porosity violating ISO 5817 Level B, immediately routing the part to rework."* |
| **3:15 - 3:45** | **Architecture & Conclusion** | Tab 5: Show GCP architecture and Firestore documents | *"ApexMfg AI runs seamlessly on Google Cloud: Cloud Run handles containerized autoscaling, Firestore guarantees real-time sync, and Gemini delivers cognitive operations. Thank you."* |

---

## 📊 Pitch Deck

Our hackathon presentation deck is pre-compiled and included in the repository:
- **File:** [`ApexMfg_AI_Pitch_Deck.pdf`](./ApexMfg_AI_Pitch_Deck.pdf)
- **Size:** ~12 KB (Complying with the `< 5 MB` limit)
- **Regenerate Script:** `python generate_pitch_deck.py`

---

## 📜 License
Distributed under the MIT License. Built for the Google Cloud & Gemini AI Hackathon.
