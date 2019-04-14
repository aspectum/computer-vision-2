import cv2
import numpy as np
import glob
import math

def calcExtrinsic(target):
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

    images = glob.glob(target)
    rots = []
    transl = []
    frame_names = []
    for fname in images:
        frame_names.append(fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (8,6),None)

        if ret == True:
            img = cv2.drawChessboardCorners(img, (8,6), corners,ret)
            cv2.imshow('img',img)
            cv2.waitKey(100)
        
        retval, rvec, tvec = cv2.solvePnP(objp, corners, intrinsics_matrix, distortion_matrix)
        rots.append(rvec)
        transl.append(tvec)
    cv2.destroyAllWindows()
    return frame_names, transl, rots

def main():
    
    frame_names, transl, rots = calcExtrinsic('test/*.jpg')

    print("Distances from camera to pattern:")
    for i in range(len(frame_names)):
        print(frame_names[i],": ",transl[i][2],", ",rots[i][2],sep="")

    cv2.destroyAllWindows()

if __name__  == "__main__":
    main()
