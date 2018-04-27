# -*- coding:utf-8 -*-
import random
from PIL import Image
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


# 防射变换+文本框偏移
def setwarp(im, size, imageboxs, small_image_size_choose_height,x_warp =1,y_warp=0.2):

    rap_num = 2
    if small_image_size_choose_height <= 42:
        rap_num = 1

    # 创建扭曲
    temp = randNum(1, 10)
    if temp < 8:
        x = random.random() * 0.03
        y = random.random() * 0.03
        for index in range(len(imageboxs)):
            imageboxs[index][0] -= 8  # 偏移量（10个字最优）
            imageboxs[index][1] -= rap_num
            imageboxs[index][2] -= 8
            imageboxs[index][3] -= (rap_num-1)

    elif temp < 6:
        x = random.random() * 0.03 * 0.3
        y = random.random() * 0.03
        for index in range(len(imageboxs)):
            imageboxs[index][0] -= 6
            imageboxs[index][1] -= rap_num
            imageboxs[index][2] -= 6
            imageboxs[index][3] -= (rap_num-1)
    elif temp < 4:
        x = random.random() * 0.05
        y = random.random() * 0.05 * -0.5
        for index in range(len(imageboxs)):
            imageboxs[index][0] -= 12
            imageboxs[index][1] += (rap_num-1)
            imageboxs[index][2] -= 12
            imageboxs[index][3] += rap_num+1
    else:
        x = random.random() * 0.05 * -0.4
        y = random.random() * 0.05 * -0.4
        for index in range(len(imageboxs)):
            imageboxs[index][0] += 4
            imageboxs[index][1] += (rap_num-1)
            imageboxs[index][2] += 4
            imageboxs[index][3] += rap_num

    x=x*2.0 # 水平方向畸變可以大一點
    y=y*0.8  # 垂直方向畸變小一點

    # 创建扭曲 ,对于第三个(a,b,c,d,e,f)参数，x=ax + by + c, y=dx + ey + f
    im = im.transform(size, Image.AFFINE, (1, x, x_warp, y, 1, y_warp),
                      Image.BILINEAR)

    # im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return im, imageboxs

# 旋轉角度
def setrorate(im,imagesize_small_height,angle_rate =0.6):

    # 旋转
    temp = randNum(-angle_rate*10, angle_rate*10)

    if imagesize_small_height >= 40:
        temp = randNum(1-angle_rate*10, angle_rate*10-1)

    if temp != 0:
        angle = np.pi / 6 / temp
        im = im.rotate(angle,expand=True)
    return im


# 模糊变换
def setdim(im):
    fts = [ImageFilter.DETAIL, ImageFilter.SMOOTH, ImageFilter.SMOOTH_MORE]
    return im.filter(np.random.choice(fts))


# 添加随机噪声点
def setnoisy(draw,image_size_choose):

    # 填充噪点
    color = [(0, 0, 0),(0, 0, 0),(100,100,100),(160, 160, 160)]
    for _ in range(randNum(1800, 3600)):
        draw.point((randNum(0, image_size_choose), randNum(0, image_size_choose)), fill=color[randNum(0,3)])


#添加干扰线
def addline(draw, size):
    draw.line((randNum(0, size[0]), randNum(0, size[1]), randNum(0, size[0]), randNum(0, size[1])),
              fill=(100, 100, 100), width=randNum(2, 3))

# 颜色增强变换
def enhance_color(img):
    enhance_color_rate = randNum(8,20)
    return ImageEnhance.Color(img).enhance(enhance_color_rate/10.0)

def enhance_brighness(img):
    enhance_brightness = randNum(10,16)
    return ImageEnhance.Brightness(img).enhance(enhance_brightness/10.0)

def enhance_sharpness(img):
    enhance_sharpness = randNum(-3,3)
    enhance_sharpness = enhance_sharpness if enhance_sharpness>=0 else 0
    return ImageEnhance.Sharpness (img).enhance(enhance_sharpness)


def randNum(low, high):
    return random.randint(low, high)