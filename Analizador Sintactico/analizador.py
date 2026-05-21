import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from AnalizadorLexico.analizador import LexiAnalyzer


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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizar el comando: analizador <archivo.pas>")
        sys.exit(1)

    try:
        parser = Parser(sys.argv[1])
        parser.parse()
        print("Análisis sintáctico exitoso")
    except ParserError as e:
        print(e)
        sys.exit(1)
