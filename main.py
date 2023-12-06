import time
import math
import os
import random
import string
from tkinter import *
from pathlib import Path
import pickle
# ----------------------------------- Setup ---------------------------------- #
location=0 #would be a node ID - 0 is the root node's ID
tree={} #all instances with nodeIDs as keys
running=True
with open('commands/properties', 'r') as file:types={end.split("-")[0]:end.split("-")[2].strip() for end in file.readlines()}

def error(msg,errortype):
    print(f"{errortype} Error: {msg}")
def forHelp(cmd): #? will use later
    print(f"Use <0{cmd[0]}> for help!")

class Branch:
    def __init__(self, ID, parentID):
        self.name = "MissingNo."
        self.ID = ID
        self.fileType= "000"
        self.data = ""
        self.children = []
        self.parent = parentID

    def addChild(self, childNode):
        global tree
        if childNode in tree.keys():
            self.children.append(childNode)
        else: error(f"{childNode} is not a Valid ID!","ID")
    
    def removeChild(self,childNode):
        self.children = [child for child in self.children if child is not childNode]
    
    def changeParent(self,parentNode):
        global tree
        if parentNode in tree.keys():
            self.parent=parentNode
        else: error(f"{parentNode} is not a Valid ID!","ID")
        
    def traverseUp(self, nodeID):
        global location
        if type(self.parent)==int:
            location = self.parent
        else: error(f"No Parent Node {self.parent}!","Traversal")

    def traverseDown(self, nodeID, moveTo):
        global location
        if moveTo in range(0,len(self.children)):
            location=moveTo
        else: error(f"No Child {moveTo}!","Index")

    def checkChildren(self):
        return {i+1:self.children[i] for i in range(len(self.children))}
    
    def descendants(self):
        global tree
        descend=[self.ID]
        i=True
        while i:
            x=[j for j in tree.keys() if tree[j].parent in descend]
            if len(x)>1: 
                descend=x
                i=True
            else:i=False
        return descend

    def destroy(self):
        if self.ID:
            global tree
            del tree[self.ID]
            del self

    def clone(self,newParent):
        global tree
        keys = sorted(tree.keys())
        duplicateLocation = newBranch(newParent)
        tree[duplicateLocation].name=self.name
        tree[duplicateLocation].fileType=self.fileType
        tree[duplicateLocation].data=self.data
        if len(self.children):
            for i in self.children:
                tree[i].clone(duplicateLocation)

def newBranch(parentID):
    global tree
    keys = sorted(tree.keys())
    newID = next((i for i,j in enumerate(keys,start=min(keys)) if i!= j), max(keys)+1)
    tree[newID]=Branch(newID,parentID)
    tree[parentID].addChild(newID)
    return newID

tree[0]=Branch(0,None)
tree[0].name="root"

def safetyCheck():
    global tree,location
    for i in tree.values():
        i.parent=0 if i.parent==i.ID or i.parent not in tree.keys() else i.parent #? checks for unknown parents or self-parenting
        i.children=[j for j in i.children if j in tree.keys()]  #? checks for unknown children
    if location not in tree.keys():
        location=0

def areYouSure():
    chars=''.join(random.choice(string.ascii_letters) for i in range(3))
    return input(f"Type in the following text: [{chars.upper()}]\n:> ").lower()==chars.lower()

#test setups            0
location=2   #          |
newBranch(0) #1         1
newBranch(1) #2        / \
newBranch(1) #3       2   3
newBranch(2) #4      / \
newBranch(2) #5     4   5
tree[2].fileType="txt"

# --------------------------------- Open File -------------------------------- #
def openFile(file):
    match types[file.fileType]:
        case "null":
            error("Unable to Open Null File!","Open")
        case "image":
            pass
        case _:
            from commands.open.txt import window
            textWindow=window(tree[location])
            textWindow.top()

