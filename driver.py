import os
import sys

# commands acceptable
FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
SPEEDUP = "SPEEDUP"
SPEEDDOWN = "SPEEDDOWN"
COMMANDS_CONSTS = [FROWARD, BACKWARD, LEFT, RIGHT, STOP, SPEEDUP, SPEEDDOWN]

# units acceptable
SECONDS = "SECONDS"

def validate_direction(command: str):
    pass

def validate_duration(command: str):
    pass

def validate_unit(command: str):
    pass

def validate_command(command: str):
    pass

def process_text(text: str):
    try:
        text.index(',')
    except:
        return 0
    
    command_list = text.strip().lower().split(',')
    for command in command_list:
        validator_retval = validate_command(command)
        if validator_retval != 0: # or somehting else
            return 0
    


if __name__ == "__main__":
    # print(len(sys.argv))
    # print(sys.argv)
    # text = "go forward 5 seconds, go left for 2 seconds, go right for 1 second, go backward for 10 cms"
    text = sys.argv[1]
    retval = process_text()
    try:
        text.index("hello")
        print("yeah")
    except:
        print("i am sadski")