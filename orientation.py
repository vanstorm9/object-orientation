import cv2
from numpy import *
from pylab import *


path = 'images/pca.jpg'
img = cv2.imread(path)
imgray = cv2.imread(path,0)

# Contour detection
#ret,thresh = cv2.threshold(imgray,127,255,0)

#imgray = cv2.GaussianBlur(imgray, (5, 5), 200)
imgray = cv2.medianBlur(imgray, 11)

#imgray = cv2.medianBlur(imgray,5)
#imgray = cv2.Canny(imgray,10,500)
thresh = cv2.Canny(imgray,75,200)

__ , contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
cnts = sorted(contours, key = cv2.contourArea, reverse = True)

test = img.copy()
cv2.drawContours(test, cnts, -1,(0,255,0),2)
cv2.imshow('contours', test)
cv2.waitKey(0)
