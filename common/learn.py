from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.convolutional import MaxPooling2D
from keras.layers import Activation, Conv2D, Flatten, Dense,Dropout
from sklearn.model_selection import train_test_split
from PIL import Image
import numpy as np
import glob
import time
import os

class LearnImage():
  """ 画像の学習に関するクラス
  """

  def __init__(self, image_path="./img", image_size=50, test_size=0.10):
    self.__image_setting(image_path, image_size, test_size)

  def __image_setting(self, image_path, image_size, test_size):
    folder = os.listdir(image_path)
    folder.pop(-1)
    self.__dense_size = len(folder)
    
    x = []
    y = []
    for index, name in enumerate(folder):
        dir = f"{image_path}/" + name
        files = glob.glob(dir + "/*.jpg")
        for i, file in enumerate(files):
            image = Image.open(file)
            image = image.convert("RGB")
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            x.append(data)
            y.append(index)
    
    x = np.array(x)
    x = x.astype('float32')
    x = x / 255.0

    y = np.array(y)
    y = np_utils.to_categorical(y, self.__dense_size)
    self.__x_train, self.__x_test, self.__y_train, self.__y_test = train_test_split(x, y, test_size=test_size)

  def learn(self, json_name="mnist_mlp_model.json", widgets_name="mnist_mlp_weights.h5" , epochs=200, validation_split=0.2, optimizers="Adadelta"):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same',input_shape=self.__x_train.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(self.__dense_size))
    model.add(Activation('softmax'))
    model.summary()
    results = {}

    model.compile(loss='categorical_crossentropy', optimizer=optimizers, metrics=['accuracy'])
    start_time = time.time()
    results= model.fit(self.__x_train, self.__y_train, validation_split=validation_split, epochs=epochs)
    model_json_str = model.to_json()
    open(json_name, 'w').write(model_json_str)
    model.save_weights(widgets_name)

    score = model.evaluate(self.__x_test, self.__y_test, verbose=0)
    print(f'json_name: {json_name}')
    print(f'widgets_name: {widgets_name}')
    print('Loss:', score[0], '（損失関数値 - 0に近いほど正解に近い）') 
    print('Accuracy:', score[1] * 100, '%', '（精度 - 100% に近いほど正解に近い）') 
    print('Computation time（計算時間）:{0:.3f} sec（秒）'.format(time.time() - start_time))
