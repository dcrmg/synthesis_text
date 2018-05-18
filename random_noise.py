# -*- coding:utf-8 -*-
import random
from PIL import Image
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import cv2
import numpy as np


def move_box(imageboxs,move_rate=0.7):
    c_num = randNum(0,100)
    if c_num>100*move_rate:
        return imageboxs
    x_ = random.randint(-3, 0)  # 上边沿
    x__= random.randint(1,4)  # 下边沿


    y_ = random.randint(-20, 20)
    y__= random.randint(-20, 20)


    for index in range(len(imageboxs)):
        imageboxs[index][0] += y_
        imageboxs[index][1] += x_
        imageboxs[index][2] += y__
        imageboxs[index][3] += x__

    
    return imageboxs


# 添加随机噪声点
def setnoisy(draw,image_size_choose,flag=True,set_rate=0.1):
    c_num = randNum(0, 100)
    if c_num > 100 * set_rate:
        return
    if not flag:
        return

    # 填充噪点
    color = [(90, 90, 90),(100, 100, 100),(120,120,120),(50, 50, 50)]
    for _ in range(randNum(1600, 3200)):
        draw.point((randNum(0, image_size_choose), randNum(0, image_size_choose)), fill=color[randNum(0,3)])


#添加干扰线
def addline(draw, size,flag,add_rate=0.1):
    if not flag:
        return
    c_num = randNum(0, 100)
    if c_num > 100 * add_rate:
        return
    fill_num = [(110, 110, 110),(130,130,130),(150, 150, 150),(120,120,120)]
    draw.line((randNum(0, size[0]), randNum(0, size[1]), randNum(0, size[0]), randNum(0, size[1])),
              fill=fill_num[randNum(0,3)], width=randNum(2, 3))

# 颜色增强变换
def enhance_color(img,enc_rate=0.1):
    c_num = randNum(0, 100)
    if c_num > 100 * enc_rate:
        return img
    enhance_color_rate = randNum(8,14)
    return ImageEnhance.Color(img).enhance(enhance_color_rate/10.0)

def enhance_brighness(img,enh_rate=0.1):
    c_num = randNum(0, 100)
    if c_num > 100 * enh_rate:
        return img
    enhance_brightness = randNum(8,13)
    return ImageEnhance.Brightness(img).enhance(enhance_brightness/10.0)

def enhance_sharpness(img,ena_rate=0.1):
    c_num = randNum(0, 100)
    if c_num > 100 * ena_rate:
        return img
    enhance_sharpness = randNum(-1,2)
    # enhance_sharpness = enhance_sharpness if enhance_sharpness>=0 else 0
    return ImageEnhance.Sharpness (img).enhance(enhance_sharpness)


def randNum(low, high):
    return random.randint(low, high)


def blur_img(bimgs,blur_rate=0.5):


    flag = True
    c_num = randNum(0, 100)
    if c_num > 100 * blur_rate:
        return bimgs, flag

    num = [0, 1, 2, 3, 4]
    num_c = np.random.choice(num)

    if num_c >=3:
        img = cv2.cvtColor(np.asarray(bimgs), cv2.COLOR_RGB2BGR)

        num_ = [2, 3, 4, 3, 3, 2, 3, 2, 4, 4, 5]
        num_cc = int(np.random.choice(num_))

        blur_im = cv2.blur(img,(num_cc, num_cc))
        bimgs = Image.fromarray(cv2.cvtColor(blur_im, cv2.COLOR_BGR2RGB))
    if num_c >=2:
        img = cv2.cvtColor(np.asarray(bimgs), cv2.COLOR_RGB2BGR)
        median = cv2.medianBlur(img, 3)
        bimgs = Image.fromarray(cv2.cvtColor(median, cv2.COLOR_BGR2RGB))
        flag = False
    elif num_c >=0:
        num_ = [1, 3, 1, 3, 3, 3, 3, 5]
        num_cc = int(np.random.choice(num_))

        sig = randNum(0,25)
        sig = sig/10.0

        img = cv2.cvtColor(np.asarray(bimgs), cv2.COLOR_RGB2BGR)
        gaussianResult = cv2.GaussianBlur(img, (num_cc, num_cc), sig)
        bimgs = Image.fromarray(cv2.cvtColor(gaussianResult, cv2.COLOR_BGR2RGB))

    return bimgs,flag


