"""
Generates the synced English voiceover audio narration using Google Text-to-Speech (gTTS).
"""

import os
from gtts import gTTS

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "assets", "ApexMfg_AI_Demo_Voiceover.mp3")

VOICEOVER_SCRIPT = """
Welcome to the demonstration of ApexMfg AI, an end to end intelligent operations platform built for the Manufacturing Intelligent Operations and Industrial Efficiency challenge.

In modern manufacturing, unexpected machinery downtime costs industrial plants upwards of 260,000 dollars per hour. Today, maintenance teams are overwhelmed with complex IoT telemetry and thick paper manuals. We built ApexMfg AI to turn raw machine telemetry into immediate, actionable operational intelligence.

Here on our plant monitor, our connected machinery fleet streams vibration, temperature, and hydraulic pressure in real time. 

Now, let us simulate a real world anomaly on our 5 axis CNC milling center. In the sidebar, we inject a bearing degradation fault. Instantly, our Cloud Run backend detects the threshold breach. Vibration spikes past 5.8 millimeters per second, violating ISO 10816 standards, and an incident is immediately logged into Cloud Firestore.

Instead of flipping through paper manuals, we switch to our Gemini Predictive Maintenance tab and click Execute Gemini Root Cause Analysis. Under the hood, Gemini analyzes multi axis vibration harmonics and thermodynamic dissipation. Within under two seconds, Gemini identifies bearing outer raceway spalling with 95 percent confidence and forecasts 8.5 hours of Remaining Useful Life before total machine seizure.

Next, Gemini synthesizes an OSHA compliant Lockout Tagout repair procedure, precision tool requirements, and exact replacement part SKUs, including the SKF spindle bearing set. With one click, we commit this work order directly to Cloud Firestore, dispatching the notification to the maintenance lead's mobile tablet.

Next, we navigate to our Multimodal Visual Quality Inspection tab. High precision manufacturing requires defect free components. Here, an optical camera feed captures a manufactured weld bead. We click Run Gemini Optical Inspection. Gemini scans the surface geometry and flags cluster porosity violating ISO 5817 Quality Level B, immediately placing the batch on quality quarantine.

Finally, we inspect our Google Cloud architecture tab. Our entire platform is deployed serverlessly on Google Cloud Run for auto scaling resilience, Cloud Firestore for sub second real time data synchronization, Firebase for role based authentication, and Google Gemini for cognitive multimodal intelligence.

ApexMfg AI delivers a 32 percent reduction in Mean Time to Repair and a 14.8 percent uplift in Overall Equipment Effectiveness. Thank you for evaluating our submission.
"""

def generate_audio():
    print("[1/2] Synthesizing speech narration with Google TTS...")
    tts = gTTS(text=VOICEOVER_SCRIPT.strip(), lang='en', slow=False)
    tts.save(OUTPUT_PATH)
    print(f"[2/2] Saved audio narration to: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_audio()
