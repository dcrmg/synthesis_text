# -*- coding:utf-8 -*-
import random
from PIL import Image
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import cv2
import numpy as np


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
            imageboxs[index][0] -= 4  # 偏移量（10个字最优）
            imageboxs[index][1] -= rap_num
            imageboxs[index][2] -= 4
            imageboxs[index][3] -= (rap_num-1)

    elif temp < 6:
        x = random.random() * 0.03 * 0.3
        y = random.random() * 0.03
        for index in range(len(imageboxs)):
            imageboxs[index][0] -= 3
            imageboxs[index][1] -= rap_num
            imageboxs[index][2] -= 3
            imageboxs[index][3] -= (rap_num-1)
    elif temp < 4:
        x = random.random() * 0.05
        y = random.random() * 0.05 * -0.5
        for index in range(len(imageboxs)):
            imageboxs[index][0] -= 4
            imageboxs[index][1] += (rap_num-1)
            imageboxs[index][2] -= 4
            imageboxs[index][3] += rap_num+1
    else:
        x = random.random() * 0.05 * -0.4
        y = random.random() * 0.05 * -0.4
        for index in range(len(imageboxs)):
            imageboxs[index][0] += 2
            imageboxs[index][1] += (rap_num-1)
            imageboxs[index][2] += 2
            imageboxs[index][3] += rap_num

    x=x*1.5 # 水平方向畸變可以大一點
    y=y*0.6  # 垂直方向畸變小一點

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
    for _ in range(randNum(2200, 4000)):
        draw.point((randNum(0, image_size_choose), randNum(0, image_size_choose)), fill=color[randNum(0,3)])


#添加干扰线
def addline(draw, size):
    draw.line((randNum(0, size[0]), randNum(0, size[1]), randNum(0, size[0]), randNum(0, size[1])),
              fill=(100, 100, 100), width=randNum(2, 3))

# 颜色增强变换
def enhance_color(img):
    enhance_color_rate = randNum(8,16)
    return ImageEnhance.Color(img).enhance(enhance_color_rate/10.0)

def enhance_brighness(img):
    enhance_brightness = randNum(8,15)
    return ImageEnhance.Brightness(img).enhance(enhance_brightness/10.0)

def enhance_sharpness(img):
    enhance_sharpness = randNum(-2,3)
    enhance_sharpness = enhance_sharpness if enhance_sharpness>=0 else 0
    return ImageEnhance.Sharpness (img).enhance(enhance_sharpness)


def randNum(low, high):
    return random.randint(low, high)


def blur_img(bimg,rate=0.3):
    c_num = randNum(0, 100)
    if c_num > 100 * rate:
        return bimg

    num = [0, 1, 2, 3, 4, 5]
    num_c = np.random.choice(num)

    if num_c >1:
        img = cv2.cvtColor(np.asarray(bimg), cv2.COLOR_RGB2BGR)

        num_ = [1, 2, 3, 4, 3, 2, 3, 2, 2, 3, 2]
        num_cc = int(np.random.choice(num_))

        blur_img = cv2.blur(img,(num_cc, num_cc))
        image = Image.fromarray(cv2.cvtColor(blur_img, cv2.COLOR_BGR2RGB))
    else:
        img = cv2.cvtColor(np.asarray(bimg), cv2.COLOR_RGB2BGR)
        median = cv2.medianBlur(img, 3)
        image = Image.fromarray(cv2.cvtColor(median, cv2.COLOR_BGR2RGB))

    return image


#
# # 中值滤波
# def median_blur(bimg):
#     img = cv2.cvtColor(np.asarray(bimg), cv2.COLOR_RGB2BGR)
#     median = cv2.medianBlur(img, 3)
#     image = Image.fromarray(cv2.cvtColor(median, cv2.COLOR_BGR2RGB))
#     return image
#
# # 均值滤波
# def _blur(bimg):
#     img = cv2.cvtColor(np.asarray(bimg), cv2.COLOR_RGB2BGR)
#
#     num = [1,2,3,4,5,2,3,4,2,3,2]
#     num_c =  np.random.choice(num)
#
#     blur_img = cv2.blur = cv2.blur(img,(num_c,num_c))
#     image = Image.fromarray(cv2.cvtColor(blur_img, cv2.COLOR_BGR2RGB))
#     return image


def warpImage(image,warp_rate=0.3):

    c_num = randNum(0,100)
    if c_num>100*warp_rate:
        return image

    img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w, h = img.shape[0:2]

    choice_xy = randNum(0,3)
    warp_angle = [-1,0,0,0,0,1]
    warp_A = np.random.choice(warp_angle)
    if choice_xy>0:
        warp_y = randNum(-40,40)
        warpR = get_warp_M(angley=warp_y,w=w,h=h,anglez=warp_A)
        warp_img = cv2.warpPerspective(img, warpR, (h, w))
    else:
        warp_x = randNum(-35,35)
        warpR = get_warp_M(anglex=warp_x,w=w,h=h,anglez=warp_A)
        warp_img = cv2.warpPerspective(img, warpR, (h, w))


    image = Image.fromarray(cv2.cvtColor(warp_img, cv2.COLOR_BGR2RGB))

    return image



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