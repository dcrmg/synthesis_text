# -*- coding:utf-8 -*-

'''

import cv2
import numpy as np
# 读取一张斯里兰卡拍摄的大象照片
img = cv2.imread('/home/dcrmg/Gen_text_0508/synthesis_text-master/data/0/5fcef00a-5295-11e8-b9cb-000c29cf3ddc.jpg')


# x轴的剪切变换，角度15°
theta = -8 * np.pi / 180
M_shear = np.array([
[1, np.tan(theta), 0],
[0, 1, 0]
], dtype=np.float32)
img_sheared = cv2.warpAffine(img, M_shear, img.shape[::-1][1:])
cv2.imwrite('lanka_safari_sheared_x.jpg', img_sheared)


# y轴的剪切变换，角度15°
theta = 45 * np.pi / 180
M_shear = np.array([
[1, 0, 0],
[0, np.tan(theta), 0]
], dtype=np.float32)
img_sheared = cv2.warpAffine(img, M_shear, img.shape[::-1][1:])
cv2.imwrite('lanka_safari_sheared_y.jpg', img_sheared)







# 某种变换，具体旋转+缩放+旋转组合可以通过SVD分解理解
M = np.array([
[1, 0.5, 0],
[0, 1, 1]
], dtype=np.float32)
img_transformed = cv2.warpAffine(img, M, img.shape[::-1][1:])
cv2.imwrite('lanka_safari_transformed.jpg', img_transformed)

'''

# -*- coding:utf-8 -*-
import cv2
import numpy as np


def rad(x):
    return x * np.pi / 180


img = cv2.imread('/home/dcrmg/Gen_text_0508/synthesis_text-master/data/0/5fcef00a-5295-11e8-b9cb-000c29cf3ddc.jpg')
cv2.imshow("original", img)

# 扩展图像，保证内容不超出可视范围
img = cv2.copyMakeBorder(img, 200, 200, 200, 200, cv2.BORDER_CONSTANT, 0)
w, h = img.shape[0:2]

anglex = 0
angley = 30
anglez = 0  # 是旋转
fov = 42
while 1:
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

    result = cv2.warpPerspective(img, warpR, (h, w))
    cv2.imshow("result", result)
    c = cv2.waitKey(30)

    # anglex += 3      #auto rotate
    # anglez += 1       #auto rotate
    # angley += 2      #auto rotate

    # 键盘控制
    if 27 == c:  # Esc quit
        break;
    if c == ord('w'):
        anglex += 1
    if c == ord('s'):
        anglex -= 1
    if c == ord('a'):
        angley += 1
        print(angley)
        # dx=0
    if c == ord('d'):
        angley -= 1
    if c == ord('u'):
        anglez += 1
    if c == ord('p'):
        anglez -= 1
    if c == ord('t'):
        fov += 1
    if c == ord('r'):
        fov -= 1
    if c == ord(' '):
        anglex = angley = anglez = 0
    if c == ord('q'):
        print("======================================")
        print('旋转矩阵：\n', r)
        print("angle alpha: ", anglex, 'angle beta: ', angley, "dz: ", anglez, ": ", z)

cv2.destroyAllWindows()