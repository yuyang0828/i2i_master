import numpy as np
import cv2
from PIL import Image

from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Flatten, Reshape
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Conv2D, Conv2DTranspose, Concatenate
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.models import Model

from tensorflow.keras.initializers import RandomNormal
from keras_contrib.layers.normalization.instancenormalization import InstanceNormalization

# generator a resnet block


def resnet_block(n_filters, input_layer):
    # weight initialization
    init = RandomNormal(stddev=0.02)
    # first layer convolutional layer
    g = Conv2D(n_filters, (3, 3), padding='same',
               kernel_initializer=init)(input_layer)
    g = InstanceNormalization(axis=-1)(g)
    g = Activation('relu')(g)
    # second convolutional layer
    g = Conv2D(n_filters, (3, 3), padding='same', kernel_initializer=init)(g)
    g = InstanceNormalization(axis=-1)(g)
    # concatenate merge channel-wise with input layer
    g = Concatenate()([g, input_layer])
    return g


def define_generator(image_shape=(128, 128, 3), n_resnet=2):
    # weight initialization
    init = RandomNormal(stddev=0.02)
    # image input
    in_image = Input(shape=image_shape)
    # c7s1-64
    g = Conv2D(64, (7, 7), padding='same', kernel_initializer=init)(in_image)
    g = InstanceNormalization(axis=-1)(g)
    g = Activation('relu')(g)
    # d128
    g = Conv2D(128, (3, 3), strides=(2, 2),
               padding='same', kernel_initializer=init)(g)
    g = InstanceNormalization(axis=-1)(g)
    g = Activation('relu')(g)
    # d256
    g = Conv2D(256, (3, 3), strides=(2, 2),
               padding='same', kernel_initializer=init)(g)
    g = InstanceNormalization(axis=-1)(g)
    g = Activation('relu')(g)
    # R256
    for _ in range(n_resnet):
        g = resnet_block(256, g)
    # u128
    g = Conv2DTranspose(128, (3, 3), strides=(
        2, 2), padding='same', kernel_initializer=init)(g)
    g = InstanceNormalization(axis=-1)(g)
    g = Activation('relu')(g)
    # u64
    g = Conv2DTranspose(64, (3, 3), strides=(
        2, 2), padding='same', kernel_initializer=init)(g)
    g = InstanceNormalization(axis=-1)(g)
    g = Activation('relu')(g)
    # c7s1-3
    g = Conv2D(3, (7, 7), padding='same', kernel_initializer=init)(g)
    g = InstanceNormalization(axis=-1)(g)
    out_image = Activation('tanh')(g)
    # define model
    model = Model(in_image, out_image)
    return model


def load_weights(g_A2B, g_B2A):
    g_A2BH5 = 'g_A2B.h5'
    g_B2AH5 = 'g_B2A.h5'
    model_dir_in = 'gan_weights/'

    try:
        g_A2B.load_weights(model_dir_in + g_A2BH5)
        g_B2A.load_weights(model_dir_in + g_B2AH5)
        print('loaded model weights')
        return True
    except Exception as e:
        print('Failed loading existing training data.')
        print(e)
        return False


def ganVersion():
    g_A2B = define_generator()
    g_B2A = define_generator()

    load_weights(g_A2B, g_B2A)

    IMAGE_SIZE = (128, 128)
    # a - a.jpg
    # imageA = '../input/myanimalfaces/n02111889/n02111889/n02111889_4093.JPEG_116_106_294_283.jpg'
    imageA = '../input/myanimalfaces/n02111889/n02111889/n02111889_5474.JPEG_142_55_322_228.jpg'

    # b - b.jpg
    # imageB = '../input/myanimalfaces/n02096585/n02096585/n02096585_1439.JPEG_168_99_344_272.jpg' #good
    # image = '../input/myanimalfaces/n02096585/n02096585/n02096585_358.JPEG_63_51_237_238.jpg' not good
    # image = '../input/myanimalfaces/n02096585/n02096585/n02096585_1042.JPEG_144_33_339_246.jpg' soso
    # image = '../input/myanimalfaces/n02096585/n02096585/n02096585_8818.JPEG_132_39_327_239.jpg' soso
    imageB = '../input/myanimalfaces/n02096585/n02096585/n02096585_269.JPEG_51_134_169_265.jpg'  # good

    imgA = cv2.imread(imageA)
    # img = cv2.flip(img, 1)
    imgA = cv2.resize(imgA, IMAGE_SIZE).astype('float32')/255.0
    imgA = np.expand_dims(imgA, 0)
    predictions_AB = g_A2B.predict(imgA)

    imgB = cv2.imread(imageB)
    imgB = cv2.resize(imgB, IMAGE_SIZE).astype('float32')/255.0
    imgB = np.expand_dims(imgB, 0)
    predictions_BA = g_B2A.predict(imgB)

    formatted = (predictions_AB[0] * 255 /
                 np.max(predictions_AB[0])).astype('uint8')
    imgAB = Image.fromarray(formatted)
    imgAB.save('ab_temp.jpg')

    formatted2 = (predictions_BA[0] * 255 /
                  np.max(predictions_BA[0])).astype('uint8')
    imgBA = Image.fromarray(formatted2)
    imgBA.save('ba_temp.jpg')

    # ======= fusion
    im = cv2.resize(cv2.imread(imageA), IMAGE_SIZE)
    obj = cv2.imread("ab_temp.jpg")

    # Create an all white mask
    mask = 255 * np.ones(obj.shape, obj.dtype)

    # The location of the center of the src in the dst
    width, height, channels = im.shape
    center = (height//2, width//2)

    obj = cv2.medianBlur(obj, 3)

    # Seamlessly clone src into dst and put the results in output
    # normal_clone = cv2.seamlessClone(obj, im, mask, center, cv2.NORMAL_CLONE)
    mixed_clone = cv2.seamlessClone(
        obj, im, mask, center, cv2.MONOCHROME_TRANSFER)
    cv2.imwrite('ab.jpg', mixed_clone)

    # ========

    im2 = cv2.resize(cv2.imread(imageB), IMAGE_SIZE)
    obj2 = cv2.imread("ba_temp.jpg")

    mask2 = 255 * np.ones(obj2.shape, obj2.dtype)

    width2, height2, channels2 = im2.shape
    center2 = (height2//2, width2//2)

    obj2 = cv2.medianBlur(obj2, 3)

    mixed_clone2 = cv2.seamlessClone(
        obj2, im2, mask2, center2, cv2.MONOCHROME_TRANSFER)
    cv2.imwrite('ba.jpg', mixed_clone2)


ganVersion()
