# Snak
is a programming language integrated within Mocha, allowing you to do many things within the tree.  
The program has full privileges, meaning there will be no confirmation. **Remember to save!**
# Getting Started
## An Example
Syntax in Snak is rather simple - for example:  
```
txt Hello, world!
var name str John Smith
txt My name is ~name~!
var countdown num set 10
txt ~countdown~
var countdown num sub ~countdown~ 1
var continue bln != ~countdown~ 0
jnz 5 continue
//checks if the countdown has reached zero, and if it hasn't, jumps back
txt Done!
jmp 13
txt This text isn't shown >:D
txt Goodbye!
```
## Comments
Comments are any command that don't exist.  
In the prior example, // is used, but you could use anything, or nothing at all!  
## Jumping
Snak doesn't make use of functions, and instead uses jumping.  
You can jump to any line, and use `jnz` to make an if statement.  
TODO: FINISH THIS
