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

def error(msg,errortype): #? def a useful function trust me
    print(f"{errortype} Error: {msg}") #will probably eventually become useful in some way
def warning(msg):
    print(msg)
class Branch:
    def __init__(self, ID, parentID):
        self.name = "MissingNo."
        self.ID = ID
        self.fileType= "000"
        self.data = None
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
        duplicateLocation = next((i for i,j in enumerate(keys,start=min(keys)) if i!=j), max(keys)+1)    
        newBranch(newParent)
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

tree[0]=Branch(0,None)
tree[0].name="root"

def safetyCheck():
    global tree,location
    for i in tree.values(): #? checks for unknown parents
        i.parent=0 if i.parent not in tree.keys() else i.parent
    for i in tree.values(): #? checks for unknown children
        i.children=[j for j in i.children if j in tree.keys()]
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
    match file.fileType:
        case "000":
            error("Unable to Open Null File!","Open")
        case _:
            from commands.open.txt import window
            textWindow=window(tree[location])
            textWindow.top()

# ------------------------------------ Loop ----------------------------------- #
def runCommand(cmd):
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
                else: error("No Children Found!","Children")
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
                            if int(cmd[2]) in tree[location].checkChildren().keys():
                                location=tree[location].checkChildren()[int(cmd[2])]
                                print(f"Moved to [{location}] {tree[location].name}")
                            else:
                                error(f"No Child {cmd[2]}","Parameter")
                        except:
                            error(f"{cmd[2]} isn't a Valid Node ID!","Parameter")
                    elif cmd[1] in ["3","t"]:
                        try:
                            if int(cmd[2:]) in tree.keys():
                                location=int(cmd[2:])
                                print(f"Successfuly Moved to {tree[location].name} [{location}]!")
                        except TypeError:
                            error(f"[{cmd[2:]}] is Not a Valid Node ID!","Parameter")
                    else:
                        error("Unknown Traversal Direction!","Parameter")
                except IndexError: error("No Parameters Provided!","Parameter")
            case "4":
                fileType="-".join([i.removesuffix("\n") for i in open("commands/properties","r").readlines()]).split("-")
                fileType={fileType[i]: fileType[i+1] for i in range(0, len(fileType), 3)}
                fileType=f"{fileType[tree[location].fileType]} [{tree[location].fileType}]" if tree[location].fileType in fileType.keys() else tree[location].fileType 
                print(f"Name: {tree[location].name}\nNode ID: {tree[location].ID}\nFile Type: {fileType}\nMemory Location: {id(tree[location])}")
            case "5":
                if len(cmd)==1:
                    error("No Parameters!", "Parameter")
                elif cmd[1]=="n" and location:
                    tree[location].name=input("Enter File Name:\n:> ").removesuffix("\n")
                    print(f"Successfully Changed File Name to {tree[location].name}")
                elif cmd[1]=="t" and location:
                    tree[location].fileType=input("Enter File Type:\n:> ").removesuffix("\n")
                    print(f"Successfully Changed File Type to {tree[location].fileType}")
                else:
                    error(f"Unknown Property {cmd[1]}!","Parameter")
            case "6": 
                openFile(tree[location])
            case "7":
                newBranch(location)
            case "8":
                if location:
                    if areYouSure():
                        ghostLocation=tree[location].parent
                        descendants=[location]+tree[location].descendants()
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
                    if location and int(cmd[1:]) in tree.keys() and len(cmd)-1:
                        tree[location].parent=int(cmd[1:])
                        print(f"Successfully Swapped to Parent ID [{tree[location].parent}]")
                    elif len(cmd)==1:
                        error(f"No Node ID Provided!","Parameter")
                    else:
                        error(f"Node ID [{int(cmd[1:])}] Doesn't Exist!","Parameter")
                except ValueError: error(f"[{cmd[1:]}] is not a Valid Node ID!","Parameter")
            case "a":
                if location:
                    tree[location].clone(tree[location].parent)
                    print(f"Successfuly Cloned {tree[location].name} [{location}]")
                else:
                    error("Cannot Duplicate Root!","Root")
            case "b":
                os.system('cls' if os.name=='nt' else 'clear')
            case "c":
                toRepeat=input(":> ")
                for i in range(int(cmd[1:])):
                    runCommand(toRepeat)
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
                print(open("commands/help","r").read())
            case _: #? Commands / Help Menu
                if len(cmd)>1 and cmd.startswith("0"):
                    if cmd[1].upper() in "0123456789ABCDEF":
                        if int(cmd[1],16) in range(16):
                            i,j=open("commands/help","r").readlines()[int(cmd[1],16)].strip().split(",")
                            print(''.join(open("commands/help","r").readlines()[int(i):int(j)]))
                        else: error("Unknown Command!","Parameter")
                    else: print(''.join(open("commands/help","r").readlines()[17:33]))
                else: print(''.join(open("commands/help","r").readlines()[17:33]))
while running and __name__=="__main__":
    runCommand(input("> "))
print("Goodbye!")
