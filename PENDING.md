# Pendientes

La cola del usuario: lo que ninguna regla cubre, las líneas delicadas con su solución provisional, los términos por decidir y los choques entre documentos. Nada de esto cambia el texto hasta que el usuario lo decide.

Formato: `- [ ] \`clave\` (rol, motivo): «fragmento» → «propuesta». Por qué.` `loc.py findings` agrega aquí, solo, los hallazgos sin regla de cada lote. Lo decidido pasa a DECISIONS.md y se borra de aquí.

## Para la prueba en el juego

Se deciden al ver la pantalla.

- [ ] `menus/exe#256360`, `#256370`, `#256380`, `#256390` (prueba técnica, ordinal del día): «%3dst day», «%3dnd day», «%3drd day», «%3dth day» → «%3d.er día», «%3d.º día», «%3d.er día», «%3d.º día». El juego elige la variante como en inglés (st para 1, 21, 31…; nd para 2, 22…; rd para 3, 23…; th para el resto, incluidos 11, 12 y 13), así que el 13 saldría «13.º día» en vez de «13.er día». «Día %3d» se vio bien en PCSX2 y evita el problema; el campo admite 15 bytes. `%3d` deja espacios delante del número.

## De los lotes