def warpImage(bimg,warp_rate=0.7):

    c_num = randNum(0,100)
    if c_num>100*warp_rate:
        return bimg

    img = cv2.cvtColor(np.asarray(bimg), cv2.COLOR_RGB2BGR)
    w, h = img.shape[0:2]

    choice_xy = randNum(1,5)
    warp_angle = [0,0]

    warp_A = np.random.choice(warp_angle)
    if choice_xy>=4:
        warp_y = randNum(-21,21)  ###############################
        warpR = get_warp_M(angley=warp_y,w=w,h=h,anglez=warp_A)
        warp_img = cv2.warpPerspective(img, warpR, (h, w))
        bimg = Image.fromarray(cv2.cvtColor(warp_img, cv2.COLOR_BGR2RGB))

    elif choice_xy >= 3:
        warp_x = randNum(-8,8)   ###############################
        warpR = get_warp_M(anglex=warp_x,w=w,h=h,anglez=warp_A)
        warp_img = cv2.warpPerspective(img, warpR, (h, w))
        bimg = Image.fromarray(cv2.cvtColor(warp_img, cv2.COLOR_BGR2RGB))

    elif choice_xy >=1:
        warp_y = randNum(-11, 11)  ###############################
        warp_x = randNum(-6,6)   ###############################
        warpR = get_warp_M(anglex = warp_x, angley=warp_y, w=w, h=h, anglez=warp_A)
        warp_img = cv2.warpPerspective(img, warpR, (h, w))
        bimg = Image.fromarray(cv2.cvtColor(warp_img, cv2.COLOR_BGR2RGB))

    return bimg



def rad(x):
    return x * np.pi / 180

def get_warp_M(anglex=0,angley=0,anglez=0,w=240,h=36,fov=42):
    # 镜头与图像间的距离，21为半可视角，算z的距离是为了保证在此可视角度下恰好显示整幅图像
    z = np.sqrt(w ** 2 + h ** 2) / 2 / np.tan(rad(fov / 2))
    # 齐次变换矩阵
    rx = np.array([[1, 0, 0, 0],
                   [0, np.cos(rad(anglex)), -np.sin(rad(anglex)), 0],
                   [0, -np.sin(rad(anglex)), np.cos(rad(anglex)), 0, ],
                   [0, 0, 0, 1]], np.float32)

    ry = np.array([[np.cos(rad(angley)), 0, np.sin(rad(angley)), 0],
                   [0, 1, 0, 0],
                   [-np.sin(rad(angley)), 0, np.cos(rad(angley)), 0, ],
                   [0, 0, 0, 1]], np.float32)

    rz = np.array([[np.cos(rad(anglez)), np.sin(rad(anglez)), 0, 0],
                   [-np.sin(rad(anglez)), np.cos(rad(anglez)), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]], np.float32)

    r = rx.dot(ry).dot(rz)

    # 四对点的生成
    pcenter = np.array([h / 2, w / 2, 0, 0], np.float32)

    p1 = np.array([0, 0, 0, 0], np.float32) - pcenter
    p2 = np.array([w, 0, 0, 0], np.float32) - pcenter
    p3 = np.array([0, h, 0, 0], np.float32) - pcenter
    p4 = np.array([w, h, 0, 0], np.float32) - pcenter

    dst1 = r.dot(p1)
    dst2 = r.dot(p2)
    dst3 = r.dot(p3)
    dst4 = r.dot(p4)

    list_dst = [dst1, dst2, dst3, dst4]

    org = np.array([[0, 0],
                    [w, 0],
                    [0, h],
                    [w, h]], np.float32)

    dst = np.zeros((4, 2), np.float32)

    # 投影至成像平面
    for i in range(4):
        dst[i, 0] = list_dst[i][0] * z / (z - list_dst[i][2]) + pcenter[0]
        dst[i, 1] = list_dst[i][1] * z / (z - list_dst[i][2]) + pcenter[1]

    warpR = cv2.getPerspectiveTransform(org, dst)
    return warpR
