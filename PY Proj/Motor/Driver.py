import requests
from Config import cfg


def Rover_Move(left_speed, right_speed):
    if left_speed > 0.4:
        left_speed = 0.4
    if left_speed < -0.4:
        left_speed = -0.4
    if right_speed > 0.4:
        right_speed = 0.4
    if right_speed < -0.4:
        right_speed = -0.4
    command = '{"T":1,"L":' + str(left_speed) + ',"R":' + str(right_speed) + '}'
    url = "http://" + cfg.ip_addr + "/js?json=" + command
    requests.get(url)


def Rover_Stop():
    command = cfg.command_List['STOP']
    url = "http://" + cfg.ip_addr + "/js?json=" + command
    requests.get(url)
