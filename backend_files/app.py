
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import cv2
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TFLITE_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monreader.tflite")
logging.info(f"Model path : {TFLITE_MODEL_PATH}")
logging.info(f"File exists: {os.path.exists(TFLITE_MODEL_PATH)}")

# tensorflow-cpu matches the TF version used to export the model (2.16.1)
# and starts in ~3s on CPU — fast enough to pass HF's health check
import tensorflow as tf
logging.info(f"TF version: {tf.__version__}")

logging.info("Loading TFLite model...")
interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)
interpreter.allocate_tensors()
input_details  = interpreter.get_input_details()
output_details = interpreter.get_output_details()
logging.info(f"Model loaded OK. Input: {input_details[0]['shape']} Output: {output_details[0]['shape']}")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "service": "MonReader page-flip predictor"})


@app.route("/v1/predict", methods=["POST", "OPTIONS"])
def predict_flip():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if "image" not in request.files:
        return jsonify({"error": "No image file provided. Send multipart/form-data with key 'image'."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected image file"}), 400

    try:
        image_data   = file.read()
        np_img       = np.frombuffer(image_data, np.uint8)
        img          = cv2.imdecode(np_img, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return jsonify({"error": "Could not decode image. Ensure the file is a valid JPG/PNG."}), 400

        img_resized  = cv2.resize(img, (200, 200))
        img_norm     = (img_resized / 255.0).astype(np.float32)
        input_tensor = img_norm[np.newaxis, :, :, np.newaxis]  # (1, 200, 200, 1)

        interpreter.set_tensor(input_details[0]['index'], input_tensor)
        interpreter.invoke()
        prediction_score = float(interpreter.get_tensor(output_details[0]['index'])[0][0])

        predicted_label = "flip" if prediction_score < 0.5 else "notflip"
        logging.info(f"Score: {prediction_score:.4f} -> {predicted_label}")

        return jsonify({
            "status": "success",
            "prediction_score": prediction_score,
            "prediction": predicted_label
        })

    except Exception as e:
        logging.error(f"Prediction error: {e}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)

