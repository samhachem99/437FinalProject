import os
import sys

text = "go forward 5 seconds, go left for 2 seconds, go right for 1 second, go backward for 10 cms"


if __name__ == "__main__":
    # print(len(sys.argv))
    # print(sys.argv)
    text = sys.argv[1]
    if text.index("hello"):
        print("yeah")
    else:
        print("i am sad")