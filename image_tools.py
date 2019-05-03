from PIL import Image, ExifTags
import base64


def get_base64_image(file_path):
    prefix = "data:image/jpeg;charset=utf-8;base64,"
    with open(file_path, "rb") as imageFile:
        encoded_string = base64.b64encode(imageFile.read()).decode("utf-8")
    return f"{prefix}{encoded_string}"


def normalize_image(file_path):
    image=Image.open(file_path)
    if "_getexif" in dir(image) and image._getexif() is not None:
        exif = dict((ExifTags.TAGS[k], v) for k, v in image._getexif().items() if k in ExifTags.TAGS)
        if "Orientation" in exif:
            if exif["Orientation"] == 3 : 
                image = image.rotate(180, expand=True)
            elif exif["Orientation"] == 6 : 
                image = image.rotate(270, expand=True)
            elif exif["Orientation"] == 8 : 
                image = image.rotate(90, expand=True)

    image.convert('RGB')
    new_width = 400
    percent = (new_width/float(image.size[0]))
    new_height = int((float(image.size[1])*float(percent)))
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    image.save(file_path, format="JPEG")