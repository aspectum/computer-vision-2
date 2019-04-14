import cv2
import numpy as np
import glob
import math
import req3

class janelaClass:
    def __init__(self, imagem, windowname, intrinsics, tvec, rvec):
        self.imagem = imagem
        self.windowname = windowname
        self.pontosx = [-1, -1]
        self.pontosy = [-1, -1]
        self.intrinsics = intrinsics
        self.tvec = tvec
        self.rvec = rvec

# pontosx = [-1,-1]
# pontosy = [-1,-1]

def realWordPoints(janela):
    camPts0 = [janela.pontosx[0], janela.pontosy[0], 1]
    camPts1 = [janela.pontosx[1], janela.pontosy[1], 1]

    inv_intr = np.linalg.inv(janela.intrinsics)
    mCamPts0 = np.dot(inv_intr, camPts0)
    mCamPts1 = np.dot(inv_intr, camPts1)

    rotMtx, jacob = cv2.Rodrigues(janela.rvec)

    # print(janela.rvec.shape)
    # print(janela.tvec.shape)
    # print(rotMtx.shape)
    # print(janela.tvec)
    # print(rotMtx)



    w2cMtx = np.concatenate([rotMtx, janela.tvec], 1)
    inv_w2cMtx = np.linalg.pinv(w2cMtx)

    wPts0 = np.dot(inv_w2cMtx, mCamPts0)
    wPts1 = np.dot(inv_w2cMtx, mCamPts1)

    wPts0 = wPts0 / wPts0[3]
    wPts1 = wPts1 / wPts1[3]

    dist = np.linalg.norm(wPts1 - wPts0)

    print(janela.windowname, "- Distancia: ", dist)




def clickEvent(event, x, y, flags, janela):
    if event == cv2.EVENT_LBUTTONDOWN:
        janela.pontosx[1] = janela.pontosx[0]
        janela.pontosx[0] = x
        janela.pontosy[1] = janela.pontosy[0]
        janela.pontosy[0] = y
        if janela.pontosx[1]!=-1:
            realWordPoints(janela)
            imagem2 = janela.imagem.copy()
            cv2.line(imagem2,(janela.pontosx[0],janela.pontosy[0]),(janela.pontosx[1],janela.pontosy[1]),(0,0,255),4)
            cv2.imshow(janela.windowname,imagem2)
            janela.pontosx = [-1,-1]
            janela.pontosy = [-1,-1]	

def main():
    intrinsics_file = cv2.FileStorage('intrinsics.xml', flags = 0)
    distortion_file = cv2.FileStorage('distortion.xml', flags = 0)

    intrinsics_matrix = intrinsics_file.getNode('intrinsics').mat()
    distortion_matrix = distortion_file.getNode('distortion').mat()

    intrinsics_file.release()
    distortion_file.release()


    image_name = 'test/IMG_20190414_142402.jpg'

    frame_names, transl, rots = req3.calcExtrinsic(image_name)

    raw = cv2.imread(image_name)

    h,  w = raw.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(intrinsics_matrix, distortion_matrix, (w, h), 1, (w, h))

    undistorted = cv2.undistort(raw, intrinsics_matrix, distortion_matrix, None, newcameramtx)
    x,y,w,h = roi
    undistorted = undistorted[y:y+h, x:x+w]

    cv2.imshow('RAW',raw)
    janelaRAW = janelaClass(raw, 'RAW', intrinsics_matrix, transl[0], rots[0])
    cv2.setMouseCallback('RAW', clickEvent, janelaRAW)

    cv2.imshow('UNDISTORTED',undistorted)
    janelaUND = janelaClass(undistorted, 'UNDISTORTED', intrinsics_matrix, transl[0], rots[0])
    cv2.setMouseCallback('UNDISTORTED', clickEvent, janelaUND)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__  == "__main__":
    main()