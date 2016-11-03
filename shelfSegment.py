import cv2
from imgops import imutils
import CVAlgo


def showImage(img):
	cv2.imshow('Showing', img)
	cv2.waitKey(0)


z = 'am'
#path = 'images/pic in bins/23.jpg'
path = 'images/pic/shelf.jpg'
#path = 'images/pic/shelf2.jpg'


img = cv2.imread(path)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = imutils.resize(img, height = 600)
imgray = imutils.resize(img, height = 600)

final = img.copy()

thresh, imgray = CVAlgo.shelfFiltering(img, imgray, z)

#showImage(imgray)


__ , contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


# Iterate through all contours
#test = CVAlgo.cnt_gui(final, contours)

#cv2.imwrite('1.jpg', final)

cv2.imshow('thresh', thresh)
cv2.imshow('contours', final)
cv2.waitKey(0)
