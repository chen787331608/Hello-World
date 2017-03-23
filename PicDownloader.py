# -*- coding:utf-8 -*-
import re
import requests


i = 0


def dowmloadPic(html, keyword):
    global i
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    print '找到关键词:' + keyword + '的图片，现在开始下载图片...'
    for each in pic_url:
        print '正在下载第' + str(i+1) + '张图片，图片地址:' + str(each)
        pic_format = str(each).split('.')[-1]
        if pic_format.find('/'):
            pic_format = 'jpg'
        try:
            pic = requests.get(each, timeout=10)
        except:
            print '【错误】当前图片无法下载'
            continue
        string = 'pictures/' + keyword + '_' + str(i) + '.%s' % pic_format
        fp = open(string.decode('utf-8'), 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1


if __name__ == '__main__':
    word = raw_input("Input key word: ")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' +\
        word + '&ct=201326592&v=flip'
    result = requests.get(url)
    dowmloadPic(result.text, word)
    while True:
        url1 = url + '&pn=%d' % i
        result = requests.get(url1)
        dowmloadPic(result.text, word)
