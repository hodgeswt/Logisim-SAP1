
rom = "v2.0 raw\n"

code = [
	[0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
    [0b0] * 16,
]

# Address: 0000 0000
#		   step op

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

i = 0b0

for t_step in range(0b0, 0b10000):
	for op in range(0b0, 0b10000):
		if op == ROT:
			print("{0:b}".format(t_step), "{0:b}".format(op))
		# Establish fetch
		if (t_step == 0b0):
			code[t_step][op] = '{0:0{1}X}'.format(CO | MI, 4)
		elif (t_step == 0b1):
			code[t_step][op] = '{0:0{1}X}'.format(RO | II | CE, 4)
		else:
			code[t_step][op] = '{0:0{1}X}'.format(0b0, 4)

#LDA
code[0b10][LDA] = '{0:0{1}X}'.format(IO | MI, 4)
code[0b11][LDA] = '{0:0{1}X}'.format(RO | AI, 4) 

#ROT
code[0b10][ROT] = '{0:0{1}X}'.format(RO | OI, 4)

#AOT
code[0b10][AOT] = '{0:0{1}X}'.format(AO | OI, 4)

#JMP
code[0b10][JMP] = '{0:0{1}X}'.format(IO | J, 4)

#HLT
code[0b10][HLT] = '{0:0{1}X}'.format(H, 4)
	
#ADA
code[0b10][ADA] = '{0:0{1}X}'.format(IO | MI, 4)
code[0b11][ADA] = '{0:0{1}X}'.format(RO | BI, 4)
code[0b100][ADA] = '{0:0{1}X}'.format(EO | AI, 4)

#SBA
code[0b10][SBA] = '{0:0{1}X}'.format(IO | MI, 4)
code[0b11][SBA] = '{0:0{1}X}'.format(RO | BI, 4)
code[0b100][SBA] = '{0:0{1}X}'.format(S | EO | AI, 4)
 
#STA
code[0b10][STA] = '{0:0{1}X}'.format(IO | MI, 4)
code[0b11][STA] = '{0:0{1}X}'.format(AO | RI, 4)

c = 0
for i in code:
	for j in i:
		if (c == 15):		
			rom += f"{j}" + "\n"
			c = 0
		else:
			rom += f"{j}" + " "
			c += 1


print(rom)

f = open('ctrl_logic.bin', 'w')
f.write(rom)
f.close()
