ip_addr = "192.168.137.82"

SELF_CHECK_TIME = 19

Stop_flag = 0

Noise_cx = []
Noise_cy = []

command_List = {'OLED_RESET': '{"T":-3}', 'IMU_DATA_GET': '{"T":126}', 'STOP': '{"T":11,"L":0,"R":0}'
                , 'DEV': '{"T":3,"lineNum":0,"Text":"Hello World!"}'}
