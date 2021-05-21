import cv2
import numpy as np
import util
import imutils
from PIL import Image


def result(img):
    width = 700
    height = 906
    img = cv2.resize(img, (width, height))
    img_cont = img.copy()
    img_cp = img.copy()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_edge = cv2.Canny(img_blur, 1, 30)

    # cv2.imshow('ffff',img_edge)
    # cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(img_edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img_cont, contours, -1, (0, 255, 0), 5)

    r = util.rectContour(contours)

    details = util.getCornerPoints(r[2])
    answers2 = util.getCornerPoints(r[1])
    answers1 = util.getCornerPoints(r[0])

    cv2.drawContours(img_cp, answers1, -1, (0, 0, 255), 5)  # red
    cv2.drawContours(img_cp, details, -1, (255, 0, 0), 5)  # blue
    cv2.drawContours(img_cp, answers2, -1, (0, 255, 0), 5)  # green

    details = util.reorder(details)
    answers2 = util.reorder(answers2)
    answers1 = util.reorder(answers1)
    # bird eye view of answers2
    pts1_ans2 = np.float32(answers2)
    pts2_ans2 = np.float32([[0, 0], [1000, 0], [0, 700], [1000, 700]])
    matrix = cv2.getPerspectiveTransform(pts1_ans2, pts2_ans2)  # GET TRANSFORMATION MATRIX
    imgWarpColored_ans2 = cv2.warpPerspective(img, matrix, (1000, 700))
    ans2_bev = cv2.cvtColor(imgWarpColored_ans2, cv2.COLOR_BGR2GRAY)
    # bird eye view of answer1
    pts1_ans1 = np.float32(answers1)
    pts2_ans1 = np.float32([[0, 0], [500, 0], [0, 550], [500, 550]])
    matrix = cv2.getPerspectiveTransform(pts1_ans1, pts2_ans1)  # GET TRANSFORMATION MATRIX
    imgWarpColored_ans1 = cv2.warpPerspective(img, matrix, (500, 550))
    ans1_bev = cv2.cvtColor(imgWarpColored_ans1, cv2.COLOR_BGR2GRAY)

    #
    answers_1t9 = ans1_bev[0:550, 30:165]
    answers_20t28 = ans1_bev[0:550, 202:330]
    answers_37t40 = ans1_bev[0:260, 360:500]
    answers_10t19 = ans2_bev[0:840, 120:480]
    answers_29t36 = ans2_bev[0:640, 600:1080]
    #



    ans1_thresh = cv2.threshold(answers_1t9, 150, 255, cv2.THRESH_BINARY_INV)[1]
    box_a1 = util.splitBoxes(ans1_thresh, 9, 4)

    ans2_thresh = cv2.threshold(answers_10t19, 150, 255, cv2.THRESH_BINARY_INV)[1]
    box_a2 = util.splitBoxes(ans2_thresh, 10, 4)

    ans3_thresh = cv2.threshold(answers_20t28, 150, 255, cv2.THRESH_BINARY_INV)[1]
    box_a3 = util.splitBoxes(ans3_thresh, 9, 4)

    ans4_thresh = cv2.threshold(answers_29t36, 150, 255, cv2.THRESH_BINARY_INV)[1]
    box_a4 = util.splitBoxes(ans4_thresh, 8, 4)

    ans5_thresh = cv2.threshold(answers_37t40, 150, 255, cv2.THRESH_BINARY_INV)[1]
    box_a5 = util.splitBoxes(ans5_thresh, 4, 4)




    ANSWER = []
    arr_1t9 = util.getArray(9, 4, box_a1)
    arr_20t28 = util.getArray(9, 4, box_a3)
    for i in range(9):
        if (np.max(arr_1t9[i]) != 0):
            ANSWER.append(options[np.argmax(arr_1t9[i])])
        else:
            ANSWER.append(" ")
    for i in range(9):
        if (np.max(arr_20t28[i]) != 0):
            ANSWER.append(options[np.argmax(arr_20t28[i])])
        else:
            ANSWER.append(" ")

    arr_10t19 = util.getArray(10, 4, box_a2)
    arr_29t36=util.getArray(8,4,box_a4)
    arr_37t40=util.getArray(4,4,box_a5)
    for i in range(10):
        if (np.max(arr_10t19[i]) != 0):
            ANSWER.append(options[np.argmax(arr_10t19[i])])
        else:
            ANSWER.append(" ")


    for i in range(8):
        if (np.max(arr_29t36[i]) != 0):
            ANSWER.append(options[np.argmax(arr_29t36[i])])
        else:
            ANSWER.append(" ")
    for i in range(4):
        if (np.max(arr_37t40[i]) != 0):
            ANSWER.append(options[np.argmax(arr_37t40[i])])
        else:
            ANSWER.append(" ")

    return ANSWER
