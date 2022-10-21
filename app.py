import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app)

@app.route("/")
def index():
        return jsonify({'success': True, 'message': 'Active'})

if __name__ == "__main__":
    app.run()