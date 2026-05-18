# Compilador Mini-Pascal

**Diseño de Compiladores e Intérpretes — Grupo 5**
Universidad Nacional del Comahue — Facultad de Informática

---

## Descripción

Proyecto integral de construcción de un compilador para un subconjunto del lenguaje Pascal (**mini-Pascal**). El desarrollo se divide en etapas, cada una correspondiente a un trabajo de laboratorio de la cátedra:

| Etapa | Módulo | Trabajo |
|---|---|---|
| 1 | [Analizador Léxico](AnalizadorLexico/) | TP N°3 |
| 2 | [Analizador Sintáctico](Analizador%20Sintactico/) | TP N°5 |

El **analizador léxico** lee el archivo fuente y lo transforma en una secuencia de tokens, generando además la tabla de símbolos. El **analizador sintáctico** consume esos tokens y verifica que cumplan con la gramática del lenguaje, implementado como un analizador descendente recursivo predictivo.

---

## Estructura del repositorio

```
Compiladores/
├── AnalizadorLexico/
│   ├── analizador.py            # Implementación del scanner
│   ├── pruebas/                 # Archivos .pas de prueba
│   ├── Consigna.pdf             # Enunciado TP3
│   ├── Diseño del Analizador Lexico.pdf
│   └── TP3.pdf                  # Informe entregado
│
└── Analizador Sintactico/
    ├── analizador.py            # Implementación del parser
    ├── Consigna.pdf             # Enunciado TP5
    ├── Diseño del Analizador Sintactico.pdf
    └── Base Teorica.pdf
```

---

## Requisitos

- **Python 3.10 o superior** (por el uso de `match`/`case` en el léxico)
- **PyInstaller** (solo si se desea generar un ejecutable autónomo)

Verificar la versión de Python:
```bash
python --version
```

---

## Uso

### Analizador Léxico (autónomo)

Desde el directorio `AnalizadorLexico/`:

```bash
python analizador.py <archivo_fuente.pas>
```

- Los **errores léxicos** se imprimen por consola con el número de línea.
- Los tokens reconocidos y la tabla de símbolos se guardan en `resultado_tokens.txt`.

### Analizador Sintáctico

El analizador sintáctico importa al léxico como módulo. Debe ejecutarse desde el directorio raíz `Compiladores/` usando la opción `-m`:

```bash
python -m "Analizador Sintactico.analizador" <archivo_fuente.pas>
```

Si la sintaxis es correcta, el análisis finaliza sin errores. En caso contrario se reporta el error y la línea donde ocurrió.

---

## Generar ejecutable autónomo

Para entregas o ejecución en máquinas sin Python instalado:

```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows

# Instalar PyInstaller
pip install pyinstaller

# Generar el binario
pyinstaller --onefile --name analizador analizador.py

deactivate
```

El binario quedará en `dist/analizador` (o `dist\analizador.exe` en Windows).

---

## Archivos de prueba

Dentro de [AnalizadorLexico/pruebas/](AnalizadorLexico/pruebas/):

| Archivo | Descripción |
|---|---|
| `prueba_correcta.pas` | Programa válido que ejercita todos los tokens |
| `prueba_correcta2.pas` | Segundo programa válido |
| `prueba_error.pas` | Errores léxicos varios |
| `prueba_error2.pas` | Comentario sin cerrar |
| `prueba_error3.pas` | Número mal formado y carácter no reconocido |

---

## Autores

- Franco Fabris — franco.fabris@est.fi.uncoma.edu.ar
- Valentina Villarroel — valentina.villarroel@est.fi.uncoma.edu.ar
