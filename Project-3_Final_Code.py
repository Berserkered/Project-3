import sys
import random
import time
sys.path.append('../')
from Common.project_library import *

# 1. Interface Configuration
project_identifier = 'P3B'
ip_address = '192.168.1.49'
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

#Author: Soham
#MacID: pates206
#Purpose: To check if the current container matches the previous container
#Input: The first containers bin ID, the current containers bin ID, and the total weight of all containers
#Output: True if the container can be put on Qbot, False otherwise
def check_Container(curr_Bin, bin_Check, weight):
    #Checks if the current container's bin ID matches the first containers bin ID AND if total weight of all containers is less than 90 grams
    if (bin_Check == curr_Bin) and (weight < 90):
        return True
    
    else:
        return False
    
#Author: Soham
#MacID: pates206
#Purpose: Dispense a random container 
#Input: None
#Output: Return's the ID of the called container
def dispense_Container():
    #Generates a random number from 1 to 6 inclusive
    rand_Num = random.randint(1,6)

    #Dispenses random number container and assigns its information to container
    container = table.dispense_container(rand_Num, True)
    return container

#Author: Soham
#MacID: pates206
#Purpose: Commands Qarm to pick up container and line it up to be placed in the hopper
#Input: None
#Output: None
def pick_Container():
    time.sleep(1)
    
    #Container pickup coordinates
    arm.move_arm(0.66, 0, 0.25)
    time.sleep(1)
    
    #Grab container
    arm.control_gripper(45)
    time.sleep(1)
    
    #Qarm starting position
    arm.move_arm(0.406, 0, 0.483)
    time.sleep(1)
    
    #Rotates Qarm 90 degrees
    arm.rotate_base(-90)

#Author: Soham
#MacID: pates206
#Purpose: Place the container in the hopper
#Input: None
#Output: None
def drop_Container():
    pick_Container()
    time.sleep(1)

    #Places all containers in same location therefore pushing a container in current location backward
    arm.move_arm(0, -0.52, 0.483)
    time.sleep(2)
    
    #Release container
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

#Author: Adam
#MacID: fernaa54
#Purpose: To command the Qbot to follow the yellow line
#Input: 
#Output: 
def line_Follow():
    #Assign variables to line sensor values
    left_Sensor, right_Sensor = bot.line_following_sensors()

    #Depending on which sensors give values of 0 rotates the bot to get it back on the yellow line
    if (bot.line_following_sensors() == [1,1]):
        bot.set_wheel_speed([0.1,0.1])
        time.sleep(0.1)
        
    elif (left_Sensor == 1 and right_Sensor == 0):
        bot.set_wheel_speed([0.02,0.04])
        
    elif (left_Sensor == 0 and right_Sensor == 1):
        bot.set_wheel_speed([0.04,0.02])
        
    elif (bot.line_following_sensors() == [0,0]):
        bot.set_wheel_speed([0.04,0.02])
        
    else:
        bot.rotate(-0.1)

#Author: Adam
#MacID: fernaa54
#Purpose: Commands Qbot to deposit the containers in the bin
#Input: None
#Output: None
def deposit_Container():
    #Activates the linear actuator and raises hopper to dump containers
    bot.activate_linear_actuator()
    bot.dump()
    bot.deactivate_linear_actuator()

#Author: Adam
#MacID: fernaa54
#Purpose: Qbot goes and looks for the correct bin to put the containers in
#Input: The bin number
#Output: None
def transfer_Container(target_Bin):
    bot.activate_ultrasonic_sensor()
    bot.activate_color_sensor()

    #Used to tell bot when to stop using sensors
    dump_Container = False
    
    if (target_Bin == "Bin01"):
        target_Color = [1,0,0]
        
    elif (target_Bin == "Bin02"):
        target_Color = [0,1,0]
        
    elif (target_Bin == "Bin03"):
        target_Color = [0,0,1]
        
    else:
        target_Color = [1,0,1]
        
    while dump_Container == False:
        #Follows the line while constantly getting readings of sensors color and distance
        line_Follow()
        distance = bot.read_ultrasonic_sensor()
        reading_One = bot.read_color_sensor()
        color = reading_One[0]

        #If the readings match these conditions the bot will go forward and dump
        if target_Color == color and distance <= 0.07:
            bot.stop()
            bot.forward_distance(0.095)
            time.sleep(1)
            
            deposit_Container()
            
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()

            dump_Container = True
        else:
            pass
        
    bot.deactivate_ultrasonic_sensor()
    bot.deactivate_color_sensor()

#Author: Soham
#MacID: pates206
#Purpose: Checks position of the Qbot constantly 
#Input: None
#Output: True if the current postion is in 0.1 range of robots starting position, False otherwise
def check_Pos():
    home_Pos = (1.5,-0.025,0)
    curr_Location = bot.position()

    #Checks if the absolute value of the difference of the bots current position and home position is greater than 0.05
    for i in range (3):
        if abs(curr_Location[i] - home_Pos[i]) > 0.05:
            return False
        
    return True

#Author: Soham
#MacID: pates206
#Purpose: Calls the line_Follow and check_Pos commands 
#Input: None
#Output: None
def return_Home():
    go_Home = check_Pos()

    #While the difference between current coordinates and home coordinates is greater than 0.05 continue line follow function
    while go_Home == False:
        line_Follow()
        go_Home = check_Pos()
        if go_Home == True:
            break
        

#Author: Soham
#MacID: pates206
#Purpose: main function
def main():
    time.sleep(2)
    loop = True

    #variable to check if a container is still on the table
    bottle = False
    
    #Stores previous containers information
    last_Container = []
    while loop:

        #Current containers information and total weight
        loaded_Container = []
        weight = 0

        #Runs the block depending on if there is a bottle on the table already or not
        if bottle == False:
            curr_Container = dispense_Container()
            loaded_Container.append(curr_Container)
            weight += loaded_Container[0][1]
            curr_Bin = loaded_Container[0][2]
            print(curr_Container)

        else:
            curr_Container = last_Container
            loaded_Container.append(last_Container)
            weight += loaded_Container[0][1]
            curr_Bin = loaded_Container[0][2]
            print(curr_Container)
            
        time.sleep(1)
        drop_Container()
        time.sleep(1)

        #Dispenses second container
        curr_Container = dispense_Container()
        loaded_Container.append(curr_Container)
        weight += loaded_Container[1][1]
        bin_Check = loaded_Container[1][2]
        print(curr_Container)
            
        time.sleep(1)

        #Checks second containers variables
        if check_Container(curr_Bin, bin_Check, weight):
            drop_Container()
            time.sleep(1)

            #Dispenses third container 
            curr_Container = dispense_Container()
            loaded_Container.append(curr_Container)
            weight += loaded_Container[2][1]
            bin_Check = loaded_Container[2][2]
            print(curr_Container)
                
            time.sleep(1)

            #Checks third containers variables
            if check_Container(curr_Bin, bin_Check, weight):
                drop_Container()

#If the container was not eligible to be placed on the hopper it's information is stored and the code knows theres a bottle already               
            else:
                last_Container = curr_Container
                bottle = True
                
        else:
            last_Container = curr_Container
            bottle = True
     
        transfer_Container(curr_Bin)
        return_Home()
        bot.stop()
        bot.forward_distance(0.075)
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
