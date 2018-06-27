from keras.applications.vgg16 import VGG16
from keras.layers import  Flatten, Dense, Conv2D, MaxPooling2D, Dropout
from keras.models import Sequential
import numpy as np
from keras.optimizers import SGD, RMSprop


def get_model(lr=0.01, w=64, h=64, train_upper_layers=True):
    vgg_model = VGG16(input_shape=(w, h, 3), weights='imagenet',
                      include_top=False)

    model = Sequential()
    block1_conv1 = Conv2D(64, (3, 3), input_shape=(w,h,6),
                          padding='same', name='block1_conv1',
                          activation='relu',
                          trainable=train_upper_layers)
    model.add(block1_conv1)
    model.add(Conv2D(64, (3,3), padding='same', name='block1_conv2',
                          activation='relu',
                     trainable=train_upper_layers))
    model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2), name='block1_pool'))

    model.add(Conv2D(128, (3,3), padding='same', name='block2_conv1',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(Conv2D(128, (3,3), padding='same', name='block2_conv2',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2), name='block2_pool'))

    model.add(Conv2D(256, (3,3), padding='same', name='block3_conv1',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(Conv2D(256, (3,3), padding='same', name='block3_conv2',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(Conv2D(256, (3,3), padding='same', name='block3_conv3',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2), name='block3_pool'))

    model.add(Conv2D(512, (3,3), padding='same', name='block4_conv1',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(Conv2D(512, (3,3), padding='same', name='block4_conv2',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(Conv2D(512, (3,3), padding='same', name='block4_conv3',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2), name='block4_pool'))

    model.add(Conv2D(512, (3,3), padding='same', name='block5_conv1',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(Conv2D(512, (3,3), padding='same', name='block5_conv2',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(Conv2D(512, (3,3), padding='same', name='block5_conv3',
                     activation='relu',
                     trainable=train_upper_layers))
    model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2), name='block5_pool'))

    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(2096, activation='relu'))
    model.add(Dropout(0.5))
    #model.add(Dense(4096, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # --- set the fixed weights ---
    W, bias = vgg_model.layers[1].get_weights()
    W = np.concatenate((W,W), axis=2)
    block1_conv1.set_weights([W, bias])
    # -----------------------------

    for i in range(1, len(vgg_model.layers)-1):
        model.layers[i].set_weights(vgg_model.layers[i+1].get_weights())


    return model
