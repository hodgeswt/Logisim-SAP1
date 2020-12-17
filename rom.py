
rom = "v2.0 raw\n"

code = [['00000000' for i in range(0b100000000)] for j in range(0b10000)]

# Address: 0000 00000000
#          code[step][op]
#		   step op

def to_hex(w):
	return hex(int(bin(w),2))[2:].rjust(8,'0')

# Control flags
IRI  = 0b1000000000000000000000000000000000000
ADRD = 0b100000000000000000000000000000000000
ADRI = 0b10000000000000000000000000000000000
ADO = 0b1000000000000000000000000000000000
_ADI = 0b100000000000000000000000000000000
TRO = 0b10000000000000000000000000000000
CRO = 0b1000000000000000000000000000000
CI  = 0b100000000000000000000000000000
TI  = 0b10000000000000000000000000000
SID = 0b1000000000000000000000000000
SI  = 0b0100000000000000000000000000
SE  = 0b0010000000000000000000000000
SO  = 0b0001000000000000000000000000
BZ  = 0b0000100000000000000000000000
NE  = 0b0000010000000000000000000000
SOI = 0b0000001000000000000000000000
OTI = 0b0000000100000000000000000000
TX  = 0b0000000010000000000000000000
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
LDC = 0b1011
COT = 0b1100
STB = 0b1101
BEQ = 0b1110
BNE = 0b1111
UFR = 0b10000
BZO = 0b10001
PHA = 0b10010
PLA = 0b10011
JST = 0b10100
RST = 0b10101
BTA = 0b10110
CTA = 0b10111
ATB = 0b11000
ATC = 0b11001
LT  = 0b11010
ATO = 0b11011
BTO = 0b11100
ADI = 0b11101
ATX = 0b11111
ARI = 0b100000
ARD = 0b100001
AIA = 0b100010
RIR = 0b100011
SAR = 0b100100
TAD = 0b100101

#
# Establish instructions
#

#Fetch
code[0] = [to_hex(CO|MI)] * 0b100000000
code[1] = [to_hex(RO|II|CE)] * 0b100000000
	
#LDA
code[2][LDA] = to_hex(IO | MI)
code[3][LDA] = to_hex(RO | AI) 

#ROT
code[2][ROT] = to_hex(RO | OI)

#AOT
code[2][AOT] = to_hex(AO | OI)

#ATO
code[2][ATO] = to_hex(AO | OTI)

#BTO
code[2][BTO] = to_hex(BO | OTI)

#JMP
code[2][JMP] = to_hex(IO | J)

#HLT
code[2][HLT] = to_hex(H)
	
#ADA
code[2][ADA] = to_hex(IO | MI)
code[3][ADA] = to_hex(RO | TI)
code[4][ADA] = to_hex(FI)
code[5][ADA] = to_hex(EO | AI)

#SBA
code[2][SBA] = to_hex(IO | MI)
code[3][SBA] = to_hex(RO | TI)
code[4][SBA] = to_hex(FI)
code[5][SBA] = to_hex(S | EO | AI)
 
#STA
code[2][STA] = to_hex(IO | MI)
code[3][STA] = to_hex(AO | RI)

#LDB
code[2][LDB] = to_hex(IO | MI)
code[3][LDB] = to_hex(RO | BI)

#BOT
code[2][BOT] = to_hex(BO | OI)

#STB
code[2][STB] = to_hex(IO | MI)
code[3][STB] = to_hex(BO | RI)

#BEQ
code[2][BEQ] = to_hex(IO | BE)

#BNE
code[2][BNE] = to_hex(IO | NE)

#UFR
code[2][UFR] = to_hex(FI)

#BZO
code[2][BZO] = to_hex(IO | BZ)

#PHA
code[2][PHA] = to_hex(SID | SE)
code[3][PHA] = to_hex(AO | SI)

#PLA
code[2][PLA] = to_hex(SO | AI)
code[3][PLA] = to_hex(SE)

#JST
code[2][JST] = to_hex(SID | SE)
code[3][JST] = to_hex(CO | SI)
code[4][JST] = to_hex(IO | J)

#RST
code[2][RST] = to_hex(SO | TI)
code[4][RST] = to_hex(SE | TRO | J)

#LDC
code[2][LDC] = to_hex(IO | MI)
code[3][LDC] = to_hex(RO | CI)

#COT
code[2][COT] = to_hex(CRO | OI)

#BTA
code[2][BTA] = to_hex(BO | AI)

#CTA
code[2][CTA] = to_hex(CO | AI)

#ATB
code[2][ATB] = to_hex(AO | BI)

#ATC
code[2][ATC] = to_hex(AO | CI)

#LT
code[2][LT] = to_hex(IO | MI)
code[3][LT] = to_hex(RO | TI)

#ATX
code[2][ATX] = to_hex(AO | SOI)
code[3][ATX] = to_hex(TX)

#ADI
code[2][ADI] = to_hex(IO | MI)
code[3][ADI] = to_hex(RO | _ADI)

#ARI
code[2][ARI] = to_hex(ADRI)

#ARD
code[2][ARD] = to_hex(ADRD)

#AIA
code[2][AIA] = to_hex(ADO | MI)
code[3][AIA] = to_hex(RO | AI)

#RIR
code[2][RIR] = to_hex(IO | MI)
code[3][RIR] = to_hex(IRI | RI)

#SAR
code[2][SAR] = to_hex(IO | MI)
code[3][SAR] = to_hex(ADO | RI)

#TAD
code[2][TAD] = to_hex(ADO | MI)
code[3][TAD] = to_hex(AO | RI)

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
