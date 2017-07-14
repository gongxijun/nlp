#!/usr/bin/env python
# encoding: utf-8

import os
import random
import re


class OpsData(object):
    """将字符数据转换成数值数据"""

    def __init__(self, source_file, train_data_file, test_data_file, train_file_percentage):
        self.source_file = source_file
        self.train_data_file = open(train_data_file, 'w')
        self.test_data_file = open(test_data_file, 'w')
        self.train_file_percentage = train_file_percentage
        self.unique_words = []
        self.unique_category = []
        # 每一个单词都使用一个数字类型的id表示，python索引的时候才会快一些
        self.category_ids = {}
        self.word_ids = {}

    def __del__(self):
        self.train_data_file.close()
        self.test_data_file.close()

    def data_scv(self):
        file_num = 0
        output_file = self.test_data_file
        for line in open(self.source_file, 'r'):
            arr = line.strip().split('#')
            category = arr[-1]
            if category not in self.category_ids:
                self.category_ids[category] = int(len(self.unique_category))
                self.unique_category.append(category)
            # 随即函数按照train_file_percentage指定的百分比来选择训练和测试数据及
            if random.random() < self.train_file_percentage:
                output_file = self.train_data_file
            else:
                output_file = self.test_data_file
            # 读取文件获得词组
            words = arr[0].split();
            output_file.write(category + ' ')
            for word in words:
                if word not in self.word_ids:
                    self.word_ids[word] = int(len(self.unique_words))
                    self.unique_words.append(word)
                output_file.write(str(self.word_ids[word]) + " ")
            output_file.write("#" + category + "\n")
            # 原始文件较多，需要交互显示进度
            file_num += 1
            if file_num % 100 == 0:
                print file_num, ' files processed'
        with open('word_map.scv', 'w') as fw:
            for word, index in self.category_ids.items():
                fw.write('category:' + word + '#' + str(index) + "\n")
            for word, index in self.word_ids.items():
                fw.write('keyword:'+word + '#' + str(index) + "\n")
        print file_num, " line loaded!"
        print len(self.unique_words), " unique words found!"


if __name__ == '__main__':
    dp = OpsData('data.txt', 'train.scv', 'test.scv', 0.9)
    dp.data_scv()
