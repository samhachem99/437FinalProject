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

# Language definitions
# Language is all lowercase
COMMAND_SEPARATOR = ","
DIRECTIONS = ['left', 'right', 'backward', 'back', 'forward', 'straight']
POWER = 'power'

def doesListContainNumberString(myList):
    for i in myList:
        try:
            converted = float(i)
            return True
        except:
            continue
    return False

class Validation():
    def __init__(self, text):
        self.commands = []

        # Splits the dictation into separate commands
        command_strings = text.lower().split(COMMAND_SEPARATOR)

        # converts each command string into a list of keywords and stores it into
        # self.commands
        for command_string in command_strings:
            self.commands.append(command_string.split())
        print(self.commands)

    # Returns whether the command contains a directional keyword
    def isCommandDirectional(self, command: list):
        return (bool(set(DIRECTIONS) & set(command)))
    
    # Returns whether the command contains a power keyword
    def isCommandPower(self, command: list):
        return (POWER in command)
    
    # Returns whether a power command is valid
    # A power command is of the form:
    #   SET POWER TO percentage
    def validatePowerCommand(self, command: list):
        return doesListContainNumberString(command)

    # Returns whether a directional command is valid
    # A directional command is of the form:
    #   GO direction FOR time SECONDS
    def validateDirectionalCommand(self, command: list):
        return doesListContainNumberString(command)

    # Returns whether a command is valid. Takes in a list of
    # strings that denote a command
    def isCommandValid(self, command: list):
        if (self.isCommandDirectional(command)):
            return self.validateDirectionalCommand(command)
        elif (self.isCommandPower(command)):
            return self.validatePowerCommand(command)
        return False
    
    # Returns whether a dictation is valid
    def isDictationValid(self):
        for command in self.commands:
            if (not self.isCommandValid(command)):
                return False
        return True

if __name__ == "__main__":
    # Gets the dictation from the shortcut
    text = sys.argv[1]
    obj = Validation(text)
    isDictationValid = obj.isDictationValid()
    if (isDictationValid):
        print("Dictation is valid!")
    else:
        print("Dictation is invalid.")
