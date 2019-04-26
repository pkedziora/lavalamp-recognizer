from keras import models
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from functions import *
import sys

print(sys.argv[1:])

setTensorFlowSession()
IMAGE_SIZE = 300

model = load_model('lavalamp_model.h5')

img_path = '/home/pakedziora/Downloads/006.jpg'

img = image.load_img(img_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
img_tensor = image.img_to_array(img)
img_tensor = np.expand_dims(img_tensor, axis=0)
img_tensor /= 255.

result = model.predict(img_tensor);
roundedResult = np.round(result).astype(int)
print(f"Result: {result}")
if roundedResult == 1:
    print("It is lava lamp!")
else:
    print("Not a lava lamp!")
