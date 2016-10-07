import numpy as np
import os
import sys
from PIL import Image
import scipy.io
import argparse

def evalVOC(result_label_folder, image_list_file=None, gt_label_folder=None):

    max_label = 21
    class_ious = np.zeros((max_label, 1))
    overall_iou = 0
    overall_accuracy = 0

    tp = np.zeros((max_label))
    fp = np.zeros((max_label))
    fn = np.zeros((max_label))

    img_tp = 0
    img_pixels = 0

    with open(image_list_file) as list_f:
        for count, imgname in enumerate(list_f):
            imgname = imgname[:-1]
            print str(count) + ". Image Name: " + imgname

            gt_file = gt_label_folder + imgname + '.png'
            result_file = result_label_folder + imgname + '.png'

            gt_image = Image.open(gt_file)

            gt_labels = np.array(gt_image)
            if os.path.isfile(result_file):
                result_labels = np.array(Image.open(result_file))
            else: 
                result_file = result_label_folder + imgname + '.npy'
                result_labels = np.load(result_file)
                print result_labels.shape, gt_labels.shape
                result_labels = result_labels[0:gt_labels.shape[0],0:gt_labels.shape[1]]#.argmax(axis=0)
                #result_labels = scipy.io.loadmat(result_file)
            

            if (np.max(result_labels) > (max_label - 1) and np.max(result_labels)!=255):
                print('Result has invalid labels: ', np.max(result_labels))
            else:
                # For each class
                for class_id in range(0, max_label):
                    class_gt = np.equal(gt_labels, class_id)
                    class_result = np.equal(result_labels, class_id)
                    # import pdb; pdb.set_trace();
                    class_result[np.equal(gt_labels, 255)] = 0
                    tp[class_id] = tp[class_id] +\
                        np.count_nonzero(class_gt & class_result)
                    fp[class_id] = fp[class_id] +\
                        np.count_nonzero(class_result & ~class_gt)
                    fn[class_id] = fn[class_id] +\
                        np.count_nonzero(~class_result & class_gt)

                img_result = result_labels
                img_gt = gt_labels
                img_result[np.equal(result_labels, 255)] = 0
                img_gt[np.equal(gt_labels, 255)] = 0
                img_tp = img_tp + np.count_nonzero(np.equal(img_gt,
                                                            img_result))
                img_pixels = img_pixels + np.size(img_gt)

    for class_id in range(0, max_label):
        class_ious[class_id] = tp[class_id] / (tp[class_id] +
                                               fp[class_id] + fn[class_id])

    overall_iou = np.mean(class_ious)
    overall_accuracy = img_tp / (img_pixels * 1.0)

    print(result_label_folder)
    print('Class IOUs:')
    print(class_ious)
    print('Overall IOU: ')
    print(overall_iou)
    print('Overall Accuracy: ')
    print(overall_accuracy)
    file_ = open(result_label_folder + '/scores_varun.txt','w')
    file_.write(result_label_folder + '\n')
    file_.write('Overall IOU: ' + str(overall_iou) + '\n' +
                'Overall Accuracy: ' + str(overall_accuracy) + '\n' + 
                'Class wise iou: ' + str(class_ious.T) + '\n'
                )
    file_.close()
    return overall_iou


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--result_dir', type=str, required=True)
    parser.add_argument('--image_list', type=str, required=True)
    parser.add_argument('--gt_dir', type=str, required=True)

    var_args = parser.parse_args()
    evalVOC(var_args.result_dir,
            var_args.image_list,
            var_args.gt_dir)

if __name__ == '__main__':
    main()
