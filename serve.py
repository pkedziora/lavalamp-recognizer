from flask import Flask, flash, redirect, render_template, request, session, abort
from recognizer import *

app = Flask(__name__)
filePath = "/home/pakedziora/Downloads/006.jpg"

@app.route("/")
def hello():
    islavalamp = recognize(filePath)
    return render_template("index.html", islavalamp = islavalamp == 1)
 
if __name__ == "__main__":
    app.run(debug = False)