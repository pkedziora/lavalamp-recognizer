from keras import models
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import tensorflow_tools as tfTools
import tensorflow as tf

IMAGE_SIZE = 300
LOCAL_MODEL = "lavalamp_model.h5"
REMOTE_MODEL = "https://s3-eu-west-1.amazonaws.com/lavalamp-recognizer/lavalamp_model.h5"

tfTools.setTensorFlowSession()
tfTools.download_model_if_required(REMOTE_MODEL, LOCAL_MODEL)

model = load_model(LOCAL_MODEL)
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

    return np.asscalar(result[0][0])

