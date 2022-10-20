import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app)

@app.route("/",methods=['POST'])
def index():
        image = request.files["imgFile"]
        print(image)
        image.save(image.filename)
        
        return jsonify({'success': True, 'message': 'Valid user'})

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1",port=port, debug=True)

if __name__ == "__main__":
    main()