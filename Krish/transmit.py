from time import sleep 
import cv2
from homo1 import calcarea
import socket

client_ip='10.21.67.213'
client_port=3000
ipsocket=socket.socket()
ipsocket.connect((client_ip,client_port))

while True:
	area,_,_=calcarea()
	if area==-1:
		print('no qr')
		ipsocket.send(b's')

	elif area <= 6000:
		print('front')
		ipsocket.send(b'w')

	elif 6000<area<10000:
		print('stay')
		ipsocket.send(b's')

	elif area>=10000:
		print('back')
		ipsocket.send(b'z')
