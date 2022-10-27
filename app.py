import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

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
    return jsonify({'label': "Estrela",
                    'percent': "30%"})

if __name__ == '__main__':
    app.run()