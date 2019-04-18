import cv2
import numpy as np
import glob
import math
import req3
from time import sleep

measured = 0

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

def realWordPoints(janela):
    camPts0 = [janela.pontosx[0], janela.pontosy[0], 1]
    camPts1 = [janela.pontosx[1], janela.pontosy[1], 1]

    inv_intr = np.linalg.inv(janela.intrinsics)
    mCamPts0 = np.dot(inv_intr, camPts0)
    mCamPts1 = np.dot(inv_intr, camPts1)

    rotMtx, jacob = cv2.Rodrigues(janela.rvec)

    w2cMtx = np.concatenate([rotMtx, janela.tvec], 1)
    inv_w2cMtx = np.linalg.pinv(w2cMtx)

    wPts0 = np.dot(inv_w2cMtx, mCamPts0)
    wPts1 = np.dot(inv_w2cMtx, mCamPts1)

    wPts0 = wPts0 / wPts0[3]
    wPts1 = wPts1 / wPts1[3]

    dist = np.linalg.norm(wPts1 - wPts0)
    janela.obj_len = dist

    # print(janela.windowname, "- Distancia: ", dist)


def clickEvent(event, x, y, flags, janela):
    global measured

    if event == cv2.EVENT_LBUTTONDOWN:
        janela.pontosx[1] = janela.pontosx[0]
        janela.pontosx[0] = x
        janela.pontosy[1] = janela.pontosy[0]
        janela.pontosy[0] = y
        if janela.pontosx[1]!=-1:
            realWordPoints(janela)
            imagem2 = janela.imagem.copy()
            cv2.line(imagem2,(janela.pontosx[0],janela.pontosy[0]),(janela.pontosx[1],janela.pontosy[1]),(0,0,255),2)
            cv2.imshow(janela.windowname,imagem2)
            janela.pontosx = [-1,-1]
            janela.pontosy = [-1,-1]	
            measured = 1

def main():
    global measured

    print("Para cada imagem, selecione as extremidades da caneta")

    test_samples = ['test/c_30*.jpg', 'test/c_60*.jpg', 'test/c_90*.jpg', 'test/p_30*.jpg', 'test/p_60*.jpg', 'test/p_90*.jpg']
    lengths = np.zeros((2, 2, 3, 3)) # [raw/undist], [center/perif], [30/60/90], [3 samples]

    intrinsics_file = cv2.FileStorage('intrinsics.xml', flags = 0)
    distortion_file = cv2.FileStorage('distortion.xml', flags = 0)

    intrinsics_matrix = intrinsics_file.getNode('intrinsics').mat()
    distortion_matrix = distortion_file.getNode('distortion').mat()

    intrinsics_file.release()
    distortion_file.release()


    for i in range(len(test_samples)):
        images = sorted(glob.glob(test_samples[i]))

        if i % 3 == 0:
            image_extrinsic = 'calib/n_30*.jpg'
        elif i % 3 ==1:
            image_extrinsic = 'calib/n_60*.jpg'
        else:
            image_extrinsic = 'calib/n_90*.jpg'

        frame_names, transl, rots = req3.calcExtrinsic(image_extrinsic, False)
        dist = np.mean(transl, 0)
        rot = np.mean(rots, 0)

        j = 0
        for image_name in images:
            raw = cv2.imread(image_name)

            h,  w = raw.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(intrinsics_matrix, distortion_matrix, (w, h), 1, (w, h))

            undistorted = cv2.undistort(raw, intrinsics_matrix, distortion_matrix, None, newcameramtx)
            x,y,w,h = roi
            undistorted = undistorted[y:y+h, x:x+w]

            cv2.namedWindow('RAW')
            cv2.imshow('RAW',raw)
            janelaRAW = janelaClass(raw, 'RAW', intrinsics_matrix, dist, rot)
            cv2.setMouseCallback('RAW', clickEvent, janelaRAW)

            while True:
                if measured:
                    sleep(0.5)
                    measured = 0
                    break
                if cv2.waitKey(50) & 0xFF == ord('q'): 
                    (lengths)
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
                    print(lengths)
                    return
            cv2.destroyAllWindows()

            lengths[0, i//3, i%3, j] = janelaRAW.obj_len
            lengths[1, i//3, i%3, j] = janelaUND.obj_len
            j += 1
    
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