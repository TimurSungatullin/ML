import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


def mnist_cnn_model(input_shape):
    model = Sequential()
    model.add(Conv2D(64, (3, 3), input_shape=input_shape, activation='relu'))
    model.add(Conv2D(15, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def mnist_mlp_train(model, input_shape):
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    train_data = x_train.reshape(x_train.shape[0], *input_shape)
    test_data = x_test.reshape(x_test.shape[0], *input_shape)

    num_classes = 10
    train_labels_cat = keras.utils.to_categorical(y_train, num_classes)
    test_labels_cat = keras.utils.to_categorical(y_test, num_classes)

    train_data = train_data.astype('float32')
    test_data = test_data.astype('float32')

    train_data /= 255.0
    test_data /= 255.0

    model.fit(train_data, train_labels_cat, epochs=5, batch_size=128, verbose=1,
              validation_data=(test_data, test_labels_cat))


def main():
    input_shape = 28, 28, 1
    model = mnist_cnn_model(input_shape)
    mnist_mlp_train(model, input_shape)
    model.save('mnist.h5')
    return model


def get_model(file_name='mnist.h5', is_new=False):
    if is_new:
        return main()
    try:
        model = keras.models.load_model(file_name)
    except Exception as e:
        print(e)
        model = main()
    return model


if __name__ == '__main__':
    main()
