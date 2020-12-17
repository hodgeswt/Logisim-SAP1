import sys
import ply.lex as lex
import ply.yacc as yacc

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

mem_add = int('ffff',16)
var = {}

def p_start(p):
	'''start : start variable_assignment
		| variable_assignment'''
	p[0] = "\n".join(p[1:])

def p_operator(p):
	'''operator : PLUS
			| MINUS
			| MULT
			| DIV'''
	p[0] = p[1]

def p_expr_variable(p):
	'''expr : O_PAREN VARIABLE_NAME operator VARIABLE_NAME C_PAREN'''
	p[2] = int(var[p[2]][1],16)
	p[4] = int(var[p[4]][1],16)
	
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
	p[2] = int(var[p[2]][1],16)
	
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
	p[4] = int(var[p[4]][1],16)
	
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
		raise SyntaxError(f"Variable {p[1]} has already been declared.\n")
	var[p[1]] = [hex(mem_add)[2:],hex(p[3])[2:][-2:],'int']
	p[0] = '# ' + hex(mem_add)[2:] + ' ' + hex(p[3])[2:][-2:]
	mem_add = mem_add - 1 

def p_variable_assignment_string(p):
	'variable_assignment : VARIABLE_NAME ASSIGN STRING SEMICOLON'
	global mem_add
	global var
	if (p[1] in var.keys()):
		raise SyntaxError(f"Variable {p[1]} has already been declared.\n")
	var[p[1]] = [hex(mem_add)[2:],p[3],'str']
	p[0] = '& ' + hex(mem_add)[2:] + ' "' + p[3] + '"'
	mem_add = mem_add - len(p[3])

def p_variable_assignment_var(p):
	'variable_assignment : VARIABLE_NAME ASSIGN VARIABLE_NAME SEMICOLON'
	global mem_add
	global var
	if (p[1] in var.keys()):
		raise SyntaxError(f"Variable {p[1]} has already been declared.\n")
	
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

print(result)
print(var)	
