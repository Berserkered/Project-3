import sys
import random
import time
sys.path.append('../')
from Common.project_library import *

# 1. Interface Configuration
project_identifier = 'P3B'
ip_address = '192.168.2.23'
hardware = False #Real life True / Q-Labs False

# 2. Servo Table configuration
short_tower_angle = 270
tall_tower_angle = 225
drop_tube_angle = 270

# 3. Qbot Configuration
bot_camera_angle = 0 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
bin1_offset = 0.14 # offset in meters
bin1_color = [1,0,0] 
bin2_offset = 0.14
bin2_color = [0,1,0]
bin3_offset = 0.14
bin3_color = [0,0,1]
bin4_offset = 0.14
bin4_color = [0,0,0]

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
def checkContainer():
        table.rotate_table_angle(45)
        
        container = []
        
        checkColorone = table.photoelectric_sensor(0.2)
        checkColortwo = table.inductive_sensor(0.2)
        print(checkColorone)
        print(checkColortwo)
        
        if (checkColorone[0] > 4 and checkColortwo[0] > 4):
            container.append("metal")
        elif (checkColorone[0] < 1 and checkColortwo[0] < 1):
            container.append("plastic")
        else:
            container.append("paper")
            
        checkClean = table.load_cell_sensor(0.2)
        container.append(checkClean)
        
        if ((container[0] == "plastic" and checkClean[0] > 9.5) or (container[0] == "metal" and checkClean[0] > 15.5) or (container[0] == "paper" and checkClean[0] > 10.5)):
            container.append("dirty")
        else:
            container.append("clean")

        if (container[0] == "metal"):
            container.append("1")
        elif ((container[0] == "plastic" or container[0] == "paper") and container[1] == "dirty"):
            container.append("4")
        elif (container[0] == "plastic"):
            container.append("3")
        else:
            container.append("2")

        table.rotate_table_angle(45)

        return container

def genRand():
    randNum = random.randint(1,6)
    table.dispense_container(randNum)

def dispenseContainer():
    if table.proximity_sensor_short():
        attributes = checkContainer()
    else:
        genRand()
        time.sleep(1)
        attributes = checkContainer()
    return attributes

def pickContainer():
    time.sleep(1)
    arm.move_arm(0.66, 0, 0.25)
    time.sleep(1)
    arm.control_gripper(45)
    time.sleep(1)

def firstPick():
    time.sleep(1)
    arm.move_arm(-0.11, -0.56, 0.6)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

def secondPick():
    time.sleep(1)
    arm.move_arm(-0.02, -0.56, 0.6)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

def thirdPick():
    time.sleep(1)
    arm.move_arm(0.07, -0.56, 0.6)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

def line_follow():
    following_list = bot.line_following_sensors()
    if following_list == [1,1]:
        bot.set_wheel_speed([0.075,0.075])
    elif following_list == [0,1]:
        bot.set_wheel_speed([0.08,0.05])
    elif following_list == [1,0]:
        bot.set_wheel_speed([0.05,0.08])
    else:
        bot.stop

def deposit_container():
    bot.stop()
    bot.activate_linear_actuator()
    bot.rotate_hopper(60)
    time.sleep(1)
    bot.rotate_hopper(-60)
    bot.deactivate_linear_actuator()
    
def transfer_container(num):
    bot.activate_ultrasonic_sensor()
    bot.activate_color_sensor()
    dump = False
    if (num == "1"):
        target = [1,0,0]
    elif (num == "2"):
        target = [0,1,0]
    elif (num == "3"):
        target = [1,0,0]
    else:
        target = [1,1,1]
    while (dump == False):
        line_follow()
        distance = bot.read_ultrasonic_sensor()
        readingOne = bot.read_color_sensor()
        color = readingOne[0]
        if (target == color and distance <= 0.05):
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True
        elif (target == color and distance <= 0.05):
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True
        elif (target == color and distance <= 0.05):
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True
        elif (target == color and distance <= 0.05):
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True
        else:
            y=1
            x=y
    
def return_home():
    length_time = 70
    start_time = time.time()
    max_time = start_time + length_time
    while time.time() <= max_time:
        line_follow()
    bot.stop()
    

loadedContainer = []
weight = 0
binNum = True
loop = True

bot.rotate(98.12)
while (loop == True):
    currContainer = dispenseContainer()
    time.sleep(1)
    print(currContainer)
    loadedContainer.append(currContainer)
    weight += loadedContainer[0][1][0]
    currBin = loadedContainer[0][3]
    pickContainer()
    firstPick()
    time.sleep(1)
    currContainer = dispenseContainer()
    time.sleep(1)
    print(currContainer)
    loadedContainer.append(currContainer)
    weight += loadedContainer[1][1][0]
    currBintwo = loadedContainer[1][3]
    if ((currBintwo == currBin) and (weight < 90)):
        pickContainer()
        secondPick()
        time.sleep(1)
        currContainer = dispenseContainer()
        time.sleep(1)
        print(currContainer)
        loadedContainer.append(currContainer)
        weight += loadedContainer[2][1][0]
        currBinthree = loadedContainer[2][3]
        if ((currBinthree == currBin) and (weight < 90)):
            pickContainer()
            thirdPick()
        else:
            table.rotate_table_angle(270)
            loop = False
    else:
        table.rotate_table_angle(270)
        loop = False
    
    loop = False
bot.rotate(-98.12)
transfer_container(currBin)
return_home()
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
