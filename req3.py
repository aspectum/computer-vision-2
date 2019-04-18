import cv2
import numpy as np
import glob
import math

# Faz o procedimento como função para poder
# importar no req4.py
def calcExtrinsic(target, flagShow):
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
    objp = 2.789 * objp

    # Carrega os parâmetros gerados pelo requisito 2
    intrinsics_file = cv2.FileStorage('intrinsics.xml', flags = 0)
    distortion_file = cv2.FileStorage('distortion.xml', flags = 0)

    intrinsics_matrix = intrinsics_file.getNode('intrinsics').mat()
    distortion_matrix = distortion_file.getNode('distortion').mat()

    intrinsics_file.release()
    distortion_file.release()

    images = sorted(glob.glob(target))  # Importante ordenar por causa da sequência das imagens
    rots = []
    transl = []
    frame_names = []
    for fname in images:
        frame_names.append(fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (8,6),None)

        if ret == True and flagShow == True:
            img = cv2.drawChessboardCorners(gray, (8,6), corners,ret)
            cv2.imshow('img',img)
            cv2.waitKey(100)

        # Calcula os extrínsecos a partir dos intrínsecos e
        # dos pontos do padrão de calibração da imagem atual
        retval, rvec, tvec = cv2.solvePnP(objp, corners, intrinsics_matrix, distortion_matrix)

        rots.append(rvec)       # Guarda os extrínsecos de cada imagem
        transl.append(tvec)

    cv2.destroyAllWindows()

    return frame_names, transl, rots


def main():

    print("Iniciando a calibracao dos extrinsecos")
    frame_names, transl, rots = calcExtrinsic('calib/n_*.jpg', True)

    print("Extrinsecos obtidos. Distancias medidas:")

    dists = np.squeeze(transl)[:,2]
    print("Para 38 cm:")
    print("Media: ", np.mean(dists[0:10]))
    print("Desvio: ", np.std(dists[0:10]))
    print('')
    print("Para 68 cm:")
    print("Media: ", np.mean(dists[10:20]))
    print("Desvio: ", np.std(dists[10:20]))
    print('')
    print("Para 98 cm:")
    print("Media: ", np.mean(dists[20:30]))
    print("Desvio: ", np.std(dists[20:30]))

    cv2.destroyAllWindows()


if __name__  == "__main__":
    main()
