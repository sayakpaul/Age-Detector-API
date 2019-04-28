import os
import base64
from io import BytesIO
from fastai import *
from fastai.vision import *
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest


def evaluate_image(img) -> str:
    pred_class = trained_model.predict(img)[0]
    return pred_class

def load_model():
    path = 'models'
    learn = load_learner(path, 'age-model.pkl')
    return learn

app = Flask(__name__)
app.config['DEBUG'] = False
trained_model = load_model()

@app.route('/', methods=['GET'])
def index():
    return "I am an age detector. Huhu!"

@app.route('/image', methods=['POST'])
def eval_image():
    """Evaluate the image!"""
    input_file = request.files.get('file')
    if not input_file:
        return BadRequest("File is not present in the request")
    if input_file.filename == '':
        return BadRequest("Filename is not present in the request")
    if not input_file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        return BadRequest("Invalid file type")
    
    input_buffer = BytesIO()
    input_file.save(input_buffer)
    
    age = evaluate_image(open_image(input_buffer))
    return jsonify({'Age': str(age)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=False)