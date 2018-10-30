from time import sleep
from homo1_ipw_2 import calcarea
import socket

client_ip='192.168.43.11'
client_port=3000
ipsocket=socket.socket()
ipsocket.connect((client_ip,client_port))
chp=''
af=15000
ab=20000
f1=0.2
f2=0.8

while True:
	area,w,cx=calcarea()
	
	if area==-1:
		if not(chp=='s'):
			print('no qr')
			chp='s'
			ipsocket.send(b's')
	elif cx<f1*w:
		if not(chp=='a'):
			print('left')
			chp='a'
			ipsocket.send(b'a')
	elif cx>f2*w:
		if not(chp=='d'):
			print('right')
			chp='d'
			ipsocket.send(b'd')
	else:
		if area <= af:
			if not(chp=='w'):
				print('front')
				chp='w'
				ipsocket.send(b'w')

		elif af<area<ab:
			if not(chp=='s'):
				print('stay')
				chp='s'
				ipsocket.send(b's')

		elif area>=ab:
			if not(chp=='z'):
				print('back')
				chp='z'
				ipsocket.send(b'z')
