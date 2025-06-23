import requests
import threading
import main
from Config import cfg
from IMU_Dir import IMU_Calc_North

PID_Para = [0.0038, 0.0015, -0.003]         #KP KI
Err_Hist = [0, 0, 0]                #Pre Last
Target = 0


def Rover_Move(left_speed, right_speed):
    if left_speed > 0.3:
        left_speed = 0.3
    if left_speed < -0.3:
        left_speed = -0.3
    if right_speed > 0.3:
        right_speed = 0.3
    if right_speed < -0.3:
        right_speed = -0.3
    command = '{"T":1,"L":' + str(left_speed) + ',"R":' + str(right_speed) + '}'
    url = "http://" + cfg.ip_addr + "/js?json=" + command
    requests.get(url)


def Rover_Stop():
    if main.Stop_flag == 1:
        command = cfg.command_List['STOP']
        url = "http://" + cfg.ip_addr + "/js?json=" + command
        requests.get(url)


def Dir_PI_Timer_Create():
    if main.Stop_flag == 0:
        t = threading.Timer(0.3, Dir_PI)
        t.start()


def Dir_PI():
    Last_Dir = IMU_Calc_North.north_y * get_sign(IMU_Calc_North.north_x)
    Err = Last_Dir
    PWM_Out = PID_Para[0] * Err + PID_Para[1] * (Err_Hist[0]+Err_Hist[1]+Err_Hist[2]+Err) + PID_Para[2] * (Err-Err_Hist[2])
    Err_Hist[0] = Err_Hist[1]
    Err_Hist[1] = Err_Hist[2]
    Err_Hist[2] = Err
    Rover_Move(-PWM_Out, PWM_Out)
    Dir_PI_Timer_Create()


def get_sign(number):
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0
