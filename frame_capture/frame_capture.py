import numpy as np
import cv2

class FrameCapturer:
    def __init__(self, grayscale = False, fps = 5):
        # Initiation of fps and the capturer
        self.fps = fps
        self.capturer = cv2.VideoCapture(0)
        self.grayscale = grayscale
    
    def __del__(self):
        self.capturer.release()

    
    def get_frame(self):
        ret, frame = self.capturer.read()
        if self.grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame


if __name__ == '__main__':
    fc = FrameCapturer()
    
    # Capture frame-by-frame
    #gray = fc.get_frame()

    # Our operations on the frame come here
    

    # Display the resulting frame
    while True:
        gray = fc.get_frame()
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    del(fc)
    cv2.destroyAllWindows()