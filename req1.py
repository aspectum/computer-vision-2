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
		# print ('Point 1: X = ',pontosy[1] ,'Y = ', pontosx[1])
		# print ('Point 2: X = ',pontosy[0] ,'Y = ', pontosx[0])
		if pontosx[1]!=-1:
			distEucl = math.sqrt((pontosx[0]-pontosx[1])**2 + (pontosy[0]-pontosy[1])**2)
			print ("Pixel distance:",distEucl)
			imagem2 = imagem.copy()
			cv2.line(imagem2,(pontosx[0],pontosy[0]),(pontosx[1],pontosy[1]),(0,0,255),4)
			cv2.imshow('Imagem',imagem2)		

def main():
	global imagem, imagem2
	imagem = cv2.imread('data/a.jpg')
	imagem2 = imagem.copy()
	cv2.imshow('Imagem',imagem2)
	cv2.setMouseCallback('Imagem', clickEvent)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__  == "__main__":
	main()