import cv2
import numpy as np
frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)

myColors=[[8,73,83,8,255,255],#red
         [70,88,105,70,255,255],#green
         [15,125,0,15,255,255], #orange
         [34,129,60,34,255,255], #yellow
         [106,119,0,106,255,255]]#blue

myColorValues=[[0,0,255],[0,153,0],[0,128,255],[0,255,255],[204,102,0]]
myPoints=[]

def findColors(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newpoints=[]
    for color in myColors:
        lower =  np.array(color[0:3])
        upper =  np.array(color[3:6])
        mask  = cv2.inRange(imgHSV, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgresult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count+=1
    return newpoints
        #cv2.imshow(str(color[0]),mask)
def getContours(img):
    contours,heirarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area= cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgresult,cnt,-1,(255,0,0),3)
            peri=cv2.arcLength(cnt, True)
            approx=cv2.approxPolyDP(cnt, 0.02*peri, True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y
def drawOnCanvas(myPoints,myColors):
    for point in myPoints:
        cv2.circle(imgresult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)


while True:
    success, img = cap.read()
    imgresult=img.copy()
    newPoints=findColors(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("result", imgresult)
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break
