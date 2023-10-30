import time
import math
import os

# ----------------------------------- Setup ---------------------------------- #
location=0 #would be a node ID - 0 is the root node's ID
IDs=[] #list of all node IDs

def error(msg): #? def a useful function trust me
    print(msg) #will probably eventually become useful in some way

class Branch:
    def __init__(self, nodeID, parentID):
        global IDs
        self.nodeID = nodeID #how u can identify the class
        IDs.append(nodeID)
        self.properties = None #something here eventually
        self.data = None #would have the file data
        self.children = []
        self.parent = parentID

    def addChild(self, childNode):
        global IDs
        if childNode in IDs:
            self.children.append(childNode)
        else: error(f"ID Error: {childNode} is not a Valid ID!")
            
    
    def removeChild(self,childNode):
        self.children = [child for child in self.children if child is not childNode]
    
    def changeParent(self,parentNode):
        global IDs
        if parentNode in IDs:
            self.parent=parentNode
        else: error(f"ID Error: {parentNode} is not a Valid ID!")
            
    def traverseUp(self, nodeID):
        global location
        if type(self.parent)==int:
            location = self.parent
        else: error(f"Traversal Error: No Parent Node {self.parent}!")

    def traverseDown(self, nodeID, moveTo):
        global location #traverses to one of the child nodes
        if moveTo in range(0,len(self.children)):
            location=
        else: error(f"Index Error: No Child {moveTo}!")

    def destroy(self):
        if self.nodeID:
            global IDs
            IDs=[i for i in IDs if i!=self.nodeID]
            del self

# ----------------------------------- Loop ----------------------------------- #
while True:
    cmd=input("> ")
    try:
        match cmd[0].lower():
            case _: #? Commands / Help Menu
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
