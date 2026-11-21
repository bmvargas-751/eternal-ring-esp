# Reglas técnicas

Lo que el juego necesita para que el texto no se rompa. Cada regla tiene un número para citarla, y la mayoría la controla `loc.py check` (el chequeo va entre paréntesis). Salen de cómo está hecho el juego, del adaptador y de la sección 8 del encargo: una traducción nunca puede romper el archivo.

Plantilla del kit: los números quedan; lo de cada regla se completa con lo que muestre la prueba técnica de este juego (PLAN, fase 1). Lo que no aplique se borra.

## Cómo está hecho el juego

Lo que mostró la fase 1 (2026-11-20 y 21). Lo que dice *por confirmar* todavía no se probó en el juego.

- **Imagen:** PAL `SLES_500.51`, sectores de 2048. Archivos: el ejecutable, `ERDATA.BIN` (432 MB, casi todo el juego), `VOICE/VOICEALL.ADX` (voces), los videos `EROPEN.PSS`, `TEXT0.PSS`, `TEXT1.PSS`, `STAFF.PSS` y `CRAVE.PSS`, y `DUMMY.OUT` (1 GB de relleno).
- **Ejecutable:** ELF con un solo segmento cargado en 0x100000 desde el desplazamiento 0x1000 (dirección = desplazamiento + 0xff000). Los textos de menús, opciones, anillos, gemas, memory card y lugares están en ASCII, terminados en `\0`, entre 0x249900 y 0x257600 aproximadamente. Muchos llevan delante un código `_NNN` (`_777Back`, `_883[Mono]`): es el color (R, G y B, un dígito cada uno).
- **`ERDATA.BIN`:** los primeros 0x2900 bytes son un índice de entradas `{sector, sectores}` (u32, sectores de 2048) que cubre solo los primeros 44 MB. Ahí están las descripciones en ASCII: magias (entrada 4), objetos (5) y armas (801 a 809), en renglones de unos 30 caracteres. Los objetos son registros de 0x80 bytes, con el nombre en +0x14 (hasta 0x14 bytes con el `\0`) y la descripción en +0x28 (hasta 0x58 bytes con el `\0`), con `\r\n` entre renglones. El resto del archivo (desde 0x2a40000) no está en ese índice: modelos, sonido, mapas y los guiones.
- **Diálogos:** en el guion de cada mapa, en `ERDATA.BIN` (de 0x4c7f6bc a 0x1862d8ec). Es bytecode de palabras u32; un mensaje es `{0x019d << 16 | n}`, `{u32 de parámetros}` y n palabras de carácter: el código ASCII en la palabra (`0x54` = `T`), `0x00040000` = salto de línea. Hay unos 517 mensajes (468 distintos, ~30 000 caracteres), uno por clip de voz (`VOICEALL.ADX` tiene 472). El juego copia el mensaje tal cual a un búfer en 0x34b9e0 (función 0x1be268; los caracteres desde +0x40) y lo dibuja letra por letra con la función 0x179e60, desde una fuente en textura. Hay caracteres especiales con tipo en los 16 bits altos (por ejemplo `0x000108f8` al inicio de un cartel); *por confirmar* qué dibujan.
- **Fuente:** en `ERDATA.BIN` 0x4e8090 (dentro de la entrada 4), sin comprimir: dos paletas de 0x400 bytes, la fuente japonesa de 2 bytes (1260 signos de 24×24 a 8 bits, desde +0x800; el PAL no la usa y del signo 1003 en adelante es relleno) y desde +0xb1b00 los 77 signos de 1 byte (16×24 a 8 bits; se ven las 12 columnas de la izquierda y cada uno avanza 12 px). En +0x106200 hay una fuente chica para el «modo angosto» de la función 0x177b20: celdas de 16×16 a 8 bits guardadas de abajo hacia arriba, con dos signos de 8 columnas (se ven 7); el signo de índice i está en la celda i ÷ 2 (izquierda si es par). Antes, desde +0xba000, está la fuente japonesa chica, sin uso y con relleno al final. La usan tres funciones, cada una con la misma cadena de comparaciones (carácter → índice del signo):
  - 0x179e60, diálogos (palabras de 32 bits). Tipo del carácter en los 16 bits altos (0: letra; 1 y 2: color; 4: salto de línea; 6: centrar). En el tipo 0, si el byte alto de los 16 bits bajos no es 0, dibuja un signo japonés de índice `(alto − 1) × 42 + (bajo − 1)`. Cadena en 0x17a088–0x17a1c7.
  - 0x177b20 y 0x1782f0, cadenas de bytes terminadas en `\0` (menús, descripciones). Un byte ≥ 0x80 se toma como primer byte de un carácter Shift-JIS (0x177be8 y 0x1783b0). Códigos de control: `0x01`, `0x02` (modo angosto: fuente chica, avance de 8; lo usa al menos la ficha de objetos, con el título y la descripción), `0x0a` (salto de línea), `_RGB` (color) y `@N`; `\r` y cualquier otro carácter que no esté en la fuente se saltan sin avanzar. Cadenas en 0x177d24–0x177e7f y 0x1784e4–0x17863f.
  `tools/font_es.py` agrega 34 signos (T-5) con índice negativo, en el relleno que queda justo antes de los de 1 byte; cambia las tres cadenas por una búsqueda en una tabla de 256 bytes (en 0x17a0c0) y apaga el desvío a Shift-JIS, que el texto PAL no usa. Con eso, el juego entero usa **Windows-1252**, un carácter por palabra o por byte. También agrega las versiones chicas, en el relleno que queda antes de la fuente chica, y cambia en 0x177f8c el redondeo de i ÷ 2 (hacia cero) por el piso, para que los índices negativos caigan ahí (con el redondeo original, á = −1 dibujaba un «1»).
