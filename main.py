import time
import math
import os
from copy import deepcopy
import random
import string
from tkinter import *
from pathlib import Path
import pickle
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
        self.data = None
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
    global tree
    for i in tree.values(): #? checks for unknown parents
        i.parent=0 if i.parent not in tree.keys() else i.parent
    for i in tree.values(): #? checks for unknown children
        i.children=[j for j in i.children if j in tree.keys()]

def areYouSure():
    chars=''.join(random.choice(string.ascii_letters) for i in range(3))
    return input(f"Type in the following text: [{chars.upper()}]\n> ").lower()==chars.lower()

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
            if tree[location]:ancestors.append("root [0]")
            print('\n'.join([f"{node+1}: {ancestors[len(ancestors)-1-node]}" for node in range(0,len(ancestors))]))
        case "2":
            if len(tree[location].children):
                print('\n'.join([f"{i}: {tree[j].name} [{j}]" for i,j in tree[location].checkChildren().items()]))
            else: error("Children Error: No Children Found!")
        case "3":
            if len(cmd)==1:
                error("Parameter Error: No Parameters!")
            elif cmd[1] in ["1","u"]:
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
            elif cmd[1] in ["3","t"]:
                try:
                    if int(cmd[2:]) in tree.keys():
                        location=int(cmd[2:])
                        print(f"Successfuly Moved to {tree[location].name} [{location}]!")
                except TypeError:
                    error(f"Parameter Error: [{cmd[2:]}] is Not a Valid Node ID!")
            else:
                error("Parameter Error: Unknown Traversal Direction!")
        case "4":
            fileType="-".join([i.removesuffix("\n") for i in open("commands/properties","r").readlines()]).split("-")
            fileType={fileType[i]: fileType[i + 1] for i in range(0, len(fileType), 2)}
            fileType=f"{fileType[tree[location].fileType]} [{tree[location].fileType}]" if tree[location].fileType in fileType.keys() else tree[location].fileType 
            print(f"Name: {tree[location].name}\nNode ID: {tree[location].ID}\nFile Type: {fileType}\nMemory Location: {id(tree[location])}")
        case "5":
            if cmd[1]=="n" and location:
                tree[location].name=input("Enter File Name: ").removesuffix("\n")
                print(f"Successfully Changed File Name to {tree[location].name}")
            elif cmd[1]=="t" and location:
                tree[location].fileType=input("Enter File Type: ").removesuffix("\n")
                print(f"Successfully Changed File Type to {tree[location].fileType}")
            else:
                error(f"Unknown Property {cmd[1]}!")
        case "6": 
            match tree[location].fileType:
                case _:
                    pass
        case "7":
            newBranch(location)
        case "8":
            if location:
                if areYouSure():
                    descendants=[location]+tree[location].descendants()
                    ghostLocation=tree[location].parent
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
                error("Root Error: Cannot Delete Root!")
        case "9":
            try:
                if int(cmd[1:]) in tree.keys() and location:
                    tree[location].parent=int(cmd[1:])
                    print(f"Successfully Swapped to Parent ID [{tree[location].parent}]")
                else:
                    error(f"Parameter Error: Node ID [{int(cmd[1:])}] Doesn't Exist!")
            except ValueError: error("Parameter Error: [{cmd[1:]}] is not a Valid Node ID!")
        case "a":
            if location:
                tree[location].clone(tree[location].parent)
                print(f"Successfuly Cloned {tree[location].name} [{location}]")
            else:
                error("Root Error: Cannot Duplicate Root!")
        case "b":
            pass
        case "c":
            toRepeat=input(":> ")
            for i in range(int(cmd[1:])):
                runCommand(toRepeat)
        case "d":
            with open("savedData.pkl", 'rb') as file:
                tree=pickle.load(file)
            print("Successfully Loaded Saved Data!")
        case "e":
            safetyCheck()
            with open("savedData.pkl", 'wb') as file: 
                pickle.dump(tree, file)
            print("Successfully Saved Data!")
        case "f":
            print("Remember to Save!")
            if areYouSure():
                global running
                running=False
        case "z": #? debug cmd
            print(tree)
        case _: #? Commands / Help Menu
            if len(cmd)>1 and cmd.startswith("0"):
                if int(cmd[2],16) in range(16):
                    i,j=open("commands/help","r").readlines()[int(cmd[2],16)].strip.split(",")
                    print(''.join(open("commands/help","r").readlines()[i:j]))
                else: error("Parameter Error: Unknown Command!")
            else:
                print(''.join(open("commands/help","r").readlines()[17:33]))
while running:
    runCommand(input("> "))
