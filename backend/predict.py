from flask import Flask, request, jsonify
import torch
import joblib
import cv2
import numpy as np
import os
from torchvision import models, transforms
from PIL import Image

app = Flask(__name__)

# ---------- モデルの読み込み ----------
model_dir = "models"
hog_model_path = os.path.join(model_dir, "011 - hog_svm_model.pth")
resnet_model_path = os.path.join(model_dir, "021 - resnet18_model.pth")

hog_svm = torch.load(hog_model_path)
resnet18 = models.resnet18()
resnet18.fc = torch.nn.Linear(resnet18.fc.in_features, 2)  # クラス数2に調整
resnet18.load_state_dict(torch.load(resnet_model_path, map_location=torch.device('cpu')))
resnet18.eval()

# ---------- 前処理 ----------
def preprocess_for_hog(image_bytes):
    image = Image.open(image_bytes).convert('L')  # グレースケール
    image = image.resize((64, 128))
    img_np = np.array(image)
    hog = cv2.HOGDescriptor()
    features = hog.compute(img_np).flatten()
    return features.reshape(1, -1)

def preprocess_for_resnet(image_bytes):
    image = Image.open(image_bytes).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    tensor = transform(image).unsqueeze(0)  # バッチ次元
    return tensor

# ---------- 推論API ----------
@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files or 'model' not in request.form:
        return jsonify({"error": "image and model are required"}), 400

    image = request.files['image']
    model_name = request.form['model']

    if model_name == "HOG+SVM":
        features = preprocess_for_hog(image)
        pred = hog_svm.predict(features)[0]
        prob = max(hog_svm.predict_proba(features)[0])

    elif model_name == "ResNet18":
        tensor = preprocess_for_resnet(image)
        with torch.no_grad():
            output = resnet18(tensor)
            prob = torch.nn.functional.softmax(output, dim=1)[0]
            pred = torch.argmax(prob).item()
            prob = prob[pred].item()

    else:
        return jsonify({"error": "Unknown model"}), 400

    return jsonify({"prediction": int(pred), "confidence": round(prob, 3)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
