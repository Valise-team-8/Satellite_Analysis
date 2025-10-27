import os
import shutil
import random

# Paths
source_dir = "dataset_unprocessed"
target_dir = "dataset"
samples_per_class = 2500

# Clean target folder
shutil.rmtree(target_dir, ignore_errors=True)
os.makedirs(target_dir, exist_ok=True)

# Detect all classes dynamically
classes = [
    d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))
]
print("Classes detected:", classes)

for cls in classes:
    cls_source = os.path.join(source_dir, cls)
    cls_target = os.path.join(target_dir, cls)
    os.makedirs(cls_target, exist_ok=True)

    all_images = os.listdir(cls_source)
    selected_images = random.sample(all_images, min(samples_per_class, len(all_images)))

    print(f"Copying {len(selected_images)} images for class {cls}")
    for img in selected_images:
        shutil.copy(os.path.join(cls_source, img), os.path.join(cls_target, img))
