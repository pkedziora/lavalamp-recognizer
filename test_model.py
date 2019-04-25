from keras.preprocessing.image import ImageDataGenerator
from keras import models
from keras.models import load_model
import numpy as np
from functions import *

IMAGE_SIZE=300

setTensorFlowSession()
model = load_model('lavalamp_model.h5')

test_dir = 'data/test'
test_imagegenerator = ImageDataGenerator(rescale=1./255)
test_generator = test_imagegenerator.flow_from_directory(
        test_dir,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=1,
        shuffle = False,
        class_mode='binary')

filenames = test_generator.filenames
sampleCount = len(filenames)

test_loss, test_acc = model.evaluate_generator(test_generator, steps=sampleCount)
result = model.predict_generator(test_generator, steps=sampleCount, verbose = 1)

roundedResults = np.round(result).astype(int)

for i, valResult in np.ndenumerate(roundedResults):
    if valResult != test_generator.classes[i[0]]:
        print(f"{test_generator.filenames[i[0]]} should be of class {test_generator.classes[i[0]]} but was {roundedResults[i[0]]}")

print('test acc:', test_acc)