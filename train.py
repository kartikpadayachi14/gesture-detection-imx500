from ultralytics import YOLO

# Load YOLO11 nano model
model = YOLO("yolo11n.pt")

# Train model
model.train(
    data="data.yaml",
    epochs=150,
    imgsz=320,
    batch=8
)

print("Training completed!")