# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
import keyboard
from Config import cfg
from IMU_Dir import IMU_Calc_North
from Motor import Driver


global Stop_flag
Stop_flag = 0


def keyboard_callback(event):
    global Stop_flag
    if event.name == 'e':
        Stop_flag = 1
        Driver.Rover_Stop()
        print("Emergency Stop!")


def main():
    keyboard.on_press(keyboard_callback)
    IMU_Calc_North.IMU_DATA_GET()
    Driver.Dir_PI()


if __name__ == "__main__":
    IMU_Calc_North.MAG_self_check_Timer_create()
    while True:
        if IMU_Calc_North.self_check_time >= cfg.SELF_CHECK_TIME:
            main()
            break
