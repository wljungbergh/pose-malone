from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys
import time

from decision_making.decision_maker import DecisionMaker
from filtering.filter import Filter
from frame_capture.frame_capture import FrameCapturer
from headpose_estimator.headpose_estimator import HeadPoseEstimator
from frame_processing.frame_processing import CaffeProcessor
from notifier.notifier import MacOSNotifier


# GLOBAL VARIABLES
REF_POS = []
REF_AREA = []
REF_HEAD_POSE = []

N = 30
# Initialize stuff
print("Loading FrameCapturer ...")
fc = FrameCapturer()
print("Loading FrameProccessor ...")
fp = CaffeProcessor()
print("Loading HeadPoseEstimator ...")
hpe = HeadPoseEstimator()
print("Loading Filters ...")
pos_y_filter = Filter(N)
area_filter = Filter(N)
roll_filter = Filter(N)
pitch_filter = Filter(N)

print("Loading DecisionMaker ...")
dm = DecisionMaker(10, 0.1, 0.1, 0.1, 5)
print("Loading MacOSNotifier ...")
notifier = MacOSNotifier()


def initialize_posture(fc: FrameCapturer, fp: CaffeProcessor, hpe: HeadPoseEstimator):
    # Initialize posture values 
    t = time.time() 
    init_counter = 0
    tot_centerX = 0
    tot_centerY = 0
    tot_area = 0
    tot_yaw = 0
    tot_pitch = 0
    tot_roll = 0

    while time.time() < t + 10:
        init_counter += 1.0
        
        frame = fc.get_frame()
        frame_copy = frame.copy()

        bbox = fp.get_bbox(frame)
        face = fp.get_face(bbox, frame_copy)
        centerX, centerY = fp.get_center(bbox)
        tot_centerX += centerX
        tot_centerY += centerY
        tot_area += fp.get_area(bbox)
        #(yaw, pitch, roll), _  = hpe.estimate_headpose(face)
        #tot_pitch += pitch
        #tot_roll += roll
        #tot_yaw += yaw


    global REF_POS
    global REF_AREA
    global REF_HEAD_POSE

    REF_POS = (tot_centerX/init_counter, tot_centerY/init_counter)
    REF_AREA = tot_area/init_counter
    #REF_HEAD_POSE = np.array([tot_yaw/init_counter, tot_pitch/init_counter, tot_roll/init_counter])



class Worker(QtCore.QRunnable):
    '''
    Worker thread
    '''

    @QtCore.pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start") 
        time.sleep(5)

        initialize_posture(fc, fp, hpe)
        
        print("Thread complete")
        

class StartWindow(QDialog):
    def __init__(self, desktop_width, desktop_height):
        super().__init__()
        self.title = "Welcome!"
        self.width = 720
        self.height = 405
        self.top = desktop_height/2 - self.height/2
        self.left = desktop_width/2 - self.width/2


        self.init_window()
        self.loading_window = LoadingWindow(desktop_width, desktop_height)

    def init_window(self):
        self.setWindowIcon(QtGui.QIcon("doc/icon_images/icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        labelImage = QLabel(self)
        pixmap = QPixmap("doc/initial_images/color/initial.png")
        labelImage.setPixmap(pixmap)
        vbox.addWidget(labelImage)
        self.setLayout(vbox)

        # Set background color
        #self.setAutoFillBackground(True)
        #p = self.palette()
        #p.setColor(self.backgroundRole(), QColor(0,153,102))
        #self.setPalette(p)

        button = QPushButton('Start Application', self)
        button.move(500, 180)
        button.clicked.connect(self.on_click)

        self.show()

    def init_main(self):
        worker = Worker()
        self.threadpool.start(worker)

    def on_click(self):
        print('CLICK')
        self.close()
        self.loading_window.show_window()

class LoadingWindow(QDialog):
    def __init__(self, desktop_width, desktop_height):
        super().__init__()
        self.title = "Initializing..."
        self.width = 720
        self.height = 405
        self.top = desktop_height/2 - self.height/2
        self.left = desktop_width/2 - self.width/2

        self.threadpool = QtCore.QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.init_window()

    def init_window(self):

        self.setWindowIcon(QtGui.QIcon("doc/icon_images/icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        labelImage = QLabel(self)
        pixmap = QPixmap("doc/initial_images/color/waiting.png")
        labelImage.setPixmap(pixmap)
        vbox.addWidget(labelImage)
        self.setLayout(vbox)
        
        # Set background color
        #self.setAutoFillBackground(True)
        #p = self.palette()
        #p.setColor(self.backgroundRole(), QColor(0,153,102))
        #self.setPalette(p)


    def show_window(self):
        self.show()
        worker = Worker()
        self.threadpool.start(worker)


class StatusBar():
    def __init__(self):
        self.icon = QIcon("doc/icon_images/icon.png")

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.menu = QMenu()
        self.reset = QAction("Reset")
        self.reset.triggered.connect(self.reset_posture)

        self.exit = QAction("Quit")
        self.exit.triggered.connect(self.exit_app)

        self.menu.addAction(self.reset)
        self.menu.addAction(self.exit)

        self.tray.setContextMenu(self.menu)

    def reset_posture(self):
        print('RESET POSTURE')

    def exit_app(self):
        QtCore.QCoreApplication.exit()


class GUI():
    def __init__(self):
        self.app = QApplication([])
        self.app.setStyle('Fusion')
        self.app.setQuitOnLastWindowClosed(False)
        self.start_gui()  


    def start_gui(self):
        screen_res = self.app.desktop().screenGeometry()
        desktop_width = screen_res.width()
        desktop_height = screen_res.height()
        
        start_window = StartWindow(desktop_width, desktop_height)
        status_bar = StatusBar()
        self.app.exec()



if __name__ == "__main__":

    gui = GUI()

    print(REF_POS,
            REF_AREA,
            REF_HEAD_POSE)

    pass