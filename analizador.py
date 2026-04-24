import sys

# Unidad léxica producida por el analizador y consumida por el parser.
class Token:
    # name: categoría del token. value: atributo (vacío si no aplica). line_number: línea de origen.
    def __init__(self, name, value, line_number):
        self.name = name
        self.value = value
        self.line_number = line_number

    # Formato de salida: <ID | symbolTable[n]>, <NAME, value> o <NAME>.
    def __str__(self):
        if self.name == 'ID':
            return f'<ID | symbolTable[{self.value}]>'
        elif self.value != '':
            return f'<{self.name}, {self.value}>'
        return f'<{self.name}>'

# Tabla de símbolos: asocia cada lexema a un puntero entero único.
class SymbolTable:
    def __init__(self):
        self.table = {}
        self.pointer_counter = 1

    # Retorna el puntero existente si el lexema ya fue registrado, o lo agrega y retorna uno nuevo.
    def get_or_add(self, lexeme):
        for ptr, lex in self.table.items():
            if lex == lexeme:
                return ptr
        ptr = self.pointer_counter
        self.table[ptr] = lexeme
        self.pointer_counter += 1
        return ptr

    # Escribe la tabla de símbolos al archivo de salida, ordenada por puntero.
    def print_symbol_table(self, output_file):
        output_file.write("\n\n=== Tabla de Símbolos ===\n")
        output_file.write(f"{'Puntero':<10} Lexema\n")
        output_file.write("-" * 25 + "\n")
        for ptr in sorted(self.table):
            output_file.write(f"{ptr:<10} {self.table[ptr]}\n")

# Analizador léxico para un subconjunto del lenguaje Pascal.
class LexiAnalyzer:
    # Abre el archivo fuente y carga el primer carácter, las palabras reservadas y los mensajes de error.
    def __init__(self, archivo):
        self.file = open(archivo, 'r')
        self.line_number = 1
        self.current_char = self.file.read(1)
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
            "COMMENT": "Comentario no cerrado. Se esperaba una llave de cierre.",
            "UNRECOGNIZED_CHAR": "Carácter no reconocido.",
            "ASIGN": "Se esperaba un '=' después de ':'.",
            "NUM_ERROR": "Número mal formado. No se permiten letras después de dígitos."
        }

    # Avanza un carácter en el archivo.
    def next_char(self):
        self.current_char = self.file.read(1)

    # Punto de entrada principal: consume caracteres hasta reconocer y retornar el siguiente token.
    def get_next_token(self) -> Token:
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
                    self.recognize_comment()
                    continue

                case c if c.isalpha():
                    return self.recognize_id_or_keyword()

                case c if c.isdigit():
                    return self.recognize_number()

                case ':':
                    self.next_char()
                    if self.current_char != '=':
                        return Token('DOS_PUNTOS', '', self.line_number)
                    self.next_char()
                    return Token('OP_ASIG', '', self.line_number)

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
                    self.next_char()

    # Consume todos los caracteres hasta la llave de cierre '}', descartando el comentario.
    def recognize_comment(self):
        while self.current_char and self.current_char != '}':
            if self.current_char == '\n':
                self.line_number += 1
            self.next_char()

        if self.current_char:
            self.next_char()
        else:
            self.print_error(self.errors["COMMENT"])

    # Reconoce un identificador o palabra reservada; retorna el token correspondiente.
    def recognize_id_or_keyword(self) -> Token:
        lexeme = ""
        while self.current_char and self.current_char.isalnum():
            lexeme += self.current_char
            self.next_char()

        lexeme = lexeme.lower()

        name = self.keywords.get(lexeme, 'ID')
        if name == 'ID':
            return Token(name, self.symbol_table.get_or_add(lexeme), self.line_number)
        return Token(name, '', self.line_number)

    # Reconoce un literal entero; reporta error y retorna None si le siguen letras al número.
    def recognize_number(self) -> Token:
        lexeme = ""
        while self.current_char and self.current_char.isdigit():
            lexeme += self.current_char
            self.next_char()

        if self.current_char and self.current_char.isalpha():
            self.print_error(self.errors["NUM_ERROR"])
            while self.current_char and self.current_char.isalnum():
                self.next_char()
            return self.get_next_token()

        return Token('NUM', lexeme, self.line_number)

    # Imprime un error léxico indicando la línea donde ocurrió.
    def print_error(self, msg):
        print(f"Error Léxico en línea {self.line_number}: {msg}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Faltan argumentos.")
        sys.exit(1)

    input_file = sys.argv[1]
    lex = LexiAnalyzer(input_file)

    with open("resultado_tokens.txt", "w") as output_file:
        token = lex.get_next_token()
        line = token.line_number if token else 1
        while token:
            if token.line_number != line:
                output_file.write("\n")
            output_file.write(str(token) + " ")
            line = token.line_number
            token = lex.get_next_token()
        lex.symbol_table.print_symbol_table(output_file)

    print("\n¡Análisis finalizado! Resultados guardados en 'resultado_tokens.txt'")
