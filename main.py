import cv2

if __name__ == "__main__":
    # get video source (0: switch 2; 1: pc webcam)
    cap = cv2.VideoCapture(0)

    # set limits for capture of switch 2
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # display captured images
    while True:
        # capture frame
        success, frame = cap.read()

        if not success:
            print("video could not be read")
            cap.release()
            cv2.destroyAllWindows()
            break
        else:
            # display frame
            cv2.imshow("HDMI Video Capture", frame)
            cv2.waitKey(1)
