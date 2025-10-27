# testing/Predict_image.py
import sys
import os
from pathlib import Path
import csv

# --- ensure project root is on sys.path ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.predict import predict_land_use

# folder containing test images (relative to project root)
TEST_FOLDER = PROJECT_ROOT / "testing" / "test_img"
OUT_CSV = PROJECT_ROOT / "testing" / "predictions.csv"

# allowed image extensions
EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}

if not TEST_FOLDER.exists():
    print(f"[ERROR] Test folder not found: {TEST_FOLDER}")
    sys.exit(1)

image_paths = sorted([p for p in TEST_FOLDER.iterdir() if p.suffix.lower() in EXTS])
if not image_paths:
    print(f"[WARN] No images found in {TEST_FOLDER} (supported: {', '.join(sorted(EXTS))})")
    sys.exit(0)

# Prepare CSV output
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["image", "predicted_class", "confidence"])

    # Process images
    for img_path in image_paths:
        try:
            predicted_class, confidence = predict_land_use(str(img_path))
            print(f"{img_path.name}: {predicted_class} ({confidence}%)")
            writer.writerow([str(img_path.name), predicted_class, confidence])
        except Exception as e:
            print(f"{img_path.name}: ERROR -> {e}")
            writer.writerow([str(img_path.name), "ERROR", str(e)])

print(f"\nDone. Predictions saved to: {OUT_CSV}")
