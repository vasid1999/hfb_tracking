from pyzbar import pyzbar

#1->QRCODE
#2->barcode
#3->Color pattern


def track_method(image,param):
	if param=="QRCODE" or param=="BARCODE":
		return qr(image,param)

def qr(image,param): 
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
			if barcodeType==param and barcodeData=="iBot HFB Human To Be Followed":
				return barcode.rect	#return bounding box of QR code
	return 0	#not our barcode
