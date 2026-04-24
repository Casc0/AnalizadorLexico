# Analizador Léxico — Mini-Pascal

**Trabajo de Laboratorio N°3 — Diseño de Compiladores e Intérpretes**
Universidad Nacional del Comahue — Facultad de Informática — Grupo 5

---

## Descripción

Este proyecto implementa un **analizador léxico** para un subconjunto del lenguaje Pascal (mini-Pascal). El analizador lee un archivo fuente, reconoce sus tokens y produce una secuencia de componentes léxicos en un archivo de salida, junto con la tabla de símbolos generada.

Los tokens reconocidos incluyen: palabras reservadas (`program`, `var`, `begin`, `end`, `if`, `while`, etc.), identificadores, números enteros, operadores relacionales y aritméticos, operador de asignación, y símbolos de puntuación. Los comentarios entre llaves `{ }` y los espacios en blanco son descartados.

Los errores léxicos (carácter no reconocido, comentario no cerrado, número mal formado) se reportan por consola indicando la línea exacta donde ocurrieron, y el análisis continúa con el resto del archivo.

---

## Requisitos

- **Python 3.10 o superior** (por el uso de `match`/`case`)
- **PyInstaller** (solo para generar el ejecutable)

Verificar la versión de Python:
```bash
python3 --version
```

---

## Generar el ejecutable

Dado que el sistema puede tener Python administrado externamente (Ubuntu/Debian), se recomienda usar un entorno virtual:

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activarlo
source venv/bin/activate

# Instalar PyInstaller
pip install pyinstaller

# Generar el ejecutable
pyinstaller --onefile --name analizador analizador.py

# Desactivar el entorno virtual
deactivate
```

El binario resultante estará en `dist/analizador`. Copiarlo al directorio del proyecto:

```bash
cp dist/analizador .
```

A partir de ahí, el ejecutable es completamente autónomo y no requiere Python instalado.

---

## Uso

```bash
./analizador <archivo_fuente>
```

Ejemplo:

```bash
./analizador prueba_correcta.pas
```

- Los **errores léxicos** se imprimen por consola con el número de línea.
- El resultado del análisis se guarda en `resultado_tokens.txt` en el directorio actual, incluyendo los tokens reconocidos y la tabla de símbolos al final.

---

## Archivos de prueba

Se incluyen tres archivos de ejemplo:

| Archivo | Descripción |
|---|---|
| `prueba_correcta.pas` | Programa válido que ejercita todos los tokens disponibles |
| `prueba_error1.pas` | Contiene un comentario sin cerrar (`COMMENT`) |
| `prueba_error2.pas` | Contiene un número mal formado (`NUM_ERROR`) y un carácter no reconocido (`UNRECOGNIZED_CHAR`) |

### Ejecutar las pruebas

```bash
./analizador prueba_correcta.pas
cat resultado_tokens.txt

./analizador prueba_error1.pas

./analizador prueba_error2.pas
```

---

## Autores

- Franco Fabris — FAI-3206 — franco.fabris@est.fi.uncoma.edu.ar
- Valentina Villarroel — FAI-3944 — valentina.villarroel@est.fi.uncoma.edu.ar
