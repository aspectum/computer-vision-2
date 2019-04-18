import cv2
import numpy as np
import math

# Definido uma classe para poder passar vários
# parâmetros para a função de callback e retornar
# valores
class janela:
    def __init__(self, imagem, windowname):
        self.imagem = imagem
        self.windowname = windowname
        self.pontosx = [-1, -1]     # Coordenadas x dos pontos
        self.pontosy = [-1, -1]     # Coordenadas y dos pontos


# Função de callback do mouse
def clickEvent(event, x, y, flags, janela):
    if event == cv2.EVENT_LBUTTONDOWN:
        janela.pontosx[1] = janela.pontosx[0]
        janela.pontosx[0] = x
        janela.pontosy[1] = janela.pontosy[0]
        janela.pontosy[0] = y

        if janela.pontosx[1]!=-1:   # Segundo clique
            distEucl = math.sqrt((janela.pontosx[0]-janela.pontosx[1])**2 + (janela.pontosy[0]-janela.pontosy[1])**2)
            print ("Pixel distance:",distEucl)
            img_display = janela.imagem.copy()
            cv2.line(img_display,(janela.pontosx[0],janela.pontosy[0]),(janela.pontosx[1],janela.pontosy[1]),(0,0,255),4)
            cv2.imshow(janela.windowname,img_display)
            janela.pontosx = [-1,-1]    # Resetando os valores
            janela.pontosy = [-1,-1]


def main():
    print("Clique em 2 pontos da imagem")
    imagem = cv2.imread('../data/test/c_30_01.jpg')
    cv2.imshow('Imagem',imagem)
    janela1 = janela(imagem, 'Imagem')
    cv2.setMouseCallback('Imagem', clickEvent, janela1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__  == "__main__":
    main()