- **Guiones (bytecode):** el intérprete es la función 0x1bd638. Tamaño de cada instrucción, en palabras:
  - `0x190 | id` (etiqueta: las entradas del guion se buscan por id, no por posición), `0x191` (fin), `0x194` y `0x195` (abrir y cerrar bloque): 1.
  - `0x197 | desplazamiento`: 1. Es el **único salto por posición**: `pc = pc + 4 + desplazamiento × 4`, con el desplazamiento de 16 bits con signo. Si un mensaje cambia de tamaño entre el salto y su destino, hay que corregirlo.
  - `0x192` (condición; salta al bloque `0x194`…`0x195` que corresponde, sin desplazamiento): 2 + 5 × (byte 1 de la palabra).
  - `0x196 | n` (expresión terminada en `0xff`): 1 + n.
  - `0x19d | n` (mensaje): 2 + n.
  - El resto (comandos, `opcode | n.º de argumentos`): 1 + 2 × argumentos (cada argumento es `{tipo, valor}`).
  Con estas reglas cada guion se recorre entero sin perder la sincronía y `tools/stage.py` lo rearma byte por byte igual.
- **Escenarios:** `ERDATA.BIN` 0x3d40 tiene una tabla de 16 escenarios `{sector, sectores}`; el LBA del disco es 0x6a1 + 0x10 + sector, y el escenario se carga entero en RAM 0x55ca80 (el más grande, el 13, mide 0xea79a0). Van uno detrás de otro, sin espacio entre ellos. Cabecera: +0 tamaño total, +4 tamaño del guion, +8 y +0xc en 0 (sin uso), y en 0x138–0x154 ocho desplazamientos a secciones que el juego convierte en punteros. El guion no tiene desplazamiento propio: el juego (0x117xxx) recorre las secciones en orden, el guion es la que sigue a la de objetos, y la siguiente empieza en guion + tamaño; el puntero queda en `*(gp−0x5328) + 0x14` y de ahí en `gp−0x4620`. Solo los escenarios 10 a 15 tienen guion con mensajes (10, el primer pueblo: 97 mensajes; 11: 6; 13: 14; 15: 1), o sea 118 de los ~517: el resto está en otros guiones que todavía no se ubicaron (*por ver*: probablemente los de la tabla de 0x333640).
  Para que un guion crezca, `tools/stage.py` pone el guion nuevo al final del escenario, su desplazamiento en +8 y su tamaño en +0xc, y deja el viejo y +4 sin tocar (así nada se mueve). Un parche en 0x1175fc (código en 0x178620) hace que el juego use cabecera + [+8] cuando no es 0. El escenario entero va al final de `ERDATA.BIN`, con su fila de la tabla y el tamaño de `ERDATA.BIN` en el directorio de la ISO al día. *Por confirmar en el juego* (prueba 3).
- **Tabla de 0x333640:** 7556 casillas (157 no vacías) con LBA del disco. *Por ver* qué carga: no son los escenarios (el del pueblo, LBA 0x25e11, no está; sus casillas caen dentro de él).
- **Espacio en el disco:** después de `ERDATA.BIN` (que termina en el LBA 0x34031) no hay ningún archivo hasta `CRAVE.PSS` (LBA 0x6bc53): unos 457 MB libres. `ERDATA.BIN` puede crecer en su lugar actualizando su tamaño en el directorio de la ISO (lo hace `tools/stage.py`).
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
  - La fuente original tiene `0-9`, `A-Z`, `a-z`, el espacio y `. , ( ) ! ? ' " - : & % [ ] /` (`^` se dibuja igual que `-`). Cualquier otro carácter se salta **sin avanzar**: no da error, la palabra sale pegada.
  - `tools/font_es.py` le agrega **á é í ó ú ü ñ Á É Í Ó Ú Ü Ñ ¿ ¡ « » “ ” ‘ ’ — … º ª °** y **`; + = * < > #`**, en Windows-1252 (á = `0xE1`, … = `0x85`, — = `0x97`). Los 18 primeros se probaron en los diálogos en PCSX2 el 2026-11-21; los demás y los menús, *por confirmar* (prueba 3).
  - Comillas: « » como primer nivel, “ ” dentro de ellas y ‘ ’ en el tercer nivel, como pide la RAE (E-58). Puntos suspensivos con `…`; raya con `—`.
  - `@` y `_` son códigos de control en menús y descripciones: no se usan como texto.

## Qué se traduce

- **T-6** Lo que no se traduce ni cuenta (restos sin localizar, textos de prueba) va en `excluded` de `loc.json`. Completar: qué es en este juego.
- **T-7** Solo se traducen los textos que ve el jugador. Los nombres internos (archivos, etiquetas) no se exportan y no se tocan.
- **T-8** Toda línea del lote se traduce completa: ninguna queda vacía, igual al original ni con frases del original mezcladas. (`vacia`, `sin_traducir`, `ingles_mezclado`)
