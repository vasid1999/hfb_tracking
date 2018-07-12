import cv2 
import numpy as np

cap=cv2.VideoCapture(0)
fgbg=cv2.createBackgroundSubtractorMOG2()

while(1):
	ret,frame=cap.read()
	fgmask=fgbg.apply(frame)
	img2=cv2.bitwise_and(frame,frame,mask=fgmask)
	
	
	cv2.imshow('original',frame)
	cv2.imshow('fg',fgmask)
	cv2.imshow('final',img2)
	
	
	k=cv2.waitKey(30)& 0xFF
	if k==27:
	  break
	  
cap.release()
cv2.destroyAllWindows()
	  
