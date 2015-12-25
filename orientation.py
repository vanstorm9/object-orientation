import cv2
from numpy import *
from pylab import *
from imgops import imutils
import math

def invert_img(img):
    img = (255-img)
    return img

def histogram_equalization(img):
    hist,bins = np.histogram(img.flatten(),256,[0,256])
 
    cdf = hist.cumsum()     
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')
    img2 = cdf[img]

    return img2

def histogram_backprojection(img):

    img_height = img.shape[0]
    img_width = img.shape[1]

    img_demi = img[0:3*(img_height/5) , 0:(img_width)]
    #img_demi = img[0:img_height , 0:5*(img_width/7)]

    hsv = cv2.cvtColor(img_demi,cv2.COLOR_BGR2HSV)
    hsvt = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    # calculating object histogram
    roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, img_height, 0, img_width] )
     
    # normalize histogram and apply backprojection
    cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
    dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,img_height,0,img_width],1)
     
    # Now convolute with circular disc
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    cv2.filter2D(dst,-1,disc,dst)
     
    # threshold and binary AND
    ret,thresh = cv2.threshold(dst,50,255,0)

    return thresh

def morph_trans(img):
    # Implementing morphological erosion & dilation
    kernel = np.ones((9,9),np.uint8)  # (6,6) to get more contours (9,9) to reduce noise
    img = cv2.erode(img, kernel, iterations = 3) # Shrink to remove noise
    img = cv2.dilate(img, kernel, iterations=8)  # Grow to combine stray blobs

    return img

def canny(imgray):
    imgray = cv2.GaussianBlur(imgray, (11,11), 200)
    canny_low = 0
    canny_high = 100

    thresh = cv2.Canny(imgray,canny_low,canny_high)
    return thresh

def cnt_gui(img, contours):
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)

    for i in range(0,len(cnts)):
        sel_cnts = sorted(contours, key = cv2.contourArea, reverse = True)[i]

        area = cv2.contourArea(sel_cnts)

        if area < 1000:
            continue
        
        # get orientation angle and center coord
        center, axis,angle = cv2.fitEllipse(sel_cnts)
        
        hyp = 100  # length of the orientation line

        # Find out coordinates of 2nd point if given length of line and center coord 
        linex = int(center[0]) + int(math.sin(math.radians(angle))*hyp)
        liney = int(center[1]) - int(math.cos(math.radians(angle))*hyp)

        # Draw orienation
        cv2.line(img, (int(center[0]),int(center[1])), (linex, liney), (0,0,255),5)             
        cv2.circle(img, (int(center[0]), int(center[1])), 10, (255,0,0), -1)

    return img

def filtering(img, imgray):
    if z == 'am':
        thresh= invert_img(histogram_backprojection(img))
        thresh = morph_trans(thresh)

    elif z == 'pr':
        
        
        imgray = cv2.medianBlur(imgray, 11)
        thresh = cv2.Canny(imgray,75,200)
    else:
        print 'error in filtering function'
        quit()

    return thresh, imgray


z = 'am'
#z = 'pr'

#path = 'images/pca.jpg'
#path = 'images/shapes.png'
#path = 'images/page.jpg'
#path = 'images/ellipse.png'
#path = 'images/obj_1.jpg'
path = 'images/pic in bins/23.jpg'
#path = 'images/pic in bins/16.jpg'


img = cv2.imread(path)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = imutils.resize(img, height = 600)
imgray = imutils.resize(img, height = 600)

final = img.copy()

thresh, imgray = filtering(img, imgray)


__ , contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Iterate through all contours
test = cnt_gui(final, contours)


cv2.imshow('thresh', thresh)
cv2.imshow('contours', final)
cv2.waitKey(0)
