import requests
import json
import threading
from Config import cfg
from Motor import Driver

self_check_time = 0
noise_xma = 0
noise_yma = 0
noise_xmi = 0xFF
noise_ymi = 0xFF
north_x = 0
north_y = 0

PID_Para = [0.0040, 0.002]         #KP KI
Err_Hist = [0, 0]                #Pre Last
Target = 0


def MAG_self_check_Timer_create():
    global self_check_time
    t = threading.Timer(0.5, MAG_self_check)
    if self_check_time <= 10:
        t.start()
        self_check_time += 1


def MAG_self_check():
    global noise_xma
    global noise_xmi
    global noise_yma
    global noise_ymi
    global self_check_time
    command = cfg.command_List['IMU_DATA_GET']
    url = "http://" + cfg.ip_addr + "/js?json=" + command
    IMU_data = json.loads(requests.get(url).text)
    noise_xma = max(IMU_data['mx'], noise_xma)
    noise_yma = max(IMU_data['my'], noise_yma)
    noise_xmi = min(IMU_data['mx'], noise_xmi)
    noise_ymi = min(IMU_data['my'], noise_ymi)
    print("IMU_Check:", end='')                                  #dev
    print(self_check_time)                                       #dev
    Driver.Rover_Move(0.2, -0.2)
    MAG_self_check_Timer_create()


def IMU_data_get_Timer_create():
    t = threading.Timer(0.2, IMU_DATA_GET)
    t.start()


def IMU_DATA_GET():
    command = cfg.command_List['IMU_DATA_GET']
    url = "http://" + cfg.ip_addr + "/js?json=" + command
    IMU_data = json.loads(requests.get(url).text)

    mag_x = IMU_data['mx']
    mag_y = IMU_data['my']

    gamaX = (noise_xma - noise_xmi) / 2
    gamaY = (noise_yma - noise_ymi) / 2

    global north_x
    global north_y

    north_x = mag_x-gamaX
    north_y = mag_y-gamaY
    print("NS_Polar: ", end='')
    print(north_y)                 #dev
    IMU_data_get_Timer_create()


def Dir_PI_Timer_Create():
    t = threading.Timer(0.3, Dir_PI)
    t.start()


def Dir_PI():
    Last_Dir = north_y * get_sign(north_x)
    Err = Last_Dir - Target
    PWM_Out = PID_Para[0] * Err + PID_Para[1] * (Err_Hist[0]+Err_Hist[1]+Err)
    Err_Hist[0] = Err_Hist[1]
    Err_Hist[1] = Err
    Driver.Rover_Move(-PWM_Out, PWM_Out)
    Dir_PI_Timer_Create()


def get_sign(number):
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0
