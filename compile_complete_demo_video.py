"""
Broadcast-Quality Demo Video Generator
Captures all live functional states from http://localhost:8502, generates a smooth 25 FPS
walkthrough strictly timed to 3 minutes 29 seconds, and merges the audio narration track
into an official MP4 video file.
"""

import os
import subprocess
import cv2
import numpy as np
from PIL import Image
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(__file__)
SCENES_DIR = os.path.join(BASE_DIR, "video_scenes")
DEMO_DIR = os.path.join(BASE_DIR, "demo_video")
AUDIO_PATH = os.path.join(BASE_DIR, "assets", "ApexMfg_AI_Demo_Voiceover.mp3")
RAW_VIDEO_PATH = os.path.join(DEMO_DIR, "temp_video_stream.mp4")
FINAL_MP4_PATH = os.path.join(DEMO_DIR, "ApexMfg_AI_Official_Demo.mp4")

os.makedirs(SCENES_DIR, exist_ok=True)
os.makedirs(DEMO_DIR, exist_ok=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def capture_scenes():
    print("[1/3] Capturing full high-res live application states...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("http://localhost:8502", wait_until="networkidle")
        page.wait_for_timeout(3000)

        # 1. Fleet Overview Top
        page.screenshot(path=os.path.join(SCENES_DIR, "s1_kpis.png"))
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SCENES_DIR, "s1_fleet.png"))

        # 2. Live Telemetry
        page.mouse.wheel(0, -300)
        page.get_by_text("Live Telemetry").first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(SCENES_DIR, "s2_telemetry_normal.png"))

        # Trigger Anomaly
        trigger_btn = page.locator("button:has-text('Trigger Fault')")
        if trigger_btn.is_visible():
            trigger_btn.click()
            page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCENES_DIR, "s2_telemetry_alert.png"))
        page.mouse.wheel(0, 260)
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SCENES_DIR, "s2_telemetry_chart.png"))

        # 3. Gemini Predictive RCA & SOP
        page.mouse.wheel(0, -260)
        page.get_by_text("Gemini Predictive").first.click()
        page.wait_for_timeout(2000)
        rca_btn = page.locator("button:has-text('Execute Gemini RCA Diagnosis')")
        if rca_btn.is_visible():
            rca_btn.click()
            page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCENES_DIR, "s3_rca_result.png"))

        sop_btn = page.locator("button:has-text('Generate Maintenance Work Order')")
        if sop_btn.is_visible():
            sop_btn.click()
            page.wait_for_timeout(2500)
        page.mouse.wheel(0, 320)
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SCENES_DIR, "s3_sop_order.png"))

        # 4. Multimodal Visual QA
        page.mouse.wheel(0, -320)
        page.get_by_text("Multimodal Visual").first.click()
        page.wait_for_timeout(2000)
        inspect_btn = page.locator("button:has-text('Run Gemini Optical Inspection')")
        if inspect_btn.is_visible():
            inspect_btn.click()
            page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(SCENES_DIR, "s4_visual_result.png"))

        # 5. GCP Architecture & Firestore
        page.get_by_text("Firestore Ledger").first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(SCENES_DIR, "s5_architecture.png"))
        page.mouse.wheel(0, 320)
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SCENES_DIR, "s5_firestore.png"))

        # 6. Conclusion
        page.mouse.wheel(0, -320)
        page.get_by_text("Fleet Digital Twin").first.click()
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(SCENES_DIR, "s6_conclusion.png"))

        browser.close()
    print("[Success] Captured all scene assets!")

def render_video_stream():
    print("[2/3] Generating 25 FPS video stream matching 3m 29s narration (5,225 frames)...")
    fps = 25
    width, height = 1280, 720

    # Sequence of scene images with durations in seconds
    # Total = 34 + 50 + 50 + 40 + 25 + 10 = 209 seconds (matches audio duration 3:29)
    scene_schedule = [
        ("s1_kpis.png", 17),
        ("s1_fleet.png", 17),
        ("s2_telemetry_normal.png", 12),
        ("s2_telemetry_alert.png", 18),
        ("s2_telemetry_chart.png", 20),
        ("s3_rca_result.png", 25),
        ("s3_sop_order.png", 25),
        ("s4_visual_result.png", 40),
        ("s5_architecture.png", 13),
        ("s5_firestore.png", 12),
        ("s6_conclusion.png", 10),
    ]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(RAW_VIDEO_PATH, fourcc, fps, (width, height))

    for img_name, duration_sec in scene_schedule:
        img_path = os.path.join(SCENES_DIR, img_name)
        if not os.path.exists(img_path):
            img_path = os.path.join(SCENES_DIR, "s1_kpis.png")

        im = cv2.imread(img_path)
        if im is None:
            im = np.zeros((height, width, 3), dtype=np.uint8)
        else:
            im = cv2.resize(im, (width, height))

        total_frames = int(duration_sec * fps)
        for _ in range(total_frames):
            out.write(im)

    out.release()
    print(f"[Success] Raw video generated at: {RAW_VIDEO_PATH}")

def merge_audio_and_video():
    print("[3/3] Merging video stream with audio narration using FFMPEG...")
    # ffmpeg -y -i raw_video -i audio -c:v libx264 -c:a aac -shortest final.mp4
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-i", RAW_VIDEO_PATH,
        "-i", AUDIO_PATH,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_MP4_PATH
    ]
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Final Video with Audio saved at: {FINAL_MP4_PATH}")

    # Remove temporary raw stream
    if os.path.exists(RAW_VIDEO_PATH):
        try:
            os.remove(RAW_VIDEO_PATH)
        except Exception:
            pass

if __name__ == "__main__":
    capture_scenes()
    render_video_stream()
    merge_audio_and_video()
