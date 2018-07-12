import numpy as np
import cv2

img = cv2.imread('india1.jpg',1)
im=cv2.pyrDown(img)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
binary=thresh
kernel = np.ones((9,9),np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

print(imgray.shape)
cols,rows=imgray.shape
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)



image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


cnt=contours[0]
M=cv2.moments(cnt)
#print (M)

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print (cx,cy)
center=(cx,cy)
im=cv2.circle(im,center,5,(0,0,255),-1)

area=cv2.contourArea(cnt)
perimeter=cv2.arcLength(cnt,True)
#print (area, perimeter)

x,y,w,h=cv2.boundingRect(cnt)
im=cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
print(w,h)


print('total no.of pixels=') 
print(cols*rows)
print(w*h)


rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
im = cv2.drawContours(im,[box],0,(0,0,255),2)
print(box)

(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
im = cv2.circle(im,center,radius,(0,255,0),2)



im = cv2.drawContours(im, contours, -1, (0,255,0), 3)
cv2.imshow('conts',im)

cv2.imshow('gray',imgray)
cv2.imshow('binary',binary)

cv2.imshow('contours',image)
cv2.waitKey(0)
cv2.destroyAllWindows()

