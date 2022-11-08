import os
from os import path, listdir
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf

app = Flask(__name__)
cors = CORS(app)

STATIC_FOLDER = "static"

dir_path = os.path.dirname(os.path.realpath(__file__))
cnn_model = tf.keras.models.load_model(STATIC_FOLDER + "/models/" + "classify_stars_and_galaxies.h5")

IMAGE_SIZE = 150

# Preprocess an image
def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [IMAGE_SIZE, IMAGE_SIZE])
    image /= 255.0  # normalize to [0,1] range

    return image

# Read the image from path and preprocess
def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)


# Predict & classify image
def classify(model, image_path):

    preprocessed_imgage = load_and_preprocess_image(image_path)
    preprocessed_imgage = tf.reshape(
        preprocessed_imgage, (1, IMAGE_SIZE, IMAGE_SIZE, 3)
    )

    prob = model.predict(preprocessed_imgage)
    label = "Galáxia" if prob[0][0] >= 0.5 else "Estrela"
    classified_prob = prob[0][0] if prob[0][0] >= 0.5 else 1 - prob[0][0]

    return label, classified_prob

@app.route("/", methods=["POST"])
def home():
    files = request.files.getlist("image")
    classifications=[]
    all_image_path = [path.join('images', p) for p in listdir('images') if path.isfile(path.join('images', p))]
    for file in  all_image_path:
        #upload_image_path = os.path.join(file.filename)
        #file.save(upload_image_path)
        label, prob = classify(cnn_model, file)
        prob = round((prob * 100), 2)
        classifications.append({'label': label,'percent':prob})
        #os.remove(upload_image_path)
    return jsonify(classifications)

if __name__ == "__main__":
    app.run(debug=True)
