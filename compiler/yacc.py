import ply.yacc as yacc
from lexer import tokens

mem_add = int('ffff',16)
var = {}

def p_start(p):
	'start : variable_assignment'

def p_variable_assignment_number(p):
	'variable_assignment : VARIABLE_NAME ASSIGN NUMBER ;'
	p[0] = '# ' + hex(mem_add)[2:] + ' ' + hex(p[3])[2:]
	var[p[0]] = hex(mem_add)[2:]
	mem_add = mem_add - 1

def p_variable_assignment_string(p):
	'variable_assignment : VARIABLE_NAME ASSIGN STRING ;'	
	p[0] = '& ' + hex(mem_add) + ' "' + p[3] + '"'
	var[p[0]] = hex(mem_add)[2:]	
	mem_add = mem_add - len(p[3])
