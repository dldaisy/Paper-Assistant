from crawler import query, get_acm

def filter(target_list, func):
    return [paper for paper in target_list if func(paper)]

def get_paper_list(words, max_cnt=10):
    """
    words       :       空格分隔的若干个关键字
    max_cnt     :       论文结果的最大数目
    """
    result = []
    
    # arxiv
    temp = query(search_query=words, max_chunk_results=10, max_results=max_cnt)
    for paper in temp:
        paper["source"] = "arxiv" 
    result.extend(temp) 
    
    # acm 
    # temp = get_acm(max_cnt) 
    # print(len(temp))
    
    return result
