from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys

class StartWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Pose Malone"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.init_window()
        self.loading_window = LoadingWindow()

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


    def on_click(self):
        print('CLICK')
        self.close()
        self.loading_window.show_window()

class LoadingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Pose Malone"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
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

app = QApplication([])
app.setStyle('Fusion')
app.setQuitOnLastWindowClosed(False)
start_window = StartWindow()
status_bar = StatusBar()
app.exec()