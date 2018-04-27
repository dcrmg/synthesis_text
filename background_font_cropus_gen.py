# -*- coding:utf-8 -*-

from PIL import Image
import numpy as np
import random
import glob

def read_txt(corpus_path = glob.glob('./corpus/*.txt')):
    # 获取语料文本数据
    dataList = []
    intP = 5
    for _ in range(intP):
        txt = np.random.choice(corpus_path)
        with open(txt, "r") as f:
            datas = f.read().decode('utf-8')
        datas = [line.strip() for line in datas.split(u'\n') if line.strip() != u'' and len(line.strip()) > 1]
        dataList.extend(datas)

    np.random.shuffle(dataList)
    np.random.shuffle(dataList)
    return np.random.choice(dataList, size=100)


def select_txt(corpus_path = glob.glob('./corpus/*.txt'),maxLen=10,minLen=10):
    # 随机产生minlen到maxlen长度的文本
    txtlist = []
    dataList = read_txt(corpus_path)
    # splitPatters = [u',', u':', u'-', u' ', u';', u'。']
    # splitPatter = np.random.choice(splitPatters, 1)
    # data = splitPatter[0].join(dataList)
    data = ''.join(dataList)
    for _ in range(50):
        num = randNum(minLen, maxLen)
        index = randNum(0, len(data) - num)
        txtlist.append(data[index:index + num])
    return txtlist


def randNum(low, high):
    return random.randint(low, high)


def buider_bimg(imgsize=[860, 1024, 1600],backPaths=glob.glob('./bg/*.*')):

    # 图像背景生成
    temp = randNum(0, 10)
    size = random.choice(imgsize)

    Size = size, size
    if temp > 8:
        p = Image.new('RGBA', Size, (255, 255, 255))
    else:
        bg = Image.open(np.random.choice(backPaths))
        p = bg.resize(Size)
    return p, Size