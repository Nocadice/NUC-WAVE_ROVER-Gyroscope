# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
import keyboard
from Config import cfg
from IMU_Dir import IMU_Calc_North
from Motor import Driver

import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QLineEdit
from GUI1 import *

from matplotlib.figure import Figure
#用来创建图形，相当于画布
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#用来将matplotlib的图形嵌入到PyQt5的窗口中
import matplotlib.pyplot as plt
#一般用来绘图，这里用来调整中文字体，因为已经有了画图的FigureCanvas


class MyWindows(QMainWindow, Ui_WAVE_ROVER_UI):
    def __init__(self):
        super(MyWindows, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.ROVER_FORWARD)
        self.pushButton_2.clicked.connect(self.ROVER_LEFT)
        self.pushButton_3.clicked.connect(self.ROVER_RIGHT)
        self.pushButton_4.clicked.connect(self.ROVER_BACK)
        self.pushButton_5.clicked.connect(self.ROVER_STOP)

    def ROVER_FORWARD(self):
        Driver.Rover_Move(0.2, 0.2)

    def ROVER_BACK(self):
        Driver.Rover_Move(-0.2, -0.2)

    def ROVER_LEFT(self):
        Driver.Rover_Move(0.2, -0.2)

    def ROVER_RIGHT(self):
        Driver.Rover_Move(-0.2, 0.2)

    def ROVER_STOP(self):
        Driver.Rover_Move(0, 0)


def GUI_Init():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindows()
    window.show()
    sys.exit(app.exec_())


def keyboard_callback(event):
    if event.name == 'e':
        cfg.Stop_flag = 1
        print("Emergency Stop!")
        Driver.Rover_Stop()


def main():
    IMU_Calc_North.IMU_DATA_GET()
    Driver.Dir_PI()


if __name__ == "__main__":
    # IMU_Calc_North.MAG_self_check_Timer_create()
    # while True:
    #     if IMU_Calc_North.self_check_time >= cfg.SELF_CHECK_TIME:
            keyboard.on_press(keyboard_callback)
            GUI_Init()
            # main()
            # break

