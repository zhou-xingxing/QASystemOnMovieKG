# -*- coding: UTF-8 -*-
# 对问题进行分类

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba


# 问题分类器
class Question_classify():
    def __init__(self):
        # 读取训练数据
        self.train_x, self.train_y = self.read_train_data()
        # 训练模型
        self.model = self.train_model_NB()

    # 读取训练数据
    def read_train_data(self):
        train_x = []
        train_y = []
        with(open("./questions/label.txt", "r", encoding="utf-8")) as fr:
            lines = fr.readlines()
            for one_line in lines:
                temp = one_line.split('    ')
                # 问题分词处理后作为train_x
                word_list = list(jieba.cut(str(temp[1]).strip()))
                train_x.append(" ".join(word_list))
                # 类别编号作为train_y
                train_y.append(temp[0])
        return train_x, train_y

    # 模型训练
    def train_model_NB(self):
        X_train, y_train = self.train_x, self.train_y
        self.tv = TfidfVectorizer()
        # 提取TF-IDF特征
        train_data = self.tv.fit_transform(X_train).toarray()
        # 构造分类器
        clf = MultinomialNB(alpha=0.01)
        clf.fit(train_data, y_train)
        return clf

    # 预测问题分类
    def predict(self, question):
        # 接收问题
        question = [" ".join(list(jieba.cut(question)))]
        # 提取特征
        test_data = self.tv.transform(question).toarray()
        # 给出分类结果
        y_predict = self.model.predict(test_data)[0]
        print("questions type:", y_predict)
        return int(y_predict)


if __name__ == '__main__':
    qc = Question_classify()
    qc.predict("成龙演过的电影有哪些")
