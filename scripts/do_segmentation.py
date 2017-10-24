
import numpy as np
import scipy.io as sio
import os
import time
from PIL import Image as PILImage
import cv2
import argparse

from config import *
# from eval_seg import evalVOC

def do_segmentation(prototxt, caffe_model, image_dir, 
                    image_list, spixel_dir, out_dir):

    net = caffe.Net(prototxt, caffe_model, caffe.TEST)
    print('Model loaded from ' + caffe_model)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    mean_vec = np.array([103.939, 116.779, 123.68], dtype=np.float32)
    reshaped_mean_vec = mean_vec.reshape(1, 1, 3)

    with open(image_list) as list_f:
        for count, imgname in enumerate(list_f):
            imgname = imgname[:-1]
            print(str(count) + ". Image Name: " + imgname + " " + \
                  time.strftime('%l:%M:%S%p %Z on %b %d, %Y'))

            img_fname = image_dir + imgname + '.jpg'
            im = 255 * caffe.io.load_image(img_fname)
            im = np.array(im).astype(np.uint8)

            width, height, channels = im.shape

            # Pad as necessary
            pad_h = np.max([0, 513 - height])
            pad_w = np.max([0, 513 - width])

            # Rearrange channels to form BGR and subtract mean
            im = im[:,:,::-1]
            im = im - reshaped_mean_vec
            im = np.pad(im, pad_width=((0, pad_w), (0, pad_h), (0, 0)),
                        mode = 'constant', constant_values = 0)
            im = np.expand_dims(np.transpose(im,(2,0,1)), axis=0)

            spixel_fname = spixel_dir + imgname + '.pgm'
            spixel_values = cv2.imread(spixel_fname, cv2.IMREAD_UNCHANGED)
            spixel_index = np.array(spixel_values).astype(np.float32)
            spixel_index = np.lib.pad(spixel_index, ((0, pad_w), (0, pad_h)),
                                      'constant', constant_values=100000)
            spixel_index = np.expand_dims(np.expand_dims(spixel_index, axis=0),
                                          axis = 0)

            result = net.forward_all(img=im, spixel_index=spixel_index)

            result = np.squeeze(result['prob_image'])#[:,0:height, 0:width]
            seg_map = result.argmax(axis=0)[0:width, 0:height]
            seg_map = PILImage.fromarray(np.uint8(seg_map))
            seg_map.putpalette(pallete)
            seg_map.save(out_dir + '/' + imgname + '.png')

    #meaniou = evalVOC(out_dir, image_list_file=image_list)
    return 

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--prototxt', type=str, required=True)
    parser.add_argument('--caffemodel', type=str, required=True)
    parser.add_argument('--image_dir', type=str, required=True)
    parser.add_argument('--image_list', type=str, required=True)
    parser.add_argument('--superpixel_dir', type=str, required=True)
    parser.add_argument('--result_dir', type=str, required=True)

    var_args = parser.parse_args()
    do_segmentation(var_args.prototxt,
                    var_args.caffemodel,
                    var_args.image_dir,
                    var_args.image_list,
                    var_args.superpixel_dir,
                    var_args.result_dir)

if __name__ == '__main__':
    main()
