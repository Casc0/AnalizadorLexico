class Token:
    """Una clase simple para representar el Token que le enviaremos al Parser."""
    def __init__(self, tipo, lexema, linea):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea

    def __repr__(self):
        return f"<Token {self.tipo}: '{self.lexema}' (Línea {self.linea})>"

class AnalizadorLexico:
    def __init__(self, archivo):
        self.file = open(archivo, 'r')
        self.line_number = 1
        self.char_actual = self.file.read(1) # Leemos el primer carácter al arrancar
        
        # Guardamos tus diccionarios como atributos de la clase
        self.keywords = {
            "program": "PROGRAM", "var": "VAR", "integer": "INTEGER", 
            "begin": "BEGIN", "end": "END", "if": "IF", "then": "THEN"
            # ... agrega el resto de tus keywords aquí
        }

    def avanzar(self):
        """Avanza un carácter en el archivo."""
        self.char_actual = self.file.read(1)

    def get_next_token(self):
        """Devuelve el siguiente Token encontrado en el archivo."""
        while self.char_actual: # Mientras no sea fin de archivo (cadena vacía '')

            # 1. Ignorar espacios y saltos de línea
            if self.char_actual in [' ', '\t', '\r']:
                self.avanzar()
                continue
            
            if self.char_actual == '\n':
                self.line_number += 1
                self.avanzar()
                continue

            # 2. Identificadores y Palabras Reservadas (Letras seguidas de letras/números)
            if self.char_actual.isalpha():
                return self._reconocer_id_o_keyword()

            # 3. Números
            if self.char_actual.isdigit():
                return self._reconocer_numero()

            # 4. Operadores de un solo carácter o Puntuación
            if self.char_actual == ';':
                token = Token('PUNTO_COMA', ';', self.line_number)
                self.avanzar()
                return token

            # 5. Operadores compuestos (Ejemplo: :=, <, <=, <>)
            if self.char_actual == '<':
                self.avanzar() # Consumimos el '<'
                if self.char_actual == '=':
                    token = Token('OP_REL_LTE', '<=', self.line_number)
                    self.avanzar() # Consumimos el '='
                    return token
                elif self.char_actual == '>':
                    token = Token('OP_REL_NOT_EQUAL', '<>', self.line_number)
                    self.avanzar() # Consumimos el '>'
                    return token
                else:
                    # ¡AQUÍ ESTÁ LA MAGIA!
                    # No avanzamos. El carácter actual no era ni '=' ni '>', 
                    # así que lo dejamos intacto en self.char_actual para la próxima vuelta.
                    return Token('OP_REL_LTT', '<', self.line_number)

            # Si llegamos aquí, es un carácter que no reconocemos
            print(f"Error Léxico en línea {self.line_number}: Carácter inesperado '{self.char_actual}'")
            self.avanzar() # Avanzamos para no quedarnos en un bucle infinito

        # Si el while termina, llegamos al fin del archivo
        return Token('EOF', '', self.line_number)

    # --- Funciones Auxiliares (Tus antiguos caseID y caseNUM) ---

    def _reconocer_id_o_keyword(self):
        lexema = ""
        # Mientras sea alfanumérico (letra o número)
        while self.char_actual and self.char_actual.isalnum():
            lexema += self.char_actual
            self.avanzar()
        
        # Cuando el while termina, self.char_actual contiene el primer carácter 
        # que NO es letra/número (ej. un punto y coma). Se queda ahí guardado.

        # Verificamos si es palabra reservada (ignorando mayúsculas/minúsculas)
        tipo = self.keywords.get(lexema.lower(), 'ID')
        return Token(tipo, lexema, self.line_number)

    def _reconocer_numero(self):
        lexema = ""
        while self.char_actual and self.char_actual.isdigit():
            lexema += self.char_actual
            self.avanzar()
        
        return Token('NUM', lexema, self.line_number)

# --- Cómo usarlo ---
if __name__ == "__main__":
    # Asegúrate de tener un archivo "input.txt" con código de prueba
    try:
        lexer = AnalizadorLexico("input.txt")
        token_actual = lexer.get_next_token()
        
        while token_actual.tipo != 'EOF':
            print(token_actual)
            token_actual = lexer.get_next_token()
            
    except FileNotFoundError:
        print("Crea un archivo 'input.txt' para probar.")