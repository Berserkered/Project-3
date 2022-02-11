import sys
import random
import time
sys.path.append('../')
from Common.project_library import *

# 1. Interface Configuration
project_identifier = 'P3B'
ip_address = '192.168.1.53' #'169.254.89.137'
hardware = False #Real life True / Q-Labs False

# 2. Servo Table configuration
short_tower_angle = 0
tall_tower_angle = 0
drop_tube_angle = 180

# 3. Qbot Configuration
bot_camera_angle = 0 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
bin1_offset = 0.15 # offset in meters
bin1_color = [1,0,0] 
bin2_offset = 0.15
bin2_color = [0,1,0]
bin3_offset = 0.15
bin3_color = [0,0,1]
bin4_offset = 0.15
bin4_color = [1,0,1]

#--------------- DO NOT modify the information below -----------------------------
if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
def check_Container(curr_Bin, bin_Check, weight):
    if (bin_Check == curr_Bin) and (weight < 90):
        return True
    else:
        return False

def dispense_Container():
    rand_Num = random.randint(1,6)
    container = table.dispense_container(rand_Num, True)
    return container

def pick_Container():
    time.sleep(1)
    arm.move_arm(0.66, 0, 0.25)
    time.sleep(1)
    arm.control_gripper(45)
    time.sleep(1)

def first_Pick():
    pick_Container()
    time.sleep(1)
    arm.move_arm(0.02, -0.59, 0.57)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

def second_Pick():
    pick_Container()
    time.sleep(1)
    arm.move_arm(0.02, -0.52, 0.56)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

def third_Pick():
    pick_Container()
    time.sleep(1)
    arm.move_arm(0.02, -0.46, 0.56)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

def line_follow():
    left_sensor, right_sensor = bot.line_following_sensors()
    if (bot.line_following_sensors() == [1,1]):
        bot.set_wheel_speed([0.1,0.1])
        time.sleep(0.1)
    elif (left_sensor == 1 and right_sensor == 0):
        bot.set_wheel_speed([0.02,0.04])
    elif (left_sensor == 0 and right_sensor == 1):
        bot.set_wheel_speed([0.04,0.02])
    else:
        bot.stop

def deposit_container():
    bot.stop()
    bot.activate_linear_actuator()
    bot.dump()
    bot.deactivate_linear_actuator()
    
def transfer_container(num):
    bot.activate_ultrasonic_sensor()
    bot.activate_color_sensor()
    dump = False
    if (num == "Bin01"):
        target = [1,0,0]
    elif (num == "Bin02"):
        target = [0,1,0]
    elif (num == "Bin03"):
        target = [0,0,1]
    else:
        target = [1,0,1]
    while dump == False:
        line_follow()
        distance = bot.read_ultrasonic_sensor()
        reading_One = bot.read_color_sensor()
        color = reading_One[0]
        if target == color and distance <= 0.049:
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True
        else:
            pass
    bot.deactivate_ultrasonic_sensor()
    bot.deactivate_color_sensor()
    
def check_Pos():
    home = (1.5,0,0)
    curr_location = bot.position()
    
    for i in range (3):
        if abs(curr_location[i] - home[i]) > 0.1:
            return False
    return True

def return_home():
    go_Home = check_Pos()
    while go_Home == False:
        line_follow()
        go_Home = check_Pos()
        if go_Home == True:
            break

loaded_Container = []
weight = 0
loop = True
while loop == True:
    curr_Container = dispense_Container()
    loaded_Container.append(curr_Container)
    weight += loaded_Container[0][1]
    curr_Bin = loaded_Container[0][2]
    print(curr_Container)
    
    time.sleep(1)
    first_Pick()
    time.sleep(1)
    
    curr_Container = dispense_Container()
    loaded_Container.append(curr_Container)
    weight += loaded_Container[1][1]
    bin_Check = loaded_Container[1][2]
    print(curr_Container)
    
    time.sleep(1)
    
    if check_Container(curr_Bin, bin_Check, weight):
        second_Pick()
        time.sleep(1)
        
        curr_Container = dispense_Container()
        loaded_Container.append(curr_Container)
        weight += loaded_Container[2][1]
        bin_Check = loaded_Container[2][2]
        print(curr_Container)
        
        time.sleep(1)
        
        if check_Container(curr_Bin, bin_Check, weight):
            third_Pick()
        else:
            loop = False
    else:
        loop = False
        
    loop = False
        
transfer_container(curr_Bin)
return_home()
bot.stop()
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
