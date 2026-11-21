# Reglas técnicas

Lo que el juego necesita para que el texto no se rompa. Cada regla tiene un número para citarla, y la mayoría la controla `loc.py check` (el chequeo va entre paréntesis). Salen de cómo está hecho el juego, del adaptador y de la sección 8 del encargo: una traducción nunca puede romper el archivo.

Plantilla del kit: los números quedan; lo de cada regla se completa con lo que muestre la prueba técnica de este juego (PLAN, fase 1). Lo que no aplique se borra.

## Cómo está hecho el juego

Lo que mostró la fase 1 (2026-11-20 y 21). Lo que dice *por confirmar* todavía no se probó en el juego.

- **Imagen:** PAL `SLES_500.51`, sectores de 2048. Archivos: el ejecutable, `ERDATA.BIN` (432 MB, casi todo el juego), `VOICE/VOICEALL.ADX` (voces), los videos `EROPEN.PSS`, `TEXT0.PSS`, `TEXT1.PSS`, `STAFF.PSS` y `CRAVE.PSS`, y `DUMMY.OUT` (1 GB de relleno).
- **Ejecutable:** ELF con un solo segmento cargado en 0x100000 desde el desplazamiento 0x1000 (dirección = desplazamiento + 0xff000). Los textos de menús, opciones, anillos, gemas, memory card y lugares están en ASCII, terminados en `\0`, entre 0x249900 y 0x257600 aproximadamente. Muchos llevan delante un código `_NNN` (`_777Back`, `_883[Mono]`); *por confirmar* qué hace (parece color).
- **`ERDATA.BIN`:** los primeros 0x2900 bytes son un índice de entradas `{sector, sectores}` (u32, sectores de 2048) que cubre solo los primeros 44 MB. Ahí están las descripciones en ASCII: magias (entrada 4), objetos (5) y armas (801 a 809), en renglones de unos 30 caracteres. El resto del archivo (desde 0x2a40000) no está en ese índice: modelos, sonido, mapas y los guiones.
- **Diálogos:** en el guion de cada mapa, en `ERDATA.BIN` (de 0x4c7f6bc a 0x1862d8ec). Es bytecode de palabras u32; un mensaje es `{0x019d << 16 | n}`, `{u32 de parámetros}` y n palabras de carácter: el código ASCII en la palabra (`0x54` = `T`), `0x00040000` = salto de línea. Hay unos 517 mensajes (468 distintos, ~30 000 caracteres), uno por clip de voz (`VOICEALL.ADX` tiene 472). El juego copia el mensaje tal cual a un búfer en 0x34b9e0 (función 0x1be268; los caracteres desde +0x40) y lo dibuja letra por letra con la función 0x179e60, desde una fuente en textura. Hay caracteres especiales con tipo en los 16 bits altos (por ejemplo `0x000108f8` al inicio de un cartel); *por confirmar* qué dibujan.
- **Fuente de los diálogos:** en `ERDATA.BIN` 0x4e8090 (dentro de la entrada 4), sin comprimir: dos paletas de 0x400 bytes, la fuente japonesa de 2 bytes (1260 signos de 24×24 a 8 bits, desde +0x800; el PAL no la usa y del signo 1003 en adelante es relleno) y desde +0xb1b00 los 77 signos de 1 byte (16×24 a 8 bits; se ven las 12 columnas de la izquierda y cada uno avanza 12 px). La función 0x179e60 lee el tipo del carácter en los 16 bits altos (0: letra; 1 y 2: color; 4: salto de línea; 6: centrar). En el tipo 0, si el byte alto de los 16 bits bajos no es 0, dibuja un signo japonés de índice `(alto − 1) × 42 + (bajo − 1)`; si no, busca el índice del signo de 1 byte. En el original esa búsqueda es una cadena de comparaciones (0x17a088–0x17a1c7). `tools/font_es.py` la cambia por una tabla de 256 bytes y pone los signos nuevos con índice negativo, en el relleno que queda justo antes de los de 1 byte (T-5).
- **Guiones (bytecode):** el intérprete es la función 0x1bd638. Tamaño de cada instrucción, en palabras:
  - `0x190 | id` (etiqueta: las entradas del guion se buscan por id, no por posición), `0x191` (fin), `0x194` y `0x195` (abrir y cerrar bloque): 1.
  - `0x197 | desplazamiento`: 1. Es el **único salto por posición**: `pc = pc + 4 + desplazamiento × 4`, con el desplazamiento de 16 bits con signo. Si un mensaje cambia de tamaño entre el salto y su destino, hay que corregirlo.
  - `0x192` (condición; salta al bloque `0x194`…`0x195` que corresponde, sin desplazamiento): 2 + 5 × (byte 1 de la palabra).
  - `0x196 | n` (expresión terminada en `0xff`): 1 + n.
  - `0x19d | n` (mensaje): 2 + n.
  - El resto (comandos, `opcode | n.º de argumentos`): 1 + 2 × argumentos (cada argumento es `{tipo, valor}`).
  Con estas reglas, el guion del mapa del primer pueblo se recorre entero sin perder la sincronía (2201 instrucciones, 87 mensajes y 90 saltos, de 0x135c26c0 a 0x135d4e40).
