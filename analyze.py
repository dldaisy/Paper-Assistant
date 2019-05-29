from datetime import datetime
from wordcloud import WordCloud
from pprint import pprint

import matplotlib.pyplot as plt

from base import get_paper_list, filter

def field_analyze(word):
    """
    领域分析：对给定的关键字，返回所有含有该关键字的论文的其他关键字的饼状图
    """
    paper_list = get_paper_list(word,max_cnt=10)
    # pprint(paper_list)
    
    key_counts = {}
    for paper in paper_list: 
        ## 现在使用title 分词模拟关键字列表
        keywords = paper["title"].split()
        keywords = filter_by_len(keywords, 4)
        keywords = [keyword.lower() for keyword in keywords]
        # 如果按关键字的话，这里本来是筛掉一部分的
        # if word not in keywords:
            # continue 
        
        # 存在该关键字，遍历关键        
        for keyword in keywords:
            if keyword == word :
                continue
            if keyword in key_counts:
                key_counts[keyword] += 1 
            else:
                key_counts[keyword] = 1 
        
    if not key_counts:
        raise NoKeywordError(word) 
    
    pie_chart = gen_pie_chart(key_counts)
    word_cloud = gen_word_cloud(key_counts)
    return [pie_chart, word_cloud]

#绘图

def gen_pie_chart(some_counts):
    """
    绘制饼状图
    params:
        some_counts     :       字符串到整数的映射
    return:
        存储图片的文件名
    """
    
    fig_dir = "images/"
    
    labels = []
    fracs = []
    for key, value in some_counts.items():
        labels.append(key)
        fracs.append(value)
    
    plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
    plt.pie(x=fracs, labels=labels, autopct='%3.1f %%',
            labeldistance=1.1, startangle = 90,pctdistance = 0.6)
    
    suffix = datetime.now().isoformat(timespec='seconds')
    suffix = suffix.replace(":", "-")
    filename = fig_dir + "pie-" + suffix + ".png"
    plt.savefig(filename, dpi=100)
    plt.clf()
    
    return filename

# word cloud display 

def gen_word_cloud(some_counts):

    # Generate a word cloud image
    wordcloud = WordCloud().generate_from_frequencies(some_counts)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    fig_dir = "images/"
    suffix = datetime.now().isoformat(timespec='seconds')
    suffix = suffix.replace(":", "-")
    filename = fig_dir + "wordcloud-" + suffix + ".png"
    plt.savefig(filename, dpi=100)
    plt.clf()

    return filename


# 筛选 

def filter_by_len(target_list, length):
    """
    length  :  max length
    """    
    def func(element):
        return len(element) >= length
        
    return filter(target_list, func)


class error(Exception):
    def __init__(self, message=None):
        if not message:
            self.message = "something wrong in analyze module" 
        else :
            self.message = message 
    
    def __str__(self):
        return self.message

class NoKeywordError(error):
    def __init__(self, word):
        super(NoKeywordError, self).__init__(message="There is no paper with keyword %s" % word)
        
        
# word = "computer"
# filename = field_analyze(word)
# print(filename)
