import requests
import json
import threading

from Config import cfg
from Motor import Driver

global gamaX
global gamaY
global north_x
global north_y


self_check_time = 0
noise_xma = 0
noise_yma = 0
noise_xmi = 0xFF
noise_ymi = 0xFF
north_x = 0
north_y = 0


def MAG_self_check_Timer_create():
    global self_check_time
    t = threading.Timer(0.5, MAG_self_check)
    if self_check_time <= cfg.SELF_CHECK_TIME:
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
    cfg.Noise_cx.append(IMU_data['mx'])
    cfg.Noise_cy.append(IMU_data['my'])
    noise_xma = max(IMU_data['mx'], noise_xma)
    noise_yma = max(IMU_data['my'], noise_yma)
    noise_xmi = min(IMU_data['mx'], noise_xmi)
    noise_ymi = min(IMU_data['my'], noise_ymi)
    print("IMU_Check:", end='')                                  #dev
    print(self_check_time)                                       #dev
    Driver.Rover_Move(0.15, -0.15)
    MAG_self_check_Timer_create()


def IMU_data_get_Timer_create():
    if cfg.Stop_flag == 0:
        t = threading.Timer(0.2, IMU_DATA_GET)
        t.start()


def IMU_DATA_GET():
    command = cfg.command_List['IMU_DATA_GET']
    url = "http://" + cfg.ip_addr + "/js?json=" + command
    IMU_data = json.loads(requests.get(url).text)

    mag_x = IMU_data['mx']
    mag_y = IMU_data['my']

    global gamaX
    global gamaY

    gamaX = (noise_xma - noise_xmi) / 2
    gamaY = (noise_yma - noise_ymi) / 2

    global north_x
    global north_y

    north_x = mag_x-gamaX
    north_y = mag_y-gamaY
    print("NS_Polar: ", end='')
    print(north_y)                 #dev
    IMU_data_get_Timer_create()

