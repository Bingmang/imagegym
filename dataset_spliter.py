"""
用于将数据集打乱并自动分为training和validation文件夹
usage: python dataset_spliter.py --dir ./training_data --factor 0.7
"""

import os
import argparse
import shutil
from random import shuffle

parser = argparse.ArgumentParser()
parser.add_argument('--dir', default='./training_data', type=str,
                    help='The folder path')
parser.add_argument('--factor', default=0.7, type=float,
                    help='The factor of traning set and validation set')

opt = parser.parse_args()
print(opt)

def main():
    training_dir = opt.dir + '/training/'
    validation_dir = opt.dir + '/validation/'
    if not os.path.exists(training_dir):
        os.mkdir(training_dir)
    if not os.path.exists(validation_dir):
        os.mkdir(validation_dir)
    file_list = os.listdir(opt.dir)
    shuffle(file_list)
    edge = int(len(file_list) * opt.factor)
    for file in file_list[:edge]:
        shutil.move(opt.dir + file, training_dir)
    for file in file_list[edge:]:
        shutil.move(opt.dir + file, validation_dir)

if __name__ == '__main__':
    main()
    