import requests
from PIL import Image
from flask import Flask, request, jsonify
import io
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_TOKEN = "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"

API_URL = "https://api-inference.huggingface.co/models/digiplay/Photon_v1"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_huggingface_model(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

@app.route('/generate_image', methods=['POST','Get'])
def generate_image():
    data = request.get_json()
    text_input = data['text']
    image_bytes = query_huggingface_model(text_input)

    # Convert bytes to an image
    image = Image.open(io.BytesIO(image_bytes))

    # Save image to a base64 encoded string
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return jsonify({'image': img_str})

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)
