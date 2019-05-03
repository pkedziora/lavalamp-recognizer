from flask import Flask, flash, redirect, render_template, request, session, abort
from werkzeug.utils import secure_filename
import recognizer
import image_tools as imgTools
import os

application = Flask(__name__, static_url_path='/assets', static_folder='web_app/assets', template_folder='web_app/templates')
application.config['TEMPLATES_AUTO_RELOAD'] = True
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class LavaLampViewModel:
    base64Image = ""
    probability = 0
    islavalamp = False

    def __init__(self, base64Image = "", probability = 0):
        self.base64Image = base64Image
        self.probability = probability
        self.islavalamp = round(probability) == 1

@application.route("/", methods = ['POST', 'GET'])
def hello():
    filePath = ""
    model = LavaLampViewModel()
    if request.method == 'POST':
        imageUpload = request.files['imageUpload']
        filePath = f"{secure_filename(imageUpload.filename)}";
        imageUpload.save(filePath)
        imgTools.normalizeImage(filePath)
        base64Img = imgTools.getBase64ImageString(filePath);
        probability = recognizer.recognize(filePath);
        model = LavaLampViewModel(base64Img, probability)
        os.remove(filePath)
    return render_template("index.html", model = model)
 
if __name__ == "__main__":
    application.run(host= '0.0.0.0', debug = False)