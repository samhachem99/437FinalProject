import sys 

# commands acceptable
FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
SPEED = "POWER"
COMMANDS_CONSTS = [FROWARD, BACKWARD, LEFT, RIGHT, STOP, SPEED]

# units acceptable
SECONDS = "SECONDS"

class Validation():
    def __init__(self, text_list: list):
        text = ""
        text_list = text_list
        
    def __init__(self):
        text = ""
        text_list = []
    
    def __init__(self, text: str):
        text = text
        text_list = []
        
    def validate_direction(self, command: str):
        pass

    def validate_duration(self, command: str):
        pass

    def validate_unit(self, command: str):
        pass

    def validate_command(self, command: str):
        pass
        
    def validate(self):
        try:
            self.text_list.index(',')
        except:
            return 0

        command_list = text.strip().lower().split(',')
        for command in command_list:
            validator_retval = self.validate_command(command)
            if validator_retval != 0: # or somehting else
                return 0

if __name__ == "__main__":
    text = sys.argv[1]
    obj = Validation(text_list=text)
    retval = obj.validate()
    print(retval)