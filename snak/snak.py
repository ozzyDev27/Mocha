import re
from math import floor, ceil
class Snak:
	def __init__(self,code):
		self.lines=code.split("\n")
		self.line=0
		self.vars={}
		self.cache=False
	def num(self,n):
		try:return int(n) 
		except:
			try:return float(n)
			except:pass
	def repVar(self,check):return re.sub(r'~(.*?)~', lambda match: str(self.vars[match.group(1)]), check)
	def runLine(self):
		self.cache=False
		if self.lines[self.line].strip():
			parts=self.lines[self.line].split(" ")
			match parts[0]:
				case "txt":
					print(' '.join([self.repVar(i) for i in parts[1:]]))
				case "cmd":
					self.cache=' '.join(parts[1:])
				case "jmp":
					self.line=int(self.repVar(parts[1]))-2
				case "jnz":
					if self.vars[parts[2]]:
						self.line=int(parts[1])-2
				case "var":
					match parts[2]:
						case "bln":
							match parts[3]:
								case "=="|"eql":self.vars[parts[1]]=str(self.repVar(parts[4]))==str(self.repVar(parts[5]))
								case "!="|"nql":self.vars[parts[1]]=str(self.repVar(parts[4]))!=str(self.repVar(parts[5]))
								case ">="|"gre":self.vars[parts[1]]=self.num(self.repVar(parts[4]))>=self.num(self.repVar(parts[5]))
								case "<="|"lse":self.vars[parts[1]]=self.num(self.repVar(parts[4]))<=self.num(self.repVar(parts[5]))
								case ">"|"grt":self.vars[parts[1]]=self.num(self.repVar(parts[4]))>self.num(self.repVar(parts[5]))
								case "<"|"les":self.vars[parts[1]]=self.num(self.repVar(parts[4]))<self.num(self.repVar(parts[5]))
								case "&"|"and":self.vars[parts[1]]=self.repVar(parts[4])&self.repVar(parts[5])
								case "!"|"not":self.vars[parts[1]]=not self.repVar(parts[4])
								case "^"|"xor":self.vars[parts[1]]=self.repVar(parts[4])^self.repVar(parts[5])
								case "|"|"orr":self.vars[parts[1]]=self.repVar(parts[4])|self.repVar(parts[5])
						case "num":
							match parts[3]:
								case "set":self.vars[parts[1]]=int(parts[4])
								case "add"|"+":self.vars[parts[1]]=self.num(self.num(self.repVar(parts[4]))+self.num(self.repVar(parts[5])))
								case "sub"|"-":self.vars[parts[1]]=self.num(self.num(self.repVar(parts[4]))-self.num(self.repVar(parts[5])))
								case "mlt"|"*":self.vars[parts[1]]=self.num(self.num(self.repVar(parts[4]))*self.num(self.repVar(parts[5])))
								case "div"|"/":self.vars[parts[1]]=self.num(self.num(self.repVar(parts[4]))/self.num(self.repVar(parts[5])))
								case "mod"|"%":self.vars[parts[1]]=self.num(self.num(self.repVar(parts[4]))%self.num(self.repVar(parts[5])))
								case "exp"|"^":self.vars[parts[1]]=self.num(self.num(self.repVar(parts[4]))**self.num(self.repVar(parts[5])))
								case "rnd":self.vars[parts[1]]=round(self.num(self.repVar(parts[4])))
								case "flr":self.vars[parts[1]]=floor(self.num(self.repVar(parts[4])))
								case "cil":self.vars[parts[1]]=ceil(self.num(self.repVar(parts[4])))
								case "abs":self.vars[parts[1]]=abs(self.num(self.repVar(parts[4])))
						case "str":
							match parts[3]:
								case "set":self.vars[parts[1]]=' '.join([self.repVar(i) for i in parts[4:]])
								case "idx":self.vars[parts[1]]=self.repVar(parts[4])[int(self.repVar(parts[5]))]
								case "len":self.vars[parts[1]]=len(self.repVar(parts[4]))
						case "cpy":self.vars[parts[1]]=self.vars[parts[3]]
						case "lst":
							match parts[3]:
								case "new":self.vars[parts[1]]=[]
								case "get":self.vars[parts[1]]=self.vars[parts[4]][int(parts[5])]
								case "app":self.vars[parts[1]].append([self.repVar(i) for i in parts[4:]])
								case "del":self.vars[parts[1]].pop(self.num(self.repVar(parts[4])))
								case "ins":self.vars[parts[1]].insert(self.num(self.repVar(parts[4])),[self.repVar(i) for i in parts[5:]])
								case "len":self.vars[parts[1]]=len(self.vars[parts[4]])
						case "inp":
							self.vars[parts[1]]=input(' '.join([self.repVar(i) for i in parts[2:]]))
				case "end":
					self.line=len(self.lines)
				case _:
					pass
		self.line+=1
testing=1
if __name__=="__main__":
	if testing:
		with open("test", "r") as f:
			runSnak(f.read())
	else:
		print(~True)
