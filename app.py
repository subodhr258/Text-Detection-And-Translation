from flask import Flask, request, jsonify, render_template
import pandas as pd
from werkzeug.utils import secure_filename
import easyocr
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from googletrans import Translator
from Languages import languages

translator = Translator()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    lang = request.form.get('languages')
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename('input.jpg')
        file.save(filename)
        
        from_language = languages[lang]
        image = cv2.imread('./input.jpg')
        reader = easyocr.Reader(['en',from_language])
        res = reader.readtext('./input.jpg')
        
        for (bbox, text, prob) in res: 
            if translator.detect(text).lang!='en':
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                translation = translator.translate(text).text
                cv2.putText(image, translation, (tl[0], tl[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        plt.rcParams['figure.figsize'] = (16,16)
        plt.axis('off')
        plt.imshow(image)
        plt.savefig('static/output.png',bbox_inches='tight', pad_inches=0)
    
    return render_template('index.html',image=True)

if __name__ == "__main__":
    app.run()
