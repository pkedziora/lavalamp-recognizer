from flask import Flask, flash, redirect, render_template, request, session, abort
from werkzeug.utils import secure_filename
from recognizer import *
import base64
import os
from PIL import Image, ExifTags
from io import BytesIO

def getBase64ImageString(filePath):
    prefix = "data:image/jpeg;charset=utf-8;base64,";
    with open(filePath, "rb") as imageFile:
        encoded_string = base64.b64encode(imageFile.read()).decode("utf-8")
    return f"{prefix}{encoded_string}"

def normalizeImage(filePath):
    image=Image.open(filePath)
    exif=dict((ExifTags.TAGS[k], v) for k, v in image._getexif().items() if k in ExifTags.TAGS)
    if exif["Orientation"] == 3 : 
        image=image.rotate(180, expand=True)
    elif exif["Orientation"] == 6 : 
        image=image.rotate(270, expand=True)
    elif exif["Orientation"] == 8 : 
        image=image.rotate(90, expand=True)
    image.save(filePath, format="JPEG")


app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def hello():
    filePath = ""
    base64Image = ""
    islavalamp = False
    # if request.method == 'POST':
    #     filePath = request.form['imagePath']
    if request.method == 'POST':
        imageUpload = request.files['imageUpload']
        filePath = f"{secure_filename(imageUpload.filename)}";
        imageUpload.save(filePath)
        normalizeImage(filePath)
        base64Image = getBase64ImageString(filePath)
        islavalamp = recognize(filePath)
        os.remove(filePath)
    return render_template("index.html", isPost=request.method == 'POST', islavalamp = islavalamp == 1, base64Image = base64Image)
 
if __name__ == "__main__":
    app.run(debug = False)