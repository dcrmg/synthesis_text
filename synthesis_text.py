# -*- coding:utf-8 -*-

from other_work import *
from image_creater import *

backPaths = glob.glob('./background/*.*')  # 背景图像路径
fonts = glob.glob('./font/*.*')  # 字体集路径, ttc 或者 ttf
corpusPaths = glob.glob('./corpus/*.txt')  # 语料库路径
maxLen = 10  # 每行最大字符个数
minLen = 10  # 每行最小字符个数

imgsize = [860, 1024, 1600]  # 背景图片缩放尺寸
width_list = [420,460,520,480]  # 生成样本实际宽度，自定义

height_lsit = [52,56,62,68,46,56,62,48]  # 生成样本实际高度，自定义

root = './data/1'  # 生成样本数据存放路径


imgsnum = 0  # 当前生成的图片个数
show_interval = 1000  # 生成n张图片打印一次

imgsize_random = 0

batch = 55000  # 生成图片批次（不是实际生成图片数量），自定义，一批大概100多张图片
wordclassnum = {}  # 统计字典


if __name__ == "__main__":

    make_root_folder(root)

    for i in range(batch):
        width = width_list[random.randint(0,len(width_list)-1)]
        height = height_lsit[random.randint(0,len(height_lsit)-1)]

        wordclassnum_ = imgscreate(width,height,wordclassnum,corpus_path=corpusPaths,background_path=backPaths,
                                   font_path=fonts,maxLen=maxLen,minLen=minLen,image_size=imgsize,root=root,
                                   show_interval=show_interval,)

        wordclassnum =dict(wordclassnum, **wordclassnum_)

        if i%1000 ==0:
            print ('{}/{}'.format(i,batch))

    write_statistics(wordclassnum, 'Statistics.txt')
