# 注

search 和 analyze 实现了多关键字搜索和单关键词统计功能，需要从爬虫模块获取数据 
数据格式与最初的pdf一致，需要一份文章信息的列表 

文章信息字段 

keyword, **title**, **authors**, afflication, source, **abstract**, **comment**.  

字段类型如Paper Assistant.pdf , 加粗字段不能为空

# 检索与统计功能使用说明

## 检索 

依赖：数据集 --- 列表，列表元素为字典对象，至少含有title, author, abstract和comment四个字段 

对外接口：

```py
search(words, input_source=["All"], type=None)
```

实现单关键字搜索，给定单词和出版社，返回结果字符串

type = "comment" 或 "abstract" 

## 统计

依赖：数据集 --- 列表，列表元素为字典对象，至少含有title, author, abstract和comment四个字段 

对外接口：

```py
field_analyze(word)
```

单关键字统计。对于含有关键字的文章的所有关键字进行统计，将饼状图存储在本地，返回图片存储位置

## 推送 

对外接口 

```py
def paper_recommend(history, max_keywords=5)
```

目前的实现是：

    模块维护一个history字典记录搜索过的关键字频次，推送就是在搜索过的关键字中寻找max_keywords个频率 
    较高的关键字搜索一次，返回论文列表 
    
    也可以尝试在histroy里预置一些数据，这样就不需要尝试搜索许多次了
    
修改实现方式只需修改接口函数

## 显示字段 

```py
def get_show_list(paper_list, type=None, max_len=10)
```

可以随便选择字段返回，只要改这个函数里的if-else块的列表内容就可以了