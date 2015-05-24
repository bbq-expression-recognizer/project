import numpy as np
import matplotlib.pyplot as plt

caffe_root = '../caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')

import caffe

MODEL_FILE = 'bbq_deploy.prototxt'
PRETRAINED = 'bbqall_iter_10000.caffemodel'
IMAGE_FILE = 'imgall/2_em_3_1.png'

caffe.set_mode_cpu()
net = caffe.Classifier(MODEL_FILE, PRETRAINED)

input_image = caffe.io.load_image(IMAGE_FILE)
prediction = net.predict([input_image])
print prediction[0].shape
print prediction[0].argmax()
