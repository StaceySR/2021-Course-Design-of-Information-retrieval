import tkinter.messagebox
from tkinter import *
from tkinter import ttk

from spider.Connection import common_crawler
from spider.CreateUrl import create_url
from spider.Spider import spider

win = tkinter.Tk()  # 定义一个窗体
win.title("个性化竞赛方案制定")

# 设置文本标签
# 第一部分：输入部分
title1 = Label(win, text='录入竞赛信息', font='Helvetica -36 bold')
type = Label(win, text='竞赛类别：', font='song -20')
level = Label(win, text='竞赛级别：', font='song -20')
range = Label(win, text='排序方式：', font='song -20')

# 设置标签排列位置
title1.grid(row=0, column=1)
type.grid(row=1, column=0, padx=5, pady=5)
level.grid(row=2, column=0, padx=5, pady=5)
range.grid(row=3, column=0, padx=5, pady=5)

url_initial = "https://www.saikr.com/vs/mcm/0/0"
soup_initial = common_crawler(url_initial, 3)
comp_type, comp_level, comp_range = create_url(soup_initial)

keys_type = tuple(comp_type.keys())
keys_level = tuple(comp_level.keys())
keys_range = tuple(comp_range.keys())

typeChosen = ttk.Combobox(win, width=28, font='song -20', state="readonly")
typeChosen['value'] = keys_type  # 设置下拉列表的值
typeChosen.grid(row=1, column=1)
typeChosen.current(0)

levelChosen = ttk.Combobox(win, width=28, font='song -20', state="readonly")
levelChosen['value'] = keys_level  # 设置下拉列表的值
levelChosen.grid(row=2, column=1)
levelChosen.current(0)

rangeChosen = ttk.Combobox(win, width=28, font='song -20', state="readonly")
rangeChosen['value'] = keys_range  # 设置下拉列表的值
rangeChosen.grid(row=3, column=1)
rangeChosen.current(0)

lb_sponsor = Label(win, bg='white', width=5, text="1")
lb_prize = Label(win, bg='white', width=5, text="1")
lb_money = Label(win, bg='white', width=5, text="1")
lb_signup = Label(win, bg='white', width=5, text="1")
lb_hot = Label(win, bg='white', width=5, text="1")
page_show = Label(win, bg='white', width=5, text="1")

value_sponsor = 1
value_prize = 1
value_money = 1
value_signup = 1
value_hot = 1


def print_selection1(v):  # v是传入s表单的选择值
    lb_sponsor.config(text=v)
    global value_sponsor
    value_sponsor = int(v)


def print_selection2(v):  # v是传入s表单的选择值
    lb_prize.config(text=v)
    global value_prize
    value_prize = int(v)


def print_selection3(v):  # v是传入s表单的选择值
    lb_money.config(text=v)
    global value_money
    value_money = int(v)


def print_selection4(v):  # v是传入s表单的选择值
    lb_signup.config(text=v)
    global value_signup
    value_signup = int(v)


def print_selection5(v):  # v是传入s表单的选择值
    lb_hot.config(text=v)
    global value_hot
    value_hot = int(v)


# page
page = 1


def pageShow(v):  # v是传入s表单的选择值
    page_show.config(text=v)
    global page
    page = int(v)


# 进度条
page_scale = tkinter.Scale(win, label='请选择要浏览的页数', from_=1, to=30, orient=tkinter.HORIZONTAL, length=400, showvalue=0,
                           tickinterval=9, resolution=1, command=pageShow, font='Helvetica -18 bold')
scale_sponsor = tkinter.Scale(win, label='主办方占比', from_=1, to=100, orient=tkinter.HORIZONTAL, length=400, showvalue=0,
                              tickinterval=9, resolution=1, command=print_selection1)
scale_prize = tkinter.Scale(win, label='获奖比例占比', from_=1, to=100, orient=tkinter.HORIZONTAL, length=400, showvalue=0,
                            tickinterval=9, resolution=1, command=print_selection2)
scale_money = tkinter.Scale(win, label='奖金额度占比', from_=1, to=100, orient=tkinter.HORIZONTAL, length=400, showvalue=0,
                            tickinterval=9, resolution=1, command=print_selection3)
scale_signup = tkinter.Scale(win, label='报名费用占比', from_=1, to=100, orient=tkinter.HORIZONTAL, length=400, showvalue=0,
                             tickinterval=9, resolution=1, command=print_selection4)
scale_hot = tkinter.Scale(win, label='热度(被浏览量)占比', from_=1, to=100, orient=tkinter.HORIZONTAL, length=400, showvalue=0,
                          tickinterval=9, resolution=1, command=print_selection5)


page_show.grid(row=4, column=2)
scale_sponsor.grid(row=5, column=1)
scale_prize.grid(row=6, column=1)
scale_money.grid(row=7, column=1)
scale_signup.grid(row=8, column=1)
scale_hot.grid(row=9, column=1)

page_scale.grid(row=4, column=1)
lb_sponsor.grid(row=5, column=2)  # 主办方占比
lb_prize.grid(row=6, column=2)  # 获奖比例占比
lb_money.grid(row=7, column=2)  # 奖金额度占比
lb_signup.grid(row=8, column=2)  # 报名费用占比
lb_hot.grid(row=9, column=2)  # 热度占比

'''
设置一个尺度表单，
orient是方向(HORIZONTAL是横向)，
showvalue是实时显示选中的值（布尔型，0就是false），
tickinterval是表单划分尺度,
resolution是精度（1是精确到整数）
'''


# 设置触发事件函数
def clear_all():  # 清空所有输入框
    typeChosen.current(0)
    levelChosen.current(0)
    rangeChosen.current(0)


# 关闭窗口事件
def quit_win():
    win.quit()  # 关闭窗口
    print('窗口已关闭')


def save():
    # 将输入的数据保存起来
    type = typeChosen.get()
    level = levelChosen.get()
    range = rangeChosen.get()
    print(type, level, range)
    xlsx_name = "../DataSet/"+type + "+" + level + "+" + range  # 保存数据的xlsx文件

    # 计算比率
    value_all = value_sponsor + value_prize + value_money + value_signup + value_hot
    rate_sponsor = value_sponsor / value_all
    rate_prize = value_prize / value_all
    rate_money = value_money / value_all
    rate_signup = value_signup / value_all
    rate_hot = value_hot / value_all

    # print(rate_sponsor)
    # print(rate_prize)
    # print(rate_money)
    # print(rate_signup)
    # print(rate_hot)

    spider(soup_initial, type, level, range, page, xlsx_name)


# 设置按钮及排列位置
reset_button = Button(win, text='重新录入', command=clear_all, font=('宋体', '16'))  # 清空所有文本框中的内容
finish_input_button = Button(win, text='录入信息', command=save, font=('宋体', '16'))  # 将已录入信息展示出来
close_button = Button(win, text='关闭窗口', command=quit_win, font=('宋体', '16'))  # 关闭系统界面

reset_button.grid(row=1, column=2, padx=5, pady=5)
finish_input_button.grid(row=2, column=2, padx=5, pady=5)
close_button.grid(row=3, column=2, padx=5, pady=5)

win.mainloop()
