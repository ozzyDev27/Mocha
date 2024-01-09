def runSnak(code):
	lines=code.split("\n")
	line=0
	vars={"name":"neel"}
	while line<len(lines):
		parts=lines[line].split(" ")
		if lines[line].strip():
			match parts[0]:
				case "dbg":
					print(' '.join(parts[1:]))
				case "cmd":
					pass #runCommand(parts[1],True)
				case "jmp":
					line=int(parts[1])-2
				case "jnz":
					line=int(parts[1])-2 if vars[parts[2]] else line
				case "var":
					match parts[2]:
						case "int":
							vars[parts[1]]=int(parts[3])	
		line+=1
