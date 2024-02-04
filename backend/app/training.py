import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf 
import keras
import cv

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout ,BatchNormalization
from keras.optimizers import Adam
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from keras.callbacks import ReduceLROnPlateau
from glob import glob
import matplotlib.image as mpimg
from keras.preprocessing import image


import os

def main():
    #for dirname, _, filenames in os.walk('/'):
    #     for filename in filenames:
    #        print(os.path.join(dirname, filename))

    # Define the paths to the train, test, and val folders
    train_path = 'data/train'
    test_path = 'data/test'
    val_path = 'data/val'

    # Display the number of images in each category
    print(f"Number of Normal images in training set: {len(os.listdir(os.path.join(train_path, 'NORMAL')))}")
    print(f"Number of Pneumonia images in training set: {len(os.listdir(os.path.join(train_path, 'PNEUMONIA')))}")

    # Display an example image from each category
    normal_img_path = glob(os.path.join(train_path, 'NORMAL', '*.jpeg'))[0]
    pneumonia_img_path = glob(os.path.join(train_path, 'PNEUMONIA', '*.jpeg'))[0]

    normal_img = mpimg.imread(normal_img_path)
    pneumonia_img = mpimg.imread(pneumonia_img_path)

    # Plot the images
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(normal_img, cmap='gray')

    plt.title('Normal X-Ray')

    plt.subplot(1, 2, 2)
    plt.imshow(pneumonia_img, cmap='gray')
    plt.title('Pneumonia X-Ray')

    plt.show()

    img_width, img_height = 150, 150

    # Create data generators for train, test, and val sets
    train_datagen = ImageDataGenerator(rescale=1./255,
                                    shear_range=0.2,
                                    zoom_range=0.2,
                                    horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(train_path,
                                                        target_size=(img_width, img_height),
                                                        batch_size=32,
                                                        class_mode='binary')

    test_generator = test_datagen.flow_from_directory(test_path,
                                                    target_size=(img_width, img_height),
                                                    batch_size=32,
                                                    class_mode='binary')

    val_generator = test_datagen.flow_from_directory(val_path,
                                                    target_size=(img_width, img_height),
                                                    batch_size=32,
                                                    class_mode='binary')

    model = Sequential()
    model.add(Conv2D(16, (3, 3), input_shape=(img_width, img_height, 3), activation='relu' , strides = 1 , padding = 'same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2,2) , strides = 2 , padding = 'same'))
    model.add(Conv2D(32 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
    model.add(Dropout(0.1))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2,2) , strides = 2 , padding = 'same'))
    model.add(Conv2D(64 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2,2) , strides = 2 , padding = 'same'))
    model.add(Conv2D(128 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
    model.add(Dropout(0.4))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2,2) , strides = 2 , padding = 'same'))
    model.add(Conv2D(256 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2,2) , strides = 2 , padding = 'same'))
    model.add(Flatten())
    model.add(Dense(256, activation = 'relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.summary()

    model.compile(loss='binary_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

    from keras.callbacks import EarlyStopping
    #Define early stopping callback
    learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', patience = 5, verbose=1,factor=0.3, min_lr=0.000001)
    early_stopping_monitor = EarlyStopping(patience = 3, monitor = "val_accuracy", mode="max", verbose = 2)

    # Train the model with early stopping
    history = model.fit(train_generator,
                        batch_size = 32,
                        epochs=22,
                        steps_per_epoch=len(train_generator),
                        validation_data=val_generator,
                        validation_steps=len(val_generator),
                        callbacks = [learning_rate_reduction,early_stopping_monitor]
                    )


    # Load an image for prediction
    img_path = 'data/person1_bacteria_1.jpeg'
    img = image.load_img(img_path, target_size=(img_width, img_height))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize the image

    # Make prediction
    prediction = model.predict(img_array)
    print(f"Probability of Pneumonia: {prediction[0][0]}")

    model.save('pneumonia_detection_model.keras')


def retrain(file):
    img_width, img_height = 150, 150

    img = image.load_img(file.filename, target_size=(img_width, img_height))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize the image

    new_model = tf.keras.models.load_model('../models/pneumonia_detection_model.keras')

    prediction = new_model.predict(img_array)
    print(f"Probability of Pneumonia: {prediction[0][0]}")
    
    return prediction


