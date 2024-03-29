#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 11:57:32 2019

@author: darshan
"""

import cv2
import glob
import numpy as np
import os.path as path
from scipy import misc
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Activation, Dropout,Dense, Conv2D, MaxPooling2D,Input, Convolution2D, Flatten
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from datetime import datetime
from keras.models import Model 
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from numpy import mean, std, argmax
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.image import ImageDataGenerator
#%matplotlib inline
import math
import os 
import numpy as np
from keras.optimizers import Adam
from sklearn.decomposition import NMF

import cv2
import glob
import numpy as np
import os.path as path
import matplotlib.pyplot as plt

# =============================================================================
# 
# =============================================================================
IMAGE_PATH = ''
file_paths = glob.glob(path.join(IMAGE_PATH, '*.bmp'))
len(file_paths)
file_paths[:10]
# Load the images
images = [cv2.imread(fpath) for fpath in file_paths]
images=[cv2.resize(image,(40,40)) for image in images ]
images = np.asarray(images)

# Get image size
image_size = np.asarray([images.shape[1], images.shape[2], images.shape[3]])
print(image_size)
# =============================================================================
# 
# =============================================================================
#Scaling

#images = scaling 

import os
import matplotlib.pyplot as plt
write_path = 'D:/study/Neww'
os.chdir(write_path)
no_noise = []
for i in range(len(scaling)):
    blur = cv2.GaussianBlur(scaling[i], (5, 5), 0)
    no_noise.append(blur)
    # storing the images into folder
    img = no_noise[i]
    plt.imshow(img)
    plt.savefig("{}".format(os.path.split(file_paths[i])[-1]))
    
# =============================================================================
#     Creating required directories
# =============================================================================
path1 = '/home/darshan/Desktop/IMAGES1/'
import glob
import os.path as path
import shutil
import os

file_paths1 = glob.glob(path.join(path1, '*.jpg'))

class_names = ['crazing','inclusion','patches','pitted_surface','rolled-in_scale','scratches']

           
os.chdir(path1)
list1 = os.listdir(path1)
for i in class_names:
    os.mkdir(path1+i)
    src = path1+i
    for j in list1:
        if j.startswith(i):
            shutil.move(j,src)
os.mkdir(path1+'test')

list2 = []

for i in class_names:
    os.chdir(path1 + i)
    src = path1 + i
    list2 = os.listdir(src)
    for j in list2[:30]:
        shutil.move(j,path1+'test')

list3 = []
os.mkdir(path1 + 'validate')
for i in class_names:
    os.chdir(path1 + i)
    src = path1 + i
    list2 = os.listdir(src)
    for j in list2[:15]:
        shutil.move(j,path1+'validate')

os.mkdir(path1+'train')
os.chdir(path1)
for i in class_names:
    shutil.move(path1+i,path1+'train')
    
os.chdir(path1+'test')
list1 = os.listdir(path1+'test')
for i in class_names:
    os.mkdir(path1+'test/'+i)
    src = path1+'test/' + i
    for j in list1:
        if j.startswith(i):
            shutil.move(j,src)
        
os.chdir(path1+'validate')
list1 = os.listdir(path1+'validate')
for i in class_names:
    os.mkdir(path1+'validate/'+i)
    src = path1+'validate/' + i
    for j in list1:
        if j.startswith(i):
            shutil.move(j,src)



# =============================================================================
# 
# =============================================================================
train_path = '/home/darshan/Projects_ipynb/Ireland/Project/gaussianblur2/train'
test_path  = '/home/darshan/Projects_ipynb/Ireland/Project/gaussianblur2/test'
validate_path = '/home/darshan/Projects_ipynb/Ireland/Project/gaussianblur2/validate'

classes = ['crazing','inclusion','patches','pitted_surface','rolled-in_scale','scratches']
train_batch = ImageDataGenerator(rescale=1./255).flow_from_directory(train_path,target_size=(224,224),classes=classes,batch_size=1530,color_mode= 'grayscale')
test_batch = ImageDataGenerator(rescale=1./255).flow_from_directory(test_path,target_size=(224,224),classes=classes,batch_size=180,color_mode= 'grayscale')
validate_batch = ImageDataGenerator(rescale=1./255).flow_from_directory(validate_path,target_size=(224,224),classes=classes,batch_size=90,color_mode= 'grayscale')

x_val, y_val = next(validate_batch)

img_train, label_train = next(train_batch)
print(img_train[1],label_train[1])
len(img_train)
type(img_train)
img_train.shape


img_train_f = []
for i in range(img_train.shape[0]) :
    x = img_train[i].flatten(order = 'F')
    img_train_f.append(x)
    
img_train_f = np.asarray(img_train_f)
img_train_f.shape    
model = NMF(n_components=6, init='random', random_state=0,tol = 5e-3)
    
W = model.fit_transform(img_train_f)
H = model.components_
matrix = np.dot(W,H)
matrix.shape
X_train = matrix
X_train.resize(1530,224,224,1)
X_train.shape


from keras.layers.normalization import BatchNormalization

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(224,224,1)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
#
model.add(Conv2D(64,(3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
#
model.add(Flatten())
#
## Fully connected layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(6))

model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

model.fit(X_train,label_train, steps_per_epoch=1,
          validation_data=(x_val,y_val), validation_steps=1, epochs=5, verbose=2)


model.predict_generator(test_batch,verbose=2)

train_batch.filenames









