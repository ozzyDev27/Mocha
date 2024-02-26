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
end
```
# Commands
## Comments
Comments are any command that don't exist.  
In the prior example, // is used, but you could use anything, or nothing at all!  
It is best to use a standardized comment prefix, for readability. 
## Text
This command can be used for anything - a print statement, a debug message, or anything you can think of.  
All you need to do is use the command `txt`, followed by your text.  
If you wrap a word with a `~`, it will print the variable.  
For example, if the variable `name` is set to "`John Smith`", the line
```
txt Hello, my name is ~name~!
```
would return `Hello, my name is John Smith!`.
## Command
This is the purpose of Snak - to integrate with Mocha.  
The command for the command command is `cmd`.  
I now notice this may not make all too much sense.  
The command command (`cmd`) simply runs a Mocha command.  
For example:   
```
cmd 31
```
runs the command `31`, which moves you up.
## Jumping
Snak doesn't make use of functions, and instead uses jumping.  
You can jump to any line, and use `jnz` to make an if statement.  
To jump, you just use the `jmp` command, followed by the line you want to jump to.  
You can also use a num variable, which could be used as a "bookmark" of sorts.  
For example:
```
var line num set 27
jmp ~line~
```
would jump to line 27.  
The `jnz` command works the same, but you must add a boolean variable to the end. If it is true, it will jump, but if it isn't, it just goes to the next line.  
You are required to use a variable, as it has no comprehension.
For example:
```
var test bln >= ~iq~ 100
jnz 27 ~test~
```
would jump to line 27 if the variable `iq` is greater or equal to 100.
## Variables
Variables are the backbone of Snak, needed to perform practically every function.  
Because of this, the variable command is rather extensive.  
The formatting for the variable command is as follows:
```
var Name str set John Smith
```
### Boolean
A boolean variable may be the most basic one there is, just having logic operators.  
The logic operators are as follows:
`==` or `eql` is equal, checking if two variables are the same.  
`!=` or `nql` is not equal, checking if two variables are not the same.  
`>` or `grt` is greater than, checking if a variable is greater than another.  
`<` or `les` is less than, checking if a variable is less than another.  
`>=` or `gre` is greater or equal to, checking if a variable is greater or equal to another.  
`<=` or `lse` is less or equal to, checking if a variable is less or equal to another.  
`&` or `and` is an and gate, checking if two variables are both true.  
`!` or `not` is a not gate, checking if a variable is false.  
`^` or `xor` is an exclusive or gate, checking if only one of the variables is true.  
`|` or `orr` is an or gate, checking if at least one of the variables is true.  
Here are a few examples of the boolean variable:
```
var logIn bln == ~enteredPassword~ ~correctPassword~
var isCool bln nql ~username~ Ultrablob
var smart bln > ~iq~ 100
var newHighScore bln >= ~score~ ~highScore~
var lowHealth bln < ~HP~ 10
var gameOver bln <= ~HP~ 0
var openDoor bln & ~attemptingToOpenDoor~ ~hasKey~
var alwaysTrue bln not 0
var qualified bln orr ~hasCollegeDegree~ ~hasUniversityDegree~
var cantThinkOfAnExample bln xor ~hmmm~ ~whatToPut~
```
### Numbers
Numbers are pretty important in programming, and this wouldn't be a real language without them.  
Similar to booleans, the number variable is rather extensive.  
`set` just sets the variable to the number you put.  
`add` or `+` adds two numbers together.  
`sub` or `-` subtracts two numbers.  
`mlt` or `*` multiplies two numbers.  
`div` or `/` divides two numbers.  
`mod` or `%` gets the modulus n of a number.  
`exp` or `^` gets the exponent n of a number.  
`rnd` rounds a number to its nearest whole.  
`flr` rounds a number down to its nearest whole.  
`cil` rounds a number up to its nearest whole.  
`abs` gets the absolute of a number.
Here are some examples:
```
var HP num set 100
var getAreaOfCircle num exp ~radius~ 2
var getAreaofCircle num mlt ~getAreaOfCircle~ 3.14159
var direction num mod ~angle~ 360
var externalHappiness num abs ~mentalHealthState~
var yeahIRanOutOfExamplesAgain num flr 5.9
```
### Strings
Guess what.  
Strings are pretty important.  
The string type has extremely basic syntax, and is practically the same as the txt command.  
For example:
```
var name str John Doe
```
would set the variable `name` to `John Doe`.

### List
*Although there are other list-related commands, such as `len`, they aren't a part of the list variable command, as they could be used for things such as strings.*  
The list variable type has a number of sub commands.  
#### New
Creates a new, blank list.
```
var myList lst new
```
#### Append
Appends an item to the end of a list
```
var myList lst app hello world, my name is ~name~!
```
#### Delete
Deletes the Nth item from the list.
```
var myList lst del 0
```

#### Insert
Inserts an item into the Nth position
```
var myList lst ins 5 hello world
```
### Miscellaneous
These are the variable types that don't deserve their own section.

#### Length
Gets the length of a variable, be it a string, list, or anything else.
```
var nameLength len ~name~
var listLength len ~myList~
```
#### Index
Gets an item from a specific index of a string, list, or anything else.  
```
var 4thLetter idx 4 ~word~
var 7thItem idx 7 ~myList~
```
#### Copy
Duplicates a variable.  
```
var theSameName cpy ~name~
```
#### Input
Gets an input from the user.
```
var name inp What is your name? > 
```

## End
End is *extremely* important.  
If the program reaches the final line without the end command, it will self destruct.  
If the program never reaches the end however, for example
```
txt hello
jmp 1
```
You do not need to use the end command.  
You may also use the command at any time, ending the program anywhere.  
## Sleep
The sleep command is purely used for timing.  
For example:
```
txt Hello,
slp 150
txt World!
end
```
would print "Hello,", wait for 1.5 seconds, and thne print "World!".