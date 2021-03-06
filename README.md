# Lava lamp recognizer [![Build Status](https://travis-ci.org/pkedziora/lavalamp-recognizer.svg?branch=master)](https://travis-ci.org/pkedziora/lavalamp-recognizer)
Is it a lava lamp? Image binary classification with Keras and Tensorflow

## Online Playground
[https://lavalamp.kedziora.dev/](https://lavalamp.kedziora.dev/)

## How-to
* To install dependencies
    * pip3 install -r requirements.txt

* To run lavalamp recognizer web app without training new model (trained model will be downloaded on first run from aws s3)
    * python3 application.py
    * Go to http://0.0.0.0:5000/

* To download training images using bing search api
    * Add api key for bing search in search_images/api_keys/bing_search.txt
    * cd search_images && python3 search_images.py [searchterm] [maxcount] 
        * (e.g. cd search_images &&  python3 search_images.py "lava lamp" 1000)
    * Images will be downloaded to search_images/download
    * Move downloaded images to data folder into appropriate catagory

* To train new model
    * **Note: It is recommended to configure Tensorflow NVIDIA GPU support for your platform first**
    * Add images to /data folder (train, validation and test images, with 2 categories each: lavalamps, another)
    * Modify train_model.py batch_size, steps_per_epoch and epochs as required
    * python3 train_model.py
    * Model will be saved to lavalamp_model_current.h5
    * For the new model to be picked up by the Flask web application, rename it to lavalamp_model.h5