#!/usr/bin/env python
# coding: utf-8

import math
import jieba


class NavieBayesPredict(object):
    """使用训练好的模型进行预测"""

    def __init__(self, test_data_file, model_data_file, result_file):
        self.test_data_file = open(test_data_file, 'r')
        self.model_data_file = open(model_data_file, 'r')
        # 每个类别的先验概率
        self.class_probabilities = {}
        # 拉普拉斯平滑，防止概率为0的情况出现
        self.laplace_smooth = 0.1
        # 模型训练结果集
        self.class_word_prob_matrix = {}
        # 当某个单词在某类别下不存在时，默认的概率（拉普拉斯平滑后 add-k模式 其中k=0.1）
        self.class_default_prob = {}
        # 所有单词
        self.unique_words = {}
        # 实际的文本分类
        self.real_classes = []
        # 预测的文本分类
        self.predict_classes = []

    def __del__(self):
        self.test_data_file.close()
        self.model_data_file.close()
        self.result_file.close()

    def loadModel(self):
        # 从模型文件的第一行读取类别的先验概率
        class_probs = self.model_data_file.readline().split('#')
        for cls in class_probs:
            arr = cls.split()
            if len(arr) == 3:
                self.class_probabilities[arr[0]] = float(arr[1])
                self.class_default_prob[arr[0]] = float(arr[2])
        # 从模型文件读取单词在每个类别下的概率
        line = self.model_data_file.readline().strip()
        while len(line) > 0:
            arr = line.split()
            assert (len(arr) % 2 == 1)
            assert (arr[0] in self.class_probabilities)
            self.class_word_prob_matrix[arr[0]] = {}
            i = 1
            while i < len(arr):
                word_id = int(arr[i])
                probability = float(arr[i + 1])
                if word_id not in self.unique_words:
                    self.unique_words[word_id] = 1
                self.class_word_prob_matrix[arr[0]][word_id] = probability
                i += 2
            line = self.model_data_file.readline().strip()
        print len(self.class_probabilities), " classes loaded!", len(self.unique_words), "words!"

    def caculate(self):
        # 读取测试数据集
        line = self.test_data_file.readline().strip()
        while len(line) > 0:
            arr = line.split()
            class_id = arr[0]
            words = arr[1:len(arr) - 1]
            # 把真实的分类保存起来
            self.real_classes.append(class_id)
            # 预测当前行（一个文本）属于各个分类的概率
            class_score = {}
            for key in self.class_probabilities.keys():
                class_score[key] = math.log(self.class_probabilities[key])
            for word_id in words:
                word_id = int(word_id)
                if word_id not in self.unique_words:
                    continue
                for class_id in self.class_probabilities.keys():
                    if word_id not in self.class_word_prob_matrix[class_id]:
                        class_score[class_id] += math.log(self.class_default_prob[class_id])
                    else:
                        class_score[class_id] += math.log(self.class_word_prob_matrix[class_id][word_id])
            # 对于当前文本，所属的概率最高的分类
            max_class_score = max(class_score.values())
            for key in class_score.keys():
                if class_score[key] == max_class_score:
                    self.predict_classes.append(key)
            line = self.test_data_file.readline().strip()
        print len(self.real_classes), len(self.predict_classes)

    def evaluation(self):
        # 评价当前分类器的准确性
        accuracy = 0
        i = 0
        while i < len(self.real_classes):
            if self.real_classes[i] == self.predict_classes[i]:
                accuracy += 1
            i += 1
        accuracy = (float)(accuracy) / (float)(len(self.real_classes))
        print "Accuracy:", accuracy
        # 评测精度和召回率
        # 精度是指所有预测中，正确的预测
        # 召回率是指所有对象中被正确预测的比率
        for class_id in self.class_probabilities:
            correctNum = 0
            allNum = 0
            predNum = 0
            i = 0
            while i < len(self.real_classes):
                if self.real_classes[i] == class_id:
                    allNum += 1
                    if self.predict_classes[i] == self.real_classes[i]:
                        correctNum += 1
                if self.predict_classes[i] == class_id:
                    predNum += 1
                i += 1

            precision = (float)(correctNum) / (float)(predNum)
            recall = (float)(correctNum) / (float)(allNum)
            print class_id, ' -> precision = ', precision, ' recall = ', recall

    def predict(self):
        self.loadModel()
        self.caculate()
        self.evaluation()

    def predict_words(self, words):
        # 预测当前行（一个文本）属于各个分类的概率
        class_score = {}
        for key in self.class_probabilities.keys():
            class_score[key] = math.log(self.class_probabilities[key])
        for word in words:
            word_id = int(hash(word))
            if word_id not in self.unique_words:
                continue
            for class_id in self.class_probabilities.keys():
                if word_id not in self.class_word_prob_matrix[class_id]:
                    class_score[class_id] += math.log(self.class_default_prob[class_id])
                else:
                    class_score[class_id] += math.log(self.class_word_prob_matrix[class_id][word_id])
        # 对于当前文本，所属的概率最高的分类
        max_class_score = max(class_score.values())
        for key in class_score.keys():
            if class_score[key] == max_class_score:
                print key


if __name__ == '__main__':
    nbp = NavieBayesPredict('test.scv', 'judgetype.model', 'judgetype.result')
    # nbp.predict()
    print jieba.cut('让我们来打开机票atp吧~', cut_all=False)
    # nbp.predict_words(jieba.cut('让我们来打开机票atp吧~',cut_all=False))
    nbp.predict_words('让　我们　不要　来　打开　机票　atp 吧　~'.split())
