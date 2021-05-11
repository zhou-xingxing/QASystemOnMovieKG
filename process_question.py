# -*- coding: UTF-8 -*-
'''
接收原始问题
对原始问题进行分词、词性标注等处理
对问题进行抽象
'''

import jieba.posseg
import re
from question_classification import Question_classify
from question_template import QuestionTemplate
import sys, os


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


# blockPrint()
# enablePrint()
#
class Question():
    def __init__(self):
        # 初始化分类器
        self.classify_model = Question_classify()
        # 读取问题模板
        with(open("./questions/question_classification.txt", "r", encoding="utf-8")) as f:
            question_mode_list = f.readlines()
        self.question_mode_dict = {}
        # 问题模板存入词典
        for one_mode in question_mode_list:
            mode_id, mode_str = str(one_mode).strip().split(":")
            self.question_mode_dict[int(mode_id)] = str(mode_str).strip()
        # 创建问题回答模板对象
        self.questiontemplate = QuestionTemplate()

    # 问题解答方法
    def question_process(self, question):
        # 接收问题
        self.raw_question = str(question).strip()
        # 分词,词性标注
        self.pos_quesiton = self.question_posseg()
        # 问题分类,确定问题模板
        self.question_template_id_str = self.get_question_template()
        # 根据模板查询,构造最终答案
        self.answer = self.query_template()
        return (self.answer)

    # 分词工具处理
    def question_posseg(self):
        # 加载用户词典,提高准确性
        jieba.load_userdict("./questions/userdict.txt")
        # 清洗字符串
        clean_question = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+", "", self.raw_question)
        self.clean_question = clean_question
        # 词性标注
        question_seged = jieba.posseg.cut(str(clean_question))
        result = []
        question_word, question_flag = [], []
        for w in question_seged:
            temp_word = f"{w.word}/{w.flag}"
            result.append(temp_word)
            word, flag = w.word, w.flag
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag) == len(question_word)
        self.question_word = question_word
        self.question_flag = question_flag
        print(result)
        return result

    # 获取问题模板
    def get_question_template(self):
        # 抽象问题
        for item in ['nr', 'nm', 'ng']:
            while (item in self.question_flag):
                ix = self.question_flag.index(item)
                self.question_word[ix] = item
                self.question_flag[ix] = item + "ed"
        # 将问题转化字符串
        str_question = "".join(self.question_word)
        print("抽象问题为：", str_question)
        # 问题分类
        question_template_num = self.classify_model.predict(str_question)
        print("使用模板编号：", question_template_num)
        question_template = self.question_mode_dict[question_template_num]
        print("问题模板：", question_template)
        # 返回编号和问题
        question_template_id_str = str(question_template_num) + "\t" + question_template
        return question_template_id_str

    # 最终查询
    def query_template(self):
        # 调用问题模板类中的问题解答方法
        try:
            answer = self.questiontemplate.get_question_answer(self.pos_quesiton, self.question_template_id_str)
            # print("get_question_answer",self.pos_quesiton, self.question_template_id_str)
        except:
            answer = "我也不知道啊！"
        return answer
