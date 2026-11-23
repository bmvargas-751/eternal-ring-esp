# Herramientas

Se corren desde la raíz del repo con `python3 -I tools/NOMBRE.py`. Lo extraído del juego vive en `../local/eternal-ring/` (nunca en el repo); el detalle técnico, en [TECH.md](../TECH.md).

| Herramienta | Qué hace |
|---|---|
| `adapter.py` | El adaptador del kit. `export` pasa el texto del juego al formato común (`source.jsonl`); `roundtrip` comprueba que escribir el original deja todo idéntico; `build ISO_ORIGINAL ISO_NUEVA translation/` arma una ISO traducida para probar en PCSX2. También mueve los textos del ejecutable que no entran en su campo (TECH, «Textos movidos»). |
| `hooks.py` | Los chequeos propios del juego para `loc.py check`: bytes, renglones y ancho de cada caja, y letras que tiene la fuente (T-3, T-4, T-5). |
| `font_es.py` | Agrega a las fuentes del juego las letras y signos del español, y las activa en las funciones de texto. Lo usa `adapter.py build`. |
| `stage.py` | Lee y reescribe los escenarios de `ERDATA.BIN` (guiones y mensajes) y la imagen ISO. Lo usa el adaptador. |
| `pseudo.py` | Pseudolocalización: todo el texto más largo y con letras españolas, para ver cortes en el juego. |
| `release.py` | Arma el paquete de una versión: `release.py VERSIÓN ISO_ORIGINAL` crea el parche `.xdelta`, el instalador para Windows (`release/patcher.cs`, compilado con el `csc.exe` de .NET Framework) y `LEEME.txt` (`release/LEEME.txt`), los comprueba y los junta en un `.zip` en `../local/eternal-ring/dist/`. Necesita `xdelta3`. |
| `ja.py`, `pair_ja.py`, `ja_glyphs.txt` | La versión japonesa de apoyo: leen su texto y emparejan cada línea inglesa con la japonesa (`../local/eternal-ring/jp/pares.jsonl`), para los agentes. |
| `mipsdis.py` | Desensamblador MIPS mínimo, para leer el ejecutable. |
