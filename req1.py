import cv2
import numpy as np
import math

class janela:
    def __init__(self, imagem, windowname):
        self.imagem = imagem
        self.windowname = windowname
        self.pontosx = [-1, -1]
        self.pontosy = [-1, -1]

def clickEvent(event, x, y, flags, janela):
    if event == cv2.EVENT_LBUTTONDOWN:
        janela.pontosx[1] = janela.pontosx[0]
        janela.pontosx[0] = x
        janela.pontosy[1] = janela.pontosy[0]
        janela.pontosy[0] = y

        if janela.pontosx[1]!=-1:
            distEucl = math.sqrt((janela.pontosx[0]-janela.pontosx[1])**2 + (janela.pontosy[0]-janela.pontosy[1])**2)
            print ("Pixel distance:",distEucl)
            imagem2 = janela.imagem.copy()
            cv2.line(imagem2,(janela.pontosx[0],janela.pontosy[0]),(janela.pontosx[1],janela.pontosy[1]),(0,0,255),4)
            cv2.imshow(janela.windowname,imagem2)
            janela.pontosx = [-1,-1]
            janela.pontosy = [-1,-1]		

def main():
    print("Clique em 2 pontos da imagem")
    imagem = cv2.imread('test/c_30_01.jpg')
    cv2.imshow('Imagem',imagem)
    janela1 = janela(imagem, 'Imagem')
    cv2.setMouseCallback('Imagem', clickEvent, janela1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__  == "__main__":
    main()