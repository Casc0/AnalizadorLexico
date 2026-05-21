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
│   ├── pruebas/                 # Archivos .pas de prueba (lexico)
│   ├── Consigna.pdf             # Enunciado TP3
│   ├── Diseño del Analizador Lexico.pdf
│   └── TP3.pdf                  # Informe entregado
│
└── Analizador Sintactico/
    ├── analizador.py            # Implementación del parser
    ├── pruebas/                 # Archivos .pas de prueba (sintactico)
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

## Uso desde código fuente

### Analizador Léxico

Desde el directorio `AnalizadorLexico/`:

```bash
python analizador.py <archivo_fuente.pas>
```

- Los **errores léxicos** se imprimen por consola con el número de línea.
- Los tokens reconocidos y la tabla de símbolos se guardan en `resultado_tokens.txt`.

### Analizador Sintáctico

Desde el directorio `Analizador Sintactico/`:

```bash
python analizador.py <archivo_fuente.pas>
```

El parser invoca internamente al léxico. Resultados:

- Si el programa es sintácticamente correcto: imprime `Análisis sintáctico exitoso` y sale con código 0.
- Si hay un error: imprime `Error sintáctico en línea N: <mensaje>` indicando el token esperado vs. el encontrado, y sale con código 1.

---

## Generar el ejecutable autónomo

Para entregas o ejecución en máquinas sin Python instalado se utiliza **PyInstaller**. El procedimiento es el mismo para ambos analizadores: hay que ejecutarlo desde el directorio del módulo que se quiera empaquetar.

### Paso 1 — Crear y activar un entorno virtual

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### Paso 2 — Instalar PyInstaller

```bash
pip install pyinstaller
```

### Paso 3 — Generar el binario

**Analizador Léxico** (desde `AnalizadorLexico/`):

```bash
pyinstaller --onefile --name analizador analizador.py
```

**Analizador Sintáctico** (desde `Analizador Sintactico/`):

```bash
pyinstaller --onefile --name analizador --add-data "../AnalizadorLexico:AnalizadorLexico" analizador.py
```

> El flag `--add-data` empaqueta el módulo del analizador léxico junto al ejecutable. En Windows reemplazar `:` por `;`:
> ```
> --add-data "../AnalizadorLexico;AnalizadorLexico"
> ```

### Paso 4 — Recuperar el ejecutable

El binario queda en `dist/analizador` (Linux/macOS) o `dist\analizador.exe` (Windows). Copiarlo al directorio actual:

```bash
# Linux / macOS
cp dist/analizador .

# Windows
copy dist\analizador.exe .
```

### Paso 5 — Desactivar el entorno virtual

```bash
deactivate
```

El ejecutable resultante es autónomo: **no requiere Python** ni dependencias en la máquina destino.

---

## Uso del ejecutable

Una vez generado, el ejecutable se invoca directamente con el archivo fuente como único argumento, tal como pide la consigna:

```bash
./analizador archivodeprueba.pas
```

En Windows:

```bash
analizador.exe archivodeprueba.pas
```

---

## Archivos de prueba

### Léxico — `AnalizadorLexico/pruebas/`

| Archivo | Descripción |
|---|---|
| `prueba_correcta.pas` | Programa válido que ejercita todos los tokens |
| `prueba_correcta2.pas` | Segundo programa válido |
| `prueba_error.pas` | Errores léxicos varios |
| `prueba_error2.pas` | Comentario sin cerrar |
| `prueba_error3.pas` | Número mal formado y carácter no reconocido |

### Sintáctico — `Analizador Sintactico/pruebas/`

| Archivo | Descripción |
|---|---|
| `prueba_funciones.pas` | Funciones con y sin parámetros |
| `prueba_procedimientos.pas` | Procedimientos con y sin parámetros |
| `prueba_anidados.pas` | `if`/`else` anidados, `while` con cuerpo compuesto, expresiones lógicas |
| `error_falta_punto_coma.pas` | Falta `;` entre declaraciones |
| `error_falta_then.pas` | Falta `then` en la sentencia `if` |

---

## Autores

- Franco Fabris — franco.fabris@est.fi.uncoma.edu.ar
- Valentina Villarroel — valentina.villarroel@est.fi.uncoma.edu.ar
