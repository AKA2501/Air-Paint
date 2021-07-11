import cv2
import numpy as np
frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,420)
cv2.createTrackbar("Hue Min",'HSV',0,180,empty)
cv2.createTrackbar("Sat Min",'HSV',0,255,empty)
cv2.createTrackbar("Val Min",'HSV',0,255,empty)
cv2.createTrackbar("Hue Max",'HSV',180,180,empty)
cv2.createTrackbar("Sat Max",'HSV',255,255,empty)
cv2.createTrackbar("Val Max",'HSV',255,255,empty)


while True:
    _,img=cap.read()
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min=cv2.getTrackbarPos("Hue Min","HSV")
    h_max=cv2.getTrackbarPos("Hue Min","HSV")
    s_min=cv2.getTrackbarPos("Sat Min","HSV")
    s_max=cv2.getTrackbarPos("Sat Max","HSV")
    v_min=cv2.getTrackbarPos("Val Min","HSV")
    v_max=cv2.getTrackbarPos("Val Max","HSV")
    print(h_min,h_max,s_min,s_max,v_min,v_max)

    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv2.inRange(imgHSV,lower,upper)

    result=cv2.bitwise_and(img,img,mask=mask)
    Stack=stackImages(0.7,[img,mask,result])

    mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    cv2.imshow("Horizontal Stacking", Stack)
    if cv2.waitKey(1) & 0xFF == ord ('q'):
            break
