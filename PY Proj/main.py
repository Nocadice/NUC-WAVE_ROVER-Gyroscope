# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
import keyboard
import threading
from Config import cfg
from IMU_Dir import IMU_Calc_North
from Motor import Driver

import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QLineEdit
from GUI1 import *
from matplotlib.figure import Figure                                                           #DrawMap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas               #matplotlib into QT
import matplotlib.pyplot as plt                                                                #Draw & Fonts


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
        cfg.Stop_flag = 1
        Driver.Rover_Move(0, 0)

    def dis_data(self):
        # 创建 FigureCanvas 并嵌入到 QWidget 中
        figure = Figure()
        canvas = FigureCanvas(figure)
        layout = QVBoxLayout(self.widget)
        # 我的绘图窗口名称叫widget，所以这里是self.widget。
        # QVBoxLayout是垂直布局，布局管理器用于管理widget中的控件，这里是FigureCanvas
        layout.addWidget(canvas)  # 将FigureCanvas添加到布局管理器中

        # 设置 matplotlib 使用的字体
        plt.rcParams['font.sans-serif'] = ['SimSun', 'Microsoft YaHei']  # 使用宋体和微软雅黑
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        ax = figure.add_subplot(111)
        ax.plot(cfg.Noise_cx, cfg.Noise_cy, marker='o')
        ax.set_title("磁场干扰")
        ax.set_xlabel("Noise_X轴")
        ax.set_ylabel("Noise_Y轴")
        ax.grid(True)
        canvas.draw()


def GUI_Init():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindows()

    window.show()
    window.textEdit.setText(f"{IMU_Calc_North.gamaX}")
    window.textEdit.append(f"{IMU_Calc_North.gamaY}")
    window.dis_data()

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
    IMU_Calc_North.MAG_self_check_Timer_create()
    while True:
        if IMU_Calc_North.self_check_time >= cfg.SELF_CHECK_TIME:
            keyboard.on_press(keyboard_callback)
            main()
            GUI_Init()
            break

