from flask import Flask, request, jsonify, render_template
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    output = []
    if request.method == 'POST':
        pass
    
    return render_template('index.html',image="")

if __name__ == "__main__":
    app.run()
