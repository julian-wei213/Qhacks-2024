from flask import Flask, jsonify, request
from flask_cors import CORS
from training import retrain


# Create an app object of class Flask
app = Flask(__name__)
CORS(app)


@app.route('/home', methods=['POST'])
def home():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the file to a desired location
        file.save(file.filename)

        pred = retrain(file)

        print("here\n")

        return jsonify({"message": "Percentage: " + str(pred)}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run()
