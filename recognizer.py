from keras import models
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from functions import *

setTensorFlowSession()
IMAGE_SIZE = 300

model = load_model('lavalamp_model.h5')
global graph
graph = tf.get_default_graph() 

def recognize(img_path):
    print(f"IMAGE  PATH: {img_path}")
    img = image.load_img(img_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    with graph.as_default():
        result = model.predict(img_tensor);
    roundedResult = np.round(result).astype(int)[0][0]
    return np.asscalar(roundedResult)
