from imutils.perspective import four_point_transform
from imutils import contours
from skimage import io
import Ans
import numpy as np
#import argparse
import imutils
import cv2
def grade(image):


    # create global variable to store the path of input image
    # if __name__ == "__main__":
    #	img_path = './images/test_01.png'

    # có thể truyền đường dẫn của ảnh vào trong lúc thực thi chương trình theo thư viện argparse của Python như sau:

    # construct the argument parse and parse the arguments
    # construct the argument parse and parse the arguments


    # {0: 1, 1: 3, 2: 0, 3: 3}
    #numofques = int(input("Input the number of questions:"))
    ANSWER_KEY =Ans.ANSWER_KEY2
    #= {}
    #for i in range(0, numofques):
        #t = i + 1
        #print("Input the index of correct answer of question", t, ":")
        #answer = int(input())
        #ANSWER_KEY[i] = answer
    print(ANSWER_KEY)
    ques = len(ANSWER_KEY)
    # load the image, convert it to grayscale, blur it
    # slightly, then find edges


    edged = cv2.Canny(image, 75, 200)

    #
    thresh = cv2.threshold(edged, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # find contours in the thresholded image, then initialize
    # the list of contours that correspond to questions
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []
    # loop over the contours
    print("len of Cnts", len(cnts))
    for c in cnts:
        # compute the bounding box of the contour, then use the
        # bounding box to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        # in order to label the contour as a question, region
        # should be sufficiently wide, sufficiently tall, and
        # have an aspect ratio approximately equal to 1
        if w >= 37.5 and h >= 22 and ar >= 1.65 and ar <= 1.75:
            questionCnts.append(c)
    # sort the question contours top-to-bottom, then initialize
    # the total number of correct answers

    questionCnts = contours.sort_contours(questionCnts,
                                          method="top-to-bottom")[0]
    correct = 0
    ans = 4
    print("ans and ques:", ans, ques)
    a = []
    for i in range(0, ques):
        a.append([])
        for j in range(0, ans):
            a[i].append(0)
    print(a)
    # each question has "ans" possible answers, to loop over the
    # question in batches of ans
    print("len of questionCnts", len(questionCnts))

    for (q, i) in enumerate(np.arange(0, len(questionCnts), ans)):
        # sort the contours for the current question from
        # left to right, then initialize the index of the
        # bubbled answer
        cnts = contours.sort_contours(questionCnts[i:i + ans])[0]
        bubbled = None

        print("len of cnts after contours", len(cnts))
        # loop over the sorted contours
        for (j, c) in enumerate(cnts):
            # construct a mask that reveals only the current
            # "bubble" for the question
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            # apply the mask to the thresholded image, then
            # count the number of non-zero pixels in the
            # bubble area
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)

            a[q][j] = total
            a[q].sort()

            # if the current total has a larger number of total
            # non-zero pixels, then we are examining the currently
            # bubbled-in answer
            print("Count non-zero pixel", total)
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)
        # initialize the contour color and the index of the
        # *correct* answer
        color = (0, 0, 255)
        k = ANSWER_KEY[q]
        # check to see if the bubbled answer is correct
        if k == bubbled[1] and a[q][ans - 2] != 1:
            color = (0, 255, 0)
            correct += 1
        # draw the outline of the correct answer on the test
        cv2.drawContours(image, [cnts[k]], -1, color, 3)
    # grab the test taker
    score = correct
    return score