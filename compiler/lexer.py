import ply.lex as lex
from ply.lex import TOKEN

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
	'ID'
] + list(reserved.values())

literals = ['+','-','*','/','{','}','(',')',';']

t_STRING = r'\".*\"'
t_ASSIGN = r':='
t_G_THAN = r'>='
t_L_THAN = r'<='
t_EQUALS = r'=='

t_ignore = ' \t'

def t_COMMENT(t):
	r'\#.*'
	pass

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
	t.value = hex(int(t.value))[2:]
	return t

def t_newline(t):
	r'\n'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print(f"Illegal character {t.value[0]}")
	t.lexer.skip(1)

