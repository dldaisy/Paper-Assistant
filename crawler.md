### 爬虫使用了 arxiv 的 api 以及 acm 提供的 csv 文件

#### arxiv 部分

使用 arxiv 的 api 时使用 chunk 分割请求，因 arxiv 提供的 api 可以一次爬取多个论文的信息，每次请求一个 chunk 大小的信息，将总共的请求分割成若干 chunk，防止因请求过多被封禁。

使用 urlencode 结合传入的参数生成爬取用的 url

因 arxiv 使用 xml 作为返回信息，直接使用 feedparser 请求 url，生成 dict，提取其中 'entries' 关键字下的内容并根据需要的数据对关键字进行一定的处理后返回。

#### acm 部分

ACM 提供了论文数据的 csv 文件 [acm_kbart.csv](https://dl.acm.org/feeds/acm_kbart.csv)，首先通过 urlretrieve 获取该文件，然后使用 csv.DictReader 对其进行解析，对其中部分关键字中的内容进行处理后返回。