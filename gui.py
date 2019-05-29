import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

from search import search
from analyze import field_analyze
from search import paper_recommend





# =========主体==============

def resize(w, h, w_box, h_box, pil_image):

  f1 = 1.0*w_box/w
  f2 = 1.0*h_box/h
  factor = min([f1, f2])
  width = int(w*factor)
  height = int(h*factor)
  return pil_image.resize((width, height), Image.ANTIALIAS)


window = tk.Tk()
window.title('gui')
window.geometry('1000x800')



# =========美工=============
title = tk.Label(window, text = 'Paper Assistant', font = ('Times', '40', 'bold italic'))
title.place(x = 10, y = 10)
# =========输入框=================
keyword = tk.Label(window, text = '关键字', bg = '#434343', fg = '#ffffff',anchor = 'nw')
keyword.place(x = 10, y =200)
InputKeyword = tk.Entry(window)
InputKeyword.place(x = 100, y = 200)

#=========数据库选项==================
range = tk.Label(window, text = '数据库', bg = '#434343', fg = '#ffffff',anchor = 'nw')
range.place(x = 10, y =300)


var1 = tk.IntVar()
check_1 = tk.Checkbutton(window, text = 'ACM', variable = var1, onvalue = 1, offvalue = 0)
check_1.place(x = 100, y =300)

var2 = tk.IntVar()
check_2 = tk.Checkbutton(window, text = 'IEEE', variable = var2, onvalue = 1, offvalue = 0)
check_2.place(x = 160, y =300)

var3 = tk.IntVar()
check_3 = tk.Checkbutton(window, text = 'Arxiv', variable = var3, onvalue = 1, offvalue = 0)
check_3.place(x = 220, y =300)

var4 = tk.IntVar()
check_4 = tk.Checkbutton(window, text = 'All', variable = var4, onvalue = 1, offvalue = 0)
check_4.place(x = 280, y =300)


#=========搜索选项======================



def Search(input_string, **kwargs) -> str:
    return search(input_string, **kwargs)

def Search_Analysis(input_string) -> str:
    return field_analyze(input_string)


i=0
length = 0
ret_list = []
def NextPage():
    # ==============================================
    global i
    global length

    i = i+1
    content = ret_list[(i-1)%length]
    #output window
    title = tk.Label(window, text = "Title", font = ('Times', '10', 'bold'))
    title.place(x = 400, y = 10)
    title_text = tk.Text(window, height = 2)
    title_text.insert('insert', content['title'])
    title_text.place(x = 400, y = 30)


    author = tk.Label(window, text = "Author", font = ('Times', '10', 'bold'))
    author.place(x = 400, y = 60)
    author_text = tk.Text(window, height = 2)
    author_text.insert('insert', content['authors'])
    author_text.place(x = 400, y = 80)

    abstract = tk.Label(window, text="Abstract", font=('Times', '10', 'bold'))
    abstract.place(x=400, y=110)
    output = ScrolledText()
    output.config(width = 80, height = 12)
    output.place(x = 400, y = 130)
    output.insert('insert', content['abstract'])

    # ====下一页按钮========
    button_next = tk.Button(window, text='next', command=NextPage)
    button_next.place(x=940, y=300)

def SearchAbstract():
    input_string = InputKeyword.get()
    input_source = []
    if(var1.get() == 1):
        input_source.append('ACM')
    if (var2.get() == 1):
        input_source.append('IEEE')
    if (var3.get() == 1):
        input_source.append('Arxiv')
    if(var4.get() == 1):
        input_source.clear()
    if not input_source:
        input_source.append('All')
    global ret_list
    ret_list = Search(input_string, input_source=input_source, type="abstract")
    global i
    global length
    length = len(ret_list)
    i = 0
    NextPage()




ret_list_comment = []
i_comment = 0
length_comment = 0

def NextPageComment():
    # ==============================================
    global i_comment
    global length_comment

    i_comment = i_comment+1
    content = ret_list_comment[(i_comment-1)%length_comment]
    #output window
    title = tk.Label(window, text = "Title", font = ('Times', '10', 'bold'))
    title.place(x = 400, y = 350)
    title_text = tk.Text(window, height = 2)
    title_text.insert('insert', content['title'])
    title_text.place(x = 400, y = 370)


    author = tk.Label(window, text = "Author", font = ('Times', '10', 'bold'))
    author.place(x = 400, y = 400)
    author_text = tk.Text(window, height = 2)
    author_text.insert('insert', content['authors'])
    author_text.place(x = 400, y = 420)

    abstract = tk.Label(window, text="Comment", font=('Times', '10', 'bold'))
    abstract.place(x=400, y=450)
    output = ScrolledText()
    output.config(width = 80, height = 12)
    output.place(x = 400, y = 470)
    output.insert('insert', content['comment'])

    # ====下一页按钮========
    button_next = tk.Button(window, text='next', command=NextPageComment)
    button_next.place(x=940, y=640)

def SearchComment():
    input_string = InputKeyword.get()
    global ret_list_comment
    ret_list_comment = Search(input_string, type="comment")
    # output window
    global i_comment
    global length_comment
    length_comment = len(ret_list_comment)
    i_comment = 0
    NextPageComment()


# ===============图片===================

# ===勿删，为了gui的正常运行，先给image赋予默认值=====
image1 = Image.open('image2.jpg')
render1 = ImageTk.PhotoImage(image1)
image2 = Image.open('image2.jpg')
render2 = ImageTk.PhotoImage(image2)
def DataAnalysis():
    # 使用canvas显示image

    top = tk.Toplevel()
    top.title("piechart")
    top.geometry('600x400')
    # =========image 1============
    input_string1 = InputKeyword.get()
    file_name_list = Search_Analysis(input_string1)
    # file_name = 'image1.jpg'  # 测试使用的
    global image1
    global render1
    file_name1 = file_name_list[0]
    image1 = Image.open(file_name1)
    render1 = ImageTk.PhotoImage(image1)
    img1 = tk.Label(top, image = render1, anchor = 'nw')
    img1.place(x=10, y=10)

    top = tk.Toplevel()
    top.title("keyword")
    top.geometry('600x400')
    # =========image 2============
    # file_name = 'image1.jpg'  # 测试使用的
    file_name2 = file_name_list[1]
    global image2
    global render2
    image2 = Image.open(file_name2)
    render2 = ImageTk.PhotoImage(image2)
    img2 = tk.Label(top, image=render2, anchor = 'nw')
    img2.place(x=10, y=10)


button_1 = tk.Button(window, text = '搜索摘要', command = SearchAbstract)
button_1.place(x = 10, y =400)

button_2 = tk.Button(window, text = '搜索评论', command = SearchComment)
button_2.place(x = 90, y =400)

button_3 = tk.Button(window, text = '数据分析', command = DataAnalysis)
button_3.place(x = 170, y =400)


#=============推荐信箱===================

def ReceiveReference():
    global ret_list
    ret_list = paper_recommend(5)
    global i
    i = 0
    global length
    length = len(ret_list)
    NextPage()


load = Image.open('mailbox.jpg')
w, h = load.size
load.thumbnail((w/10, h/10))
render = ImageTk.PhotoImage(load)

img = tk.Label(window, image=render)
img.place(x=10, y=550)

num = 0
button_recv = tk.Button(window, text = f'check mailbox {num}', command = ReceiveReference)
button_recv.place(x = 10, y = 600)






window.mainloop()