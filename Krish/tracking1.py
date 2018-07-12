import numpy as np
import cv2

#barcodedet begins
# import the necessary packages
from pyzbar import pyzbar

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

# setup initial location of window
(c,r,w,h) = qr(frame)  # simply hardcoded the values
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # Draw it on image
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame,[pts],True, 255,2)
        cv2.imshow('img2',img2)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg",img2)

    else:
        break

cv2.destroyAllWindows()
cap.release()
