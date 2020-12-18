import sys
import ply.lex as lex
import ply.yacc as yacc
from string import ascii_lowercase as al
from itertools import product

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
	return t

def t_VARIABLE_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if (t.value in reserved.keys()):
        t.type = reserved.get(t.value,'ID')
    else:
        t.value = '_' + t.value
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
    print(f"Illegal character {t.value[0]}")
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

filename = sys.argv[1]

f = open(filename, 'r')
inp = f.read()
f.close()

result = yacc.parse(inp)

result = ": 0\n_buffer ffff\n_counter fffe\n_zero fffd\n_one fffc\n# _one 1\n" + result + "HLT 0000"
result = "\n".join([s for s in result.split("\n") if s])

output = sys.argv[2]
f = open(output, 'w')
f.write(result)
f.close()

print(result)
