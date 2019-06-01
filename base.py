from crawler import query
from pprint import pprint 
from crawler_acm import crawler

# results = crawler(key='quantum', max_results=2)
# for result in results:
#     print(result)


def filter(target_list, func):
    rtn = [paper for paper in target_list if func(paper)]
    if not rtn :
        rtn = target_list 
    return rtn

def get_paper_list(words, max_cnt=10):
    """
    words       :       空格分隔的若干个关键字
    max_cnt     :       论文结果的最大数目
    """
    result = []
    
    # arxiv
    temp = query(search_query=words, max_chunk_results=max_cnt, max_results=max_cnt)
    for paper in temp:
        paper["source"] = "Arxiv" 
    result.extend(temp) 
    
    # acm 
    temp = crawler(key=words, max_results=max_cnt)
    for paper in temp:
        paper["source"] = "ACM"
    result.extend(temp)
    
    return result
