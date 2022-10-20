from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def home():
        image = request.files["imgFile"]
        print(image)
        image.save(image.filename)
        
        return jsonify({'success': True, 'message': 'Valid user'})

app.run(debug=True)