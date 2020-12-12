'''
	Assembler for WH-01 Processor
	Opcodes are defined below

	Other operands:
		# a v // stores value v at address a
		: xxx // Does a comment. 
		O a   // Starts code at the provided address
	Comments are valid at the end of any completed line
		or at the start of a line, if preceded by ;
'''

import sys

input_file = sys.argv[1]
size = int(sys.argv[2])

opcodes = {
	'NOP' : 0b0000, # No operation
	'LDA' : 0b0001, # Load A register with value store at memory address operand
	'ROT' : 0b0010, # Output the value at the current ram address to the display
	'AOT' : 0b0011, # Output the value of the A register to the display
	'JMP' : 0b0100, # Jump operation to line indicated by operand
	'HLT' : 0b0101, # Halt execution
	'ADA' : 0b0110, # Add value stored at memory address operand to the A register 
	'SBA' : 0b0111, # Subtract value stored at mem addrs operand to the A register 
	'STA' : 0b1000, # Store value of A register to provided memory address
	'LDB' : 0b1001, # Load B register with value stored at memory address operand
 	'BOT' : 0b1010, # Output value at B register to display
 	'LDC' : 0b1011, # Add value at ram address to B register - Overwrites A register
 	'COT' : 0b1100, # Subtract value at ram address from B register - Overwrites A register
 	'STB' : 0b1101, # Store B at indicated memory address
	'BEQ' : 0b1110, # Jumps to provided memory address if the equal flag is set
	'BNE' : 0b1111, # Jumps to provided memory address if the equal flag was not set
	'UFR' : 0b10000,# Latches outputs from ALU to the flags register
	'BZO' : 0b10001,# Branches if the ALU output == 0
	'PHA' : 0b10010,# Pushes A value onto stack
	'PLA' : 0b10011,# Pulls A value off of stack
	'JST' : 0b10100,# Jumps to provided address and stores current address on stack
	'RST' : 0b10101,# Jumps to value on stack and increments counter by operand (RST 01 pops stack, adds one, and jumps)
	'BTA' : 0b10110,# Move B register to A register
 	'CTA' : 0b10111,# Move C register to A register
 	'ATB' : 0b11000,# Move A register to B register
 	'ATC' : 0b11001,# Move A register to C register
	'LT'  : 0b11010 # Loads value at given address into TMP register
}

code = ['{0:0{1}X}'.format(0b0,4) for i in range(size)]
s = "v2.0 raw\n"

f = open(input_file, 'r')
add = 0
for line in f:
	if (line[0] == ';'): # Ignore comments
		pass			 # Comments at ends of lines shoul
						 # be ignored by default

	elif (line[0] == ':'): # Store value at proper address
		add += int(line.split()[1], 16)
	else:
		op = line.split()[0]
		if (op == "#"): # If setting a memory value
			a = line.split()[1] # address 
			v = line.split()[2] # value
			code[int(a, 16)] = v.rjust(4,'0') # process add as hex, make val 4 digits
		else:
			op = opcodes[op]
			op = op << 8
			
			opd = line.split()[1]
			opd = int(opd, 16)
		
			word = bin(op ^ opd)
			word = word[2:]
			word = hex(int(word,2))
			word = word[2:].rjust(4,'0')
			code[add] = word
			add += 1
f.close()

c = 0
for w in code:
	if (c == 15):
		s += w + "\n"
		c = 0	
	else:
		s += w + " "
		c += 1
print(s)
f = open('out.bin', 'w')
f.write(s)
f.close()
