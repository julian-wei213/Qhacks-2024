from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return "Hello, World!"  # You can change this to render your React app if needed

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        resp = jsonify({"message": 'No file part in the request', "status": 'failed'})
        resp.status_code = 400
        return resp

    file = request.files['file']
    if file.filename == '':
        resp = jsonify({"message": 'No selected file', "status": 'failed'})
        resp.status_code = 400
        return resp

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({"message": 'File successfully uploaded', "status": 'success'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({"message": 'File type is not allowed', "status": 'failed'})
        resp.status_code = 400
        return resp

if __name__ == '__main__':
    app.run(debug=True)
