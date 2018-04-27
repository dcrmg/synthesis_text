# -*- coding:utf-8 -*-

import os
from random_noise import *
from background_font_cropus_gen import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from uuid import uuid1
from other_work import expend_box



img_num_has_created = 0

def draw_txt(H,corpus_path = glob.glob('./corpus/*.txt'),fonts=glob.glob('./font/*.*'),
             maxLen=10,minLen=10,imgsize=[860, 1024, 1600],backPaths=glob.glob('./bg/*.*'),swap_rate=0.9):

    # 绘制文字  生成50个，每个长度是10的文字序列
    txtlist = select_txt(corpus_path,maxLen,minLen)

    # 随机挑选一个背景图片并随机resize，很小概率下会生成纯白色图片
    bimg, size = buider_bimg(imgsize,backPaths)

    # print size
    X, Y = size
    initX, initY = int(size[0] * 0.1), int(size[0] * 0.1)

    textboxs = []
    imgBoxes = []

    draw = ImageDraw.Draw(bimg)
    fontType = random.choice(fonts)  # 随机获取一种字体

    cX = initX
    cY = initY
    span = 30
    for lable in txtlist:
        fontSize = random.randint(28, 40)  # 字体大小
        # fontSize=10
        font = ImageFont.truetype(fontType, fontSize)

        charW, charH = draw.textsize(text=lable, font=font)
        if cY < Y - 3.4*initY and cX + charW <= X - initX:
            draw.text(xy=(cX, cY), text=lable, font=font, fill="black")
            box = cX, cY, cX + charW, cY + charH


            # x1, y1, x2, y2 = fromat_box(box)
            x1, y1, x2, y2 = expend_box(box,size[0])


            # imgBoxes.append([x1, y1, x2, y2])
            imgBoxes.append([x1, y1, x2, y2])
            textboxs.append(lable)
            cY += charH + span
            cX += span-5
        else:
            pass

    temp = randNum(0, 1200)


    bimg = enhance_sharpness(bimg)
    bimg = enhance_brighness(bimg)
    bimg = enhance_color(bimg)

    if temp >=1020 and temp<=1200*swap_rate:
        bimg = enhance_brighness(bimg)
        bimg = enhance_color(bimg)

    elif temp>= 950:
        bimg = enhance_sharpness(bimg)
        addline(draw, size)

    elif temp >= 700:
        bimg, imgBoxes = setwarp(bimg, size, imgBoxes,H)
        addline(draw, size)
    elif temp >= 600:
        setnoisy(draw,size[0])
        bimg = setrorate(bimg,H)
        addline(draw, size)
    elif temp >= 500:
        setnoisy(draw,size[0])
        addline(draw, size)
        bimg = setdim(bimg)
    elif temp >= 400:
        setnoisy(draw,size[0])
    elif temp >= 300:
        setnoisy(draw,size[0])
        addline(draw, size)
    elif temp >= 200:
        bimg = setdim(bimg)
        bimg = setrorate(bimg,H)
    elif temp >= 100:
        bimg, imgBoxes = setwarp(bimg, size, imgBoxes,H)
    elif temp >=50:
        bimg=setrorate(bimg,H)

    return bimg, imgBoxes, textboxs


def imgscreate(W,H,wordclassnum,corpus_path = glob.glob('./corpus/*.txt'),
               background_path=glob.glob('./bg/*.*'),font_path=glob.glob('./font/*.*'),
               maxLen=10,minLen=10,image_size=[860, 1024, 1600] ,root='./data/0',show_interval=1000):

    global img_num_has_created

    # 图像生成和对应文本保存
    im, imgBoxes, texts = draw_txt(H,corpus_path,font_path,maxLen,minLen,image_size,background_path)

    for index, box in enumerate(imgBoxes):
        # print box
        img_num_has_created += 1
        smimg = im.crop(box)
        path = os.path.join(root, uuid1().__str__())
        smimg = smimg.resize((W, H), Image.ANTIALIAS)
        sming = smimg.convert("RGB")
        sming.save(path + ".jpg")

        with open(path + ".txt", "w") as datatxt:
            datatxt.write(texts[index].encode('utf-8'))

        for word in texts[index]:
            if word not in wordclassnum.keys():
                wordclassnum[word] = 1
            else:
                num = wordclassnum[word]
                wordclassnum[word] = num + 1

        if img_num_has_created % show_interval == 0:
            print "create %d picture" % img_num_has_created

    return wordclassnum