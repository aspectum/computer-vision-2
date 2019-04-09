import cv2
import numpy as np

windowName = 'Janela'
undistortedName = 'desdestorcido'
board_h = 6
board_w = 8
board_sz = (board_w, board_h)
n_boards = 5
board_total = board_w * board_h
frame_step = 10

objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

image_points = []
object_points = []

def main():
    cap = cv2.VideoCapture(0)
    if (cap.isOpened()== False):  
        print("Error opening video file") 
    cv2.namedWindow(windowName)
    
    successes = 0
    frame_count = 0

    while successes < n_boards:
        ret, frame = cap.read()
        frame_count += 1
        if frame_count % frame_step == 0:
            patternWasFound, corners = cv2.findChessboardCorners(frame, board_sz)
            
            if patternWasFound:
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # find cornerSubPix??

                frame_display = cv2.drawChessboardCorners(frame, board_sz, corners, patternWasFound)

                if len(corners) == board_total:
                    image_points.append(corners)
                    object_points.append(objp)
                    successes += 1
            else:
                frame_display = frame.copy()
        else:
            frame_display = frame.copy()
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
        cv2.imshow(windowName, frame)
    retVal, instrinsic_matrix, distortion_matrix, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, frame.shape[:-1], None, None)

    print(instrinsic_matrix)
    print('-----------')
    print(distortion_matrix)

    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(instrinsic_matrix, distortion_matrix, (board_w, board_h), 1, (board_w, board_h))
    mapx, mapy = cv2.initUndistortRectifyMap(instrinsic_matrix, distortion_matrix, None, new_camera_matrix, (board_w, board_h), 5)

    cv2.namedWindow(undistortedName)
    

    while cap.isOpened():
        ret, frame = cap.read()
        # dispFrame = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        dispFrame = cv2.undistort(frame, instrinsic_matrix, distortion_matrix, None, new_camera_matrix)

        #x,y,w,h = roi
        #dispFrame = dispFrame[y:y+h, x:x+w]

        cv2.imshow(undistortedName, dispFrame)

        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
    
    cv2.destroyAllWindows()


if __name__  == "__main__":
    main()