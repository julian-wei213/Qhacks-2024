from flask import Flask, request, render_template
import numpy as np 
import pickle

# Create an app object of class Flask
app = Flask(__name__)

#Load the trained model from a pickle file
model = pickle.load(open('models/model.pkl', 'rb'))



@app.route('/')
def home():
    return render_template('.my-app\src\App.js')


@app.route('predict', method=['POST'])
def cnn_predict():
    int_features = [float(x) for x in request.form.values()]
    features = [np.array(int_features)]
    prediction = model.predict(features)

    output = prediction
    
    return render_template()


if __name__ == '__main__':
    app.run