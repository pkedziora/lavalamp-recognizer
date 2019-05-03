from keras.backend.tensorflow_backend import set_session
import tensorflow as tf
import requests
from clint.textui import progress
import os.path

def setTensorFlowSession():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True  # fix cuDNN failed to initialize error
    #config.log_device_placement = True
    sess = tf.Session(config=config)
    set_session(sess)

def download_model_if_required(url, localPath):
    if os.path.isfile(localPath):
        print(f"{localPath} exists. Skipping downloading model")
        return

    print(f"{localPath} does not exist. Downloading model")
    r = requests.get(url, stream=True)
    with open(localPath, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                    f.write(chunk)
                    f.flush()