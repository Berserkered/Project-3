from Common.project_library import *
import sys
import random
import time
sys.path.append('../')

# 1. Interface Configuration
project_identifier = 'P3B'
ip_address = '192.168.1.53'
hardware = False  # Real life True / Q-Labs False

# 2. Servo Table configuration
short_tower_angle = 270
tall_tower_angle = 225
drop_tube_angle = 270

# 3. Qbot Configuration
bot_camera_angle = 0  # angle in degrees between -21.5 and 0

# 4. Bin Configuration
bin1_offset = 0.15  # offset in meters
bin1_color = [1, 0, 0]
bin2_offset = 0.15
bin2_color = [0, 1, 0]
bin3_offset = 0.15
bin3_color = [0, 0, 1]
bin4_offset = 0.15
bin4_color = [1, 0, 1]

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


def check_Container():
    table.rotate_table_angle(45)

    container = []

    check_Color_one = table.photoelectric_sensor(0.2)
    check_Color_two = table.inductive_sensor(0.2)

    if check_Color_one[0] > 4 and check_Color_two[0] > 4:
        container.append("metal")
    elif check_Color_one[0] < 1 and check_Color_two[0] < 1:
        container.append("plastic")
    else:
        container.append("paper")

    check_Clean = table.load_cell_sensor(0.2)
    container.append(check_Clean)

    if (container[0] == "plastic" and check_Clean[0] > 9.5) or (container[0] == "metal" and check_Clean[0] > 15.5) or (container[0] == "paper" and check_Clean[0] > 10.5):
        container.append("dirty")
        if container[0] == "metal":
            container.append("1")
        elif container[0] == "plastic":
            container.append("4")
        else:
            container.append("4")
    else:
        container.append("clean")
        if container[0] == "metal":
            container.append("1")
        elif container[0] == "plastic":
            container.append("3")
        else:
            container.append("2")

    table.rotate_table_angle(45)

    return container


def gen_Rand():
    rand_Num = random.randint(1, 6)
    table.dispense_container(rand_Num)


def dispense_Container():
    if table.proximity_sensor_short():
        attributes = check_Container()
    else:
        gen_Rand()
        time.sleep(1)
        attributes = check_Container()
    return attributes


def pick_Container():
    time.sleep(1)
    arm.move_arm(0.66, 0, 0.25)
    time.sleep(1)
    arm.control_gripper(45)
    time.sleep(1)


def first_Pick():
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
    if (bot.line_following_sensors() == [1, 1]):
        bot.set_wheel_speed([0.1, 0.1])
        time.sleep(0.1)
    elif (left_sensor == 1 and right_sensor == 0):
        bot.set_wheel_speed([0.02, 0.04])
    elif (left_sensor == 0 and right_sensor == 1):
        bot.set_wheel_speed([0.04, 0.02])
    else:
        bot.stop


def deposit_container():
    bot.stop()
    bot.activate_linear_actuator()
    bot.rotate_hopper(50)
    time.sleep(1)
    bot.rotate_hopper(-50)
    bot.deactivate_linear_actuator()


def transfer_container(num):
    bot.activate_ultrasonic_sensor()
    bot.activate_color_sensor()
    dump = False
    if (num == "1"):
        target = [1, 0, 0]
    elif (num == "2"):
        target = [0, 1, 0]
    elif (num == "3"):
        target = [0, 0, 1]
    else:
        target = [1, 0, 1]
    while dump == False:
        line_follow()
        distance = bot.read_ultrasonic_sensor()
        reading_One = bot.read_color_sensor()
        color = reading_One[0]
        if target == color and distance <= 0.05:
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True
        elif target == color and distance <= 0.05:
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True
        elif target == color and distance <= 0.05:
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True
        elif target == color and distance <= 0.05:
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True
        else:
            pass


def return_home(num):
    curr_location = bot.position()
    while curr_location != home:
        curr_location = bot.position()
        line_follow()
    bot.stop()


loaded_Container = []
weight = 0
loop = True
home = bot.position()
print(home)
while loop == True:
    curr_Container = dispense_Container()
    time.sleep(1)
    print(curr_Container)
    loaded_Container.append(curr_Container)
    weight += loaded_Container[0][1][0]
    curr_Bin = loaded_Container[0][3]
    pick_Container()
    first_Pick()
    time.sleep(1)
    curr_Container = dispense_Container()
    time.sleep(1)
    print(curr_Container)
    loaded_Container.append(curr_Container)
    weight += loaded_Container[1][1][0]
    curr_Bin_two = loaded_Container[1][3]
    if (curr_Bin_two == curr_Bin) and (weight < 90):
        pick_Container()
        second_Pick()
        time.sleep(1)
        curr_Container = dispense_Container()
        time.sleep(1)
        print(curr_Container)
        loaded_Container.append(curr_Container)
        weight += loaded_Container[2][1][0]
        curr_Bin_three = loaded_Container[2][3]
        if (curr_Bin_three == curr_Bin) and (weight < 90):
            pick_Container()
            third_Pick()
        else:
            table.rotate_table_angle(270)
            loop = False
    else:
        table.rotate_table_angle(270)
        loop = False

    loop = False

transfer_container(curr_Bin)
return_home(curr_Bin)
# ---------------------------------------------------------------------------------
# STUDENT CODE ENDS
# ---------------------------------------------------------------------------------
