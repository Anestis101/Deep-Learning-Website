from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load your trained model
model = load_model('your_model.h5')

# Classes or conditions (update based on your model's output)
conditions = ["No issues detected", "Possible melanoma", "Other skin condition"]

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo uploaded'}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Preprocess the image
    try:
        image = Image.open(file_path).convert('RGB')  # Ensure RGB format
        image = image.resize((224, 224))  # Resize to model input size
        image_array = img_to_array(image) / 255.0  # Normalize pixel values
        image_array = np.expand_dims(image_array, axis=0)

        # Predict with the model
        prediction = model.predict(image_array)
        result_index = np.argmax(prediction, axis=1)[0]
        result = conditions[result_index]

        return jsonify({
            'result': result,
            'message': "Please note: This is an AI-based analysis. Always consult a doctor for a professional diagnosis."
        })
    except Exception as e:
        return jsonify({'error': f"Error processing image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
