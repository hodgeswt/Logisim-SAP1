
rom = "v2.0 raw\n"

code = [['0000' for i in range(0b100000000)] for j in range(0b10000)]

# Address: 0000 00000000
#          code[step][op]
#		   step op

def to_hex(w):
	return hex(int(bin(w),2))[2:].rjust(4,'0')

J   = 0b01000000000000000
CE  = 0b00100000000000000
CO  = 0b00010000000000000
MI  = 0b00001000000000000
MO  = 0b00000100000000000
RI  = 0b00000010000000000
RO  = 0b00000001000000000
II  = 0b00000000100000000
IO  = 0b00000000010000000
AI  = 0b00000000001000000
AO  = 0b00000000000100000
BI  = 0b00000000000010000
H   = 0b00000000000001000
OI  = 0b00000000000000100
S   = 0b00000000000000010
EO  = 0b00000000000000001

NOP = 0b0000
LDA = 0b0001
ROT = 0b0010
AOT = 0b0011
JMP = 0b0100
HLT = 0b0101
ADA = 0b0110
SBA = 0b0111
STA = 0b1000

code[0b0000] = [to_hex(CO|MI)] * 0b100000000
code[0b0001] = [to_hex(RO|II|CE)] * 0b100000000
	
#LDA
code[0b0010][LDA] = to_hex(IO | MI)
code[0b0011][LDA] = to_hex(RO | AI) 

#ROT
code[2][ROT] = to_hex(RO | OI)

#AOT
code[2][AOT] = to_hex(AO | OI)

#JMP
code[2][JMP] = to_hex(IO | J)

#HLT
code[2][HLT] = to_hex(H)
	
#ADA
code[2][ADA] = to_hex(IO | MI)
code[3][ADA] = to_hex(RO | BI)
code[4][ADA] = to_hex(EO | AI)

#SBA
code[2][SBA] = to_hex(IO | MI)
code[3][SBA] = to_hex(RO | BI)
code[4][SBA] = to_hex(S | EO | AI)
 
#STA
code[2][STA] = to_hex(IO | MI)
code[3][STA] = to_hex(AO | RI)

for t_step in range(0b0, 0b10000):
	print("t_step: ", t_step, end=" ")
	for opcode in range(0b0, 0b100000000):
		print(code[t_step][opcode], end=", ")
		rom += f"{code[t_step][opcode]}"
		if (opcode != 0b11111111):
			rom += " "
		else:
			rom += "\n"
	print()

#print(rom)

f = open('ctrl_logic.bin', 'w')
f.write(rom)
f.close()
