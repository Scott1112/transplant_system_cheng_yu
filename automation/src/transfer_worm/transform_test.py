from tkinter import EXCEPTION
from mt24x import MT24X
from worm_image_det import ImageProcessing
import time
import colorama
from colorama import Fore
from colorama import Style
from serial import SerialException
from sound import Sound
import sys

# slow_mode = input("slow mode?(y/n)")
slow_mode ="y"
if slow_mode == "y" or "":
    acc_step, dec_step, vec_step = 12000, 12000, 3000
elif slow_mode == "n":
    acc_step, dec_step, vec_step = 20000, 20000, 20000
    # acc_step, dec_step, vec_step = 75000, 75000, 25000


# initialize motor and set speed (馬達連線)
try:
    motor = MT24X(acc_step,  dec_step, vec_step, 'COM3', 115200, ratio=1.9322) # ratio(well)=1.8195, ratio(larve)=1.7857
    motor.move_MODE_P(2, -10000, 36000, 36000, 6000, wait = True)
    motor.calibration(0, 36000, 36000, -6000)  # calibration馬達校正 校正速度需一致 馬達的歸零速度要一致才不會有誤差
    motor.calibration(1, 36000, 36000, 6000)
    motor.calibration(2, 36000, 36000, 6000, wait = True)
except SerialException:
    print(Fore.RED+"Cannot connect motor, please turn off MTHelper.exe, check COM port number, or replug cable"+Style.RESET_ALL)
    sys.exit(1)

motor.block_init_cam = [50000, -38000, -6000] #相機拍攝位置
motor.z_safe_pos = -32500 #Z軸安全高度
motor.z_pick_pos = -40300 #Z軸吸取高度
camera_point = [111, 53] #手動填寫相機座標點
# matrix = [2839, -2792, -7124, 7147] # a11 a12 a21 a22
x_ratio = [39.9169632, 31125.1483]
y_ratio = [39.7, -79224.7]

# move to camera init point
motor.move_MODE_P(0, motor.block_init_cam[0])
motor.move_MODE_P(1, motor.block_init_cam[1])
motor.move_MODE_P(2, motor.block_init_cam[2], wait=True)

# motor.set_out(0, 1)
# time.sleep(5)
# motor.set_out(0, 0)

# time.sleep(1)

# motor.set_out(1, 1)
# time.sleep(2)
# motor.set_out(1, 0)

# motor_x = matrix[0]*camera_point[0] + matrix[1]*camera_point[1]
# motor_y = matrix[2]*camera_point[0] + matrix[3]*camera_point[1]

# motor_x = int(camera_point[0]*x_ratio[0]+x_ratio[1])
# motor_y = int(camera_point[1]*y_ratio[0]+y_ratio[1])
# motor.motor_point = [motor_x, motor_y]
 

# print('motor point:', motor.motor_point)
# time.sleep(2) #check motor_point

# # ----- move to motor point -----
# motor.move_MODE_P(2, motor.z_safe_pos, wait=True)

# motor.move_MODE_P(0, motor.motor_point[0])
# motor.move_MODE_P(1, motor.motor_point[1], wait=True)

# motor.move_MODE_P(2, motor.z_pick_pos, wait=True)

# time.sleep(5) #確認馬達與相機位置是否相同

# motor.move_MODE_P(2, motor.z_safe_pos, wait=True)