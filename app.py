import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route("/", methods=["POST"])
def home():
        file = request.files["image"]
        upload_image_path = os.path.join(file.filename)
        print(upload_image_path)
        file.save(upload_image_path)
        return jsonify({'Teste':'Sucesso'})

if __name__ == "__main__":
    app.run()