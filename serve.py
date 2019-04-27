from flask import Flask, flash, redirect, render_template, request, session, abort
from werkzeug.utils import secure_filename
from recognizer import *
import base64
import os
from PIL import Image, ExifTags

def getBase64ImageString(filePath):
    prefix = "data:image/jpeg;charset=utf-8;base64,";
    with open(filePath, "rb") as imageFile:
        encoded_string = base64.b64encode(imageFile.read()).decode("utf-8")
    return f"{prefix}{encoded_string}"

def normalizeImage(filePath):
    image=Image.open(filePath)
    if (image._getexif() is not None):
        exif=dict((ExifTags.TAGS[k], v) for k, v in image._getexif().items() if k in ExifTags.TAGS)
        if "Orientation" in exif:
            if exif["Orientation"] == 3 : 
                image=image.rotate(180, expand=True)
            elif exif["Orientation"] == 6 : 
                image=image.rotate(270, expand=True)
            elif exif["Orientation"] == 8 : 
                image=image.rotate(90, expand=True)

    image.save(filePath, format="JPEG")


app = Flask(__name__)

class LavaLampViewModel:
    base64Image = ""
    probability = 0
    islavalamp = False

    def __init__(self, base64Image = "", probability = 0):
        self.base64Image = base64Image
        self.probability = probability
        self.islavalamp = round(probability) == 1

@app.route("/", methods = ['POST', 'GET'])
def hello():
    filePath = ""
    model = LavaLampViewModel()
    if request.method == 'POST':
        imageUpload = request.files['imageUpload']
        filePath = f"{secure_filename(imageUpload.filename)}";
        imageUpload.save(filePath)
        normalizeImage(filePath)
        base64 = getBase64ImageString(filePath);
        probability = recognize(filePath);
        model = LavaLampViewModel(base64, probability)
        os.remove(filePath)
    return render_template("index.html", model = model)
 
if __name__ == "__main__":
    app.run(debug = False)