import cv2
import numpy as np
import glob

def main():
    windowName = 'Janela'
    board_h = 6
    board_w = 8
    board_sz = (board_w, board_h)
    board_total = board_w * board_h

    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)      # "Coordenadas do mundo real" do tabuleiro de xadrez
    objp = 2.789 * objp     #--> Colocar o lado do quadrado parece não influenciar nada o resultado.

    image_points = []
    object_points = []

    successes = 0
    frame_names = []
    images = glob.glob('calib/*.jpg')

    for fname in images:
        frame_names.append(fname)
        frame = cv2.imread(fname)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        patternWasFound, corners = cv2.findChessboardCorners(frame, board_sz)
        
        if patternWasFound:         # Se achou o tabuleiro
            frame_display = cv2.drawChessboardCorners(frame, board_sz, corners, patternWasFound)

            if len(corners) == board_total:     # Se achou todos os pontos na imagem
                image_points.append(corners)    # Coordenadas no espaço da imagem
                object_points.append(objp)      # Coordenadas no mundo real (sempre o mesmo (?))
                successes += 1
            else: 
                print("Este frame nao achou o padrao corretamente:",fname)
        else:
            print("Este frame nao achou o padrao:",fname)
            frame_display = frame.copy()

        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
        cv2.imshow(windowName, frame)

    # Função que faz a calibração
    retVal, intrinsics_matrix, distortion_matrix, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, frame.shape[::-1], None, None)

    # Salva os .xml com os parâmetros do requisito 2
    intrinsics_file = cv2.FileStorage('intrinsics.xml', flags = 1)
    distortion_file = cv2.FileStorage('distortion.xml', flags = 1)
    intrinsics_file.write(name = 'intrinsics', val = intrinsics_matrix)
    distortion_file.write(name = 'distortion', val = distortion_matrix)
    intrinsics_file.release()
    distortion_file.release()

    cv2.destroyAllWindows()

    print("Distances from camera to pattern:")
    for i in range(successes):
        print(frame_names[i],": ",tvecs[i][2][0],", ",rvecs[i][2][0],sep="")

if __name__  == "__main__":
    main()