import cv2
from numpy import *
from pylab import *
from imgops import imutils
import math

path = 'images/pca.jpg'
#path = 'images/shapes.png'
#path = 'images/page.jpg'
#path = 'images/ellipse.png'

img = cv2.imread(path)
imgray = cv2.imread(path,0)

img = imutils.resize(img, height = 600)
imgray = imutils.resize(imgray, height = 600)

test = img.copy()

# Contour detection
#ret,thresh = cv2.threshold(imgray,127,255,0)

#imgray = cv2.GaussianBlur(imgray, (5, 5), 200)
imgray = cv2.medianBlur(imgray, 11)

#imgray = cv2.medianBlur(imgray,5)
#imgray = cv2.Canny(imgray,10,500)

canny_thresh_val = 75

thresh = cv2.Canny(imgray,canny_thresh_val,200)

__ , contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


cnts = sorted(contours, key = cv2.contourArea, reverse = True)
cv2.drawContours(test, cnts, -1,(0,255,0),2)

# Iterate through all contours
for i in range(0,len(cnts)-1):
    sel_cnts = sorted(contours, key = cv2.contourArea, reverse = True)[i]

    area = cv2.contourArea(sel_cnts)

    # To filter out cnts that are too small
    if area < 1000:
        continue


    # get orientation angle and center coord
    center, axis,angle = cv2.fitEllipse(sel_cnts)

    hyp = 100  # length of the orientation line

    # Find out coordinates of 2nd point if given length of line and center coord 
    linex = int(center[0]) + int(math.sin(math.radians(angle))*hyp)
    liney = int(center[1]) - int(math.cos(math.radians(angle))*hyp)

    # Draw orienation
    cv2.line(test, (int(center[0]),int(center[1])), (linex, liney), (0,0,255),5)             
    cv2.circle(test, (int(center[0]), int(center[1])), 10, (255,0,0), -1)


cv2.imshow('contours', test)
cv2.waitKey(0)
