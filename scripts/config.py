import sys
CAFFE_ROOT = '../build/tmp_caffe_clone/src/CaffeUpstream/'
sys.path.insert(0, CAFFE_ROOT + 'python')
import caffe
caffe.set_mode_gpu()
