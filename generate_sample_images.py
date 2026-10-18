"""
Generates synthetic industrial defect images for visual optical inspection testing.
"""

import os
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "assets", "samples")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_samples():
    # 1. Defective Weld (Pitting & Porosity)
    img1 = Image.new("RGB", (600, 400), color=(60, 65, 75))
    draw1 = ImageDraw.Draw(img1)
    # Draw metallic weld bead
    for y in range(160, 240, 2):
        shade = 110 + int(30 * (1 - abs(y - 200) / 40.0))
        draw1.line([(50, y), (550, y)], fill=(shade, shade + 5, shade + 15), width=2)
    # Draw pores / pits
    pits = [(260, 195, 8), (280, 210, 12), (300, 190, 7), (315, 205, 14), (340, 198, 9), (410, 202, 6)]
    for x, y, r in pits:
        draw1.ellipse([x - r, y - r, x + r, y + r], fill=(25, 25, 30), outline=(15, 15, 20))
        draw1.ellipse([x - r//2, y - r//2, x, y], fill=(10, 10, 10))
    # Draw red inspection bounding box
    draw1.rectangle([240, 175, 360, 225], outline=(255, 60, 60), width=3)
    draw1.text((245, 155), "ANOMALY: POROSITY CLUSTER", fill=(255, 70, 70))
    img1.save(os.path.join(OUTPUT_DIR, "weld_porosity_defect.jpg"), "JPEG")

    # 2. Defective Bearing Ring (Spalling & Fracture Crack)
    img2 = Image.new("RGB", (600, 400), color=(45, 48, 55))
    draw2 = ImageDraw.Draw(img2)
    # Draw polished steel ring
    draw2.ellipse([150, 50, 450, 350], fill=(160, 165, 175), outline=(110, 115, 125), width=15)
    draw2.ellipse([210, 110, 390, 290], fill=(45, 48, 55), outline=(110, 115, 125), width=10)
    # Draw micro-crack
    crack_pts = [(300, 55), (305, 70), (298, 85), (310, 105)]
    draw2.line(crack_pts, fill=(20, 20, 25), width=4)
    draw2.rectangle([285, 45, 325, 115], outline=(255, 60, 60), width=3)
    draw2.text((240, 25), "ANOMALY: SURFACE SPALL / CRACK", fill=(255, 70, 70))
    img2.save(os.path.join(OUTPUT_DIR, "bearing_crack_defect.jpg"), "JPEG")

    # 3. Clean Nominal Component (PASS)
    img3 = Image.new("RGB", (600, 400), color=(50, 55, 65))
    draw3 = ImageDraw.Draw(img3)
    # Draw pristine machined cylinder
    draw3.rounded_rectangle([120, 120, 480, 280], radius=20, fill=(180, 185, 195), outline=(220, 225, 235), width=4)
    # Add subtle machining lathe texture lines
    for x in range(140, 460, 8):
        draw3.line([(x, 130), (x, 270)], fill=(165, 170, 180), width=1)
    draw3.rectangle([110, 110, 490, 290], outline=(40, 200, 80), width=3)
    draw3.text((120, 85), "QA STATUS: NOMINAL TOLERANCE (PASS)", fill=(50, 230, 90))
    img3.save(os.path.join(OUTPUT_DIR, "nominal_machined_part.jpg"), "JPEG")

    print("[Success] Generated 3 synthetic industrial test images in assets/samples/")

if __name__ == "__main__":
    generate_samples()
