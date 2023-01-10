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
egg_count = 0

#init colorbar
colorama.init()

# slow_mode = input("slow mode?(y/n)")
slow_mode ="n"
if slow_mode == "y" or "":
    acc_step, dec_step, vec_step = 12000, 12000, 3000
elif slow_mode == "n":
    acc_step, dec_step, vec_step = 50000, 50000, 25000
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

# ----- 設定位置參數 -----
mode = 100
# 吸取
motor.block_init_cam = [50000, -38000, -6000] #相機拍攝位置
motor.block_init_pos = [67000, -43000, -32500] #吸取初始位置
motor.z_safe_pos = -32500 #Z軸安全高度
motor.z_pick_pos = -40350 #Z軸吸取高度
# 放置 
motor.plate_size = [10, 10] 
motor.plate_init_pos = [79800, -76000, -32500] #放的第一格 
motor.z_place_pos = -32500
motor.plate_step = [3600, -3600] #[X, Y]有方向
  

# # ----- move test (without camera) -----
# motor.test_point = [57000, -60000, -40300]  # test point

# motor.move_MODE_P(0, motor.block_init_cam[0])
# motor.move_MODE_P(1, motor.block_init_cam[1])
# motor.move_MODE_P(2, motor.block_init_cam[2], wait=True)
# time.sleep(1)

# motor.move_MODE_P(0, motor.test_point[0])
# motor.move_MODE_P(1, motor.test_point[1], wait=True)
# time.sleep(1)

# motor.move_MODE_P(2, motor.test_point[2], wait=True)
# time.sleep(2)

# motor.move_MODE_P(2, motor.block_init_pos[2], wait=True)
# time.sleep(1)

# motor.move_MODE_P(0, motor.plate_init_pos[0])
# motor.move_MODE_P(1, motor.plate_init_pos[1])
# motor.move_MODE_P(2, motor.plate_init_pos[2], wait=True)

# # ----- move test (without camera) END -----


# ----- set folder path -----
# folder_name = input('input folder name:')
# folder_name = "test"
folder_name = time.strftime("%Y%m%d_%H%M%S", time.localtime())
image_path = f"C:/Users/User/Desktop/transplant_system_cheng_yu/automation/data/img/inhold_worm/{folder_name}"
# print(f"save images at: {image_path}")

# ----- initialize camera -----
try:
    motor.move_MODE_P(0, motor.block_init_cam[0])
    motor.move_MODE_P(1, motor.block_init_cam[1])
    motor.move_MODE_P(2, motor.block_init_cam[2], wait=True)
    cam = ImageProcessing(image_path)

except AttributeError as e:
    print(Fore.RED+"Cannot connect camera, please unplug or close camera app"+Style.RESET_ALL)
    print(e)
    sys.exit(1)


# start transplantation
cam.motor_egg_count = egg_count
try: 
    before = time.time()

    # find worm centers
    cam.take_photo()
    centers = cam.find_worm_center(show=True)
    # print('center:', center)
    motor.move_MODE_P(2, motor.z_safe_pos, wait=True)
    
    while cam.motor_egg_count <= mode:

        if not centers :
            print(f"{Fore.RED}worm not found!{Style.RESET_ALL}")
            break

        else:
            # start inholding worms
            for center in centers:
                if cam.motor_egg_count == mode:
                    print(f"{Fore.RED}egg plate is full, please change plate!{Style.RESET_ALL}")
                    sound = Sound
                    sound.play_sound()                        
                    raise 
                print(f"center: {center}")
                print(Fore.GREEN+"-"*30+f"worm count: {cam.motor_egg_count}"+"-"*30+Style.RESET_ALL)
                motor.move_to_center(center)
                # cam.take_photo()

                # --- inhold egg ---
                motor.set_out(0, 1)
                motor.move_MODE_P(2, motor.z_pick_pos, 25000, 25000, 10000, wait=True)
                # time.sleep(1)
                # cam.take_photo()
                motor.move_MODE_P(2, motor.z_safe_pos, 25000, 25000, 10000, wait=True)


                # --- motor move to hole ---
                hole_0, hole_1 = motor.get_hole_pos(cam.motor_egg_count)
                motor.move_MODE_P(0, hole_0)
                motor.move_MODE_P(1, hole_1, wait=True)
                motor.move_MODE_P(2, motor.z_place_pos, 25000, 25000, 10000, wait=True)
                # time.sleep(1)
                # cam.take_photo()

                # --- release worm ---
                motor.set_out(0, 0)
                time.sleep(1)
                motor.set_out(1, 1)
                time.sleep(1)
                motor.set_out(1, 0)
                
                # --- finish ---
                motor.move_MODE_P(2, motor.z_safe_pos, 12000, 12000, 3000, wait=True)
                time.sleep(1)

                cam.motor_egg_count += 1
                # print('worm_count:', cam.motor_egg_count)

                # if cam.motor_egg_count == 10 or 20 or 30 or 40 or 50 or 60 or 70 or 80 or 90:
                #     motor.move_MODE_P(0, motor.block_init_cam[0])
                #     motor.move_MODE_P(1, motor.block_init_cam[1])
                #     motor.move_MODE_P(2, motor.block_init_cam[2], wait=True)
                #     cam.take_photo()
                #     centers = cam.find_worm_center(show=True)
                #     motor.move_MODE_P(2, motor.z_safe_pos, wait=True)
                # else:
                #     pass
 

    # if cam.motor_egg_count <= mode:  
    #     print(f"{Fore.RED}out of egg, please add eggs{Style.RESET_ALL}") 
    #     motor.calibration(2, motor.block_init_cam[2], wait=True)
    #     time.sleep(2)
    #     motor.move_MODE_P(1, motor.block_init_cam[1], wait=True)
    #     motor.move_MODE_P(0, motor.block_init_cam[0], wait=True)
    #     input("press enter after adding eggs")
            
except KeyboardInterrupt :
    print(f"{Fore.GREEN}Keyboard Interrrupt{Style.RESET_ALL}")
    pass

# except Exception as e :
#     print(e)
#     # print(f"{Fore.GREEN}{Style.RESET_ALL}") 
#     # motor.calibration(3, 3000, 3000, 1000)
#     # motor.move_MODE_P(0, motor.block_init_pos[0])
#     # motor.move_MODE_P(1, motor.block_init_pos[1], wait=True)
#     pass

after = time.time()
print(f'time last: {after-before}')
motor.move_MODE_P(2, -10000, 36000, 36000, 6000, wait = True)
motor.calibration(0, 36000, 36000, -6000)
motor.calibration(1, 36000, 36000, 6000)
motor.calibration(2, 36000, 36000, 6000, wait = True)
# motor.calibration(2, motor.block_init_cam[2], wait=True)
# motor.move_MODE_P(1, motor.block_init_cam[1])
# motor.move_MODE_P(0, motor.block_init_cam[0], wait=True)