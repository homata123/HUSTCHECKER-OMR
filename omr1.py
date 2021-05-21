import cv2
import numpy as np
import util
import argparse
import imutils
import test,test2,test3,test4,test5
from test import grade
from imutils import contours
from imutils.perspective import four_point_transform
import imutils
from PIL import Image
from skimage import io
#

#
img=cv2.imread('data/raw26.png')
 #
width = 700
height = 906
img = cv2.resize(img, (width, height))
img_cont = img.copy()
img_cp = img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
img_edge = cv2.Canny(img_blur, 1, 30)

#cv2.imshow('ffff',img_edge)
#cv2.waitKey(0)
contours, hierarchy = cv2.findContours(img_edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img_cont, contours, -1, (0, 255, 0), 5)

r = util.rectContour(contours)

details = util.getCornerPoints(r[2])
answers2 = util.getCornerPoints(r[1])
answers1 = util.getCornerPoints(r[0])



cv2.drawContours(img_cp, answers1, -1, (0, 0, 255), 5) #red
cv2.drawContours(img_cp, details, -1, (255, 0, 0), 5) #blue
cv2.drawContours(img_cp, answers2, -1, (0, 255, 0), 5) #green



details = util.reorder(details)
answers2 = util.reorder(answers2)
answers1 = util.reorder(answers1)


#bird eye view of details
pts1 = np.float32(details)
pts2 = np.float32([[0, 0],[1000, 0], [0, 600],[1000, 600]])
matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
imgWarpColored_details = cv2.warpPerspective(img, matrix, (1000, 600))
details_bev = cv2.cvtColor(imgWarpColored_details,cv2.COLOR_BGR2GRAY)
# bird eye view of answers2
pts1_ans2 = np.float32(answers2)
pts2_ans2 = np.float32([[0, 0], [500, 0], [0, 350], [500, 350]])
matrix = cv2.getPerspectiveTransform(pts1_ans2, pts2_ans2)  # GET TRANSFORMATION MATRIX
imgWarpColored_ans2 = cv2.warpPerspective(img, matrix, (500, 350))
ans2_bev = cv2.cvtColor(imgWarpColored_ans2, cv2.COLOR_BGR2GRAY)
#bird eye view of answer1
pts1_ans1 = np.float32(answers1)
pts2_ans1 = np.float32([[0, 0], [500, 0], [0, 550], [500, 550]])
matrix = cv2.getPerspectiveTransform(pts1_ans1, pts2_ans1)  # GET TRANSFORMATION MATRIX
imgWarpColored_ans1 = cv2.warpPerspective(img, matrix, (500, 550))
ans1_bev = cv2.cvtColor(imgWarpColored_ans1, cv2.COLOR_BGR2GRAY)

#
answers_1t9 = ans1_bev[10:550, 30:165]
answers_20t28 = ans1_bev[10:550, 202:330]
answers_37t40 = ans1_bev[15:260, 360:500]
answers_10t19 = ans2_bev[2:400, 55:245]
answers_29t36 = ans2_bev[5:275, 300:520]
md=ans2_bev[305:352, 300:495]

#
details=details_bev[60:800,10:1200]
#
answers_10t19=cv2.resize(src=answers_10t19,dsize=(128,600))
answers_29t36=cv2.resize(src=answers_29t36,dsize=(140,510))


#
cv2.imwrite('data/a8.png',answers_29t36)

#resu=test.grade(answers_1t9)+test3.grade(answers_20t28)
#print("Số điểm đạt được:",resu)