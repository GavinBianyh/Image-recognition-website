import os
from flask import Flask, request
from flask_cors import CORS

from PIL import Image
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
CORS(app)

model = ResNet50(weights='imagenet')

@app.route("/")
def main():
    return "Welcome!"

@app.route("/test", methods=['GET'])
def test():
    return "test success"

@app.route('/file-upload', methods=['POST'])
def getImageClass():
    if 'file' not in request.files:
        return "400 Bad request: no file in request"
    file = request.files['file']
    if file.filename == '':
        return "No file selected for uploading"
    # file_type = type(file).__name__             # -> FileStorage
    # read_type = type(file.read()).__name__      # -> bytes
    pil_img = Image.open(file.stream)
    pil_img = pil_img.resize((224,224), Image.ANTIALIAS)
    x = image.img_to_array(pil_img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    top3 = decode_predictions(preds, top=3)[0]
    result = ""
    for pred in top3:
        result += "{" + pred[1] + " : " + str(pred[2]) + "} "
    result_str = str(top3).strip('[]')
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)