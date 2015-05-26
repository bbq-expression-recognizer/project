import struct
import numpy as np
from PIL import Image, ImageOps
from os import path

# folder to save images and listfile
imgpath = 'train_mnist'
# prefix for image name
imgprefix = 'mnist_train_'

imgidxname = 'train-images-idx3-ubyte'
labelidxname = 'train-labels-idx1-ubyte'

# open image idx, label idx, listfile
with open(imgidxname, 'rb') as imgidx, open(labelidxname, 'rb') as labelidx, open(path.join(imgpath, 'listfile.txt'), 'w') as listfile:
    # read headers
    magic, n, r, c = struct.unpack('>4I', imgidx.read(16))
    magic, n = struct.unpack('>2I', labelidx.read(8))
    for i in xrange(n):
        imgname = '%s%05d.png' % (imgprefix, i)
        print 'Processing %s...' % imgname
        # read image as tuple from file
        imgtup = struct.unpack('%dB' % (r * c), imgidx.read(r * c))
        # convert into numpy array
        imgarr = np.asarray(imgtup, np.uint8).reshape((r, c))
        # convert into PIL image and invert color
        img = ImageOps.invert(Image.fromarray(imgarr, 'L'))
        # save image
        img.save(path.join(imgpath, imgname))
        # read label from file
        label = struct.unpack('B', labelidx.read(1))[0]
        # write filename and label to listfile
        listfile.write('%s %d\n' % (imgname, label))
