#! /usr/bin/env/python3
# -*- coding = utf-8 -*-
# author:Since July 2021.02.26

from bs4 import BeautifulSoup # 网页解析，获取数据

import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作

# 预先编译正则表达式对象
findtitle = re.compile(r'<div class="list_text" title="(.*?)">')



def main():
    baseurl = "http://www.future.whu.edu.cn/"

    datalist = getdata(baseurl)
    savepath = "未来网.xls"
    savedata(datalist,savepath)


def getdata(baseurl):
    datalist = []  # 用来存储爬取的网页信息
    #url = baseurl + str(i * 25)
    html = askurl(baseurl)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())
    for item in soup.find_all('div', class_="block_content"):  # 查找符合要求的字符串
        print(item)
        data = []
        item = str(item)
        link = re.findall(findtitle, item)  # 通过正则表达式查找
        for i in link:
            data.append(i)
        # print(link)
        # data.append(link)

        datalist.append(data)


    return datalist






def askurl(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

def savedata(datalist,savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet = book.add_sheet('未来网', cell_overwrite_ok=True) #创建工作表
    col = ("通知","文件","学习","活动")
    for i in range(0,4):
        sheet.write(0,i,col[i])  #列名
    for i in range(0,4):
       # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist[i]
        for j in range(0,6):
            sheet.write(j+1,i,data[j])  #数据
    book.save(savepath) #保存

if __name__ == "__main__":  # 当程序执行时
    # 调用函数
     main()

     print("爬取完毕！")
