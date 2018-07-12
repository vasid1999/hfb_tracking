import cv2
import numpy as np
from pykalman import KalmanFilter
import math
from pyzbar import pyzbar

def center(points):
    x = (points[0][0] + points[1][0] + points[2][0] + points[3][0]) / 4.0
    y = (points[0][1] + points[1][1] + points[2][1] + points[3][1]) / 4.0
    return np.array([np.float32(x), np.float32(y)], np.float32)
def qr(image): 
	# find the barcodes in the image and decode each of the barcodes
	barcodes = pyzbar.decode(image)
	
	if len(barcodes)==0:	#no barcode detected
		return 0
	else:
		# loop over the detected barcodes
		for barcode in barcodes:
		 
			# the barcode data is a bytes object so if we want to draw it on
			# our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")	#INTERNET?!	Nope; the information is encoded in the QR code itself
			barcodeType = barcode.type
			if barcodeType=="QRCODE" and barcodeData=="iBot HFB Human To Be Followed":
				return barcode.rect	#return bounding box of QR code
	return 0	#not our barcode
#barcodedet ends
cap = cv2.VideoCapture(0)
ret,frame = cap.read()

while qr(frame)==0:
	ret,frame = cap.read()

print("1")	
(c,r,w,h) = qr(frame)  # simply hardcoded the values
track_window = (c,r,w,h)	
# define display window name
# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0,1],mask,[180,256],[0,180,0,256])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

windowName = "Kalman Object Tracking" # window name
windowName2 = "Hue histogram back projection" # window name
windowNameSelection = "initial selected region"
            

kalman = cv2.KalmanFilter(4,2)
kalman.measurementMatrix = np.array([[1,0,0,0],
                                     [0,1,0,0]],np.float32)  

kalman.transitionMatrix = np.array([[1,0,1,0],
                                    [0,1,0,1],
                                    [0,0,1,0],
                                    [0,0,0,1]],np.float32) 

kalman.processNoiseCov = np.array([[1,0,0,0],
                                   [0,1,0,0],
                                   [0,0,1,0],
                                   [0,0,0,1]],np.float32) * 0.03

measurement = np.array((2,1), np.float32)
prediction = np.zeros((2,1), np.float32)
while True :
    ret,frame = cap.read()
    		

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # back projection of histogram based on Hue and Saturation only
    img_bproject = cv2.calcBackProject([img_hsv],[0,1],roi_hist,[0,180,0,255],1)
    cv2.imshow(windowName2,img_bproject)

            # apply camshift to predict new location (observation)
            # basic HSV histogram comparision with adaptive window size
            # see : http://docs.opencv.org/3.1.0/db/df8/tutorial_py_meanshift.html
    ret, track_window = cv2.CamShift(img_bproject, track_window, term_crit)

            # draw observation on image
    x,y,w,h = track_window
    frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),2)
            # The main observation is of blur colour.
            
            # extract centre of this observation as points
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)
            # (cx, cy), radius = cv2.minEnclosingCircle(pts)

            # use to correct kalman filter

    kalman.correct(center(pts))

            # get new kalman filter prediction
    prediction = kalman.predict()
    res = cv2.rectangle(frame, (prediction[0]-(0.5*w),prediction[1]-(0.5*h)), (prediction[0]+(0.5*w),prediction[1]+(0.5*h)), (0,255,0),2)
    cv2.imshow("frame",res)
    if cv2.waitKey(1)== 27:
    	break
            # draw predicton on image

		
cap.release()
cv2.destroyAllWindows()
