from unittest import case


FILE = "input.txt"
global line_number
line_number = 1

def main() -> None:
	with open(FILE, 'r') as file:
		valid = True
		while valid:
			char = file.read(1)
			valid = recognize_lexeme(char, file) == 0

			
	
def recognize_lexeme(char: str, file) -> int:
	token = tokens.get(char)
	
	match token:
		case "ID":
			error = caseID(char, file)
		case "NUM":
			error = caseNUM(char, file)
		case "LLAVE_ABRE":
			error = comentario(file)
		case "IGNORE": #ignore whitespace
			return 0
		case "LINE_BREAK":
			line_number += 1
			return 0
	return error


def comentario(file) -> int:
	#hacer error!!!!
	while True:
		char = file.read(1)
		token = tokens.get(char) 
		if char == 'LLAVE_CIERRA':
			return 0
		case "ID":
			continue
		case "LINE_BREAK":
			line_number += 1
			return 0	
		case _:
			continue
			
def caseID(file) -> int:
	#hacer error!!!!
	while True:
		char = file.read(1)
		token = tokens.get(char)
		match token:
			case "ID":
				continue
			case "NUM":
				continue
			case "IGNORE":
				return 0
			case "LINE_BREAK":
				line_number += 1
				return 0
			case _:
				return error("ID_ERROR")
			
def caseNUM(file) -> int:
	#hacer error!!!!
	while True:
		char = file.read(1)
		token = tokens.get(char)
		match token:
			case "NUM":
				continue
			case _:
				return error("NUM_ERROR")
            
def error(er: str) -> int:
	print("Error in line " + str(line_number) + ": " + errors.get(er))
	return 1

tokens ={
	"(" : 'PAR_ABRE',
    ")" : 'PAR_CIERRA',
    "," : 'COMA',
    "." : 'PUNTO',
    ";" : 'PUNTO_COMA',
    ":" : 'DOS_PUNTOS',
	"{" : 'LLAVE_ABRE',
	"}" : 'LLAVE_CIERRA',
	"+" : 'OP_ARIT_ADD',
	"-" : 'OP_ARIT_SUB',
	"*" : 'OP_ARIT_MUL',
	"/" : 'OP_ARIT_DIV',
	"=" : 'OP_REL_EQUAL',
	"<>" : 'OP_REL_NOT_EQUAL',
	"<" : 'OP_REL_LTT',
	">" : 'OP_REL_GTT',
	"<=" : 'OP_REL_LTE',
	">=" : 'OP_REL_GTE',
	" " : 'IGNORE',
	"\t" : 'IGNORE',
	"\n" : 'LINE_BREAK'
}

keyword = {
	"program" : 'PROGRAM',
	"var" : 'VAR',
	"integer" : 'INTEGER',
	"boolean" : 'BOOLEAN',
	"function" : 'FUNCTION',
	"procedure" : 'PROCEDURE',
	"begin" : 'BEGIN',
	"end" : 'END',
	"if" : 'IF',
	"then" : 'THEN',
    "else" : 'ELSE',
	"while" : 'WHILE',
	"do" : 'DO',
	"read" : 'READ',
	"write" : 'WRITE',
	"true" : 'TRUE',
	"false" : 'FALSE',
	"or" : 'OR',
	"and" : 'AND',
	"not" : 'NOT'
}

letter = {
	"A" : 'A',
	"B" : 'B',
	"C" : 'C',
	"D" : 'D',
	"E" : 'E',
	"F" : 'F',
	"G" : 'G',
	"H" : 'H',
	"I" : 'I',
	"J" : 'J',
	"K" : 'K',
	"L" : 'L',
	"M" : 'M',
	"N" : 'N',
	"O" : 'O',
	"P" : 'P',
	"Q" : 'Q',
	"R" : 'R',
	"S" : 'S',
	"T" : 'T',
	"U" : 'U',
	"V" : 'V',
	"W" : 'W',
	"X" : 'X',
	"Y" : 'Y',
	"Z" : 'Z',
	"a" : 'a',
	"b" : 'b',
	"c" : 'c',
	"d" : 'd',
	"e" : 'e',
	"f" : 'f',
	"g" : 'g',
	"h" : 'h',
	"i" : 'i',
	"j" : 'j',
	"k" : 'k',
	"l" : 'l',
	"m" : 'm',
	"n" : 'n',
	"o" : 'o',
	"p" : 'p',
	"q" : 'q',
	"r" : 'r',
	"s" : 's',
	"t" : 't',
	"u" : 'u',
	"v" : 'v',
	"w" : 'w',
	"x" : 'x',
	"y" : 'y',
	"z" : 'z'
}

digit = {
	"0" : '0',
	"1" : '1',
	"2" : '2',
	"3" : '3',
	"4" : '4',
	"5" : '5',
	"6" : '6',
	"7" : '7',
	"8" : '8',
	"9" : '9'
}

tokens.update({letter: 'ID' for letter in letter})
tokens.update({digit: 'NUM' for digit in digit})

errors = {
	"ID_ERROR" : "Lexema no reconocido. Se esperaba un ID o un NUM.",
	"NUM_ERROR" : "Lexema no reconocido. Se esperaba un NUM."
}




