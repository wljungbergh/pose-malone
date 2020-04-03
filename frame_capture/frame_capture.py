import numpy as np
import cv2

class FrameCapturer:
    def __init__(self, fps = 5):
        # Initiation of fps and the capturer
        self.fps = fps
        self.capturer = cv2.VideoCapture(0)
        self.quit = False
    
    def __del__(self):
        self.capturer.release()

    
    def get_frame(self):
        ret, frame = self.capturer.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray


if __name__ == '__main__':
    fc = FrameCapturer()
    
    # Capture frame-by-frame
    gray = fc.get_frame()

    # Our operations on the frame come here
    

    # Display the resulting frame
    while True:
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    del(fc)
    cv2.destroyAllWindows()