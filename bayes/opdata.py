#!/usr/bin/env python
# encoding: utf-8

import os
import random
import re


class DataChange(object):
    """string to int"""
    def __init__(self, source_file, train_data_file, test_data_file, train_file_percentage):
        self.source_file = source_file
        self.train_data_file = open(train_data_file, 'w')
        self.test_data_file = open(test_data_file, 'w')
        self.train_rate = train_file_percentage
        self.unique_words = []
        # 每一个单词都使用一个数字类型的id表示，python索引的时候才会快一些
        self.word_ids = {}

    def __del__(self):
        self.train_data_file.close()
        self.test_data_file.close()

    def data_scv(self):
        output_file = self.test_data_file
        for line in open(self.source_file, 'r'):
            arr = line.strip().split('#')
            category = arr[-1]
            # 按照比例train/test比例进行分配
            if random.random() < self.train_rate:
                output_file = self.train_data_file
            else:
                output_file = self.test_data_file
            # 读取文件获得词组
            words = arr[0].split();
            output_file.write(category + ' ')
            for word in words:
                if word not in self.word_ids:
                    self.unique_words.append(word)
                    self.word_ids[word] = hash(word)
                output_file.write(str(self.word_ids[word]) + " ")
            output_file.write("#" + category + "\n")
        with open('word_map.bin','w') as fw:
            for word ,index in self.word_ids.items():
                fw.write(word+'#'+str(index)+"\n")


if __name__ == '__main__':

    dp = DataChange('./data.txt', './train.scv', './test.scv', 0.9)
    dp.data_scv()
