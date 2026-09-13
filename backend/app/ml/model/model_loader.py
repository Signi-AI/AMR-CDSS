import json
from pathlib import Path
import timm
import torch

MODEL_PATH = Path(__file__).with_name("model.pth")
CLASS_NAMES_PATH = Path(__file__).with_name("class_names.json")

# 1. Load the 20 class names
with open(CLASS_NAMES_PATH, "r") as f:
    class_names = json.load(f)

# 2. Build the EfficientNet architecture matching your classes
model = timm.create_model(
    "tf_efficientnet_b0",
    pretrained=False,
    num_classes=len(class_names),  # 20 classes
)

# 3. If model.pth doesn't exist, generate a dummy placeholder file
if not MODEL_PATH.exists():
    print(f"[INFO] model.pth not found. Generating dummy placeholder weights at {MODEL_PATH}...")
    torch.save(model.state_dict(), MODEL_PATH)
    print("[INFO] Placeholder model.pth created successfully!")

# 4. Load weights into the model
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu", weights_only=True))
model.eval()