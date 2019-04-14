import cv2
import numpy as np
import glob
import math

# # Checks if a matrix is a valid rotation matrix.
# def isRotationMatrix(R) :
#     Rt = np.transpose(R)
#     shouldBeIdentity = np.dot(Rt, R)
#     I = np.identity(3, dtype = R.dtype)
#     n = np.linalg.norm(I - shouldBeIdentity)
#     return n < 1e-6
 
 
# # Calculates rotation matrix to euler angles
# # The result is the same as MATLAB except the order
# # of the euler angles ( x and z are swapped ).
# def rotationMatrixToEulerAngles(R) :
 
#     assert(isRotationMatrix(R))
     
#     sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
     
#     singular = sy < 1e-6
 
#     if  not singular :
#         x = math.atan2(R[2,1] , R[2,2])
#         y = math.atan2(-R[2,0], sy)
#         z = math.atan2(R[1,0], R[0,0])
#     else :
#         x = math.atan2(-R[1,2], R[1,1])
#         y = math.atan2(-R[2,0], sy)
#         z = 0
 
#     return np.array([x, y, z])

def calcExtrinsic(target):
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
    objp = 2.789 * objp     #--> Nesse código parece fazer diferença o tamanho do quadrado. 2.8cm seria o lado do quadrado

    # Carrega os parâmetros gerados pelo requisito 2
    intrinsics_file = cv2.FileStorage('intrinsics.xml', flags = 0)
    distortion_file = cv2.FileStorage('distortion.xml', flags = 0)

    intrinsics_matrix = intrinsics_file.getNode('intrinsics').mat()
    distortion_matrix = distortion_file.getNode('distortion').mat()

    intrinsics_file.release()
    distortion_file.release()

    images = glob.glob(target) # Carrega as imagens (1 a 30cm, 2 a 60cm e 3 a 90cm)
    rots = []
    transl = []
    count=0
    frame_names = []
    for fname in images:
        frame_names.append(fname)
        count+=1
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

    # angs = []
    # for i in range(count):
    #     dst, jacob = cv2.Rodrigues(rots[i])
    #     ang = rotationMatrixToEulerAngles(dst)
    #     angs.append(ang)


    print("Distances from camera to pattern:")
    for i in range(len(frame_names)):
        print(frame_names[i],": ",transl[i][2],", ",rots[i][2],sep="")

    cv2.destroyAllWindows()

if __name__  == "__main__":
    main()
