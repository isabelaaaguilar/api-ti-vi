from flask import Flask, request, jsonify
import tensorflow as tf
import os

app = Flask(__name__)
STATIC_FOLDER = "static"

dir_path = os.path.dirname(os.path.realpath(__file__))
cnn_model = tf.keras.models.load_model(STATIC_FOLDER + "/models/" + "galaxy-convnet-v2.h5")

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

    prob = cnn_model.predict(preprocessed_imgage)
    
    label = "Galaxia" if prob[0][0] >= 0.5 else "Estrela"
    classified_prob = prob[0][0] if prob[0][0] >= 0.5 else 1 - prob[0][0]

    return label, classified_prob


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return jsonify({'name':'Jimit',
                    'address':'India'})

    else:
        file = request.files["image"]
        upload_image_path = os.path.join(file.filename)
        print(upload_image_path)
        file.save(upload_image_path)
        label, prob = classify(cnn_model, upload_image_path)

        prob = round((prob * 100), 2)
        print(prob)
    return jsonify({'label': label,
                    'percent':prob})

app.run(debug=True)