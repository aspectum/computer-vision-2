import cv2
import numpy as np
import math

pontosx = [-1,-1]
pontosy = [-1,-1]

def clickEvent(event, x, y, flags, param):
	global pontosx,pontosy
	if event == cv2.EVENT_LBUTTONDOWN:
		pontosx[1] = pontosx[0]
		pontosx[0] = x
		pontosy[1] = pontosy[0]
		pontosy[0] = y
		print ('Ponto 1: X = ',pontosy[1] ,'Y = ', pontosx[1])
		print ('Ponto 2: X = ',pontosy[0] ,'Y = ', pontosx[0])
		distEucl = math.sqrt((pontosx[0]-pontosx[1])**2 + (pontosy[0]-pontosy[1])**2)
		print (distEucl)
		taxax = (pontosx[1] - pontosx[0])/1000
		taxay = (pontosy[1] - pontosy[0])/1000
		imagem2 = imagem.copy()
		if pontosx[1] != -1:
			for i in range(1000):
				imagem2[int(pontosy[1]-i*taxay),int(pontosx[1]-i*taxax),2] = 0
				imagem2[int(pontosy[1]-i*taxay),int(pontosx[1]-i*taxax),1] = 255
				imagem2[int(pontosy[1]-i*taxay),int(pontosx[1]-i*taxax),0] = 0
			cv2.imshow('Imagem',imagem2)		


imagem = cv2.imread('../data/imagem.jpg')
imagem2 = imagem.copy()
cv2.imshow('Imagem',imagem2)
cv2.setMouseCallback('Imagem', clickEvent)
cv2.waitKey(0)
cv2.destroyAllWindows()

input()
