import time
import math
import os


# ----------------------------------- Setup ---------------------------------- #
currentBranch=[]
files={} #nodeID:(filetype,otherpropertieshere,data)

def error(msg): #? def a useful function trust me
    print(msg)

class Trees:
    def __init__(self, nodeID):
        self.nodeID = nodeID #pointer to file object
        self.children = []

    def addChild(self, childNode):
        #creates edge
        self.children.append(childNode)
    
    def removeChild(self,childNode):
        #destroyes edge
        self.children = [child for child in self.children if child is not childNode]

    def traverse(self, nodeID):
        pass #TODO!
# ----------------------------------- Loop ----------------------------------- #
while True:
    cmd=input("> ")
    try:
        match cmd[0].lower():
            case "0": #? Commands / Help Menu
                if len(cmd)==1:
                    print(''.join(open("commands/help","r").readlines()[:16]))
                elif len(cmd)==2:
                    pass #go in depth abt command that was asked abt
                    if False: error("Parameter Error: Unknown Command!")
                else: error("Parameter Error: Incorrect Parameters!")
            case "1":
                pass
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                pass
            case "6": 
                pass
            case "7":
                pass
            case "8":
                pass
            case "9":
                pass
            case "a":
                pass
            case "b":
                pass
            case "c":
                pass
            case "d":
                pass
            case "e":
                pass
            case "f":
                pass
            

    except:
        error("Command Error: Unknown Command! (Use \"0\" for help!)")