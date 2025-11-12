from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this import
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import base64

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS
model = load_model('sign_language_model.keras')

# Label map and confidence threshold
label_map = {0: 'hello', 1: 'thanks', 2: 'yes', 3: 'no'}
confidence_threshold = 0.5

def preprocess_frame(frame):
    """Resize and normalize the image for prediction."""
    img = cv2.resize(frame, (128, 128))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route("/predict", methods=["POST"])
def predict():
    # Check if JSON contains 'image'
    if not request.is_json or 'image' not in request.json:
        return jsonify({"error": "Missing 'image' key in JSON"}), 400

    data = request.json['image']

    # Remove data prefix if present
    if ',' in data:
        data = data.split(',')[1]

    try:
        img_data = base64.b64decode(data)
    except Exception as e:
        return jsonify({"error": "Failed to decode base64 image", "details": str(e)}), 400

    # Convert to numpy array and decode with OpenCV
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Failed to decode image. Check base64 input."}), 400

    # Preprocess and predict
    processed = preprocess_frame(frame)
    predictions = model.predict(processed)
    max_prob = float(np.max(predictions[0]))
    predicted_class = int(np.argmax(predictions[0]))

    if max_prob >= confidence_threshold:
        label = label_map.get(predicted_class, "Unknown")
    else:
        label = "No sign detected"

    return jsonify({"prediction": label, "confidence": max_prob})

if __name__ == "__main__":
    app.run(debug=True)