
from pathlib import Path
import random
import shutil
import sys

# Folder containing your downloaded JPG and TXT files
SOURCE = Path.home() / "Downloads" / "archive (9)" / "agri_data" / "data"

# Existing AgriSense project dataset folder
PROJECT = Path(__file__).resolve().parent
DEST = PROJECT / "dataset" / "weed_detection"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
random.seed(42)

if not SOURCE.exists():
    sys.exit(f"Source folder not found: {SOURCE}")

# Find images that have matching annotation files
pairs = []
unmatched = []

for image in SOURCE.rglob("*"):
    if image.is_file() and image.suffix.lower() in IMAGE_EXTENSIONS:
        label = image.with_suffix(".txt")
        if label.exists():
            pairs.append((image, label))
        else:
            unmatched.append(image.name)

if not pairs:
    sys.exit(
        "No matching image and TXT label pairs found. "
        "Check the SOURCE folder path and dataset format."
    )

# Check annotation values before copying
valid_pairs = []
invalid_labels = []

for image, label in pairs:
    try:
        lines = label.read_text(encoding="utf-8-sig").splitlines()
        valid = True

        for line in lines:
            parts = line.split()
            if len(parts) != 5:
                valid = False
                break

            class_id = int(parts[0])
            coords = [float(v) for v in parts[1:]]

            if class_id not in (0, 1):
                valid = False
                break

            if any(v < 0 or v > 1 for v in coords):
                valid = False
                break

            _, _, width, height = coords
            if width <= 0 or height <= 0:
                valid = False
                break

        if valid:
            valid_pairs.append((image, label))
        else:
            invalid_labels.append(label.name)

    except (ValueError, OSError):
        invalid_labels.append(label.name)

if not valid_pairs:
    sys.exit(
        "No valid YOLO labels found. Check the annotation format "
        "and class IDs before proceeding."
    )

random.shuffle(valid_pairs)
split_at = max(1, int(len(valid_pairs) * 0.8))
if len(valid_pairs) > 1:
    split_at = min(split_at, len(valid_pairs) - 1)

splits = {
    "train": valid_pairs[:split_at],
    "val": valid_pairs[split_at:]
}

for split, items in splits.items():
    image_dir = DEST / "images" / split
    label_dir = DEST / "labels" / split
    image_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)

    for image, label in items:
        shutil.copy2(image, image_dir / image.name)
        shutil.copy2(label, label_dir / label.name)

print("Dataset organization complete.")
print(f"Valid image-label pairs: {len(valid_pairs)}")
print(f"Training pairs: {len(splits['train'])}")
print(f"Validation pairs: {len(splits['val'])}")
print(f"Images without labels skipped: {len(unmatched)}")
print(f"Invalid annotations skipped: {len(invalid_labels)}")
print(f"Destination: {DEST}")

if invalid_labels:
    print("Some annotations were skipped. Review their class IDs and format.")
