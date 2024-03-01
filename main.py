import time
import math
import os
import random
import string
from pathlib import Path
import pickle
from snak.snak import Snak
exec(f"from {'tkinter' if os.name=='nt' else 'tk'} import *") #?dont judge I just got linux on my laptop
# ----------------------------------- Setup ---------------------------------- #
location=0
tree={}
clipboard=None
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
        global tree
        del tree[self.ID]
        del self

    def getClipboardData(self,getChildren):
        global tree
        return {
            "ID":self.ID,
            "name":self.name,
            "fileType": self.fileType,
            "data":self.data,
            "children":[tree[child].getClipboardData(True) for child in self.children] if getChildren else False
        }

def newBranch(parentID):
    global tree
    keys = sorted(tree.keys())
    newID = next((i for i,j in enumerate(keys,start=min(keys)) if i!= j), max(keys)+1)
    tree[newID]=Branch(newID,parentID)
    tree[parentID].children.append(newID)
    return newID

def paste(parent,data):
    global tree
    newNode=newBranch(parent)
    tree[newNode].name=data["name"]
    tree[newNode].ID=data["ID"]
    tree[newNode].fileType=data["fileType"]
    tree[newNode].data=data["data"]
    for child in data["children"]:paste(newNode,child)

tree[0]=Branch(0,None)
tree[0].name="root"
clipboard=None

def safetyCheck():
    global tree,location
    for i in tree.values():
        i.parent=0 if i.parent==i.ID or i.parent not in tree.keys() else i.parent #? checks for unknown parents or self-parenting
        i.children=[j for j in i.children if j in tree.keys() and j!=i.ID]  #? checks for unknown children and self-childrening
        i.data="" if i.fileType=="000" else i.data
    for i in tree:
        tree[i].ID=i
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
    global tree,location,clipboard
    if len(cmd):
        match cmd[0].lower():
            case "1":
                ancestors=[]
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
                elif not location:
                    error("Cannot Edit Properties of Root Node!","Root")
                elif cmd[1]=="n":
                    tree[location].name=input("Enter File Name:\n:> ").removesuffix("\n")
                    print(f"Successfully Changed File Name to {tree[location].name}")
                elif cmd[1]=="t":
                    toChangeTo=input("Enter File Type:\n:> ").removesuffix("\n")
                    if toChangeTo=="000" and tree[location].fileType!="000":
                        print("Changing This File's Type to Null Will Remove All Data. Are You Sure?")
                        if not areYouSure():
                            return
                    tree[location].fileType=toChangeTo
                    tree[location].data=""
                    print(f"Successfully Changed File Type to {tree[location].fileType}")
                else:
                    error(f"Unknown Property {cmd[1]}!","Parameter")
            case "6": 
                match cmd[1].lower():
                    case "1":
                        openFile(tree[location])
                        pass #within window
                    case "2":
                        pass #in terminal
                        match cmd[2].lower():
                            case "1":
                                print(tree[location].data)
                            case "2":
                                tree[location].data.append(input(":>"))
                    case "3":
                        match tree[location].fileType:
                            case "snk":
                                runSnak=Snak(tree[location].data)
                                #//print([runSnak.lines,len(runSnak.lines)])
                                while runSnak.life:
                                    runSnak.runLine()
                                    if runSnak.cache:
                                        runCommand(runSnak.cache,True)
                                runSnak=None
                            case _:
                                print(tree[location].data)
            case "7":
                print(f"Successfully Created a Branch With Node ID [{newBranch(location)}]!")
            case "8":
                if location:
                    if withinLoop or areYouSure():
                        ghostLocation=tree[location].parent
                        descendants=tree[location].descendants()
                        tree[tree[location].parent].children.remove(location)
                        while descendants:
                            tree[descendants[0]].destroy()
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
                match cmd[1]:
                    case "1":
                        if len(cmd)<3:
                            error("Copy Type Not Provided", "Parameter")
                        else:clipboard=tree[location].getClipboardData(cmd[2]=="2")
                    case "2":
                        if clipboard:
                            if not clipboard["children"]:
                                child=newBranch(location)
                                tree[child].name=clipboard["name"]
                                tree[child].ID=clipboard["ID"]
                                tree[child].fileType=clipboard["fileType"]
                                tree[child].data=clipboard["data"]
                            else:
                                paste(location,clipboard)
                        else:
                            error("No Clipboard Data!","Clipboard")
            case "b":
                os.system('cls' if os.name=='nt' else 'clear')
            case "c":
                if len(cmd)==1:
                    error("No Parameters!","Parameter")
                else:
                    toRepeat=input(":> ")
                    if toRepeat[0].lower()!="c" and areYouSure():
                        for i in range(int(cmd[1:])):
                            runCommand(toRepeat,True)
                        print(f"Completed {int(cmd[1:])} Repeats of <{toRepeat}>!")
                    elif toRepeat[0].lower()=="c":
                        error("Cannot Nest Repeats!","Parameter")
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
                match cmd[1]:
                    case "1":
                        tree[location].data="""var test num set 0
var test num add ~test~ 1
txt ~test~
slp 100
jmp 2""" 
                    case _:
                        print(clipboard)
            case _: #? Commands / Help Menu
                if len(cmd)>1 and cmd.startswith("0") and cmd[1].upper() in "0123456789ABCDEF":
                    if int(cmd[1],16) in range(16):
                        i,j=open("commands/help","r").readlines()[int(cmd[1],16)].strip().split(",")
                        print(''.join(open("commands/help","r").readlines()[int(i):int(j)]))
                    else: error("Unknown Command!","Parameter")
                else: print(''.join(open("commands/help","r").readlines()[17:33]))
if __name__=="__main__":
    while running:
        runCommand(input("> "),False)
    print("Goodbye!")
