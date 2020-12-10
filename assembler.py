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
	'STA' : 0b1000  # Store value of A register to provided memory address
}

code = ['{0:0{1}X}'.format(0b0,4) for i in range(size)]
s = "v2.0 raw\n"

f = open(input_file, 'r')
add = 0
for line in f:
	op = line.split()[0]
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

for w in code:
	s += w + " "	

print(s)
f = open('out.bin', 'w')
f.write(s)
f.close()
