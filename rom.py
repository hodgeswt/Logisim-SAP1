
rom = "v2.0 raw\n"

code = [['00000000' for i in range(0b100000000)] for j in range(0b10000)]

# Address: 0000 00000000
#          code[step][op]
#		   step op

def to_hex(w):
	return hex(int(bin(w),2))[2:].rjust(8,'0')

# Control flags

SID = 0b1000000000000000000000000000
SI  = 0b0100000000000000000000000000
SE  = 0b0010000000000000000000000000
SO  = 0b0001000000000000000000000000
BZ  = 0b0000100000000000000000000000
NE  = 0b0000010000000000000000000000
BL  = 0b0000001000000000000000000000
BG  = 0b0000000100000000000000000000
BC  = 0b0000000010000000000000000000
BE  = 0b0000000001000000000000000000
FI  = 0b0000000000100000000000000000
BO  = 0b0000000000010000000000000000
J   = 0b0000000000001000000000000000
CE  = 0b0000000000000100000000000000
CO  = 0b0000000000000010000000000000
MI  = 0b0000000000000001000000000000
MO  = 0b0000000000000000100000000000
RI  = 0b0000000000000000010000000000
RO  = 0b0000000000000000001000000000
II  = 0b0000000000000000000100000000
IO  = 0b000000000000000010000000
AI  = 0b000000000000000001000000
AO  = 0b000000000000000000100000
BI  = 0b000000000000000000010000
H   = 0b000000000000000000001000
OI  = 0b000000000000000000000100
S   = 0b000000000000000000000010
EO  = 0b000000000000000000000001

# Opcodes
NOP = 0b0000
LDA = 0b0001
ROT = 0b0010
AOT = 0b0011
JMP = 0b0100
HLT = 0b0101
ADA = 0b0110
SBA = 0b0111
STA = 0b1000
LDB = 0b1001
BOT = 0b1010
ADB = 0b1011
SBB = 0b1100
STB = 0b1101
BEQ = 0b1110
BNE = 0b1111
UFR = 0b10000
BZO = 0b10001
PHB = 0b10010
PLB = 0b10011

#
# Establish instructions
#

#Fetch
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
code[4][ADA] = to_hex(EO | AI | FI)

#SBA
code[2][SBA] = to_hex(IO | MI)
code[3][SBA] = to_hex(RO | BI)
code[4][SBA] = to_hex(S | EO | AI | FI)
 
#STA
code[2][STA] = to_hex(IO | MI)
code[3][STA] = to_hex(AO | RI)

#LDB
code[0b0010][LDB] = to_hex(IO | MI)
code[0b0011][LDB] = to_hex(RO | BI)

#BOT
code[2][BOT] = to_hex(BO | OI)

#ADB
code[2][ADB] = to_hex(IO | MI)
code[3][ADB] = to_hex(RO | AI)
code[4][ADB] = to_hex(EO | BI | FI)

#SBB
code[2][SBB] = to_hex(IO | MI)
code[3][SBB] = to_hex(RO | AI)
code[4][SBB] = to_hex(S | EO | BI | FI)

#STB
code[2][STA] = to_hex(IO | MI)
code[3][STA] = to_hex(BO | RI)

#BEQ
code[2][BEQ] = to_hex(IO | BE)

#BNE
code[2][BNE] = to_hex(IO | NE)

#UFR
code[2][UFR] = to_hex(FI)

#BZO
code[2][BZO] = to_hex(IO | BZ)

#PHB
code[2][PHB] = to_hex(SID | SE)
code[3][PHB] = to_hex(BO | SI)

#PLB
code[2][PLB] = to_hex(SO | BI)
code[3][PLB] = to_hex(SE)

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
