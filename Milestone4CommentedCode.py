#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def check_Container():                                      #Definiing check_container function
        table.rotate_table_angle(45)                        #rotate servo table by 45 degrees
        
        container = []                                      
        
        check_Color_one = table.photoelectric_sensor(0.2)       #Intialise variable check_Color_one to photoelectric value
        check_Color_two = table.inductive_sensor(0.2)           #Intialise variable check_Color_two to inductive value
        
        if check_Color_one[0] > 4 and check_Color_two[0] > 4:      #compare values for first index of sensor values to determine if metal
            container.append("metal")
        elif check_Color_one[0] < 1 and check_Color_two[0] < 1:     #compare values for first index of sensor values to determine if plastic
            container.append("plastic")
        else:
            container.append("paper")                               #anything else is paper
            
        check_Clean = table.load_cell_sensor(0.2)                   #set check_Clean variable equal to output of table.load_sensor
        container.append(check_Clean)                               #append check_CLean values to container list
        
        if (container[0] == "plastic" and check_Clean[0] > 9.5) or (container[0] == "metal" and check_Clean[0] > 15.5) or (container[0] == "paper" and check_Clean[0] > 10.5):    #checking container material IDs and weights and comapring them to preset values to check if they are clean or dirty
            container.append("dirty")                             #if containers meet conditions for dirty, append string dirty to container list
            if container[0] == "metal":                           #if container ID is equal to metal, append string 1 to container list
                container.append("1")
            elif container[0] == "plastic":                       #if container ID is equal to plastic, append sring 4 to container list
                container.append("4")
            else:
                container.append("4")                             #if none of above conditions met, append string 4 to container list
        else:
            container.append("clean")                             #if dirty conditions are not met from earlier conditional, append string clean to container list
            if container[0] == "metal":                           #if container ID is metal, append string 1 to container list
                container.append("1")
            elif container[0] == "plastic":                       #if container ID is plastic, append string 3 to container list
                container.append("3")
            else:
                container.append("2")                            #if none of above conditions met, append string 2 to container list

        table.rotate_table_angle(45)

        return container                                         #return container list with all of container attributes (i.e. clean/dirty, container ID, etc.)

def gen_Rand():                                            #generate random number from 1 to 6 related to container ID
    rand_Num = random.randint(1,6)
    table.dispense_container(rand_Num)

def dispense_Container():                                  
    if table.proximity_sensor_short():
        attributes = check_Container()                    #If container is evaluated to true (i.e. present), attributes variable set equal to container attributes from check container function
    else:
        gen_Rand()
        time.sleep(1)
        attributes = check_Container()                    #If container evaluated to false (i.e. not present), generate another container and then define attributes equal to check container function
    return attributes

def pick_Container():                                     #Pick up container from servo table using q-arm, move to hopper on q-bot
    time.sleep(1)
    arm.move_arm(0.66, 0, 0.25)
    time.sleep(1)
    arm.control_gripper(45)
    time.sleep(1)

def first_Pick():                                         #First pick function places container at back of hopper from servo table, used for first container id
    time.sleep(1)
    arm.move_arm(0.02, -0.59, 0.57)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

def second_Pick():                                      #Second pick function places container directly before the first container, used for second container id
    time.sleep(1)
    arm.move_arm(0.02, -0.52, 0.56)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

def third_Pick():                                       #Third pick function places container directly before the second container, used for third container id
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
    left_sensor, right_sensor = bot.line_following_sensors()            #Setting left and right sensor variables equal to list bot line following sensor values
    if (bot.line_following_sensors() == [1,1]):                         #If bot on line (i.e. list values equal to one and one), advance q-bot by setting wheel speeds equal to 0.1 m/s
        bot.set_wheel_speed([0.1,0.1])
        time.sleep(0.1)
    elif (left_sensor == 1 and right_sensor == 0):                      #If bot deviates from line on right, increase right wheel speed greater than left to make q-bot turn until values are [1,1] again
        bot.set_wheel_speed([0.02,0.04])
    elif (left_sensor == 0 and right_sensor == 1):                      #If bot deviates from line on left, increase left wheel speed greater than right to make q-bot turn until values are [1,1] again       
        bot.set_wheel_speed([0.04,0.02])
    else:
        bot.stop                                                         #If values do not evaulate to movement, immediately stop bot

def deposit_container():                             
    bot.stop()
    bot.activate_linear_actuator()                                       #Activate linear actuator for movement of hopper
    i = 0
    while i <= 60:                                                       #While loop to restrict movement angle of q-bot to 60 degrees
        bot.rotate_hopper(i)
        time.sleep(0.1)
        i += 15
    time.sleep(1)
    bot.rotate_hopper(0)                                                  #Rotate hopper back down to 0 degrees after depositing motion finsihed
    bot.deactivate_linear_actuator()                                      #Activate linear actuator for movement of hopper
    
def transfer_container(num):
    bot.activate_ultrasonic_sensor()                                     #Activate ultrasonic sensor to detect distance from box
    bot.activate_color_sensor()                                          #Activate color sensor to detect bin color 
    dump = False                                                         #Initialise dump variable to false
    if (num == "1"):                                                     #Check num variable against previously generated container IDs and set target to respective bin destination
        target = [1,0,0]
    elif (num == "2"):
        target = [0,1,0]
    elif (num == "3"):
        target = [0,0,1]
    else:
        target = [1,0,1]
    while dump == False:                                                 #while loop to follow line until color/bin ID is equal to reading from color sensor
        line_follow()
        distance = bot.read_ultrasonic_sensor()
        reading_One = bot.read_color_sensor()
        color = reading_One[0]
        if target == color and distance <= 0.05:                         #Check if target color variable equals color of bin ID and distance is less than 0.05 to activate deposit container function
            bot.stop()
            deposit_container()
            bot.deactivate_ultrasonic_sensor()
            bot.deactivate_color_sensor()
            dump = True                                                  #After container dispensed in bin, set dump variable equal to true to terminate while loop
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
    
def check_Pos():                                                    #check_Pos function compares current q-bot position coordinates with difference between home coordinates
    home = (1.5,0,0)
    curr_location = bot.position()
    
    for i in range (3):                                             
        if abs(curr_location[i] - home[i]) > 0.1:                 #for loop compares absolute value of difference bewtween current and home location until it is less than 0.1, giving buffer between home position and correct stop position
            return False
    return True                                                   #Return True value if difference is less than 0.1

def return_home():                                                
    go_Home = check_Pos()                                         #set go_home variable equal to output of check possition function
    while go_Home == False:                                       #while loop runnning while go_Home variable equals false
        line_follow()                                    
        go_Home = check_Pos()                                    
        if go_Home == True:                                       #Follow line until go_Home function evaluates to true (i.e. q-bot reached home), and then break loop
            break

loaded_Container = []
weight = 0
loop = True
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
return_home()
bot.stop()

