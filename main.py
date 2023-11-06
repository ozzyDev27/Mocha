import time
import math
import os
import random
import string
# ----------------------------------- Setup ---------------------------------- #
location=0 #would be a node ID - 0 is the root node's ID
tree={} #all instances with nodeIDs as keys
running=True

def error(msg): #? def a useful function trust me
    print(msg) #will probably eventually become useful in some way

class Branch:
    def __init__(self, ID, parentID):
        self.name = "MissingNo."
        self.ID = ID
        self.fileType= "000"
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

    def checkChildren(self):
        return {i+1:self.children[i] for i in range(len(self.children))}

    def destroy(self):
        if self.ID:
            global tree
            del tree[self.ID]
            del self #! This line either works, does nothing, or breaks everything.

def newBranch(parentID):
    global tree
    keys = sorted(tree.keys())
    newID = next((i for i,j in enumerate(keys,start=min(keys)) if i!= j), max(keys)+1)
    tree[newID]=Branch(newID,parentID)
    tree[parentID].addChild(newID)

tree[0]=Branch(0,None)
tree[0].name="root"

#test setups            0
location=2   #          |
newBranch(0) #1         1
newBranch(1) #2        / \
newBranch(1) #3       2   3
newBranch(2) #4      / \
newBranch(2) #5     4   5

# ------------------------------------ Loop ----------------------------------- #
def runCommand(cmd):
    global tree,location
    match cmd[0].lower():
        case "1":
            ancestors=[]
            level=1
            ghostLocation=location
            ancestors.append(f"{tree[ghostLocation].name} [{ghostLocation}]")
            while tree[ghostLocation].parent:
                ancestors.append(f"{tree[tree[ghostLocation].parent].name} [{tree[ghostLocation].parent}]")
                ghostLocation=tree[ghostLocation].parent
            ancestors.append("root [0]")
            print('\n'.join([f"{node+1}: {ancestors[len(ancestors)-1-node]}" for node in range(0,len(ancestors))]))
        case "2":
            print('\n'.join([f"{i}: {j}" for i,j in tree[location].checkChildren().items()]))
        case "3":
            if cmd[1] in ["1","u"]:
                if location:
                    location=tree[location].parent
                    print(f"Moved to [{location}] {tree[location].name}")
                else:
                    error("Traversal Error: No Parent of Root Node!")
            elif cmd[1] in ["2","d"]:
                try:
                    if int(cmd[2]) in tree[location].checkChildren().keys():
                        location=tree[location].checkChildren()[int(cmd[2])]
                        print(f"Moved to [{location}] {tree[location].name}")
                    else:
                        error(f"Parameter Error: No Child {cmd[2]}")
                except:
                    error(f"Parameter Error: Unkown Child {cmd[2]}")
            else:
                error("Parameter Error: Unknown Traversal Direction!")
        case "4":
            fileType="-".join([i.removesuffix("\n") for i in open("commands/properties","r").readlines()]).split("-")
            fileType={fileType[i]: fileType[i + 1] for i in range(0, len(fileType), 2)}
            fileType=f"{fileType[tree[location].fileType]} [{tree[location].fileType}]" if tree[location].fileType in fileType.keys() else tree[location].fileType 
            print(f"Name: {tree[location].name}\nNode ID: {tree[location].ID}\nFile Type: {fileType}\nMemory Location: {id(tree[location])}")
        case "5":
            if cmd[2]=="n":
                tree[location].name=input("Enter File Name: ").removesuffix("\n")
                print(f"Successfully Changed File Name to {tree[location].name}")
            elif cmd[2]=="t":
                tree[location].fileType=input("Enter File Type: ").removesuffix("\n")
                print(f"Successfully Changed File Type to {tree[location].fileType}")
            else:
                error(f"Unknown Property {cmd[2]}!")
        case "6": 
            pass
        case "7":
            newBranch(location)
        case "8": #TODO: destroy all children
            chars=''.join(random.choice(string.ascii_letters) for i in range(3))
            if input(f"Type in the following text: [{chars.upper()}]\n> ").lower()==chars.lower():
                ghostLocation=location
                location=tree[location].parent
                tree[ghostLocation].destroy()
                print(f"Successfully Deleted [{ghostLocation}]")
            else:
                print("Deletion Cancelled!")
        case "9":
            if int(cmd[1:]) in tree.keys():
                tree[location].parent=int(cmd[1:])
                print(f"Successfully Moved Swapped to Parent ID [{tree[location].parent}]")
            else:
                error(f"Parameter Error: Node ID [{int(cmd[1:])}] Doesn't Exist!")
        case "a": #TODO
            keys = sorted(tree.keys())
            duplicateLocation = next((i for i,j in enumerate(keys,start=min(keys)) if i!= j), max(keys)+1)    
            newBranch(tree[location].parent)
            tree[duplicateLocation].name=tree[location].name
            #tree[duplicateLocation].
        case "b":
            pass
        case "c":
            pass
        case "d":
            pass
        case "e":
            pass
        case "f":
            global running
            running=False
        case _: #? Commands / Help Menu
            if len(cmd)>1 and cmd.startswith("0"):
                if int(cmd[2],16) in range(16):
                    i,j=open("commands/help","r").readlines()[int(cmd[2],16)].strip.split(",")
                    print(''.join(open("commands/help","r").readlines()[i:j]))
                else: error("Parameter Error: Unknown Command!")
            else:
                print(''.join(open("commands/help","r").readlines()[:16]))
while running:
    runCommand(input("> "))
