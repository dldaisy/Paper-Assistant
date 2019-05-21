import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

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

keyword = tk.Label(window, text = '关键字', bg = '#434343', fg = '#ffffff',anchor = 'nw')
keyword.place(x = 10, y =200)
#=========输入框=================
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
def Search(input_string, input_source = None) -> str:
    pass

def Search_Analysis(input_string) -> str:
    pass

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
        input_source.append('All')
    text = Search(input_string, input_source)
    #output window
    output = ScrolledText()
    output.config(width = 80, height = 20)
    output.place(x = 400, y = 100)
    output.insert('insert', text)

def SearchComment():
    input_string = InputKeyword.get()
    text = Search(input_string)
    # output window
    output = ScrolledText()
    output.config(width=80, height=20)
    output.place(x=400, y=400)
    output.insert('insert', text)

def DataAnalysis():
    # 使用canvas显示image
    pass
button_1 = tk.Button(window, text = '搜索摘要', command = SearchAbstract)
button_1.place(x = 10, y =400)

button_2 = tk.Button(window, text = '搜索评论', command = SearchComment)
button_2.place(x = 90, y =400)

button_3 = tk.Button(window, text = '数据分析', command = DataAnalysis)
button_3.place(x = 170, y =400)


#=============推荐信箱===================

def ReceiveReference():
    pass

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