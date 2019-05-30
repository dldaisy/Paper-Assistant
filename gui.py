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
load_icon = Image.open('bookicon.jpg')
w, h = load_icon.size
load_icon.thumbnail((w/3, h/3))
render_icon = ImageTk.PhotoImage(load_icon)

img = tk.Label(window, image=render_icon, bg = '#ffffff', width = 380, anchor = 'nw')
img.place(x=5, y=5)

title = tk.Label(window, text = 'Paper Assistant', font = ('Comic Sans MS', '35', 'bold italic'), bg = '#ffffff', width = 13, anchor = 'nw')
title.place(x = 5, y = 54)
# =========输入框=================
load_star1 = Image.open('star1.jpg')
w, h = load_star1.size
load_star1.thumbnail((w/6, h/6))
render_star1 = ImageTk.PhotoImage(load_star1)

img = tk.Label(window, image=render_star1, bg = '#ffffff')
img.place(x=5, y=160)


functions = tk.Label(window, text = ' 搜索选项', font = ('仿宋', '13', 'bold'), fg = '#000000',bg = '#ffffff', anchor = 'nw')
functions.place(x = 25, y =160)

keyword = tk.Label(window, text = 'Keyword', font = ('Cambria', '10', 'bold'), fg = '#000000',anchor = 'nw')
keyword.place(x = 10, y =200)
InputKeyword = tk.Entry(window, width = 40)
InputKeyword.place(x = 90, y = 200)

#=========数据库选项==================
range = tk.Label(window, text = 'Database', font = ('Cambria', '10', 'bold'), fg = '#000000',anchor = 'nw')
range.place(x = 10, y =250)


var1 = tk.IntVar()
check_1 = tk.Checkbutton(window, text = 'ACM', font = ('Comic Sans MS', '10', 'bold'), variable = var1, onvalue = 1, offvalue = 0)
check_1.place(x = 100, y =250)

var2 = tk.IntVar()
check_2 = tk.Checkbutton(window, text = 'IEEE', font = ('Comic Sans MS', '10', 'bold'), variable = var2, onvalue = 1, offvalue = 0)
check_2.place(x = 160, y =250)

var3 = tk.IntVar()
check_3 = tk.Checkbutton(window, text = 'Arxiv', font = ('Comic Sans MS', '10', 'bold'), variable = var3, onvalue = 1, offvalue = 0)
check_3.place(x = 220, y =250)

var4 = tk.IntVar()
check_4 = tk.Checkbutton(window, text = 'All', font = ('Comic Sans MS', '10', 'bold'), variable = var4, onvalue = 1, offvalue = 0)
check_4.place(x = 280, y =250)


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
    output.config(width = 80, height = 20)
    output.place(x = 400, y = 130)
    output.insert('insert', content['abstract'])

    # ====下一页按钮========
    button_next = tk.Button(window, text='next', command=NextPage)
    button_next.place(x=940, y=300)

num = 0
recommend_string = tk.StringVar()
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

    global num
    num = 5
    global recommend_string
    recommend_string.set('check recommendation ' + str(num))
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



    abstract = tk.Label(window, text="Comment", font=('Times', '10', 'bold'))
    abstract.place(x=400, y=450)
    output = ScrolledText()
    output.config(width = 80, height = 12)
    output.place(x = 400, y = 470)
    output.insert('insert', content)

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



load_star2 = Image.open('star2.jpg')
w, h = load_star2.size
load_star2.thumbnail((w/6, h/6))
render_star2 = ImageTk.PhotoImage(load_star2)

img = tk.Label(window, image=render_star2, bg = '#ffffff')
img.place(x=5, y=370)


functions2 = tk.Label(window, text = ' 功能选项', font = ('仿宋', '13', 'bold'), fg = '#000000',bg = '#ffffff', anchor = 'nw')

functions2.place(x = 25, y =370)


button_1 = tk.Button(window, text = '搜索摘要', font = ('仿宋', '12', 'bold'), command = SearchAbstract)
button_1.place(x = 10, y =400)

button_2 = tk.Button(window, text = '搜索评论', font = ('仿宋', '12', 'bold'), command = SearchComment)
button_2.place(x = 120, y =400)

button_3 = tk.Button(window, text = '数据分析', font = ('仿宋', '12', 'bold'), command = DataAnalysis)
button_3.place(x = 230, y =400)


#=============推荐信箱===================


def ReceiveReference():
    global ret_list
    ret_list = paper_recommend(5)
    global i
    i = 0

    global length
    length = len(ret_list)
    global num
    num = 0
    global recommend_string
    recommend_string.set('check recommendation ' + str(num))
    NextPage()

load_star3 = Image.open('star3.jpg')
w, h = load_star3.size
load_star3.thumbnail((w/6, h/6))
render_star3 = ImageTk.PhotoImage(load_star3)

img = tk.Label(window, image=render_star3, bg = '#ffffff')
img.place(x=5, y=520)

functions3 = tk.Label(window, text = ' 推荐论文', font = ('仿宋', '13', 'bold'), fg = '#000000',bg = '#ffffff', anchor = 'nw')
functions3.place(x = 25, y =520)
load = Image.open('mailbox.jpg')
w, h = load.size
load.thumbnail((w/5, h/5))
render = ImageTk.PhotoImage(load)

img = tk.Label(window, image=render)
img.place(x=10, y=550)

recommend_string.set('check recommendation ' + str(num))
button_recv = tk.Button(window, textvariable = recommend_string, command = ReceiveReference)
button_recv.place(x = 10, y = 630)




window.mainloop()