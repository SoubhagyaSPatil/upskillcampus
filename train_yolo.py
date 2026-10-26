
from pathlib import Path
from ultralytics import YOLO

# Project folder
ROOT = Path(__file__).resolve().parent

# Find the dataset configuration file
yaml_files = list(ROOT.glob("dataset/**/data.yaml"))

if not yaml_files:
    yaml_files = list(ROOT.glob("dataset/**/*.yaml"))

if not yaml_files:
    raise FileNotFoundError(
        "No data.yaml file found inside the dataset folder. "
        "Check your dataset configuration."
    )

DATA_YAML = yaml_files[0]
print("Using dataset:", DATA_YAML)

# Load the small pretrained YOLO model
model = YOLO(str(ROOT / "yolo11n.pt"))

# Train with faster settings
model.train(
    data=str(DATA_YAML),
    epochs=10,
    imgsz=416,
    batch=4,
    device="cpu",
    patience=3,
    workers=0,
    cache=False,
    project=str(ROOT / "runs" / "detect"),
    name="weed_fast",
    exist_ok=True,
    save=True
)

print("Training finished!")
print("Check runs/detect/weed_fast/weights/best.pt")
