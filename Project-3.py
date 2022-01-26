from Common.project_library import *
import sys
import random
import time
sys.path.append('../')

# 1. Interface Configuration
project_identifier = 'P3B'
ip_address = '192.168.2.23'
hardware = False  # Real life True / Q-Labs False

# 2. Servo Table configuration
short_tower_angle = 270
tall_tower_angle = 225
drop_tube_angle = 270

# 3. Qbot Configuration
bot_camera_angle = 0  # angle in degrees between -21.5 and 0

# 4. Bin Configuration
bin1_offset = 0.20  # offset in meters
bin1_color = [1, 0, 0]
bin2_offset = 0.20
bin2_color = [0, 1, 0]
bin3_offset = 0.20
bin3_color = [0, 0, 1]
bin4_offset = 0.20
bin4_color = [0, 0, 0]

# --------------- DO NOT modify the information below -----------------------------
if project_identifier == 'P0':
    QLabs = configure_environment(
        project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1, ip_address, QLabs, None, hardware)

elif project_identifier in ["P2A", "P2B"]:
    QLabs = configure_environment(
        project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier, ip_address, QLabs, hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,
                           tall_tower_angle, drop_tube_angle]
    # Configuring just the table
    configuration_information = [table_configuration, None, None]
    QLabs = configure_environment(
        project_identifier, ip_address, hardware, configuration_information).QLabs
    table = servo_table(ip_address, QLabs, table_configuration, hardware)
    arm = qarm(project_identifier, ip_address, QLabs, hardware)

elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,
                           tall_tower_angle, drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset, bin2_offset, bin3_offset, bin4_offset], [
        bin1_color, bin2_color, bin3_color, bin4_color]]
    configuration_information = [
        table_configuration, qbot_configuration, bin_configuration]
    QLabs = configure_environment(
        project_identifier, ip_address, hardware, configuration_information).QLabs
    table = servo_table(ip_address, QLabs, table_configuration, hardware)
    arm = qarm(project_identifier, ip_address, QLabs, hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1, ip_address, QLabs, bins, hardware)
# ---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
# ---------------------------------------------------------------------------------


def dispenseContainer():
    if table.proximity_sensor_short():

        rotate_table_angle(45)

        container = []

        checkColorone = table.photoelectric_sensor(0.2)
        checkColortwo = table.inductive_sensor(0.2)
        if (checkColorone[0] > 4 and checkColorone[0] > 4):
            container.append("metal")
        elif (checkColorone[0] < 1 and checkColorone[0] < 1):
            container.append("plastic")
        else:
            container.append("paper")

        checkClean = table.load_cell_sensor(0.2)
        if ((container[0] == "plastic" and checkClean[0] > 9.5) or (container[0] == "metal" and checkClean[0] > 15.5) or (container[0] == "paper" and checkClean[0] > 10.5)):
            container.append("dirty")
        else:
            container.append("clean")

        if (container[0] == "metal"):
            container.append("bin1")
        elif ((container[0] == "plastic" or container[0] == "paper") and container[1] == "dirty"):
            container.append("bin4")
        elif (container[0] == "plastic"):
            container.append("bin3")
        else:
            container.append("bin2")

        rotate_table_angle(45)

        return container

def loadContainer():
    bot.rotate(98.12)
    def pickContainer():
        time.sleep(1)
        arm.move_arm(0.66, 0, 0.25)
        time.sleep(1)
        arm.control_gripper(45)
        time.sleep(1)

    def firstPick():
        time.sleep(1)
        arm.move_arm(-0.11, -0.57, 0.6)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(1)
        arm.rotate_shoulder(-40)
        time.sleep(1)
        arm.home()
        time.sleep(1)

    def secondPick():
        time.sleep(1)
        arm.move_arm(-0.2, -0.57, 0.6)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(1)
        arm.rotate_shoulder(-40)
        time.sleep(1)
        arm.home()
        time.sleep(1)   
       
    def thirdPick():
        time.sleep(1)
        arm.move_arm(0.07, -0.57, 0.6)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(1)
        arm.rotate_shoulder(-40)
        time.sleep(1)
        arm.home()
        time.sleep(1)
    

# ---------------------------------------------------------------------------------
# STUDENT CODE ENDS
# ---------------------------------------------------------------------------------
