import numpy as np
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys
import time
from math import sqrt

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
FC = []
FP = []
HPE = []
DM = []
NOTIFIER = []
QUIT = False
RESET = False

def load_modules():
    global FC
    global FP
    global HPE
    global DM
    global NOTIFIER

    # Initialize stuff
    print("Loading FrameCapturer ...")
    FC = FrameCapturer()
    print("Loading FrameProccessor ...")
    FP = CaffeProcessor()
    print("Loading HeadPoseEstimator ...")
    HPE = HeadPoseEstimator()

    print("Loading DecisionMaker ...")
    DM = DecisionMaker(10, 50, 15, 50, 30)
    print("Loading MacOSNotifier ...")
    NOTIFIER = MacOSNotifier()


def initialize_posture():   
    # Initialize posture values 
    t = time.time() 
    init_counter = 0
    tot_centerX = 0
    tot_centerY = 0
    tot_area = 0
    tot_yaw = 0
    tot_pitch = 0
    tot_roll = 0

    while time.time() < t + 5:
        init_counter += 1.0
        
        frame = FC.get_frame()
        frame_copy = frame.copy()

        bbox = FP.get_bbox(frame)
        face = FP.get_face(bbox, frame_copy)
        centerX, centerY = FP.get_center(bbox)
        tot_centerX += centerX
        tot_centerY += centerY
        tot_area += FP.get_area(bbox)
        (yaw, pitch, roll), _  = HPE.estimate_headpose(face)
        tot_pitch += pitch
        tot_roll += roll
        tot_yaw += yaw

    global REF_POS
    global REF_AREA
    global REF_HEAD_POSE

    REF_POS = (tot_centerX/init_counter, tot_centerY/init_counter)
    REF_AREA = tot_area/init_counter
    REF_HEAD_POSE = np.array([tot_yaw/init_counter, tot_pitch/init_counter, tot_roll/init_counter])

class Worker(QtCore.QRunnable):
    @QtCore.pyqtSlot()
    def run(self):
        print("Thread start") 
        time.sleep(5)

        load_modules()
        initialize_posture()
        self.window.close()

        print("Loading Filters ...")
        N = 100
        
        pos_y_filter = Filter(N, init_value=REF_POS[1])
        area_filter = Filter(N, init_value=sqrt(REF_AREA))
        roll_filter = Filter(N, init_value=REF_HEAD_POSE[2])
        pitch_filter = Filter(N, init_value=REF_HEAD_POSE[1])

        DM.set_references(sqrt(REF_AREA), REF_HEAD_POSE, REF_POS[1])
        render = False
        global RESET
        while (not QUIT):

            if RESET:
                print('Reset posture')
                initialize_posture()

                pos_y_filter = Filter(N, init_value=REF_POS[1])
                area_filter = Filter(N, init_value=sqrt(REF_AREA))
                roll_filter = Filter(N, init_value=REF_HEAD_POSE[2])
                pitch_filter = Filter(N, init_value=REF_HEAD_POSE[1])
                
                DM.set_references(sqrt(REF_AREA), REF_HEAD_POSE, REF_POS[1])
                RESET = False
                print('Reset done')


            frame = FC.get_frame()
            frame_copy = frame.copy()

            bbox = FP.get_bbox(frame)
            face = FP.get_face(bbox, frame_copy)
            center = FP.get_center(bbox)
            area = FP.get_area(bbox)
            area_filter.add_data(sqrt(area))
            pos_y_filter.add_data(center[1])

            if render: 
                x, y, x2, y2 = bbox
                rectangle(frame, (x, y), (x2, y2), (0,255,0), 1)
                circle(frame, center, 5, (0,255,0), 1)
                text = "Area = {}" .format(area)
                putText(frame, text, (x, y), FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

                imshow('Frame', frame)
                
            if face.shape[0]>100 and face.shape[1]>100:
                (yaw, pitch, roll), img = HPE.estimate_headpose(face, render)
                pitch_filter.add_data(pitch)
                roll_filter.add_data(roll)
                if render:
                    imshow('Face', face)
                
            else:
                if render:
                    imshow('Face', BLACK_SCREEN)
            
            head_pos = [0, pitch_filter.get_smooth_data(), roll_filter.get_smooth_data()]
            good_posture = DM.add_data(area_filter.get_smooth_data(), np.array(head_pos), pos_y_filter.get_smooth_data())
            #print("Good posture? {}".format(good_posture))
            if not good_posture:
                NOTIFIER.send_notification(1, "Pose Malone Says")

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
        self.setWindowIcon(QtGui.QIcon("doc/icon_images/icon_192.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        labelImage = QLabel(self)
        pixmap = QPixmap("doc/initial_images/color/initial.png")
        labelImage.setPixmap(pixmap)
        vbox.addWidget(labelImage)
        self.setLayout(vbox)

        button = QPushButton(self)
        button.setGeometry(QtCore.QRect(100, 100, 254, 49))
        button.move(430, 200)
        button.setIcon(QtGui.QIcon("doc/icon_images/button.png"))
        button.setIconSize(QtCore.QSize(254, 49))
        button.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
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

        self.setWindowIcon(QtGui.QIcon("doc/icon_images/icon_192.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        labelImage = QLabel(self)
        pixmap = QPixmap("doc/initial_images/color/waiting.png")
        labelImage.setPixmap(pixmap)
        vbox.addWidget(labelImage)
        self.setLayout(vbox)
        

    def show_window(self):
        self.show()
        worker = Worker()
        worker.window = self
        self.threadpool.start(worker)

class StatusBar():
    def __init__(self):
        self.icon = QIcon("doc/icon_images/icon_32.png")

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
        global RESET
        RESET = True

    def exit_app(self):
        global QUIT
        QUIT = True
        QtCore.QCoreApplication.exit()

class Application():
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
    gui = Application()