- **Mapas:** el ejecutable tiene en 0x333640 una tabla de 7556 casillas con el **LBA del disco** de cada mapa (no el sector de `ERDATA.BIN`, que empieza en el LBA 0x6a1). Las casillas vacías valen 0. El mapa del primer pueblo va del LBA 0x2707f al 0x27315 (`ERDATA` 0x134ef000, 1,3 MB). Dentro hay subarchivos con punteros relativos a su propio inicio, que el juego reubica al cargarlos. El del guion empieza en 0x135bf570 y su primera palabra (0x3150) es el desplazamiento del guion. *Por confirmar:* el resto de la cabecera del subarchivo y si el guion puede ir a otro lugar del mapa (por ejemplo, al final) cambiando solo ese desplazamiento.
- **Espacio en el disco:** después de `ERDATA.BIN` (que termina en el LBA 0x34031) no hay ningún archivo hasta `CRAVE.PSS` (LBA 0x6bc53): unos 457 MB libres. `ERDATA.BIN` puede crecer en su lugar; para eso hay que actualizar su tamaño en el directorio de la ISO y la tabla de LBA de los mapas.
- **Voces:** `VOICEALL.ADX` no es ADX de CRI: son 472 bloques `SShd`/`SSbd` alineados a sector, PCM de 16 bits, estéreo, a 48 kHz (uno a 44,1 kHz). Unos 40 minutos.
- **Videos:** `TEXT0.PSS` (1:54) y `TEXT1.PSS` (1:32) son la narración de la introducción y del final, con el texto dibujado en el video (MPEG-2 de 640×448 a 25 fps). Traducirlos obliga a rehacer el video.
- **Restos:** en `ERDATA.BIN` quedan descripciones de objetos en japonés (Shift-JIS) de la versión japonesa, sin usar.

## Códigos y saltos

- **T-1** Los códigos (variables, etiquetas, colores, nombres insertados) quedan intactos y en el mismo orden que en el original. Los reconoce la lista `codes` de `loc.json`. (`codigos`)
  - Completar: qué hace cada código de este juego.
- **T-2** Saltos de línea: los fijos (`fixed_break` en `loc.json`) van exactamente donde están en el original, ni más ni menos. Los demás, si el adaptador parte los renglones, los pone el adaptador. (`saltos`)

## Espacio

- **T-3** La caja: ningún renglón puede pasar del ancho que permite el juego. Si el límite medido es el del original y no el de la pantalla, el aviso no obliga a recortar: se permiten abreviaturas reconocibles, pero nunca se quitan palabras ni se acorta de forma que se pierda el sentido. Si la forma completa no cabe, va completa y con su aviso, y se revisa en el juego. [IVA] (chequeo del proyecto, en `hooks`)
- **T-4** Los textos con largo máximo en bytes (`max` en el lote) no pueden pasarlo: es un límite duro. Completar: cuántos bytes ocupa cada letra en este juego. (`bytes`)

## Caracteres

- **T-5** Solo se usan caracteres que tiene la fuente del juego. (`caracteres`, con el módulo `hooks` que se arma junto con el adaptador)
  - La fuente original de los diálogos tiene `0-9`, `A-Z`, `a-z`, el espacio y `. , ( ) ! ? ' " - : & % [ ] /` (`^` se dibuja igual que `-`). Cualquier otro carácter se salta **sin avanzar**: no da error, la palabra sale pegada.
  - `tools/font_es.py` le agrega **á é í ó ú ü ñ Á É Í Ó Ú Ü Ñ ¿ ¡ « »**, que en el guion se escriben con su código Latin-1 (á = `0xE1`). Probado en PCSX2 el 2026-11-21: se ven todas y avanzan como las demás.
  - No hay `;`, `*`, `+`, `=`, `#`, `<`, `>`, `—`, `…` ni comillas curvas. Las citas van con « » (E-58), los puntos suspensivos con tres puntos y el apóstrofo es `'`. Si hace falta otro signo, se agrega con `font_es.py` (hay casillas de sobra).

## Qué se traduce

- **T-6** Lo que no se traduce ni cuenta (restos sin localizar, textos de prueba) va en `excluded` de `loc.json`. Completar: qué es en este juego.
- **T-7** Solo se traducen los textos que ve el jugador. Los nombres internos (archivos, etiquetas) no se exportan y no se tocan.
- **T-8** Toda línea del lote se traduce completa: ninguna queda vacía, igual al original ni con frases del original mezcladas. (`vacia`, `sin_traducir`, `ingles_mezclado`)
