
from pathlib import Path
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "runs" / "detect" / "weed_fast" / "weights" / "best.pt"
DATASET_PATH = ROOT / "dataset"

# Check trained model
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))
print("Model loaded successfully!")
print("Classes:", model.names)

# Find an image automatically in the dataset
extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
images = [
    p for p in DATASET_PATH.rglob("*")
    if p.is_file() and p.suffix.lower() in extensions
]

if not images:
    raise FileNotFoundError(
        "No images found in the dataset folder. "
        "Check your dataset directory."
    )

image_path = images[0]
print("Testing image:", image_path)

# Run detection
results = model.predict(
    source=str(image_path),
    conf=0.25,
    save=True
)

for result in results:
    if result.boxes is None or len(result.boxes) == 0:
        print("No objects detected in this image.")
    else:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            print(f"{model.names[class_id]}: {confidence:.2%}")

print("Prediction completed!")
print("Check the runs/detect folder for the output image.")
