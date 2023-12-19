import requests
from PIL import Image, UnidentifiedImageError
from flask import Flask, request, jsonify
import io
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_TOKEN = "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"

API_URL = "https://api-inference.huggingface.co/models/digiplay/Photon_v1"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_huggingface_model(text, nprompt, steps):
    payload = {
        "inputs": text,
        "negative_prompt": nprompt,
        "num_inference_steps": steps,
        "seed": 1627275462,
        "guidance_scale": 6.5,
        "Sampler": "Eular",
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

@app.route('/generate_image', methods=['POST', 'GET'])
def generate_image():
    data = request.json  # Getting JSON data from the request

    if 'inputs' in data:
        text_input = data['inputs']
        negative_prompt = data.get('negative_prompt')  # Fetch optional parameter if present
        num_inference_steps = data.get('num_inference_steps')  # Fetch optional parameter if present

        image_bytes = query_huggingface_model(text_input, negative_prompt, num_inference_steps)


 # Convert bytes to an image
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except UnidentifiedImageError:
        print("The image file cannot be identified by PIL")

    # Save image to a buffer
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    # Convert bytes to base64 string
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Return base64 string in JSON response
    return jsonify({'image': image_base64})


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)
