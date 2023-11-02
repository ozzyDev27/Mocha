import time
import math
import os

# ----------------------------------- Setup ---------------------------------- #
location=0 #would be a node ID - 0 is the root node's ID
tree={} #all instances with nodeIDs as keys

def error(msg): #? def a useful function trust me
    print(msg) #will probably eventually become useful in some way

class Branch:
    def __init__(self, ID, parentID):
        self.properties = None #something here eventually
        self.name="MissingNo"
        self.ID=ID
        self.data = None #would have the file data
        self.children = []
        self.parent = parentID

    def addChild(self, childNode):
        global tree
        if childNode in tree.keys():
            self.children.append(childNode)
        else: error(f"ID Error: {childNode} is not a Valid ID!")
    
    def removeChild(self,childNode):
        self.children = [child for child in self.children if child is not childNode]
    
    def changeParent(self,parentNode):
        global tree
        if parentNode in tree.keys():
            self.parent=parentNode
        else: error(f"ID Error: {parentNode} is not a Valid ID!")
            
    def traverseUp(self, nodeID):
        global location
        if type(self.parent)==int:
            location = self.parent
        else: error(f"Traversal Error: No Parent Node {self.parent}!")

    def traverseDown(self, nodeID, moveTo):
        global location
        if moveTo in range(0,len(self.children)):
            location=moveTo
        else: error(f"Index Error: No Child {moveTo}!")

    def destroy(self):
        if self.nodeID:
            global tree
            del tree[self.ID]
            del self #! This line either works, does nothing, or breaks everything.

def newBranch(parentID):
    global tree
    keys = sorted(tree.keys())
    newID = next((i for i,j in enumerate(keys,start=min(keys)) if i!= j), max(keys)+1)
    tree[newID]=Branch(newID,parentID)

tree[0]=Branch(0,None)
tree[0].name="root"

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
