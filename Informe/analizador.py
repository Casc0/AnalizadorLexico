import sys


# ============================================================
#  ANALIZADOR LÉXICO
# ============================================================

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


# ============================================================
#  ANALIZADOR SINTÁCTICO
# ============================================================

class ParserError(Exception):
    pass


# Analizador sintáctico descendente recursivo predictivo para mini-Pascal.
class Parser:
    def __init__(self, source_file):
        self.lex = LexiAnalyzer(source_file)
        self.lookahead = self.lex.get_next_token()

    # Punto de entrada. Verifica el programa completo y que no queden tokens.
    def parse(self):
        self._statement()
        if self.lookahead is not None:
            self._error("Tokens inesperados después del final del programa")

    # --- Auxiliares ---

    def _peek(self):
        return self.lookahead.name if self.lookahead else None

    def _peek_value(self):
        return self.lookahead.value if self.lookahead else None

    def _line(self):
        return self.lookahead.line_number if self.lookahead else '?'

    def _match(self, expected):
        if self._peek() == expected:
            self.lookahead = self.lex.get_next_token()
        else:
            found = self._peek() or 'EOF'
            self._error(f"Se esperaba '{expected}', se encontró '{found}'")

    def _error(self, msg):
        raise ParserError(f"Error sintáctico en línea {self._line()}: {msg}")

    def _es_inicio_de_factor(self):
        return self._peek() in ('ID', 'NUM', 'TRUE', 'FALSE', 'PAR_ABRE', 'NOT')

    # --- Procedimientos de la gramática ---

    def _statement(self):
        self._match('PROGRAM')
        self._ident()
        self._match('PUNTO_COMA')
        self._bloque()
        self._match('PUNTO')

    def _bloque(self):
        p = self._peek()
        if p == 'VAR':
            self._match('VAR')
            self._sentencia_de_tipos()
            if self._peek() in ('FUNCTION', 'PROCEDURE'):
                self._lista_subprogramas()
            self._cuerpo()
        elif p in ('FUNCTION', 'PROCEDURE'):
            self._lista_subprogramas()
            self._cuerpo()
        elif p == 'BEGIN':
            self._cuerpo()
        else:
            self._error("Se esperaba 'var', 'function', 'procedure' o 'begin'")

    def _sentencia_de_tipos(self):
        self._declaracion_de_var()
        self._match('PUNTO_COMA')
        self._sentencia_de_tipos_prima()

    def _sentencia_de_tipos_prima(self):
        if self._peek() == 'ID':
            self._sentencia_de_tipos()

    def _declaracion_de_var(self):
        self._lista_var()
        self._match('DOS_PUNTOS')
        self._tipo()

    def _lista_var(self):
        self._ident()
        self._lista_var_prima()

    def _lista_var_prima(self):
        if self._peek() == 'COMA':
            self._match('COMA')
            self._lista_var()

    def _tipo(self):
        p = self._peek()
        if p == 'INTEGER':
            self._match('INTEGER')
        elif p == 'BOOLEAN':
            self._match('BOOLEAN')
        else:
            self._error("Se esperaba 'integer' o 'boolean'")

    def _lista_subprogramas(self):
        self._subprograma()
        self._lista_subprogramas_prima()

    def _lista_subprogramas_prima(self):
        if self._peek() == 'PUNTO_COMA':
            self._match('PUNTO_COMA')
            self._lista_subprogramas()

    def _subprograma(self):
        p = self._peek()
        if p == 'FUNCTION':
            self._funcion()
        elif p == 'PROCEDURE':
            self._procedimiento()
        else:
            self._error("Se esperaba 'function' o 'procedure'")

    def _funcion(self):
        self._match('FUNCTION')
        self._ident()
        self._funcion_prima()

    def _funcion_prima(self):
        p = self._peek()
        if p == 'PAR_ABRE':
            self._match('PAR_ABRE')
            self._param_formales()
            self._match('PAR_CIERRA')
            self._match('DOS_PUNTOS')
            self._tipo()
            self._match('PUNTO_COMA')
            self._bloque()
        elif p == 'DOS_PUNTOS':
            self._match('DOS_PUNTOS')
            self._tipo()
            self._match('PUNTO_COMA')
            self._bloque()
        else:
            self._error("Error en declaración de función: se esperaba '(' o ':'")

    def _procedimiento(self):
        self._match('PROCEDURE')
        self._ident()
        self._procedimiento_prima()

    def _procedimiento_prima(self):
        p = self._peek()
        if p == 'PAR_ABRE':
            self._match('PAR_ABRE')
            self._param_formales()
            self._match('PAR_CIERRA')
            self._match('PUNTO_COMA')
            self._bloque()
        elif p == 'PUNTO_COMA':
            self._match('PUNTO_COMA')
            self._bloque()
        else:
            self._error("Error en declaración de procedimiento: se esperaba '(' o ';'")

    def _param_formales(self):
        self._lista_ident()
        self._match('DOS_PUNTOS')
        self._tipo()
        self._param_formales_prima()

    def _param_formales_prima(self):
        if self._peek() == 'PUNTO_COMA':
            self._match('PUNTO_COMA')
            self._param_formales()

    def _lista_ident(self):
        self._ident()
        self._lista_ident_prima()

    def _lista_ident_prima(self):
        if self._peek() == 'COMA':
            self._match('COMA')
            self._lista_ident()

    def _cuerpo(self):
        self._match('BEGIN')
        self._lista_sentencias()
        self._match('END')

    def _lista_sentencias(self):
        self._sentencia()
        self._lista_sentencias_prima()

    def _lista_sentencias_prima(self):
        if self._peek() == 'PUNTO_COMA':
            self._match('PUNTO_COMA')
            self._lista_sentencias()

    def _sentencia(self):
        p = self._peek()
        if p == 'ID':
            self._ident()
            self._sentencia_prima()
        elif p == 'IF':
            self._alternativa()
        elif p == 'WHILE':
            self._repetitiva()
        elif p == 'BEGIN':
            self._cuerpo()
        elif p == 'READ':
            self._lectura()
        elif p == 'WRITE':
            self._escritura()
        else:
            self._error("Sentencia inválida")

    def _sentencia_prima(self):
        p = self._peek()
        if p == 'OP_ASIG':
            self._match('OP_ASIG')
            self._expresion()
        elif p == 'PAR_ABRE':
            self._match('PAR_ABRE')
            self._lista_expresion()
            self._match('PAR_CIERRA')

    def _alternativa(self):
        self._match('IF')
        self._expresion()
        self._match('THEN')
        self._sentencia()
        self._alternativa_prima()

    def _alternativa_prima(self):
        if self._peek() == 'ELSE':
            self._match('ELSE')
            self._sentencia()

    def _repetitiva(self):
        self._match('WHILE')
        self._expresion()
        self._match('DO')
        self._sentencia()

    def _lectura(self):
        self._match('READ')
        self._match('PAR_ABRE')
        self._ident()
        self._match('PAR_CIERRA')

    def _escritura(self):
        self._match('WRITE')
        self._match('PAR_ABRE')
        self._expresion()
        self._match('PAR_CIERRA')

    def _lista_expresion(self):
        self._expresion()
        self._lista_expresion_prima()

    def _lista_expresion_prima(self):
        if self._peek() == 'COMA':
            self._match('COMA')
            self._lista_expresion()

    def _expresion(self):
        self._expresion_simple()
        self._expresion_prima()

    def _expresion_prima(self):
        if self._peek() == 'OP_REL':
            self._relacion()
            self._expresion_simple()

    def _relacion(self):
        if self._peek() == 'OP_REL':
            self._match('OP_REL')
        else:
            self._error("Se esperaba un operador relacional")

    def _expresion_simple(self):
        if self._peek() == 'OP_ARIT' and self._peek_value() in ('ADD', 'SUB'):
            self._signo()
            self._termino()
            self._expresion_simple_prima()
        elif self._es_inicio_de_factor():
            self._termino()
            self._expresion_simple_prima()
        else:
            self._error("Error en expresión simple")

    def _expresion_simple_prima(self):
        if self._peek() == 'OR' or (self._peek() == 'OP_ARIT' and self._peek_value() in ('ADD', 'SUB')):
            self._lista_expresion_simple()
            self._expresion_simple_prima()

    def _lista_expresion_simple(self):
        p = self._peek()
        if p == 'OR':
            self._match('OR')
            self._termino()
        elif p == 'OP_ARIT' and self._peek_value() in ('ADD', 'SUB'):
            self._signo()
            self._termino()
        else:
            self._error("Error en operador de expresión")

    def _signo(self):
        if self._peek() == 'OP_ARIT' and self._peek_value() in ('ADD', 'SUB'):
            self._match('OP_ARIT')
        else:
            self._error("Se esperaba un signo (+ o -)")

    def _termino(self):
        self._factor()
        self._termino_prima()

    def _termino_prima(self):
        if self._peek() == 'AND' or (self._peek() == 'OP_ARIT' and self._peek_value() in ('MUL', 'DIV')):
            self._lista_terminos()

    def _lista_terminos(self):
        self._operacion()
        self._factor()
        self._lista_terminos_prima()

    def _lista_terminos_prima(self):
        if self._peek() == 'AND' or (self._peek() == 'OP_ARIT' and self._peek_value() in ('MUL', 'DIV')):
            self._lista_terminos()

    def _operacion(self):
        p = self._peek()
        if p == 'OP_ARIT' and self._peek_value() in ('MUL', 'DIV'):
            self._match('OP_ARIT')
        elif p == 'AND':
            self._match('AND')
        else:
            self._error("Se esperaba '*', '/' o 'and'")

    def _factor(self):
        p = self._peek()
        if p == 'ID':
            self._ident()
            self._llamada_funcion()
        elif p == 'NUM':
            self._numero()
        elif p == 'TRUE':
            self._match('TRUE')
        elif p == 'FALSE':
            self._match('FALSE')
        elif p == 'PAR_ABRE':
            self._match('PAR_ABRE')
            self._expresion()
            self._match('PAR_CIERRA')
        elif p == 'NOT':
            self._match('NOT')
            self._factor()
        else:
            self._error("Error en factor")

    def _llamada_funcion(self):
        if self._peek() == 'PAR_ABRE':
            self._match('PAR_ABRE')
            self._lista_expresion()
            self._match('PAR_CIERRA')

    def _ident(self):
        self._match('ID')

    def _numero(self):
        self._match('NUM')


# ============================================================
#  PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: analizador <archivo.pas>")
        sys.exit(1)

    try:
        parser = Parser(sys.argv[1])
        parser.parse()
        print("Análisis sintáctico exitoso")
    except ParserError as e:
        print(e)
        sys.exit(1)
