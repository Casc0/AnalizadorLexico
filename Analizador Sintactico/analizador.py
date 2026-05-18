import sys

from ..AnalizadorLexico.analizador import LexiAnalyzer

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
