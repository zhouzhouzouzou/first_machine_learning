# -*- coding: utf-8 -*-
# udacity深度学习课程
# written by Luckky_Zhou
# 2018/2/6

from __future__ import print_function
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display,Image
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle

image_size = 28  # Pixel width and height.
pixel_depth = 255.0  # Number of levels per pixel.

def load_letter(folder, min_num_images):
    """Load the data for a single letter label."""
    image_files = os.listdir(folder) #返回指定的文件夹包含的文件或文件夹的名字的列表
    dataset = np.ndarray(shape=(len(image_files), image_size, image_size),dtype=np.float32) #创建一个numpy矩阵，个数为files的个数，长度为28*28，数据类型为float32
    print(folder)
    num_images = 0
    for image in image_files:
        image_file = os.path.join(folder, image) #将多个路径组合后返回，返回的是图片的路径和名字
        try:
            image_data = (imageio.imread(image_file).astype(float) - pixel_depth / 2) / pixel_depth #读取(image_file-image像素/2)/image像素作为image_data
            if image_data.shape != (image_size, image_size):
                raise Exception('Unexpected image shape: %s' % str(image_data.shape))
            dataset[num_images, :, :] = image_data #dataset中第num_images图片赋值为image_data的数据
            num_images = num_images + 1
        except (IOError, ValueError) as e:
            print('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')

    dataset = dataset[0:num_images, :, :] #将dataset的数据合并
    if num_images < min_num_images:
        raise Exception('Many fewer images than expected: %d < %d' % (num_images, min_num_images))

    print('Full dataset tensor:', dataset.shape)
    print('Mean:', np.mean(dataset)) #矩阵均值
    print('Standard deviation:', np.std(dataset)) #矩阵标准差
    return dataset #返回数据集


def maybe_pickle(data_folders, min_num_images_per_class, force=False):
    dataset_names = []
    for folder in data_folders:
        set_filename = folder + '.pickle'
        dataset_names.append(set_filename)
        if os.path.exists(set_filename) and not force:
            # You may override by setting force=True.
            print('%s already present - Skipping pickling.' % set_filename)
        else:
            print('Pickling %s.' % set_filename)
            dataset = load_letter(folder, min_num_images_per_class)
            try:
                with open(set_filename, 'wb') as f: #wb指二进制形式
                    pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL) #pickle.dump(对象, 文件，[使用协议])，将要持久化的数据对象保存在二进制数据流文件中
            except Exception as e:
                print('Unable to save data to', set_filename, ':', e)

    return dataset_names

train_folders = ['C:/Users/dong/Desktop/hanjia/notMNIST_large/A','C:/Users/dong/Desktop/hanjia/notMNIST_large/B','C:/Users/dong/Desktop/hanjia/notMNIST_large/C','C:/Users/dong/Desktop/hanjia/notMNIST_large/D','C:/Users/dong/Desktop/hanjia/notMNIST_large/E','C:/Users/dong/Desktop/hanjia/notMNIST_large/F','C:/Users/dong/Desktop/hanjia/notMNIST_large/G','C:/Users/dong/Desktop/hanjia/notMNIST_large/H','C:/Users/dong/Desktop/hanjia/notMNIST_large/I','C:/Users/dong/Desktop/hanjia/notMNIST_large/J']
test_folders = ['C:/Users/dong/Desktop/hanjia/notMNIST_small/A','C:/Users/dong/Desktop/hanjia/notMNIST_small/B','C:/Users/dong/Desktop/hanjia/notMNIST_small/C','C:/Users/dong/Desktop/hanjia/notMNIST_small/D','C:/Users/dong/Desktop/hanjia/notMNIST_small/E','C:/Users/dong/Desktop/hanjia/notMNIST_small/F','C:/Users/dong/Desktop/hanjia/notMNIST_small/G','C:/Users/dong/Desktop/hanjia/notMNIST_small/H','C:/Users/dong/Desktop/hanjia/notMNIST_small/I','C:/Users/dong/Desktop/hanjia/notMNIST_small/J']
train_datasets = maybe_pickle(train_folders, 45000)
test_datasets = maybe_pickle(test_folders, 1800)