#!/usr/bin/env python
# coding: utf-8

import numpy as np
import math


class NgramPredict(object):
    def __init__(self, model_file, test_file, char_map_file):
        self.model_data = open(model_file, 'r');
        self.test_data = open(test_file, 'r');
        self.laplace_smooth = 0.1
        self.char_map = {}
        self.category_map = {}
        self.init_char_map(char_map_file);
        self.probability_words = np.zeros(
            (int(len(self.category_map)), int(len(self.char_map)), int(len(self.char_map))), dtype=np.float);
        # 解析数据,并将数据装载到有向图中. 就是统计各词组的频率,以及所依赖的前几个词组的频率
        self.probability_feature_dict = np.zeros((int(len(self.category_map)), int(len(self.char_map))));

    def __del__(self):
        self.model_data.close();
        self.test_data.close();

    def init_char_map(self, char_map_file):
        for line in open(char_map_file, 'r'):
            cm = line.strip().split(':');
            varword = cm[-1].strip('\n').split('#');
            if cm[0] == 'category':
                self.category_map[varword[0]] = varword[1];
            if cm[0] == 'keyword':
                self.char_map[varword[0]] = varword[1];

    def init_model(self):
        ind_category = 0;
        ind_word_d = 0;
        for line in self.model_data:
            arry_data = line.split(':')
            if arry_data[0] == 'category':
                for word_id, word in enumerate(arry_data[-1].split()):
                    self.probability_feature_dict[ind_category][word_id] = float(word);
                ind_category += 1;

            if arry_data[0] == 'keyword':
                for preword_id, preword in enumerate(arry_data[-1].strip('\n').split('#')):
                    for word_id, word in enumerate(preword.strip('\n').split()):
                        self.probability_words[ind_word_d][preword_id][word_id] = float(word)
                ind_word_d += 1;

    def predict_words(self, words):
        class_score = {}
        for category_id in range(len(self.category_map)):
            pre_word = None;
            for word in words:
                if word not in self.char_map or self.probability_feature_dict[category_id][int(self.char_map[word])]==0.0:
                    continue
                print category_id ,self.probability_feature_dict[category_id][int(self.char_map[word])]
                if not pre_word:
                    class_score[category_id] = self.probability_feature_dict[category_id][int(self.char_map[word])];
                else:
                    class_score[category_id] *= self.probability_words[category_id][self.char_map[pre_word]][
                        self.char_map[word]];
        # 对于当前文本，所属的概率最高的分类
        print class_score
        max_class_score = max(class_score.values())
        for key in class_score.keys():
            if class_score[key] == max_class_score:
                for category, value in self.category_map.items():
                    if int(value) == key:
                        print category, value


if __name__ == '__main__':
    ngr = NgramPredict('ngram.model', 'test.scv', 'word_map.scv')
    ngr.init_model()
    ngr.predict_words('打开.机票.app'.split('.'))
