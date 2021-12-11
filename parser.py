import sys
from text2int import text2int

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

# File where the commands are saved after the parsing
FILE_DESTINATION = "commands.txt"

# Encoded keywords (keywords that will be put in the file)
ENC_KEYWORD_POWER = "POWER"
ENC_KEYWORD_LEFT = "LEFT"
ENC_KEYWORD_RIGHT = "RIGHT"
ENC_KEYWORD_FORWARD = "FORWARD"
ENC_KEYWORD_BACKWARD = "BACKWARD"
ENC_KEYWORD_STOP = "STOP"

# Language definitions
# Language is all lowercase
LANG_KEYWORD_SEPARATOR_SYNONYMS = ['comma', 'then', 'than', 'after that', 'next', 'followed by']
LANG_KEYWORD_SEPARATOR = ","

# Different synonyms for the same direction
LANG_KEYWORD_LEFT_SYNONYMS = [ENC_KEYWORD_LEFT]
LANG_KEYWORD_RIGHT_SYNONYMS = [ENC_KEYWORD_RIGHT]
LANG_KEYWORD_FORWARD_SYNONYMS = [ENC_KEYWORD_FORWARD, 'STRAIGHT']
LANG_KEYWORD_BACKWARD_SYNONYMS = [ENC_KEYWORD_BACKWARD, 'BACK', 'REVERSE']
LANG_KEYWORD_STOP_SYNONYMS = [ENC_KEYWORD_STOP, 'STAY', 'FREEZE']

# All directions in the same list
LANG_KEYWORD_DIRECTIONS = []
LANG_KEYWORD_DIRECTIONS.append(LANG_KEYWORD_LEFT_SYNONYMS)
LANG_KEYWORD_DIRECTIONS.append(LANG_KEYWORD_RIGHT_SYNONYMS)
LANG_KEYWORD_DIRECTIONS.append(LANG_KEYWORD_FORWARD_SYNONYMS)
LANG_KEYWORD_DIRECTIONS.append(LANG_KEYWORD_BACKWARD_SYNONYMS)
LANG_KEYWORD_DIRECTIONS.append(LANG_KEYWORD_STOP_SYNONYMS)
LANG_KEYWORD_POWER = 'POWER'

def getFirstNumberFromStringList(myList):
    for word in myList:
        try:
            converted = float(word)
            return converted
        except:
            try:
                converted = float(text2int(word.lower()))
                return converted
            except Exception as e:
                continue
    raise ValueError("There were no numbers in the list!")

def doesListContainNumberString(myList):
    try:
        temp = getFirstNumberFromStringList(myList)
        return True
    except:
        return False

class Validation():
    def __init__(self, text):
        self.commands = []

        # The commands that will be sent to a file
        self.encoded_commands = []

        # Splits the dictation into separate commands
        for separator_synonym in LANG_KEYWORD_SEPARATOR_SYNONYMS:
            text = text.replace(separator_synonym, LANG_KEYWORD_SEPARATOR)
        command_strings = text.upper().split(LANG_KEYWORD_SEPARATOR)

        # converts each command string into a list of keywords and stores it into
        # self.commands
        for command_string in command_strings:
            self.commands.append(command_string.split())

    # Returns whether the command contains a directional keyword
    def getCommandDirection(self, command: list):
        for word in command:
            if (word in LANG_KEYWORD_LEFT_SYNONYMS):
                return ENC_KEYWORD_LEFT
            elif (word in LANG_KEYWORD_RIGHT_SYNONYMS):
                return ENC_KEYWORD_RIGHT
            elif (word in LANG_KEYWORD_FORWARD_SYNONYMS):
                return ENC_KEYWORD_FORWARD
            elif (word in LANG_KEYWORD_BACKWARD_SYNONYMS):
                return ENC_KEYWORD_BACKWARD
            elif (word in LANG_KEYWORD_STOP_SYNONYMS):
                return ENC_KEYWORD_STOP
        return None
    
    # Returns whether the command contains a power keyword
    def isCommandPower(self, command: list):
        return (LANG_KEYWORD_POWER in command)
    
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

    # Adds a power command to the list of encoded commands
    def addPowerCommandToEncoding(self, command: list):
        power = getFirstNumberFromStringList(command)
        self.encoded_commands.append((ENC_KEYWORD_POWER, power))

    # Adds a directional command to the list of encoded commands
    def addDirectionalCommandToEncoding(self, command: list, direction):
        velocity = getFirstNumberFromStringList(command)
        self.encoded_commands.append((direction, velocity))

    # Returns whether a command is valid. Takes in a list of
    # strings that denote a command
    def isCommandValid(self, command: list):
        commandIsValid = False
        directionFromCommand = self.getCommandDirection(command)

        # Check if the command is directional
        if (directionFromCommand != None):
            commandIsValid = self.validateDirectionalCommand(command)
            if (commandIsValid):
                self.addDirectionalCommandToEncoding(command, directionFromCommand)
        # Checks if the command is a power command
        elif (self.isCommandPower(command)):
            commandIsValid = self.validatePowerCommand(command)
            if (commandIsValid):
                self.addPowerCommandToEncoding(command)
        return commandIsValid
    
    # Returns whether a dictation is valid
    def isDictationValid(self):
        self.encoded_commands = []
        atLeastOneIsValid = False
        for command in self.commands:
            atLeastOneIsValid = self.isCommandValid(command) or atLeastOneIsValid
        return atLeastOneIsValid
    
    # Displays the encoding
    def printEncoding(self):
        for command in self.encoded_commands:
            print(command[0], command[1])
    
    # saves the encoding to a file
    def saveEncodingToFile(self, filename):
        f = open(filename, "w")
        for command in self.encoded_commands:
            f.write(command[0] + " " + str(command[1]) + "\n")
        f.close()

if __name__ == "__main__":
    # Gets the dictation from the shortcut
    text = sys.argv[1]
    obj = Validation(text)
    isDictationValid = obj.isDictationValid()
    if (isDictationValid):
        print("Dictation is valid!")
        obj.printEncoding()
        obj.saveEncodingToFile(FILE_DESTINATION)
    else:
        print("Dictation is invalid.")
