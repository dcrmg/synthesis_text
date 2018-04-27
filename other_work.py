# -*- coding:utf-8 -*-

import os
import random

def make_root_folder(root='./data/0'):
    if not os.path.exists(root):
        os.makedirs(root)

def write_statistics(wordclassnum,filename = 'Statistics.txt'):
    with open(filename, 'w') as fs:
        Stat = ""
        for key, value in wordclassnum.items():
            Stat += key.encode('utf-8') + "->" + str(value) + "\n"
        fs.write(Stat)


def expend_box(box,imagesize_choose):

    x_expend = random.randint(34, 38)
    y_expend = random.randint(3, 4)

    x, y, x1, y1 = box

    x = x - x_expend if (x - x_expend >= 0) else 0
    y = y - y_expend if y - y_expend >= 0 else 0

    x1 = x1 + x_expend if imagesize_choose > (x1 + x_expend) else imagesize_choose - 1
    y1 = y1 + y_expend if imagesize_choose > (y1 + y_expend) else imagesize_choose - 1

    return x, y, x1, y1

def fromat_box(box):

    global width,height
    # 格式化坐标点
    a, b, a1, b1 = box

    # a = random.randint

    # width = width1[random.randint(0,7)]
    # height =height1[random.randint(0,8)]

    if a1 - a < width and b1 - b < height:
        spanx = (width - a1 + a) // 2
        x1, x2 = a - spanx, a1 + spanx
        spany = (height - b1 + b) // 2
        y1, y2 = b - spany, b1 + spany
    elif a1 - a < width and b1 - b > height:
        spanx = (width - a1 + a) // 2
        x1, x2 = a - spanx, a1 + spanx
        spany = (b1 - b - height) // 2
        y1, y2 = b + spany, b1 - spany
    elif a1 - a > width and b1 - b < height:
        spany = (height - b1 + b) // 2
        y1, y2 = b - spany, b1 + spany
        spanx = (a1 - a - width) // 2
        x1, x2 = a + spanx, a1 - spanx
    else:
        x1, y1, x2, y2 = a - 10, b - 2, a1 + 10, b1 + 2

    return x1, y1, x2, y2