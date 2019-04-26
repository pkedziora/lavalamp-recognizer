from keras.applications import VGG16
from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from functions import *

MODEL_FILENAME = 'lavalamp_model.h5'
IMAGE_SIZE = 300

setTensorFlowSession()
conv_base = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3))


#Build model
model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.summary()

conv_base.trainable = False

#Compile model
model.compile(loss='binary_crossentropy',
              optimizer=optimizers.RMSprop(lr=2e-5),
              metrics=['acc'])

#Create data generators
train_dir = 'data/train'
train_imagegenerator = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest')
train_generator = train_imagegenerator.flow_from_directory(
        train_dir,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=16,
        class_mode='binary')

validation_dir = 'data/validation'
validation_imagegenerator = ImageDataGenerator(rescale=1./255)
validation_generator = validation_imagegenerator.flow_from_directory(
        validation_dir,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=10,
        class_mode='binary')

checkpoint = ModelCheckpoint(MODEL_FILENAME, monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='max')
callbacks_list = [checkpoint]

#train model
history = model.fit_generator(
      train_generator,
      steps_per_epoch=200,
      epochs=100,
      validation_data=validation_generator,
      validation_steps=50,
      callbacks=callbacks_list,
      workers=8)

#test model
test_dir = 'data/test'
test_imagegenerator = ImageDataGenerator(rescale=1./255)
test_generator = test_imagegenerator.flow_from_directory(
        test_dir,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=10,
        class_mode='binary')

test_loss, test_acc = model.evaluate_generator(test_generator, steps=50)
print('test accuracy:', test_acc)