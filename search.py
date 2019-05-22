# -*- coding: utf-8 -*-
from math import log

"""

对外接口 ： search(paper_list, type=None)
    params 
        - paper_list    :   paper对象列表，对象为字典类型，
                            至少含有title, author, ocmment, abstract字段
        - type          :   "abstract" , "comment"
"""

# 外部接口

def get_paper_list():
    # 待爬虫模块实现接口
    # 目前为测试列表
    test_list = [
        {
            "title" : "4 abc cc dcv df er df",
            "abstract" : "4 abc cc dcv df er df",
            "authors" : "abc dfr sfr vcxs dfr" ,
            "keyword" : "abc dfr sfr vcxs dfr" ,
            "source" : "ACM" ,
            "comment" : "sd wer avc abc "        
        },    
        {
            "title" : "7 abc cc dcv df er df",
            "abstract" : "7 abc cc dcv df er df",
            "authors" : "abc abc sfr vcxs dfr" ,
            "keyword" : "abc abc sfr vcxs dfr" ,
            "source" : "IEEE" ,
            "comment" : "abc wer avc abc "        
        },    
        {
            "title" : "5 abc abc cc dcv df er df",
            "abstract" : "5 abc abc cc dcv df er df",
            "authors" : "abc dfr sfr vcxs dfr" ,
            "keyword" : "abc dfr sfr vcxs dfr" ,
            "source" : "Arxiv" ,
            "comment" : "sd wer avc abc "        
        }
    ]
    
    return test_list

def search(word, input_source=["All"], type=None):
    """
    返回需要显示的文本
    type:
        - None 返回标题，作者 
        - "abstract" ： 返回标题，作者、摘要
        - "comment"  :  返回标题、作者、评论
    """
    
    paper_list = get_paper_list()
    paper_list = filter_source(paper_list, input_source)
    
    count = 10                  # 最多显示的论文数
    
    sort_paper(paper_list, word) 
    paper_list_len = len(paper_list)
    show_len = min(count, paper_list_len)

    show_list = []
    for paper in paper_list[0:show_len]:
        show_paper = []
        show_paper.append("title:\t\t"+paper["title"])
        show_paper.append("author:\t\t"+paper["authors"])
        if type=="abstract":
            show_paper.append("abstract:\t"+paper["abstract"])
        elif type=="comment":
            show_paper.append("commment:\t"+paper["comment"])
        show_str = '\n'.join(show_paper)
        show_list.append(show_str)
    return '\n\n'.join(show_list)

# 评分、排序

def pre_score(paper_list, word):
    """
    获取DF参数
    
    DF : 单词再所有文档中出现的次数
    """
    rtn = 0
    
    for paper in paper_list: 
        for _, value in paper.items():
            rtn += value.count(word) 
    
    return rtn 
    
def score(paper_list, word):
    """
    为所有文章评分，根据给定关键字，将结果写入paper对象的
    score子段
    params:
        - paper_list    : 论文列表
        - word          : 带检索单词
    formula:
        W = TF * IDF 
        IDF = log(N/DF)
    """
    score_list = []
    N = len(paper_list)
    for paper in paper_list: 
        IDF = 0 
        for _, value in paper.items():
            TF = value.count(word) 
            IDF += TF
        score_list.append(IDF) 
    DF = sum(score_list)    
    IDF = log(N/DF)
    
    score_list = [TF * IDF for TF in score_list]
    for paper, score in zip(paper_list, score_list):
        paper["score"] = score 

def sort_paper(paper_list, word):
    # def cmp(paper0, paper1):
        # return paper0["score"] > paper1["score"]
    
    score(paper_list, word)
    paper_list.sort(key=lambda paper : paper["score"], reverse=False)

# 筛选、过滤

def filter(paper_list, func):
    return [paper for paper in paper_list if func(paper)]
    
def filter_source(paper_list, values):
    """
    values  :  list of str
    """
    if "All" in values:
        return paper_list
    
    def func(paper):
        return paper["source"] in values
        
    return filter(paper_list, func)

## 模块异常
## 为了gui接口正常工作，没有把异常加进去
## 如果需要可以添加无结果异常

class error(Exception):
    def __init__(self, message=None):
        if not message:
            self.message = "something wrong in search module" 
        else :
            self.message = message 
    
    def __str__(self):
        return self.message

class NoPaperMatchedError(error):
    def __init__(self):
        super(NoPaperMatchedError, self).__init__(message="There is no paper matched")
    

## 测试    
# res = search("abc", type="comment")
# print(res)
