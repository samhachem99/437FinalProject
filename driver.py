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

if __name__ == "__main__":
    # print(len(sys.argv))
    # print(sys.argv)
    # text = "go forward 5 seconds, go left for 2 seconds, go right for 1 second, go backward for 10 cms"
    text = sys.argv[1]
    try:
        text.index("hello")
        print("yeah")
    except:
        print("i am sadski")