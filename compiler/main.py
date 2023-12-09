import re
import ply.lex as lex
import ply.yacc as yacc
from string import ascii_lowercase as al
from itertools import product
import argparse

def assemble(f, size, output_file):
	log("Assembling", args)

	if (type(f) == str):
		f = f.split('\n')

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
		'RST' : 0b10101,# Jumps to value on stack. Pass 00 as argument
		'BTA' : 0b10110,# Move B register to A register
		'CTA' : 0b10111,# Move C register to A register
		'ATB' : 0b11000,# Move A register to B register
		'ATC' : 0b11001,# Move A register to C register
		'LT'  : 0b11010,# Loads value at given address into TMP register
		'ATO' : 0b11011,# Outputs A to Output Register 2
		'BTO' : 0b11100,# Outputs B to Output Register 2
		'ADI' : 0b11101,# Address Register in
		'ATX' : 0b11111,# Outputs A to Serial Out
		'ARI' : 0b100000, # Address register increment
		'ARD' : 0b100001, # Address register decrement
		'AIA' : 0b100010, # Stores value at address register into A register
		'RIR' : 0b100011, # Reads value from Input Register into A register
		'SAR' : 0b100100, # Stores address register
		'TAD' : 0b100101  # Stores A register at address in address register
	}

	code = ['{0:0{1}X}'.format(0b0,6) for i in range(size)]
	s = "v2.0 raw\n"

	add = 0
	var = {}
	pointers = {}
	for line in f:
		log(line, args)
		if (line[0] == ';'): # Ignore comments
			pass			 # Comments at ends of lines shoul
							# be ignored by default
		elif (line[0] == ':'): # Store value at proper address
			add += int(line.split()[1], 16)
		elif (line[0] == '&'):
			if (line.split()[1][0] == "_"):
				a = pointers[line.split()[1]]
			else:
				a = line.split()[1]
			a = int(a,16)
			l = re.findall(r'"(.*?)"',line)[0]
			for i in range(0, len(l)):
				code[a] = hex(ord(l[i]))[2:].rjust(6,'0')
				a -= 1
		elif (line[0] == "."):
			v = line[1:]
			var[v] = add
		elif (line[0] == "_"):
			pointers[line.split()[0]] = line.split()[1]
		else:
			op = line.split()[0]
			if (op == "#"): # If setting a memory value
				a = line.split()[1] # address
				if (a[0] == "_"):
					a = pointers[a]
				v = line.split()[2] # value
				if (v[0] != '%'):
					code[int(a, 16)] = v.rjust(6,'0') # process add as hex, make val 4 digits
				else:
					if (len(v) > 2):
						raise ValueError("Character on line " + add + "must be one character")
					elif (len(v) == 2):
						code[int(a, 16)] = hex(ord(v[1:]))[2:].rjust(6,'0')
					else:
						code[int(a, 16)] = '000020' # space
			else:
				op = opcodes[op]
				op = op << 16

				opd = line.split()[1]
				if (opd[0] == "."):
					try:
						opd = var[opd[1:]]
					except:
						raise Exception("Variable not yet declared")
				elif (opd[0] == "_"):
					try:
						opd = int(pointers[opd],16)
					except:
						raise Exception("Variable not yet declared")
				else:
					opd = int(opd, 16)

				word = bin(op ^ opd)
				word = word[2:]
				word = hex(int(word,2))
				word = word[2:].rjust(6,'0')
				code[add] = word
				add += 1

	empty_line = "000000 000000 000000 000000 000000 000000 000000 000000 000000 000000 000000 000000 000000 000000 000000 000000"

	c = 0
	for w in code:
		if (c == 15):
			s += w + "\n"
			c = 0
		else:
			s += w + " "
			c += 1
	last_output = ""

	if (args.verbose):
		for line in s.splitlines():
			if line != empty_line:
				if (last_output == "."):
					print()
					print(line)
					last_output = ""
				else:
					print(line)
					last_output = ""
			else:
				last_output = "."
				print(".", end="")

	f = open(output_file, 'w')
	f.write(s)
	f.close()

def handle_assemble(args):
	log('Assembling', args)
	f = f.open(args.input, 'r')
	input_file = f.read()
	f.close()
	size = args.memory
	output_file = args.output

	assemble(input_file, size, output_file)

reserved = {
	'if' : 'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'println' : 'PRINTLN',
	'print' : 'PRINT'
}

tokens = [
	'NUMBER',
	'VARIABLE_NAME',
	'STRING',
	'COMMENT',
	'ASSIGN',
	'G_THAN',
	'L_THAN',
	'EQUALS',
	'SEMICOLON',
	'O_PAREN',
	'C_PAREN',
	'O_BRACE',
	'C_BRACE',
	'PLUS',
	'MINUS',
	'MULT',
	'DIV',
	'ID'
] + list(reserved.values())

def get_asm_var_name(var_name):
	return '_' + var_name

