from predcit import *
import json
import requests
from numpy import *
from requests_toolbelt import MultipartEncoder
import os
import cv2
import numpy as np
fb_token = 'EAAF3eZAbuBR8BAOIKtW9JeIUDWqMioUQNEoKZCvCSum1ZAVGsXDHuGTu42Btu6hNTIijGJ5TKyorjzzYEVkXs2U5d2QRv7YTHOyjxtZCZCIqGv64jp3rfxLBdHbtmtEO2ZB19GFktS6uRZBSkv3FTLZBBmmQ5sg7FIHxE4vcQZCd4hRk0TtEfjqvg'
all_count = 1


def get_rec(coordinate, num_list):
    x_cor = [coordinate[num_list[0]][0], coordinate[num_list[1]]
             [0], coordinate[num_list[2]][0], coordinate[num_list[3]][0]]
    y_cor = [coordinate[num_list[0]][1], coordinate[num_list[1]]
             [1], coordinate[num_list[2]][1], coordinate[num_list[3]][1]]

    return min(x_cor), max(x_cor) - min(x_cor), min(y_cor), max(y_cor) - min(y_cor)


def conver1(coordinates):
    """
    图片TPS变换
    :return:
    """
    tps = cv2.createThinPlateSplineShapeTransformer()
    sshape = np.array(coordinates[0], np.int32)
    tshape = np.array(coordinates[1], np.int32)
    sshape = sshape.reshape(1, -1, 2)
    tshape = tshape.reshape(1, -1, 2)

    matches = list()
    for i in range(13):
        matches.append(cv2.DMatch(i, i, 0))
    tps.estimateTransformation(tshape, sshape, matches)
    img2_o = cv2.imread('my_animal.jpg')
    out_img = tps.warpImage(img2_o)
    # 融合原图像
    targimg = cv2.imread('target.jpg')

    # 获得重点区域矩阵
    x1, width1, y1, height1 = get_rec(coordinates[1], [0, 1, 2, 3])
    x2, width2, y2, height2 = get_rec(coordinates[1], [4, 5, 6, 7])
    x3, width3, y3, height3 = get_rec(coordinates[1], [9, 10, 11, 12])

    center1 = (int(x1 + width1 / 2), int(y1 + height1 / 2))
    center2 = (int(x2 + width2 / 2), int(y2 + height2 / 2))
    center3 = (int(x3 + width3 / 2), int(y3 + height3 / 2))

    lefteyeimg = targimg[y1 - 15:y1 + height1 + 15, x1 - 15:x1 + width1 + 15]
    righteyeimg = targimg[y2 - 15:y2 + height2 + 15, x2 - 15:x2 + width2 + 15]
    mouthimg = targimg[y3 - 15:y3 + height3 + 15, x3 - 15:x3 + width3 + 15]

    mask1 = 255 * np.ones(lefteyeimg.shape, lefteyeimg.dtype)
    mask2 = 255 * np.ones(righteyeimg.shape, righteyeimg.dtype)
    mask3 = 255 * np.ones(mouthimg.shape, mouthimg.dtype)
    out_img = cv2.seamlessClone(
        lefteyeimg, out_img, mask1, center1, cv2.NORMAL_CLONE)
    out_img = cv2.seamlessClone(
        righteyeimg, out_img, mask2, center2, cv2.NORMAL_CLONE)
    out_img = cv2.seamlessClone(
        mouthimg, out_img, mask3, center3, cv2.NORMAL_CLONE)

    cv2.imwrite('final.jpg', out_img)


def reply():
    """
    Deal with request message
    :return:
    """

    # 获得预测坐标点
    result_index = get_result(['my_animal.jpg', 'target.jpg'])
    if len(result_index):
        conver1(result_index)
