from flask import Flask, jsonify, request, render_template
import tensorflow as tf
import numpy as np
import os
from keras.models import load_model
import pathlib
import base64
from io import BytesIO
from PIL import Image
import time

app = Flask(__name__)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
directory_path = os.getcwd()
<<<<<<< HEAD
path = directory_path + "\\VGG16_model.h5"
=======
path = directory_path + "\\model_cpu_with_early_stopping.h5"
>>>>>>> 5e9fa89 (code changes)
directory = directory_path + "\\skin_disease_augmented"
best_model = tf.keras.models.load_model(path)
print(directory)

def get_class(directory):
    data_dir = pathlib.Path(directory)
    class_names = np.array(sorted([item.name for item in data_dir.glob("*")]))
    return class_names

def load_and_resize_image(img_raw, size):
<<<<<<< HEAD
    
    img = tf.image.decode_image(img_raw.read(), channels=3)
    
    img = tf.image.resize(img, [size, size])
    
=======
    # Compile image
    img = tf.image.decode_image(img_raw.read(), channels=3)
    # Resize image
    img = tf.image.resize(img, [size, size])
    # Scale the tensor
>>>>>>> 5e9fa89 (code changes)
    img = img / 255
    return img

def encode_image_base64(image):
    img_pil = Image.fromarray((image * 255).astype(np.uint8))
    img_io = BytesIO()
    img_pil.save(img_io, 'PNG')
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return img_base64

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("home.html",error="NA")

    if request.method == 'POST':
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        f = request.files['file']
        class_names = get_class(directory)

        image = load_and_resize_image(f, 150)
        pred = best_model.predict(tf.expand_dims(image, axis=0))

        class_names = get_class(directory)
        result_idx = pred[0].argmax()
        if result_idx >= len(class_names):
            return "Error: Predicted index out of range"
        time.sleep(1)
        result = class_names[result_idx]
  
        return render_template('home.html', img = encode_image_base64(image.numpy()), result = result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
