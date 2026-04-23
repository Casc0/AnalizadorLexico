class Token:
    """Token que le enviaremos al Parser."""
    def __init__(self, name,  value, line_number):
        self.name = name
        self.value = value
        self.line_number = line_number

class SymbolTable:
	def __init__(self):
		self.table = {}
        self.pointer_counter = 1

    def get_or_add(self, lexeme):
        # Retorna un "puntero" simulado (un entero) a la tabla de símbolos
        if lexeme not in self.table:
            self.table[lexeme] = self.pointer_counter
            self.pointer_counter += 1
        return self.table[lexeme]

class AnalizadorLexico:
    def __init__(self, archivo):
        self.file = open(archivo, 'r')
        self.line_number = 1
        self.char_actual = self.file.read(1) # Leemos el primer carácter al arrancar
		self.symbol_table = SymbolTable()

		self.keywords = {
            "program": 'PROGRAM', "var": 'VAR', "integer": 'INTEGER',
            "boolean": 'BOOLEAN', "function": 'FUNCTION', "procedure": 'PROCEDURE',
            "begin": 'BEGIN', "end": 'END', "if": 'IF', "then": 'THEN',
            "else": 'ELSE', "while": 'WHILE', "do": 'DO', "read": 'READ',
            "write": 'WRITE', "true": 'TRUE', "false": 'FALSE',
            "or": 'OR', "and": 'AND', "not": 'NOT'
        }
		
		self.errors = {
			"COMMENT" : "Comentario no cerrado. Se esperaba una llave de cierre.",
			"UNRECOGNIZED_CHAR" : "Carácter no reconocido.",
			"ASIGN" : "Se esperaba un '=' después de ':'.",
			"NUM_ERROR" : "Número mal formado. No se permiten letras después de dígitos."
		}

	def next_char(self):
        """Avanza un carácter en el archivo."""
        self.current_char = self.file.read(1)
	
	def get_next_token(self):
		while self.current_char:
			match self.current_char:
				case ' ' | '\t':
                    self.next_char()
                    continue

				case '\n':
                    self.line_number += 1
                    self.next_char()
                    continue

				case '{':
                    self.next_char()
					token = self.recognize_comment()
					if token:
						return token
					continue 
                
				case c if c.isalpha():
                    return self.recognize_id_or_keyword()

				case c if c.isdigit():
                	return self.recognize_number()
				
				case ':':
                    self.next_char()
                    if self.current_char == '=':
                        self.next_char()
                        return Token('OP_ASIG', ':=', self.line_number)
                    print_error(self.errors["ASIGN"])

				case '<':
                    self.next_char()
                    if self.current_char == '>':
                        self.next_char()
                        return Token('OP_REL', 'NE', self.line_number)
                    elif self.current_char == '=':
                        self.next_char()
                        return Token('OP_REL', 'LE', self.line_number)
                    return Token('OP_REL', 'LT', self.line_number)

                case '>':
                    self.next_char()
                    if self.current_char == '=':
                        self.next_char()
                        return Token('OP_REL', 'GE', self.line_number)
                    return Token('OP_REL', 'GT', self.line_number)

				case '=':
                    self.next_char()
                    return Token('OP_REL', 'EQ', self.line_number)

				case '+':
                    self.next_char()
                    return Token('OP_ARIT', 'ADD', self.line_number)

                case '-':
                    self.next_char()
                    return Token('OP_ARIT', 'SUB', self.line_number)

                case '*':
                    self.next_char()
                    return Token('OP_ARIT', 'MUL', self.line_number)

				case '/':
                    self.next_char()
                    return Token('OP_ARIT', 'DIV', self.line_number)

				case '(':
                    self.next_char()
                    return Token('PAR_ABRE', '', self.line_number)

                case ')':
                    self.next_char()
                    return Token('PAR_CIERRA', '', self.line_number)

                case ',':
                    self.next_char()
                    return Token('COMA', '', self.line_number)

                case '.':
                    self.next_char()
                    return Token('PUNTO', '', self.line_number)

                case ';':
                    self.next_char()
                    return Token('PUNTO_COMA', '', self.line_number)

				case _:
                    self.print_error(self.errors["UNRECOGNIZED_CHAR"])
                    self.next_char() # Avanzar para no generar un bucle infinito
				
	def recognize_comment(self):
		while self.current_char and self.current_char != '}':
            if self.current_char == '\n':
                self.line_number += 1
            self.next_char()
						
		if self.current_char == '}':
            self.next_char()
            return 1
        else:
            self.print_error(self.errors["COMMENT"])
            return 0


	def recognize_id_or_keyword(self) -> int:
		lexeme = ""
		while self.current_char and self.current_char.isalnum():
            lexeme += self.current_char
            self.next_char()

		lexeme = lexeme.lower()

		name = self.keywords.get(lexeme, 'ID')
		if name == 'ID':
			return Token(name, self.symbol_table.get_or_add(lexeme), self.line_number)
		else:
			return Token(name, "", self.line_number)
			

	def recognize_number(self) -> int:
		lexema = ""
        while self.current_char and self.current_char.isdigit():
            lexema += self.current_char
            self.next_char()

		if self.current_char and self.current_char.isalpha():
			self.print_error(self.errors["NUM_ERROR"])
        return Token('NUM', lexema, self.line_number)

	def print_error(self, msg):
        print(f"Error Léxico en línea {self.line_number}: {msg}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Faltan argumentos.")
        sys.exit(1)
        
    input_file = sys.argv[1]
    lex = LexicAnalyzer(input_file)
    
    with open("resultado_tokens.txt", "w") as output_file:
        token = lex.get_next_token()
        while token:
            if token.name != "ERROR":
                # Escribimos en el archivo y también imprimimos en consola
                output_file.write(str(token) + "\n")
            token = lex.get_next_token()
            
    print("\n¡Análisis finalizado! Resultados guardados en 'resultado_tokens.txt'")

			

    






