from datetime import datetime
import matplotlib.pyplot as plt

# 外部接口

def get_paper_list():
    # 待爬虫模块实现接口
    # 目前为测试列表
    test_list = [
        {
            "title" : "4 abc cc dcv df er df",
            "authors" : "abc dfr sfr vcxs dfr" ,
            "keyword" : "abc AI network security" ,
            "source" : "ACM" ,
            "comment" : "sd wer avc abc "        
        },    
        {
            "title" : "7 abc cc dcv df er df",
            "authors" : "abc abc sfr vcxs dfr" ,
            "keyword" : "abc hardware security" ,
            "source" : "IEEE" ,
            "comment" : "abc wer avc abc "        
        },    
        {
            "title" : "5 abc abc cc dcv df er df",
            "authors" : "abc dfr sfr vcxs dfr" ,
            "keyword" : "abc AI software IoT" ,
            "source" : "Arxiv" ,
            "comment" : "sd wer avc abc "        
        }
    ]
    
    return test_list

def field_analyze(word):
    """
    领域分析：对给定的关键字，返回所有含有该关键字的论文的其他关键字的饼状图
    """
    paper_list = get_paper_list()
    
    key_counts = {}
    for paper in paper_list: 
        keywords = paper["keyword"].split()
        
        # keywords = set(keywords)                最后看性能有没有必要
        if word not in keywords:
            continue 
        
        # 存在该关键字，遍历关键字 
        for keyword in keywords:
            if keyword == word :
                continue
            if keyword in key_counts:
                key_counts[keyword] += 1 
            else:
                key_counts[keyword] = 1 
        
    if not key_counts:
        raise NoKeywordError(word) 
    
    return draw_pie_chart(key_counts)

#绘图

def draw_pie_chart(some_counts):
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
    filename = fig_dir + "pie-" + suffix + ".jpg"
    plt.savefig(filename, dpi=300)
    
    return filename

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
        
        
# 测试

# key_counts = field_analyze("abc")
# test = draw_pie_chart(key_counts)
# print(test)