import os
import sys
import time
# import picar_4wd as fc

# commands acceptable
FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
POWER = "POWER"
COMMANDS_CONSTS = [FROWARD, BACKWARD, LEFT, RIGHT, STOP, POWER]
FILE_NAME = "commands.txt" # "/home/pi/sirimessages/picommands.txt"

# units acceptable
SECONDS = "SECONDS"

power_val = 50
fd = None

# def process_data(data=""):
#     global power_val

#     if data != "":
#         if data == FROWARD:
#             fc.forward(power=power_val)
#         elif data == BACKWARD:
#             fc.backward(power=power_val)
#         elif data == RIGHT:
#             fc.turn_right(power=power_val)
#         elif data == LEFT:
#             fc.turn_left(power=power_val)
#         elif data == POWER:
#             power_val = min(100, power_val+10)
#         elif data == STOP:
#             fc.stop()

def get_file_data():
    global fd
    
    if os.path.getsize(filename=FILE_NAME) == 0:
        return None
    data = fd.readlines()
    fd.truncate(0)
    return data
       
def run_driver():
    global fd
    
    fd = open(FILE_NAME, "r+")
    
    while True:
        data = get_file_data()
        if data != None:
            print(data)
        else:
            print("file is empty")
        time.sleep(0.5)

if __name__ == "__main__":
    # print(len(sys.argv))
    # print(sys.argv)
    # text = "go forward 5 seconds, go left for 2 seconds, go right for 1 second, go backward for 10 cms"
    run_driver()