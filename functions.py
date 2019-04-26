from keras.backend.tensorflow_backend import set_session
import tensorflow as tf

def setTensorFlowSession():
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True  # fix cuDNN failed to initialize error
        #config.log_device_placement = True
        sess = tf.Session(config=config)
        set_session(sess)