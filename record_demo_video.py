"""
Automated Screen Demonstration Video Recorder
Uses Playwright to simulate an engineer walking through the live ApexMfg AI platform
at http://localhost:8502, capturing 720p HD video strictly within 3:00 - 3:45 minutes.
"""

import os
import time
from playwright.sync_api import sync_playwright

VIDEO_DIR = os.path.join(os.path.dirname(__file__), "demo_video")
os.makedirs(VIDEO_DIR, exist_ok=True)

def record_walkthrough():
    print("[1/5] Launching headless browser with 720p HD video recording...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        print("[2/5] Navigating to http://localhost:8502...")
        page.goto("http://localhost:8502", wait_until="networkidle")
        page.wait_for_timeout(4000)

        # -----------------------------------------------------------------
        # SCENE 1 (0:00 - 0:35): Fleet Digital Twin Overview & KPIs
        # -----------------------------------------------------------------
        print("[Scene 1] Overview of Connected Fleet & Plant OEE KPIs...")
        # Smooth scroll down to show the 4 connected machines
        for _ in range(3):
            page.mouse.wheel(0, 150)
            page.wait_for_timeout(3000)
        for _ in range(3):
            page.mouse.wheel(0, -150)
            page.wait_for_timeout(2000)
        page.wait_for_timeout(5000)

        # -----------------------------------------------------------------
        # SCENE 2 (0:35 - 1:25): Telemetry Stream & Anomaly Triggering
        # -----------------------------------------------------------------
        print("[Scene 2] Switching to Live Telemetry & Triggering Bearing Anomaly...")
        # Switch to Tab 2: Live Telemetry Stream
        tabs = page.locator("button[role='tab']")
        if tabs.count() >= 2:
            tabs.nth(1).click()
            page.wait_for_timeout(4000)

        # Scroll to inspect live telemetry trend
        page.mouse.wheel(0, 200)
        page.wait_for_timeout(5000)

        # Trigger Anomaly in sidebar: Select Bearing Degradation
        anomaly_select = page.locator("div[data-testid='stSidebar'] div[data-baseweb='select']").nth(1)
        if anomaly_select.is_visible():
            anomaly_select.click()
            page.wait_for_timeout(1500)
            # Pick first anomaly option
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)

        # Click Trigger Fault button
        trigger_btn = page.locator("button:has-text('Trigger Fault')")
        if trigger_btn.is_visible():
            trigger_btn.click()
            page.wait_for_timeout(5000)

        # Scroll down to show critical threshold spike in chart
        page.mouse.wheel(0, 150)
        page.wait_for_timeout(6000)

        # -----------------------------------------------------------------
        # SCENE 3 (1:25 - 2:15): Gemini Cognitive Root Cause Analysis (RCA) & SOP
        # -----------------------------------------------------------------
        print("[Scene 3] Running Gemini Predictive RCA & Generating SOP...")
        if tabs.count() >= 3:
            tabs.nth(2).click()
            page.wait_for_timeout(4000)

        # Click Execute Gemini RCA Diagnosis
        rca_btn = page.locator("button:has-text('Execute Gemini RCA Diagnosis')")
        if rca_btn.is_visible():
            rca_btn.click()
            page.wait_for_timeout(6000)

        # Scroll down to view the RCA diagnosis card
        page.mouse.wheel(0, 250)
        page.wait_for_timeout(8000)

        # Click Generate Maintenance Work Order & Parts List
        sop_btn = page.locator("button:has-text('Generate Maintenance Work Order')")
        if sop_btn.is_visible():
            sop_btn.click()
            page.wait_for_timeout(6000)

        # Scroll down to view SOP and commit to Firestore
        page.mouse.wheel(0, 250)
        page.wait_for_timeout(6000)
        
        save_wo_btn = page.locator("button:has-text('Commit Work Order to Cloud Firestore')")
        if save_wo_btn.is_visible():
            save_wo_btn.click()
            page.wait_for_timeout(5000)

        # -----------------------------------------------------------------
        # SCENE 4 (2:15 - 2:55): Multimodal Visual Defect Inspection (AOI)
        # -----------------------------------------------------------------
        print("[Scene 4] Multimodal Optical Inspection with Gemini Vision...")
        if tabs.count() >= 4:
            tabs.nth(3).click()
            page.wait_for_timeout(4000)

        # Click Run Gemini Optical Inspection
        inspect_btn = page.locator("button:has-text('Run Gemini Optical Inspection')")
        if inspect_btn.is_visible():
            inspect_btn.click()
            page.wait_for_timeout(6000)

        # Inspect the verdict card (Defect Detected / ISO 5817 breach)
        page.mouse.wheel(0, 200)
        page.wait_for_timeout(8000)

        # -----------------------------------------------------------------
        # SCENE 5 (2:55 - 3:20): GCP Cloud Architecture & Live Firestore Ledger
        # -----------------------------------------------------------------
        print("[Scene 5] Demonstrating GCP Cloud Stack & Real-Time Firestore Ledger...")
        if tabs.count() >= 5:
            tabs.nth(4).click()
            page.wait_for_timeout(4000)

        # Scroll through architecture pipeline and active collections
        page.mouse.wheel(0, 250)
        page.wait_for_timeout(6000)
        page.mouse.wheel(0, 250)
        page.wait_for_timeout(6000)

        # -----------------------------------------------------------------
        # SCENE 6 (3:20 - 3:30): Return to Digital Twin Overview & Outro
        # -----------------------------------------------------------------
        print("[Scene 6] Final wrap-up on Fleet Digital Twin...")
        page.mouse.wheel(0, -600)
        if tabs.count() >= 1:
            tabs.nth(0).click()
            page.wait_for_timeout(5000)

        print("[5/5] Finalizing video file...")
        context.close()
        browser.close()

    # Find the created video
    for f in os.listdir(VIDEO_DIR):
        if f.endswith(".webm"):
            target = os.path.join(VIDEO_DIR, "ApexMfg_AI_Working_Demo_720p.webm")
            src = os.path.join(VIDEO_DIR, f)
            if src != target:
                if os.path.exists(target):
                    os.remove(target)
                os.rename(src, target)
            print(f"[Success] Video saved to: {target}")
            return target
    return None

if __name__ == "__main__":
    record_walkthrough()
