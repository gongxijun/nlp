#!/usr/bin/env python
# coding:utf-8
import numpy as np


class BinGram(object):
    __doc__ = '数据量太小,矩阵比较稀疏我们使用一个二元模型'

    def __init__(self, char_map_file, train_file, save_model):
        self.char_map = {}
        self.category_map = {}
        self.init_char_map(char_map_file);
        self.train_file = train_file;
        self.save_model = save_model;
        self.laplace_smooth = 0.0001
        self.probability_words = np.zeros(
            (int(len(self.category_map)), int(len(self.char_map)), int(len(self.char_map))), dtype=np.float);
        # 解析数据,并将数据装载到有向图中. 就是统计各词组的频率,以及所依赖的前几个词组的频率
        self.probability_feature_dict = np.zeros((int(len(self.category_map)), int(len(self.char_map))));
        self.feature_dict = np.zeros((int(len(self.category_map)), int(len(self.char_map))));
        self.bingram_dict = np.zeros((int(len(self.category_map)), int(len(self.char_map)), int(len(self.char_map))));

    def loadData(self):
          for line in open(self.train_file, 'r'):
              words = line.strip().split('#')[0].split();

              category = int(self.category_map[words[0]]);
              pre_word = None;
              for word in words[1:]:
                  word = int(word);
                  self.feature_dict[category][word] += 1;
                  if not pre_word:
                      self.bingram_dict[category][word][pre_word] += 1;
                  pre_word = word;

    def computeModel(self):
        sum_category = np.zeros((int(len(self.category_map))));

        for category_id, arr_category in enumerate(self.feature_dict):
            for word in arr_category:
                sum_category[category_id] += word;

        for category_id, arr_category in enumerate(self.feature_dict):
            for word_id, word in enumerate(arr_category):
                self.probability_feature_dict[category_id][word_id] = (float)(
                    word + self.laplace_smooth) / (sum_category[category_id] + sum_category[category_id]* self.laplace_smooth)

        for category_id, arr_category in enumerate(self.bingram_dict):
            for arr_word_id, arr_word in enumerate(arr_category):
                for word_id, word_count in enumerate(arr_word):
                    if self.feature_dict[category_id][arr_word_id]>0:
                        self.probability_words[category_id][arr_word_id][word_id] \
                        = (float)(word_count + self.laplace_smooth) / \
                          (self.feature_dict[category_id][arr_word_id] + self.laplace_smooth*(1+len(self.feature_dict[category_id])))
                    else:
                        self.probability_words[category_id][arr_word_id][word_id]=0.;
                print word_count,self.feature_dict[category_id][arr_word_id],self.probability_words[category_id][arr_word_id][word_id]

    def saveModel(self):
        with open(self.save_model, 'w') as fw:
            for category_id, arr_category in enumerate(self.probability_feature_dict):
                line = 'category:'
                for word_id, prob in enumerate(arr_category):
                    line += ' ' + str(prob);
                fw.write(line + '\n');
            for category_id, arr_category in enumerate(self.probability_words):
                line = 'keyword:'
                for arr_word_id, arr_word in enumerate(arr_category):
                    for word_id, word_prob in enumerate(arr_word):
                        line += ' ' + str(word_prob);
                    line+='#'
                fw.write(line+'\n')

    def init_char_map(self, char_map_file):
        for line in open(char_map_file, 'r'):
            cm = line.strip().split(':');
            varword = cm[-1].strip('\n').split('#');
            if cm[0] == 'category':
                self.category_map[varword[0]] = varword[1];
            if cm[0] == 'keyword':
                self.char_map[varword[0]] = varword[1];


if __name__ == '__main__':
    te = BinGram('./word_map.scv', './train.scv', 'ngram.model')
    te.loadData()
    te.computeModel()
    te.saveModel()
