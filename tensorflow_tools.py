from keras.backend.tensorflow_backend import set_session
import tensorflow as tf
import requests
from clint.textui import progress
import os.path


def set_tensorflow_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True  # fix cuDNN failed to initialize error
    sess = tf.Session(config=config)
    set_session(sess)


def download_model_if_required(url, local_path):
    if os.path.isfile(local_path):
        print(f"{local_path} exists. Skipping downloading model")
        return

    print(f"{local_path} does not exist. Downloading model")
    r = requests.get(url, stream=True)
    with open(local_path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                    f.write(chunk)
                    f.flush()