t_O_PAREN = r'\(';
t_C_PAREN = r'\)';
t_O_BRACE = r'{';
t_C_BRACE = r'}';
t_PLUS = r'\+';
t_MINUS = r'\-';
t_MULT = r'\*';
t_DIV = r'/';
t_SEMICOLON = r';'
t_ASSIGN = r':='
t_G_THAN = r'>='
t_L_THAN = r'<='
t_EQUALS = r'=='

t_ignore = ' \t'

def t_COMMENT(t):
	r'\#.*'
	pass

def t_STRING(t):
	r'\".*\"'
	t.value = t.value[1:-1] # Trim quotations
	r = '(?<!{){[^{}]+}(?!})'
	interp = re.findall(r, t.value)
	interp_map = {}

	for var_name in interp:
		v = get_asm_var_name(var_name[1:-1])
		if (v not in var.keys()):
			raise ValueError(f"Variable {var_name[1:-1]} not declared.")
		interp_map[var_name] = var[v][1]

	def interp_var(match):
		return interp_map[match.group(0)]

	t.value = re.sub(r, interp_var, t.value)
	return t

def t_VARIABLE_NAME(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	if (t.value in reserved.keys()):
		t.type = reserved.get(t.value,'ID')
	else:
		t.value = get_asm_var_name(t.value)
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')    # Check for reserved words
	return t

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_newline(t):
	r'\n'
	t.lexer.lineno += len(t.value)

def t_error(t):
	raise ValueError(f"Illegal character {t.value[0]}")
	t.lexer.skip(1)

def t_eof(t):
	return None

lexer = lex.lex()

mem_add = int('fffb',16)
var = {}
words = ["".join(p) for i in range(1,6) for p in product(al, repeat = i)]
ind = 0

def p_start(p):
	'''start : start statement
		| statement'''
	p[0] = "\n".join(p[1:])

def p_statement(p):
	'''statement : variable_assignment
				| print_cmd
				| println_cmd'''
	p[0] = p[1]

def p_println_string(p):
	'''println_cmd : PRINTLN O_PAREN STRING C_PAREN SEMICOLON'''
	global mem_add
	global var 
	global words
	global ind 
	string = p[3]
	code = "# " + hex(mem_add)[2:] + " " + hex(mem_add - 2)[2:] + "\n"
	mem_add = mem_add - 1 
	code += "# " + hex(mem_add)[2:] + " " + hex(len(string) + 1)[2:] + "\n"
	mem_add = mem_add - 1 
	code += "& " + hex(mem_add)[2:] + " \"" + string + "\"\n"
	code += "# " + hex(mem_add - len(string))[2:] + " a\n"
	code += "ADI " + hex(mem_add + 2)[2:] + "\n"
	code += "LDA _zero\nSTA _counter\n"
	code += "." + words[ind] + "\n"
	code += "AIA 0000\nATO 0000\nARD 0000\nLDA _counter\nADA _one\nSTA _counter\nLT "
	code += hex(mem_add + 1)[2:] + "\n"
	code += "UFR 0000\nBNE ." + words[ind] + "\n"
	ind = ind + 1 
	mem_add = mem_add - len(string) - 1
	p[0] = code	

def p_print_string(p):
	'''print_cmd : PRINT O_PAREN STRING C_PAREN SEMICOLON'''
	global mem_add
	global var
	global words
	global ind
	string = p[3]
	code = "# " + hex(mem_add)[2:] + " " + hex(mem_add - 2)[2:] + "\n"
	mem_add = mem_add - 1
	code += "# " + hex(mem_add)[2:] + " " + hex(len(string))[2:] + "\n"
	mem_add = mem_add - 1
	code += "& " + hex(mem_add)[2:] + " \"" + string + "\"\n"
	code += "ADI " + hex(mem_add + 2)[2:] + "\n"
	code += "LDA _zero\nSTA _counter\n"
	code += "." + words[ind] + "\n"
	code += "AIA 0000\nATO 0000\nARD 0000\nLDA _counter\nADA _one\nSTA _counter\nLT "
	code += hex(mem_add + 1)[2:] + "\n"
	code += "UFR 0000\nBNE ." + words[ind] + "\n"
	ind = ind + 1
	mem_add = mem_add - len(string)
	p[0] = code

def p_operator(p):
	'''operator : PLUS
			| MINUS
			| MULT
			| DIV'''
	p[0] = p[1]

def p_expr_variable(p):
	'''expr : O_PAREN VARIABLE_NAME operator VARIABLE_NAME C_PAREN'''
	try:	
		p[2] = int(var[p[2]][1],16)
		p[4] = int(var[p[4]][1],16)
	except:
		raise ValueError(f"Variables {p[2]} and {p[4]}  must be of type int.")

	if (p[3] == '+'):
		p[0] = p[2] + p[4]
	elif (p[3] == '-'):
		p[0] = p[2] - p[4]
	elif (p[3] == '*'):
		p[0] = p[2] * p[4]
	elif (p[3] == '/'):
		p[0] = p[2] / p[4]

def p_expr_variable_a(p):
	'''expr : O_PAREN VARIABLE_NAME operator NUMBER C_PAREN
			| O_PAREN VARIABLE_NAME operator expr C_PAREN'''
	try:
		p[2] = int(var[p[2]][1],16)
	except:
		raise ValueError(f"Variable {p[2]} must be of type int.")	

	if (p[3] == '+'):
		p[0] = p[2] + p[4]
	elif (p[3] == '-'):
		p[0] = p[2] - p[4]
	elif (p[3] == '*'):
		p[0] = p[2] * p[4]
	elif (p[3] == '/'):
		p[0] = p[2] / p[4]

def p_expr_variable_b(p):
	'''expr : O_PAREN NUMBER operator VARIABLE_NAME C_PAREN
			| O_PAREN expr operator VARIABLE_NAME C_PAREN'''
	try:
		p[4] = int(var[p[4]][1],16)
	except:
		raise ValueError(f"Variable {p[4]} must be of type int.")

	if (p[3] == '+'):
		p[0] = p[2] + p[4]
	elif (p[3] == '-'):
		p[0] = p[2] - p[4]
	elif (p[3] == '*'):
		p[0] = p[2] * p[4]
	elif (p[3] == '/'):
		p[0] = p[2] / p[4]

def p_expr(p):
	'''expr : O_PAREN expr operator expr C_PAREN
			| O_PAREN NUMBER operator expr C_PAREN
			| O_PAREN expr operator NUMBER C_PAREN
			| O_PAREN NUMBER operator NUMBER C_PAREN'''

	if (p[3] == '+'):
		p[0] = p[2] + p[4]
	elif (p[3] == '-'):
		p[0] = p[2] - p[4]
	elif (p[3] == '*'):
		p[0] = p[2] * p[4]
	elif (p[3] == '/'):
		p[0] = p[2] / p[4]
	
def p_variable_assignment_number(p):
	'''variable_assignment : VARIABLE_NAME ASSIGN NUMBER SEMICOLON
						| VARIABLE_NAME ASSIGN expr SEMICOLON'''
	global mem_add
	global var
	if (p[1] in var.keys()):
		raise ValueError(f"Variable {p[1]} has already been declared.\n")
	var[p[1]] = [hex(mem_add)[2:],hex(p[3])[2:][-2:],'int']
	p[0] = '# ' + hex(mem_add)[2:] + ' ' + hex(p[3])[2:][-2:]
	mem_add = mem_add - 1 

def p_variable_assignment_string(p):
	'variable_assignment : VARIABLE_NAME ASSIGN STRING SEMICOLON'
	global mem_add
	global var
	if (p[1] in var.keys()):
		raise ValueError(f"Variable {p[1]} has already been declared.\n")
	var[p[1]] = [hex(mem_add)[2:],p[3],'str']
	p[0] = '& ' + hex(mem_add)[2:] + ' "' + p[3] + '"'
	mem_add = mem_add - len(p[3])

def p_variable_assignment_var(p):
	'variable_assignment : VARIABLE_NAME ASSIGN VARIABLE_NAME SEMICOLON'
	global mem_add
	global var
	if (p[1] in var.keys()):
		raise ValueError(f"Variable {p[1]} has already been declared.\n")
	
	val = var[p[3]][1]
	typ = var[p[3]][2]
	
	if (typ == 'int'):
		var[p[1]] = [hex(mem_add)[2:],val,'int']
		p[0] = '# ' + hex(mem_add)[2:] + ' ' + val
		mem_add = mem_add - 1
	else:
		var[p[1]] = [hex(mem_add)[2:],val,'str']
		p[0] = '& ' + hex(mem_add)[2:] + ' "' + val + '"'
		mem_add = mem_add - len(val)

yacc.yacc(debug=True)

def compile(args):
	log('Compiling', args)
	f = open(args.input, 'r')
	inp = f.read()
	f.close()

	result = yacc.parse(inp)
	log(result, args)

	if (result == None):
		raise ValueError("No result from parser")

	result = ": 0\n_buffer ffff\n_counter fffe\n_zero fffd\n_one fffc\n# _one 1\n" + result + "HLT 0000"
	result = "\n".join([s for s in result.split("\n") if s])

	log(result, args)

	if (args.asm):
		log('Writing assembly to file', args)
		f = open(args.output, 'w')
		f.write(result)
		f.close()
		return
	else:
		assemble(result, args.memory, args.output)

def log(m, args):
	if (args.verbose):
		print(m)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--input', help='Input file')
	parser.add_argument('-o', '--output', help='Output file')
	parser.add_argument('-q', '--assemble', action='store_true', help='Input assembly code')
	parser.add_argument('-a', '--asm', action='store_true', help='Output assembly code')
	parser.add_argument('-m', '--memory', default=65536, help='Size of memory')
	parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

	args = parser.parse_args()

	if (not args.assemble):
		log('Compile mode', args)
		compile(args)
	else:
		log('Assemble mode', args)
		handle_assemble(args)