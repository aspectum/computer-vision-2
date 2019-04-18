import cv2
import numpy as np
import glob
import math
import req3
from time import sleep

# Flag que continua mostrando a imagem até
# que seja feita a medição (2 cliques do usuário)
measured = 0

# Como no req1.py, ela possibilita a passagem
# de mais de um parâmetro e o armazenamento de
# um retorno. Essa tem alguns atributos a mais
class janelaClass:
    def __init__(self, imagem, windowname, intrinsics, tvec, rvec):
        self.imagem = imagem
        self.windowname = windowname
        self.pontosx = [-1, -1]
        self.pontosy = [-1, -1]
        self.intrinsics = intrinsics
        self.tvec = tvec
        self.rvec = rvec
        self.obj_len = 0


# A partir dos pontos na imagem e dos parâmetros
# intrínsecos e extrínsecos, faz as transformações,
# encontra as coordenadas do mundo real e calcula
# a distância euclidiana entre os pontos
def realWordPoints(janela):
    camPts0 = [janela.pontosx[0], janela.pontosy[0], 1]
    camPts1 = [janela.pontosx[1], janela.pontosy[1], 1]

    # Multiplicação pela inversa dos intrínsecos
    inv_intr = np.linalg.inv(janela.intrinsics)
    mCamPts0 = np.dot(inv_intr, camPts0)
    mCamPts1 = np.dot(inv_intr, camPts1)

    # Gera a matriz de rotação a partir do vetor de
    # rotação que o cv2.solvePnP() retorna
    rotMtx, jacob = cv2.Rodrigues(janela.rvec)

    # Gera a matriz dos extrínsecos concatenando a
    # matriz de rotação e o vetor de translação
    w2cMtx = np.concatenate([rotMtx, janela.tvec], 1)

    # Multiplicação pela pseudo-inversa dos extrínsecos
    inv_w2cMtx = np.linalg.pinv(w2cMtx)
    wPts0 = np.dot(inv_w2cMtx, mCamPts0)
    wPts1 = np.dot(inv_w2cMtx, mCamPts1)

    # Coloca em formato de Coordenadas Homogêneas
    wPts0 = wPts0 / wPts0[3]
    wPts1 = wPts1 / wPts1[3]

    # Calcula a distância euclidiana
    dist = np.linalg.norm(wPts1 - wPts0)
    janela.obj_len = dist

    # print(janela.windowname, "- Distancia: ", dist)

# Funcionamento análogo ao do req1.py
def clickEvent(event, x, y, flags, janela):
    global measured

    if event == cv2.EVENT_LBUTTONDOWN:
        janela.pontosx[1] = janela.pontosx[0]
        janela.pontosx[0] = x
        janela.pontosy[1] = janela.pontosy[0]
        janela.pontosy[0] = y

        if janela.pontosx[1]!=-1:
            realWordPoints(janela)
            img_display = janela.imagem.copy()
            cv2.line(img_display,(janela.pontosx[0],janela.pontosy[0]),(janela.pontosx[1],janela.pontosy[1]),(0,0,255),2)
            cv2.imshow(janela.windowname,img_display)
            janela.pontosx = [-1,-1]
            janela.pontosy = [-1,-1]
            measured = 1


