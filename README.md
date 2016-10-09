# Superpixel Convolutional Networks using Bilateral Inceptions

This is the code accompanying the following **ECCV 2016** publication:

--------

**Superpixel Convolutional Networks using Bilateral Inceptions**.

--------

This is developed and maintained by
[Raghudeep Gadde](https://ps.is.tuebingen.mpg.de/person/rgadde),
[Varun Jampani](https://ps.is.tuebingen.mpg.de/person/vjampani),
[Martin Kiefel](https://ps.is.tuebingen.mpg.de/person/mkiefel),
[Daniel Kappler](https://am.is.tuebingen.mpg.de/person/dkappler) and
[Peter V. Gehler](https://ps.is.tuebingen.mpg.de/person/pgehler).

Please visit the project website [http://segmentation.is.tue.mpg.de](http://segmentation.is.tue.mpg.de) for more details about the paper and overall methodology.

## Installation

The code provided in this repository relies on the same installation procedure as the one from [Caffe](http://caffe.berkeleyvision.org/).
Before you start with the `BilateralInception` code, please install all the requirements of Caffe by following the instructions from [this page](http://caffe.berkeleyvision.org/installation.html) first.
You will then be able to build Caffe with our code.
The repository also contains external code from [https://github.com/carlren/gSLICr](https://github.com/carlren/gSLICr) to compute the SLIC superpixels.

## Integration into Caffe

There are mainly two ways for integrating the additional layers provided by our library into Caffe:

* Dowloading a fresh clone of Caffe and patching it with our source files, so that you will be able to test the code with minimal effort.
* Patching an existing copy of Caffe, so that you can integrate our code with your own development on Caffe.

### Downloading and Patching

This can be done just by the following commands:
```
cd $bilateralinceptions
mkdir build
cd build
cmake ..
```

This will configure the project, you may then run:

* for building the project
  ```
  make 
  ```
  This will clone a Caffe version from the main Caffe repository into the `build` folder and compiles together with our newly added layers.
* for running the tests, including the ones of the BilateralInceptions:
  ```
  make runtest
  ```

  (this follows the same commands as for Caffe)

**Notes**

* Our code has been tested with revision `a2179bdec004bd1cc2edfc8cf1fbc5b07a117de6` of Caffe, and this
is the version that is cloned. You may change the version by passing the option `CAFFE_VERSION` on the command line of
`cmake`:

        cmake -DCAFFE_VERSION=some_hash_or_tag ..

such as `cmake -DCAFFE_VERSION=HEAD ..`.

* If you want to use your fork instead of the original Caffe repository, you may provide the option `CAFFE_REPOSITORY` on the `cmake` command line (it works exactly as for `CAFFE_VERSION`).
* Any additional command line argument you pass to `cmake` will be forwarded to Caffe, except for those
  used directly by our code:

      cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DBOOST_ROOT=../osx/boost_1_60_0/
        -DBoost_ADDITIONAL_VERSIONS="1.60\;1.60.0" ..

### Patching an existing Caffe version

#### Automatic CMAKE way
You may patch an existing version of Caffe by providing the `CAFFE_SRC` on the command line
```
cd $bilateralinceptions
mkdir build
cd build
cmake -DCAFFE_SRC=/your/caffe/local/copy ..
```

This will add the files of the BilateralNN to the source files of the existing Caffe copy, but **will also
overwrite caffe.proto** (a backup is made in the same folder).
The command will also create a build folder local to the BilateralInception repository (inside the `build` folder on the previous example): you may use this one
or use any previous one, Caffe should automatically use the sources of the BilateralInceptions.

#### Manual way
The above patching that is performed by `cmake` is rather a copying of the files from the folder of the `bilateralinceptions` to the
corresponding folders of Caffe. Caffe will then add the new files into the project.

Alternatively, you can manually copy all but `caffe.proto` source files in `bilateralinceptions` folder to the corresponding locations in your Caffe repository. Then, for merging the `caffe.proto` file of `bilateralinceptions` to your version of the `caffe.proto`:

1. the copy the lines 407-410 and 1137-1177 in `caffe.proto` to the corresponding `caffe.proto` file in the destination Caffe repository.
2. Change the parameter IDs for `PdistParameter`, `SmearParameter`, `SpixelFeatureParameter` and `InterpParameter` based on the next available `LayerParameter` ID in your Caffe.

## Example Usage
To use the provided code and replicate the results on the VOC2012 dataset, 

#### Preparing the data
Run the get_voc.sh (It downloads the VOC2012 dataset in `data` folder.)
```
cd $bilateralinceptions/scripts
sh get_voc.sh
```

#### Computing superpixels
 Next, compute the SLIC superpixels using the following command 
```
cd $bilaretalinceptions
./build/tools/compute_superpixels path_to_image_directory path_to_image_list path_to_save_superpixel_indices_directory 
```
example:
```
./build/tools/compute_superpixels data/VOCdevkit/VOC2012/JPEGImages/ data/reducedval.txt results/spix_inces/ 
```

#### Applying the provided models
Using the Python scripts given in the folder `$bilateralinceptions/scripts` which rely on the Python extensions of Caffe.
```
cd $bilaretalinceptions
python scripts/do_segmentation.py --protoxt path_to_prototxt --caffemodel path_to_caffemodel --image_dir path_to_image_directory --image_list path_to_image_list --superpixel_dir path_to_superpixel_indices_directory --result_dir path_to_save_results_directory
```
example:
```
python scripts/do_segmentation.py --prototxt models/deeplab_coco_largefov_bi6_2_bi7_6_deploy.prototxt --caffemodel models/deeplab_coco_largefov_bi6_2_bi7_6.caffemodel --image_dir data/VOCdevkit/VOC2012/JPEGImages/ --image_list data/reducedval.txt --superpixel_dir results/spix_indices/ --result_dir results/segmentations/
```

#### Evaluating the results
We provide a python script to compute the IoU accuracy of the obtained segmentations.
```
cd $bilaretalinceptions
python scripts/eval_segmentation.py --result_dir path_to_result_directory --image_list path_to_image_list --gt_dir path_to_ground_truth_directory
```
example:
```
python scripts/eval_segmentation.py --result_dir results/segmentations/ --image_list data/reducedval.txt --gt_dir data/VOCdevkit/VOC2012/SegmentationClass/
```

You would find on [http://segmentation.is.tue.mpg.de](http://segmentation.is.tue.mpg.de) a detailed description of the layer usage and an example.

## Citations

Please consider citing the following papers if you make use of this work and/or the corresponding code:

```
@inproceedings{gadde2015superpixel,
	title = {Superpixel Convolutional Networks using Bilateral Inceptions},
	author = {Gadde, Raghudeep and Jampani, Varun and Kiefel, Martin and Gehler, Peter V},
	booktitle = {Computer Vision - ECCV},
	year = {2016}
}
```
and the GPU implementation of SLIC superpixels. Please do not forget citing the original SLIC superpixel paper. 
```
@article{gSLICr_2015,
    author = {Carl Yuheng Ren and Victor Adrian Prisacariu and Ian D Reid},
    title = "{gSLICr: SLIC superpixels at over 250Hz}",
    journal = {ArXiv e-prints},
    eprint = {1509.04232},
    year = 2015,
    month = sep
}
```
```
@article{achanta2012slic,
    author = {Achanta, Radhakrishna and Shaji, Appu and Smith, Kevin and Lucchi, Aurelien and Fua, Pascal and Susstrunk, Sabine},
    title = {SLIC Superpixels Compared to State-of-the-Art Superpixel Methods},
    journal = {IEEE Trans. Pattern Anal. Mach. Intell.},
    volume = {34},
    number = {11},
    month = nov,
    year = {2012},
    pages = {2274--2282},
    numpages = {9}
} 
```
