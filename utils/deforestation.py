import cv2
import numpy as np


def detect_deforestation(before_path, after_path, threshold=30):
    """
    Compare two satellite images to detect deforestation or afforestation
    """
    before = cv2.imread(before_path)
    after = cv2.imread(after_path)

    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(before_gray, after_gray)
    changed_pixels = np.sum(diff > threshold)
    total_pixels = diff.size

    # identifies changed areas
    change_percent = (changed_pixels / total_pixels) * 100

    # --- Added part below ---
    mean_before = np.mean(before_gray)
    mean_after = np.mean(after_gray)

    if change_percent > 5:
        if mean_after > mean_before:
            status = "Deforestation Detected"  # image got brighter → forest lost
        else:
            status = "Afforestation Detected"  # image got darker → forest gained
    else:
        status = "No Major Change"
    # --- End of added part ---

    return round(change_percent, 2), status
