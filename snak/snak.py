import re
from math import floor, ceil
def repVar(check):return re.sub(r'(?<=~)\w+(?=~)', lambda x: var[x.group(0)], check).replace("~", "")
def num(n):
	try:return int(n) 
	except:
		try:return float(n)
		except:pass
def runSnak(code):
	lines=code.split("\n")
	line=0
	vars={}
	while line<len(lines):
		parts=lines[line].split(" ")
		if lines[line].strip():
			match parts[0]:
				case "txt":
					print(' '.join([repVar(i) for i in parts[1:]]))
				case "cmd":
					pass #runCommand(parts[1],True)
				case "jmp":
					line=int(parts[1])-2
				case "jnz":
					line=int(parts[1])-2 if vars[parts[2]] else line
				case "var":
					match parts[2]:
						case "bln":
							match parts[3]:
								case "==":vars[parts[1]]=vars[parts[4]]==vars[parts[5]]
								case "!=":vars[parts[1]]=vars[parts[4]]!=vars[parts[5]]
								case ">=":vars[parts[1]]=vars[parts[4]]>=vars[parts[5]]
								case "<=":vars[parts[1]]=vars[parts[4]]<=vars[parts[5]]
								case ">":vars[parts[1]]=vars[parts[4]]>vars[parts[5]]
								case "<":vars[parts[1]]=vars[parts[4]]<vars[parts[5]]
								case "&":vars[parts[1]]=vars[parts[4]] &vars[parts[5]]
								case "!":vars[parts[1]]=~vars[parts[4]]
								case "^":vars[parts[1]]=vars[parts[4]]^vars[parts[5]]
								case "|":vars[parts[1]]=vars[parts[4]]|vars[parts[5]]
						case "num":
							match parts[3]:
								case "set":vars[parts[1]]=int(parts[4])
								case "add":parts[1]==num(num(repVar(parts[4]))+num(repVar(parts[5])))
								case "sub":parts[1]==num(num(repVar(parts[4]))-num(repVar(parts[5])))
								case "mlt":parts[1]==num(num(repVar(parts[4]))*num(repVar(parts[5])))
								case "div":parts[1]==num(num(repVar(parts[4]))/num(repVar(parts[5])))
								case "mod":parts[1]==num(num(repVar(parts[4]))%num(repVar(parts[5])))
								case "exp":parts[1]==num(num(repVar(parts[4]))**num(repVar(parts[5])))
								case "rnd":parts[1]==round(num(repVar(parts[4])))
								case "flr":parts[1]==floor(num(repVar(parts[4])))
								case "cil":parts[1]==ceil(num(repVar(parts[4])))
								case "abs":parts[1]==abs(num(repVar(parts[4])))
						case "str":vars[parts[1]]=' '.join([repVar(i) for i in parts[3:]])
						case "cpy":vars[parts[1]]=vars[parts[3]]
						case "lst":
							match parts[3]:
								case "new":vars[parts[1]]=[]
								case "get":vars[parts[1]]=vars[parts[4]][int(parts[5])]
								case "app":vars[parts[1]].append([repVar(i) for i in parts[4:]])
								case "del":vars[parts[1]].pop(num(repVar(parts[4])))
								case "ins":vars[parts[1]].insert(num(repVar(parts[4])),[repVar(i) for i in parts[5:]]))
								case "len":vars[parts[1]]=len(vars[parts[4]])
				case _:
					pass
		line+=1
testing=0
if testing:
	with open("test", "r") as f:
		runSnak(f.read())
else:
	test=[1,2,3,4,5,6,7,8,9,10]
	print(test[4:])
