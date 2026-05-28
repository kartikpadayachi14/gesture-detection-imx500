Gesture Detection using YOLO11 + Raspberry Pi 5 + Sony IMX500 AI Camera
YOLO11 Hardware License

This repository contains a complete, end-to-end pipeline to implement a real-time hand gesture detection system on the edge. By leveraging YOLO11 nano, the Raspberry Pi 5, and the hardware-accelerated Sony IMX500 AI Camera, this system achieves high-frame-rate embedded inference for three core gestures: Palm, Thumbs Up, and Thumbs Down.

📌 Project Overview
The project covers the entire deployment lifecycle:

Dataset Collection & Labeling using Label Studio (including negative image sampling).
Model Training using Ultralytics YOLO11.
Optimization & Exporting via ONNX and the Sony IMX500 compilation toolchain to generate an .rpk package.
Edge Deployment utilizing Picamera2 and IMX500 hardware acceleration on Raspberry Pi OS Bookworm.

🛠️ Requirements
Hardware
Raspberry Pi 5
Sony IMX500 AI Camera
MicroSD Card (32GB or larger recommended)
Official Raspberry Pi Power Supply (5V 5A)
HDMI Display or SSH Access

Software Environment
System	Requirements / Dependencies
Training Host (Laptop/Linux PC)	Python 3.10+, requirements.txt
Edge Target (Raspberry Pi 5)	Raspberry Pi OS Bookworm (64-bit), Picamera2, IMX500 system packages

🔄 Project Workflow
Dataset Collection ──> Labeling Images ──> YOLO11 Training ──> Model Testing
                                                                   │
Real-Time Detection <── Pi Deployment <── RPK Packaging <── IMX Export <── ONNX Export

📂 Dataset Preparation
Target Classes
0: Palm
1: Thumbs Up
2: Thumbs Down
Image Collection Guidelines
To ensure high accuracy and robustness, collect images under varied distributions:

Environments: Different lighting conditions, indoor/outdoor settings, and diverse backgrounds.
Subjects: Multiple people, capturing both left and right hands at various angles/distances.
Negative Images: Crucial for reducing false positives. Include pictures of keyboards, faces, desks, monitors, and empty backgrounds. Do not draw bounding boxes on negative images; simply upload them unannotated.
Label Studio Configuration
Setup an Object Detection with Bounding Boxes project in Label Studio. Use the following XML layout config:

<View>
  <Image name="image" value="$image"/>
  <RectangleLabels name="label" toName="image">
    <Label background="green" value="Palm"/>
    <Label background="blue" value="Thumbs up"/>
    <Label background="red" value="Thumbs down"/>
  </RectangleLabels>
</View>
Directory Structure
Organize your dataset locally as follows:

data/
├── train/
│   ├── images/
│   └── labels/
└── valid/
    ├── images/
    └── labels/

Create a data.yaml file in the root directory:

train: ./data/train/images
val: ./data/valid/images

nc: 3
names:
  - Palm
  - Thumbs up
  - Thumbs down
📦 Installation & Setup
1. Training Environment (Host PC)
To set up your workstation for data labeling, training, and exporting:

pip install -r requirements.txt
(Note: If you have an NVIDIA GPU, it is recommended to install the CUDA-compatible version of PyTorch before running the pip command).

2. Deployment Environment (Raspberry Pi 5)
First, install the hardware accelerator libraries through the system package manager:

sudo apt update && sudo apt install imx500-all python3-opencv -y
Then install the lightweight Python prerequisites:

pip install -r requirements.txt
🏋️ Training & Local Testing
1. Model Training
Run train.py on your training machine to train the YOLO11 nano model:

# train.py
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="data.yaml",
    epochs=100,
    imgsz=320,
    batch=8
)
Execute with: python train.py

2. Local Verification
Verify the trained weights using a local webcam:

# test.py
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")
model.predict(source=0, show=True, conf=0.7)
Execute with: python test.py

🚀 Optimization & Export Pipeline
1. Export to ONNX
# export_onnx.py
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")
model.export(format="onnx", opset=12, simplify=True, imgsz=320)
print("ONNX export completed!")
Execute with: python export_onnx.py

2. Export to Sony IMX500 Format
(Note: This step requires a Linux environment)

# yolo_export.py
from ultralytics import YOLO

model = YOLO("best.pt")
model.export(format="imx", data="data.yaml", int8=True)
print("IMX export completed!")
Execute with: uv run python yolo_export.py

Output Files Generated:

packerOut.zip
labels.txt
🎛️ Raspberry Pi 5 Deployment
1. Compile the RPK Package
Convert the compiled .zip file into the final firmware file readable by the IMX500:

imx500-package -i packerOut.zip -o output
This generates the application package at output/network.rpk.

2. Run Real-Time Hardware Inference
Navigate to the native Picamera2 IMX500 examples directory and boot the demo script with your custom model:

cd ~/picamera2/examples/imx500

python imx500_object_detection_demo.py \
  --model ~/output/network.rpk \
  --labels ~/labels.txt \
  --bbox-normalization \
  --bbox-order xy \
  --threshold 0.2
📊 Results & Live Inference
The system successfully executes real-time, hardware-accelerated inference via the Sony IMX500 chip. It isolates hand positions against complex environments under varied indoor lighting distributions.

Inference Performance Metrics
Gesture Class	Target Label	Sample Confidence	Detection Bounding Box
0	Palm (Open Hand)	~0.84	Blue 🟦
1	Thumbs up	~0.48	White ⬜
2	Thumbs down	~0.86	Cyan 🟩
