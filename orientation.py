import cv2
from imgops import imutils
import CVAlgo

z = 'am'
#z = 'pr'

#path = 'images/pca.jpg'
#path = 'images/shapes.png'
#path = 'images/page.jpg'
#path = 'images/ellipse.png'
#path = 'images/obj_1.jpg'


#path = 'images/pic in bins/23.jpg'
#path = 'duck.jpg'
#path = 'greenies.jpg'
path =  'cheezit.jpg'


#path = 'images/pic in bins/10.jpg'


ref_path = 'images/background/304.jpg'


img = cv2.imread(path)
ref_img = cv2.imread(ref_path)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = imutils.resize(img, height = 600)
imgray = imutils.resize(img, height = 600)

final = img.copy()

thresh, imgray = CVAlgo.filtering(img, imgray, ref_img, z)


__ , contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Iterate through all contours
test = CVAlgo.cnt_gui(final, contours)

#cv2.imwrite('1.jpg', final)

cv2.imshow('thresh', thresh)
cv2.imshow('contours', final)
cv2.waitKey(0)
