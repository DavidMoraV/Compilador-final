# Proyecto Compilador

Este proyecto es una implementación por etapas de un compilador simple, desarrollado para el curso de **Paradigmas de Programación**. 
El objetivo es ilustrar el funcionamiento interno de un compilador mediante tres etapas progresivas: análisis léxico y sintáctico, reconocimiento 
extendido de estructuras y generación de código en formato ensamblador.

##  Estructura del Proyecto


proyecto_compilador_final_entrega/
 compilador_etapa1/
 
   c1shell.py
   c1.in
   
 compilador_etapa2/
 
   c1shell.py 
    
   c1.in

compilador_etapa3/
  c1shell.py
  
  c1.in
  
  c1.out
  
 samples
 
   sample1.s    
   sample2.s    
   sample3.s
        


## Descripción por Etapas

###  Etapa 1: Análisis Léxico y Sintáctico Clásico

- **Ubicación:** `/compilador_etapa1/`
- **Archivo:** `c1shell.py`
- Reconoce únicamente estructuras básicas de código como nombres, números, operadores `=`, `+`, `*`, etc.
- Si se utiliza un `if`, `^`, `/`, `[` `]` o cadenas de texto, se genera un error sintáctico.


###  Etapa 2: Análisis Léxico y Sintáctico Extendido

- **Ubicación:** `/compilador_etapa2/`
- **Archivo:** `c1shell.py`
- Permite reconocer estructuras más complejas como:
  - Potencia (`^`)
  - División (`/`)
  - Condiciones (`if`, `>`, `<`)
  - Strings (`"texto"`)
  - Bloques delimitados con `[` y `]`
- No genera código ensamblador aún.


###  Etapa 3: Generación de Código Ensamblador

- **Ubicación:** `/compilador_etapa3/`
- **Archivo:** `c1shell.py`
- Genera código ensamblador simulado para arquitectura ARM.
- Soporta:
  - Declaraciones y asignaciones con expresiones (`+`, `-`, `*`)
  - Comparaciones con `>`, `<`
  - Sentencias condicionales `if [...]`
  - Impresión de cadenas con `print("mensaje")`
- La salida se divide en una sección `.text` (código) y `.data` (strings), tal como se muestra en los archivos de ejemplo.



##  Cómo Ejecutar

### Etapa 1
```bash
cd "E:\...\proyecto_compilador\compilador_etapa1"
python c1shell.py c1.in c1.out
```

### Etapa 2
```bash
cd "E:\...\proyecto_compilador\compilador_etapa2"
python c1shell.py c1.in c1.out
```

### Etapa 3
```bash
cd "E:\...\proyecto_compilador\compilador_etapa3"
python c1shell.py c1.in c1.out
```

> El archivo `c1.out` contiene el resultado del análisis o código generado, según la etapa.

---

##  Notas Finales

- Los archivos `sample1.s`, `sample2.s`, `sample3.s` en la etapa 3 sirven como referencia de formato para comparar la salida del compilador.
- Se recomienda probar distintos ejemplos en `c1.in` para observar el funcionamiento progresivo de cada etapa del compilador.
- Este proyecto demuestra la evolución desde el análisis hasta la generación de código de una manera modular y extensible.

