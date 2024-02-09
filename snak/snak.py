import re
from math import floor, ceil
class Snak:
	def __init__(self,code):
		def num(n):
			try:return int(n) 
			except:
				try:return float(n)
				except:pass
		def repVar(check):return re.sub(r'~(.*?)~', lambda match: str(self.vars[match.group(1)]), check)
		lines=code.split("\n")
		line=0
		global vars,labels,cache
		self.cache=[]
		self.vars={}
		while line<len(lines):
			parts=lines[line].split(" ")
			if lines[line].strip():
				match parts[0]:
					case "txt":
						print(' '.join([repVar(i) for i in parts[1:]]))
					case "cmd":
						self.cache.append(' '.join(parts[1:]))
					case "jmp":
						line=int(repVar(parts[1]))-2
					case "jnz":
						if self.vars[parts[2]]:
							line=int(parts[1])-2
					case "var":
						match parts[2]:
							case "bln":
								match parts[3]:
									case "=="|"eql":self.vars[parts[1]]=str(repVar(parts[4]))==str(repVar(parts[5]))
									case "!="|"nql":self.vars[parts[1]]=str(repVar(parts[4]))!=str(repVar(parts[5]))
									case ">="|"gre":self.vars[parts[1]]=num(repVar(parts[4]))>=num(repVar(parts[5]))
									case "<="|"lse":self.vars[parts[1]]=num(repVar(parts[4]))<=num(repVar(parts[5]))
									case ">"|"grt":self.vars[parts[1]]=num(repVar(parts[4]))>num(repVar(parts[5]))
									case "<"|"les":self.vars[parts[1]]=num(repVar(parts[4]))<num(repVar(parts[5]))
									case "&"|"and":self.vars[parts[1]]=repVar(parts[4])&repVar(parts[5])
									case "!"|"not":self.vars[parts[1]]=not repVar(parts[4])
									case "^"|"xor":self.vars[parts[1]]=repVar(parts[4])^repVar(parts[5])
									case "|"|"orr":self.vars[parts[1]]=repVar(parts[4])|repVar(parts[5])
							case "num":
								match parts[3]:
									case "set":self.vars[parts[1]]=int(parts[4])
									case "add"|"+":self.vars[parts[1]]=num(num(repVar(parts[4]))+num(repVar(parts[5])))
									case "sub"|"-":self.vars[parts[1]]=num(num(repVar(parts[4]))-num(repVar(parts[5])))
									case "mlt"|"*":self.vars[parts[1]]=num(num(repVar(parts[4]))*num(repVar(parts[5])))
									case "div"|"/":self.vars[parts[1]]=num(num(repVar(parts[4]))/num(repVar(parts[5])))
									case "mod"|"%":self.vars[parts[1]]=num(num(repVar(parts[4]))%num(repVar(parts[5])))
									case "exp"|"^":self.vars[parts[1]]=num(num(repVar(parts[4]))**num(repVar(parts[5])))
									case "rnd":self.vars[parts[1]]=round(num(repVar(parts[4])))
									case "flr":self.vars[parts[1]]=floor(num(repVar(parts[4])))
									case "cil":self.vars[parts[1]]=ceil(num(repVar(parts[4])))
									case "abs":self.vars[parts[1]]=abs(num(repVar(parts[4])))
							case "str":
								match parts[3]:
									case "set":self.vars[parts[1]]=' '.join([repVar(i) for i in parts[4:]])
									case "idx":self.vars[parts[1]]=repVar(parts[4])[int(repVar(parts[5]))]
									case "len":self.vars[parts[1]]=len(repVar(parts[4]))
							case "cpy":self.vars[parts[1]]=self.vars[parts[3]]
							case "lst":
								match parts[3]:
									case "new":self.vars[parts[1]]=[]
									case "get":self.vars[parts[1]]=self.vars[parts[4]][int(parts[5])]
									case "app":self.vars[parts[1]].append([repVar(i) for i in parts[4:]])
									case "del":self.vars[parts[1]].pop(num(repVar(parts[4])))
									case "ins":self.vars[parts[1]].insert(num(repVar(parts[4])),[repVar(i) for i in parts[5:]])
									case "len":self.vars[parts[1]]=len(self.vars[parts[4]])
							case "inp":
								self.vars[parts[1]]=input(' '.join([repVar(i) for i in parts[2:]]))
					case "end":
						line=len(lines)
					case _:
						pass
			line+=1
testing=1
if __name__=="__main__":
	if testing:
		with open("test", "r") as f:
			runSnak(f.read())
	else:
		print(~True)
