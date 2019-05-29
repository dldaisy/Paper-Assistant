from crawler import query

def filter(target_list, func):
    return [paper for paper in target_list if func(paper)]

def get_paper_list(words, max_cnt=20):
    """
    words       :       空格分隔的若干个关键字
    max_cnt     :       论文结果的最大数目
    """
    result = []
    
    result = query(search_query=words, max_chunk_results=10, max_results=max_cnt)
    
    return result