def main():
    global measured

    print("Para cada imagem, selecione as extremidades da caneta")

    test_samples = ['test/c_30*.jpg', 'test/c_60*.jpg', 'test/c_90*.jpg', 'test/p_30*.jpg', 'test/p_60*.jpg', 'test/p_90*.jpg']
    lengths = np.zeros((2, 2, 3, 3)) # [raw/undist], [center/perif], [38/68/98], [3 samples]

    intrinsics_file = cv2.FileStorage('intrinsics.xml', flags = 0)
    distortion_file = cv2.FileStorage('distortion.xml', flags = 0)

    intrinsics_matrix = intrinsics_file.getNode('intrinsics').mat()
    distortion_matrix = distortion_file.getNode('distortion').mat()

    intrinsics_file.release()
    distortion_file.release()

    # Itera entre as categorias (distâncias e enquadramento do objeto diferentes)
    for i in range(len(test_samples)):
        images = sorted(glob.glob(test_samples[i]))

        # Decide os extrínsecos que vai usar
        if i % 3 == 0:
            image_extrinsic = 'calib/n_30*.jpg'
        elif i % 3 ==1:
            image_extrinsic = 'calib/n_60*.jpg'
        else:
            image_extrinsic = 'calib/n_90*.jpg'

        # Calcula os extrínsecos
        frame_names, transl, rots = req3.calcExtrinsic(image_extrinsic, False)
        dist = np.mean(transl, 0)
        rot = np.mean(rots, 0)

        j = 0
        # Itera entre as amostras
        for image_name in images:
            raw = cv2.imread(image_name)

            h,  w = raw.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(intrinsics_matrix, distortion_matrix, (w, h), 1, (w, h))

            # Gera a imagem sem distorção e faz o crop
            undistorted = cv2.undistort(raw, intrinsics_matrix, distortion_matrix, None, newcameramtx)
            x,y,w,h = roi
            undistorted = undistorted[y:y+h, x:x+w]

            cv2.namedWindow('RAW')
            cv2.imshow('RAW',raw)
            janelaRAW = janelaClass(raw, 'RAW', intrinsics_matrix, dist, rot)
            cv2.setMouseCallback('RAW', clickEvent, janelaRAW)

            # Espera o usuário selecionar os pontos
            while True:
                if measured:
                    sleep(0.5)  # Para não mudar de imagem instantaneamente
                    measured = 0
                    break
                if cv2.waitKey(50) & 0xFF == ord('q'):
                    return
            cv2.destroyAllWindows()

            cv2.namedWindow('UNDISTORTED')
            cv2.imshow('UNDISTORTED',undistorted)
            janelaUND = janelaClass(undistorted, 'UNDISTORTED', intrinsics_matrix, dist, rot)
            cv2.setMouseCallback('UNDISTORTED', clickEvent, janelaUND)

            while True:
                if measured:
                    sleep(0.5)
                    measured = 0
                    break
                if cv2.waitKey(50) & 0xFF == ord('q'):
                    return

            cv2.destroyAllWindows()

            # Armazena as medições
            lengths[0, i//3, i%3, j] = janelaRAW.obj_len
            lengths[1, i//3, i%3, j] = janelaUND.obj_len
            j += 1

    # Separa as medições
    l_raw_center_30 = lengths[0, 0, 0]
    l_raw_perif_30 = lengths[0, 1, 0]
    l_und_center_30 = lengths[1, 0, 0]
    l_und_perif_30 = lengths[1, 1, 0]
    l_raw_center_60 = lengths[0, 0, 1]
    l_raw_perif_60 = lengths[0, 1, 1]
    l_und_center_60 = lengths[1, 0, 1]
    l_und_perif_60 = lengths[1, 1, 1]
    l_raw_center_90 = lengths[0, 0, 2]
    l_raw_perif_90 = lengths[0, 1, 2]
    l_und_center_90 = lengths[1, 0, 2]
    l_und_perif_90 = lengths[1, 1, 2]

    # Calcula e exibe as médias e desvios padrões
    print("Medicoes")
    print("l_raw_center_30:")
    print("Media: ", np.mean(l_raw_center_30))
    print("Desvio: ", np.std(l_raw_center_30))
    print('')
    print("l_raw_center_60:")
    print("Media: ", np.mean(l_raw_center_60))
    print("Desvio: ", np.std(l_raw_center_60))
    print('')
    print("l_raw_center_90:")
    print("Media: ", np.mean(l_raw_center_90))
    print("Desvio: ", np.std(l_raw_center_90))
    print('')
    print("l_raw_perif_30:")
    print("Media: ", np.mean(l_raw_perif_30))
    print("Desvio: ", np.std(l_raw_perif_30))
    print('')
    print("l_raw_perif_60:")
    print("Media: ", np.mean(l_raw_perif_60))
    print("Desvio: ", np.std(l_raw_perif_60))
    print('')
    print("l_raw_perif_90:")
    print("Media: ", np.mean(l_raw_perif_90))
    print("Desvio: ", np.std(l_raw_perif_90))
    print('')
    print("l_und_center_30:")
    print("Media: ", np.mean(l_und_center_30))
    print("Desvio: ", np.std(l_und_center_30))
    print('')
    print("l_und_center_60:")
    print("Media: ", np.mean(l_und_center_60))
    print("Desvio: ", np.std(l_und_center_60))
    print('')
    print("l_und_center_90:")
    print("Media: ", np.mean(l_und_center_90))
    print("Desvio: ", np.std(l_und_center_90))
    print('')
    print("l_und_perif_30:")
    print("Media: ", np.mean(l_und_perif_30))
    print("Desvio: ", np.std(l_und_perif_30))
    print('')
    print("l_und_perif_60:")
    print("Media: ", np.mean(l_und_perif_60))
    print("Desvio: ", np.std(l_und_perif_60))
    print('')
    print("l_und_perif_90:")
    print("Media: ", np.mean(l_und_perif_90))
    print("Desvio: ", np.std(l_und_perif_90))
    print('')


if __name__  == "__main__":
    main()