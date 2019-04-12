import cv2
import numpy as np
import glob

windowName = 'Janela'
undistortedName = 'desdestorcido'
board_h = 6
board_w = 8
board_sz = (board_w, board_h)
n_boards = 40
board_total = board_w * board_h
frame_step = 40

objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
# objp = 2.8 * objp     #--> Nesse código parece fazer diferença o tamanho do quadrado. 2.8cm seria o lado do quadrado

image_points = []
object_points = []

def main():
    # Carrega os parâmetros gerados pelo requisito 2
    intrinsics_file = cv2.FileStorage('intrinsics.xml', flags = 0)
    distortion_file = cv2.FileStorage('distortion.xml', flags = 0)

    intrinsics_matrix = intrinsics_file.getNode('intrinsics').mat()
    distortion_matrix = distortion_file.getNode('distortion').mat()

    intrinsics_file.release()
    distortion_file.release()
    
    images = glob.glob('data/*.jpg') # Carrega as imagens (1 a 30cm, 2 a 60cm e 3 a 90cm)
    rots = []
    transl = []
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (8,6),None)

        if ret == True:
            img = cv2.drawChessboardCorners(img, (8,6), corners,ret)
            cv2.imshow('img',img)
            cv2.waitKey(500)
        
        # Calcula os "extrínsecos"? Pelo que eu endendi os extrínsecos são a matriz de rotação (vetor rvec) e o vetor de translação (tvec)
        # que levam do espaço do mundo para o espaço da câmera. Então o tvec deveria fornecer a distância entre a câmera e o tabuleiro.
        # Não parece funcionar bem.
        retval, rvec, tvec = cv2.solvePnP(objp, corners, intrinsics_matrix, distortion_matrix)
        rots.append(rvec)
        transl.append(tvec)


    

    print(transl)
    print('---------------')
    print(rots)


    cv2.destroyAllWindows()


if __name__  == "__main__":
    main()