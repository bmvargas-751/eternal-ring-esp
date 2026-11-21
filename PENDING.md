# Pendientes

La cola del usuario: lo que ninguna regla cubre, las líneas delicadas con su solución provisional, los términos por decidir y los choques entre documentos. Nada de esto cambia el texto hasta que el usuario lo decide.

Formato: `- [ ] \`clave\` (rol, motivo): «fragmento» → «propuesta». Por qué.` `loc.py findings` agrega aquí, solo, los hallazgos sin regla de cada lote. Lo decidido pasa a DECISIONS.md y se borra de aquí.

## Para la prueba en el juego

Se deciden al ver la pantalla.

- [ ] `menus/exe#256360`, `#256370`, `#256380`, `#256390` (prueba técnica, ordinal del día): «%3dst day», «%3dnd day», «%3drd day», «%3dth day» → «%3d.er día», «%3d.º día», «%3d.er día», «%3d.º día». El juego elige la variante como en inglés (st para 1, 21, 31…; nd para 2, 22…; rd para 3, 23…; th para el resto, incluidos 11, 12 y 13), así que el 13 saldría «13.º día» en vez de «13.er día». «Día %3d» se vio bien en PCSX2 y evita el problema; el campo admite 15 bytes. `%3d` deja espacios delante del número.

- [ ] Descripciones de magias, armas y objetos (prueba técnica, T-3): cuántos renglones entran en la ficha. La pseudolocalización agrega un «[3.er renglón de prueba]» donde el campo lo permite (magias, objetos de descripción corta); no se llegó a ver. Hasta entonces, 2 renglones, como el original.
- [ ] Imágenes con texto (prueba técnica): OK, CANCEL, SELECT, RETURN, USE, SHORTCUT, INFO., CHANGE, ON/OFF, STEREO/MONO, MIN/MAX, «Time of Fire» son texturas. ¿Se traducen (editar imágenes) o quedan en inglés, como los videos `TEXT0`/`TEXT1` mientras tanto?
- [ ] Títulos de 7 letras (prueba técnica, T-3): en el ejecutable, 0x25d558–0x25d740, los campos son de 8 bytes («Options» → «Ajustes» entra; «Opciones», no). Si alguno necesita más, hay que mover la cadena y corregir sus referencias en el código. «Options» → «Opciones» (8) en 0x25d678 ya lo necesita [DECISIONS 2026-11-21].
- [ ] Lista corta de lugares (T-3; [DECISIONS 2026-11-21]): en el ejecutable, 0x24a540–0x24a760, campos de 7 a 17 bytes. Se mueven las cadenas y se corrigen sus referencias en el código, para que cada lugar use su forma completa del glosario. Junto con los títulos de 7 letras.

## De los lotes
