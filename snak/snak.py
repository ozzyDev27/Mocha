import re
from math import floor, ceil


def repVar(check):return re.sub(r'~(.*?)~', lambda match: str(vars[match.group(1)]), check)
def num(n):
	try:return int(n) 
	except:
		try:return float(n)
		except:pass
def runSnak(code):
	lines=code.split("\n")
	line=0
	global vars, labels
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
					line=int(repVar(parts[1]))-2
				case "jnz":
					if vars[parts[2]]:
						line=int(parts[1])-2
				case "var":
					match parts[2]:
						case "bln":
							match parts[3]:
								case "==":vars[parts[1]]=str(repVar(parts[4]))==str(repVar(parts[5]))
								case "!=":vars[parts[1]]=str(repVar(parts[4]))!=str(repVar(parts[5]))
								case ">=":vars[parts[1]]=repVar(parts[4])>=repVar(parts[5])
								case "<=":vars[parts[1]]=repVar(parts[4])<=repVar(parts[5])
								case ">":vars[parts[1]]=repVar(parts[4])>repVar(parts[5])
								case "<":vars[parts[1]]=repVar(parts[4])<repVar(parts[5])
								case "&":vars[parts[1]]=repVar(parts[4])&repVar(parts[5])
								case "!":vars[parts[1]]=~repVar(parts[4])
								case "^":vars[parts[1]]=repVar(parts[4])^repVar(parts[5])
								case "|":vars[parts[1]]=repVar(parts[4])|repVar(parts[5])
						case "num":
							match parts[3]:
								case "set":vars[parts[1]]=int(parts[4])
								case "add":vars[parts[1]]=num(num(repVar(parts[4]))+num(repVar(parts[5])))
								case "sub":vars[parts[1]]=num(num(repVar(parts[4]))-num(repVar(parts[5])))
								case "mlt":vars[parts[1]]=num(num(repVar(parts[4]))*num(repVar(parts[5])))
								case "div":vars[parts[1]]=num(num(repVar(parts[4]))/num(repVar(parts[5])))
								case "mod":vars[parts[1]]=num(num(repVar(parts[4]))%num(repVar(parts[5])))
								case "exp":vars[parts[1]]=num(num(repVar(parts[4]))**num(repVar(parts[5])))
								case "rnd":vars[parts[1]]=round(num(repVar(parts[4])))
								case "flr":vars[parts[1]]=floor(num(repVar(parts[4])))
								case "cil":vars[parts[1]]=ceil(num(repVar(parts[4])))
								case "abs":vars[parts[1]]=abs(num(repVar(parts[4])))
						case "str":vars[parts[1]]=' '.join([repVar(i) for i in parts[3:]])
						case "cpy":vars[parts[1]]=vars[parts[3]]
						case "lst":
							match parts[3]:
								case "new":vars[parts[1]]=[]
								case "get":vars[parts[1]]=vars[parts[4]][int(parts[5])]
								case "app":vars[parts[1]].append([repVar(i) for i in parts[4:]])
								case "del":vars[parts[1]].pop(num(repVar(parts[4])))
								case "ins":vars[parts[1]].insert(num(repVar(parts[4])),[repVar(i) for i in parts[5:]])
								case "len":vars[parts[1]]=len(vars[parts[4]])
				case "end":
					line=len(lines)
				case _:
					pass
		line+=1
if  __name__ == "__main__":	
	with open("test", "r") as f:
		runSnak(f.read())
