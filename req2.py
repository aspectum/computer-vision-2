import cv2

windowName = 'Janela'
board_h = 6
board_w = 8
board_sz = (board_w, board_h)
n_boards = 5
board_total = board_w * board_h

def main():
    cap = cv2.VideoCapture(0)
    if (cap.isOpened()== False):  
        print("Error opening video file") 
    cv2.namedWindow(windowName)
    
    successes = 0

    # while successes < n_boards:
    #     ret, frame = cap.read()
    #     patternWasFound, corners = cv2.findChessboardCorners(frame, board_sz)

    #     frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     # find cornerSubPix??

    #     frame_display = cv2.drawChessboardCorners(frame, board_sz, corners, patternWasFound)


    while cap.isOpened():
        ret, frame = cap.read()
        patternWasFound, corners = cv2.findChessboardCorners(frame, board_sz)

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # find cornerSubPix??

        frame_display = cv2.drawChessboardCorners(frame, board_sz, corners, patternWasFound)

        cv2.imshow(windowName, frame_display)

        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
    
    cv2.destroyAllWindows()


if __name__  == "__main__":
    main()