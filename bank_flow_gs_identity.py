#-*- coding:utf-8 -*-
import cv2
import numpy as np
import pytesseract
import os

import ocr
import time
import shutil
import numpy as np
import sys
from PIL import Image
from glob import glob

print(sys.path)
def bank_flow_identity(imagePath): # imagePath  './test_images/gs.jpg'
    image = cv2.imread(imagePath, 1)
    print(image)
    #二值化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)

    rows,cols=binary.shape
    scale = 40
    #识别横线
    kernel  = cv2.getStructuringElement(cv2.MORPH_RECT,(cols//scale,1))
    eroded = cv2.erode(binary,kernel,iterations = 1)
    dilatedcol = cv2.dilate(eroded,kernel,iterations = 1)


    #识别竖线
    scale = 20
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,rows//scale))
    eroded = cv2.erode(binary,kernel,iterations = 1)
    dilatedrow = cv2.dilate(eroded,kernel,iterations = 1)


    #标识交点
    bitwiseAnd = cv2.bitwise_and(dilatedcol,dilatedrow)


    #标识表格
    merge = cv2.add(dilatedcol,dilatedrow)


    #识别黑白图中的白色点
    ys,xs = np.where(bitwiseAnd>0)
    mylisty=[]
    mylistx=[]

    #通过排序，获取跳变的x和y的值，说明是交点，否则交点会有好多像素值，我只取最后一点
    i = 0
    myxs=np.sort(xs)
    for i in range(len(myxs)-1):
        if(myxs[i+1]-myxs[i]>10):
            mylistx.append(myxs[i])
        i=i+1
    mylistx.append(myxs[i])
    # print(mylistx)
    # print(len(mylistx))

    i = 0
    myys=np.sort(ys)
    #print(np.sort(ys))
    for i in range(len(myys)-1):
        if(myys[i+1]-myys[i]>20):
            mylisty.append(myys[i])
        i=i+1
    mylisty.append(myys[i])

    i=0
    t = time.time()
    res=''
    for i in range(13):  #只有13行有效数字
        ROI = image[mylisty[i]:mylisty[i+1],mylistx[9]:mylistx[10]]

        result, image_framed = ocr.model(ROI)
        for key in result:
            print(result[key][1])
            res=res+result[key][1]+'||'
        i=i+1
    print("tsk complete, it took {:.3f}s".format(time.time() - t))
    return res

if __name__ == "__main__":

    testImgPath = os.path.join(os.getcwd(), 'test_images/gs.jpg')
    print(testImgPath)
    bank_flow_identity(testImgPath)