# ------------------------------------ Loop ----------------------------------- #
def runCommand(cmd,withinLoop):
    global tree,location
    if len(cmd):
        match cmd[0].lower():
            case "1":
                ancestors=[]
                level=1
                ghostLocation=location
                ancestors.append(f"{tree[ghostLocation].name} [{ghostLocation}]")
                while tree[ghostLocation].parent:
                    ancestors.append(f"{tree[tree[ghostLocation].parent].name} [{tree[ghostLocation].parent}]")
                    ghostLocation=tree[ghostLocation].parent
                if tree[location]:ancestors.append("root [0]")
                print('\n'.join([f"{node+1}: {ancestors[len(ancestors)-1-node]}" for node in range(0,len(ancestors))]))
            case "2":
                if len(tree[location].children):
                    print('\n'.join([f"{i}: {tree[j].name} [{j}]" for i,j in tree[location].checkChildren().items()]))
                else: print("No Children Found!")
            case "3":
                try:
                    if len(cmd)==1:
                        error("No Parameters!","Parameter")
                    elif cmd[1] in ["1","u"]:
                        if location:
                            location=tree[location].parent
                            print(f"Moved to [{location}] {tree[location].name}")
                        else:
                            error("No Parent of Root Node!","Traversal")
                    elif cmd[1] in ["2","d"]:
                        try:
                            if int(cmd[2:]) in tree[location].checkChildren().keys():
                                location=tree[location].checkChildren()[int(cmd[2:])]
                                print(f"Moved to [{location}] {tree[location].name}")
                            else:
                                error(f"No Child {cmd[2:]}!","Parameter")
                        except:
                            error(f"{cmd[2]} isn't a Valid Node ID!","Parameter")
                    elif cmd[1] in ["3","t"]:
                        try:
                            if int(cmd[2:]) in tree.keys():
                                location=int(cmd[2:])
                                print(f"Successfuly Moved to {tree[location].name} [{location}]!")
                        except TypeError:
                            error(f"[{cmd[2:]}] is Not a Valid Node ID!","Parameter")
                        except ValueError:
                            error("No Node ID Provided!", "Parameter")
                    else:
                        error("Unknown Traversal Direction!","Parameter")
                except IndexError: error("No Parameters Provided!","Parameter")
            case "4":
                fileType="-".join([i.removesuffix("\n") for i in open("commands/properties","r").readlines()]).split("-")
                fileType={fileType[i]: fileType[i+1] for i in range(0, len(fileType), 3)}
                fileType=f"{fileType[tree[location].fileType]} [{tree[location].fileType}]" if tree[location].fileType in fileType.keys() else tree[location].fileType 
                print(f"Name: {tree[location].name}\nNode ID: [{tree[location].ID}]\nParent ID: [{tree[location].parent}]\nFile Type: {fileType}\nMemory Location: {id(tree[location])}\nFile Size: {len(str(tree[location].data))}")
            case "5":
                if len(cmd)==1:
                    error("No Parameters!", "Parameter")
                elif cmd[1]=="n" and location:
                    tree[location].name=input("Enter File Name:\n:> ").removesuffix("\n")
                    print(f"Successfully Changed File Name to {tree[location].name}")
                elif cmd[1]=="t" and location:
                    tree[location].fileType=input("Enter File Type:\n:> ").removesuffix("\n")
                    print(f"Successfully Changed File Type to {tree[location].fileType}")
                elif not location:
                    error("Cannot Edit Properties of Root Node!","Root")
                else:
                    error(f"Unknown Property {cmd[1]}!","Parameter")
            case "6": 
                openFile(tree[location])
            case "7":
                print(f"Successfully Created a Branch With Node ID [{newBranch(location)}]!")
            case "8":
                if location:
                    if withinLoop or areYouSure():
                        ghostLocation=tree[location].parent
                        descendants=tree[location].descendants()
                        tree[tree[location].parent].children.remove(location)
                        while descendants:
                            location=descendants[0]
                            tree[location].destroy()
                            descendants.pop(0)
                        location=ghostLocation
                        print("Deletion Successful!")
                    else:
                        print("Deletion Cancelled!")
                else:
                    error("Cannot Delete Root!","Root")
            case "9":
                try:
                    if location and int(cmd[1:]) in tree.keys() and len(cmd)-1 and int(cmd[1:])!=location:
                        tree[tree[location].parent].children.pop(tree[tree[location].parent].children.index(location))
                        tree[location].parent=int(cmd[1:])
                        tree[tree[location].parent].children.append(location)
                        print(f"Successfully Swapped to Parent ID [{tree[location].parent}]")
                    elif not location:
                        error("Cannot Change Parent of Root Node!","Root")
                    elif int(cmd[1:])==location:
                        error("Cannot Change Parent to Itself!", "Parameter")
                    elif len(cmd)==1:
                        error("No Node ID Provided!","Parameter")
                    else:
                        error(f"Node ID [{int(cmd[1:])}] Doesn't Exist!","Parameter")
                except ValueError: error(f"[{cmd[1:]}] is not a Valid Node ID!","Parameter")
            case "a":
                if location:
                    try:
                        if cmd[1]=="1":
                            tree[location].clone(tree[location].parent)
                            print(f"Successfuly Cloned {tree[location].name} [{location}]")
                        elif cmd[1]=="0":
                            duplicateLocation = newBranch(newParent)
                            tree[duplicateLocation].name=tree[location].name
                            tree[duplicateLocation].fileType=tree[location].fileType
                            tree[duplicateLocation].data=tree[location].data
                            print(f"Successfuly Cloned {tree[location].name} [{location}]")
                        else:
                            error("Unknown Duplicate Type!", "Parameter")
                    except IndexError:
                        error("No Parameters!","Parameter")
                else:
                    error("Cannot Duplicate Root!","Root")
            case "b":
                os.system('cls' if os.name=='nt' else 'clear')
            case "c":
                if len(cmd)==1:
                    error("No Parameters!","Parameter")
                else:
                    toRepeat=input(":> ")
                    if areYouSure():
                        for i in range(int(cmd[1:])):
                            runCommand(toRepeat,True)
                        print(f"Completed {int(cmd[1:])} Repeats of <{toRepeat}>!")
                    else:
                        print(f"Cancelled {int(cmd[1:])} Repeats of <{toRepeat}>!")
            case "d":
                with open("save.pkl", 'rb') as file:
                    tree=pickle.load(file)
                safetyCheck()
                print("Successfully Loaded Saved Data!")
            case "e":
                safetyCheck()
                with open("save.pkl", 'wb') as file: 
                    pickle.dump(tree, file)
                print("Successfully Saved Data!")
            case "f":
                print("Remember to Save!")
                if areYouSure():
                    global running
                    running=False
                else:
                    print("Cancelled Exiting Mocha!")
            case "z": #? debug cmd
                safetyCheck()
            case _: #? Commands / Help Menu
                if len(cmd)>1 and cmd.startswith("0") and cmd[1].upper() in "0123456789ABCDEF":
                    if int(cmd[1],16) in range(16):
                        i,j=open("commands/help","r").readlines()[int(cmd[1],16)].strip().split(",")
                        print(''.join(open("commands/help","r").readlines()[int(i):int(j)]))
                    else: error("Unknown Command!","Parameter")
                else: print(''.join(open("commands/help","r").readlines()[17:33]))

while running and __name__=="__main__":
    runCommand(input("> "),False)
print("Goodbye!")
