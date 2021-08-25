from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import recognizer
import image_tools
import os

application = Flask(__name__, static_url_path='/assets', static_folder='web_app/assets',
                    template_folder='web_app/templates')
application.config['TEMPLATES_AUTO_RELOAD'] = True
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


class LavaLampViewModel:
    base64Image = ""
    probability = 0
    islavalamp = False

    def __init__(self, base64_image="", probability=0):
        self.base64Image = base64_image
        self.probability = probability
        self.islavalamp = round(probability) == 1


@application.route("/", methods=['POST', 'GET'])
def hello():
    model = LavaLampViewModel()
    if request.method == 'POST':
        image_upload = request.files['imageUpload']
        file_path = f"{secure_filename(image_upload.filename)}"
        image_upload.save(file_path)
        image_tools.normalize_image(file_path)
        base64_img = image_tools.get_base64_image(file_path, image_upload.content_type)
        probability = recognizer.recognize(file_path)
        model = LavaLampViewModel(base64_img, probability)
        os.remove(file_path)
    return render_template("index.html", model=model)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
