import feedparser
from bs4 import BeautifulSoup
from urllib.parse import urlencode, parse_qs, urlparse
from urllib.request import urlopen, install_opener, build_opener
from time import sleep

opener=build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
install_opener(opener)
def get_paper_list(key=None, max_result=20):
    # url_string = 'http://portal.acm.org/browse_dl.cfm?linked=1&part=series&coll=portal&dl=ACM&CFID=81659906&CFTOKEN=15682890'
    # url_string = https://dl.acm.org/results.cfm?query=learning&start=0
    cnt = 0
    paper_url = {}
    while cnt*20 < max_result:
        url_string = 'https://dl.acm.org/results.cfm?'+urlencode({"query": key, "start": cnt*20})
        print(url_string)
        res = urlopen(url_string).read()
        soup = BeautifulSoup(res, features="lxml")
        papers = []
        paper_list = soup.find_all("div", class_="title")
        for i in paper_list:
            papers.append(i.find_all("a")[0])
        for k in papers:
            paper_url[k.getText()] = 'https://dl.acm.org/'+k.get('href', None)
        print(paper_url)
        sleep(0.5)
        cnt += 1
    return paper_url

def get_paper_info(url):
    paper_info = {}
    arg = urlparse(url).query
    args = parse_qs(arg)
    urlargs = urlencode({"id": args['id'], "usebody": "tabbody"})
    tmp = urlopen('https://dl.acm.org/tab_abstract.cfm?'+urlargs)
    abstract = tmp.read()
    paper_info['abstract'] = BeautifulSoup(abstract).text
    tmp = urlopen('https://dl.acm.org/tab_comments.cfm?'+urlargs)
    author_list = []
    authors = tmp.read()
    authors_part = BeautifulSoup(authors).find_all('strong')
    for i in authors_part:
        tmp = i.find_all('a')
        if len(tmp) == 0:
            continue
        else:
            tmp = tmp[0].getText()
            if tmp != 'Bibliometrics':
                author_list.append(tmp)
    paper_info['authors'] = author_list