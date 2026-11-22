# Pendientes

La cola del usuario: lo que ninguna regla cubre, las líneas delicadas con su solución provisional, los términos por decidir y los choques entre documentos. Nada de esto cambia el texto hasta que el usuario lo decide.

Formato: `- [ ] \`clave\` (rol, motivo): «fragmento» → «propuesta». Por qué.` `loc.py findings` agrega aquí, solo, los hallazgos sin regla de cada lote. Lo decidido pasa a DECISIONS.md y se borra de aquí.

## Para la prueba en el juego

Se deciden al ver la pantalla. La 0.9.0 sale con todo en su forma larga para eso [DECISIONS 2026-11-22]: si algo se corta o se encima, se abrevia para la 1.0.0.

- [ ] Textos movidos del ejecutable (TECH, «Textos movidos»): ver que salen bien y no cuelgan el juego. El título «Opciones», «¿Cargar?»/«¿Guardar?» y los mensajes de la memory card («No hay datos guardados.», «Error al formatear.», «¿Revisar MEMORY CARD(PS2) otra vez?», «Revisa de nuevo.», «MEMORY CARD Ranura 1»), «Crear anillo mágico.», «Elige una gema a combinar.», «Elige un anillo.», «_377(MP usado:  )», «_665MP usado: --», «_773Tipo: Objeto», «_577Botón analógico».
- [ ] Lista corta de lugares (pantalla de cargar y guardar): «Nº1 Nv05/Valle de Desechos 1» mide 3 o 4 letras más que el inglés más largo. Ver que entra en el recuadro de la partida.
- [ ] Descripciones de magias, armas y objetos (T-3): se traducen con hasta 3 renglones [DECISIONS 2026-11-22]. Ver en el juego que el 3.º renglón se dibuja dentro del recuadro; si no, se recortan a 2 las que usen 3.
- [ ] `menus/exe#256430` (set de oro, T-3): «_665MP usado: %s%s». El original termina el rótulo en espacio («MP Used: », 9 caracteres), y el chequeo lo toma como campo de ancho fijo: «MP usado: » mide 10. Ver si el valor se corre o se corta; si pasa, se quita el espacio (aquí y en «_665MP usado: --», #256448).
- [ ] Rótulos de menú más largos que el original (piloto, T-3; caben en los bytes, falta ver si entran en pantalla): `243d30` «DARK» → «OSCURIDAD»; `243edc` «Summon Magic» → «Magia de invocación»; `243ef0` «Change attrib.» → «Cambio de atributo»; `243f60` «_882Mag Splitting» → «_882División de magia»; `243f80` «_882Fire weapon» → «_882Arma con fuego»; `243fc0` «_882Reduce MP used» → «_882Reduce el MP usado»; `243fe0` «_882Avoid death» → «_882Evita la muerte»; `244000` «_882Magic Following» → «_882Magia con seguimiento»; `244040` «_882Slow time» → «_882Ralentiza el tiempo»; `244060` «_882Up walk SPD» → «_882Más velocidad al andar»; `2440a0` «_882Recover sight» → «_882Recupera la vista». «OSCURIDAD» va en la fuente grande, junto a los demás elementos.
- [ ] Menús del lote menus-resto más largos que el original (T-3; caben en los bytes, falta verlos en pantalla): `2562f0`, `256578`, `2566d8`, `2567b0`, `256838`, `256af8`, `256b80`, `256c10`, `256c60`, `257540`, `257958`, `257968`, `25d5e8`. También las cabeceras de gemas `256468` «Cant» y `256490` «(Tienes)» (las columnas pueden desalinearse) y los mensajes centrados sobre 39 caracteres `255100`, `255128`, `255150`.
- [ ] `menus/exe#2566c8` «acquired.» → «Se obtuvo.» y `#2566d8` «Can't hold» → «No puedes tener» (lote menus-resto): sin ver qué va delante o detrás en pantalla. Quizá «No puedes llevar».

## Para la 1.0.0

- [ ] Imágenes con texto: OK, CANCEL, SELECT, RETURN, USE, SHORTCUT, INFO., CHANGE, ON/OFF, STEREO/MONO, MIN/MAX y «Time of Fire» son texturas, y los videos `TEXT0`/`TEXT1` tienen texto. En la 0.9.0 quedan en inglés [DECISIONS 2026-11-22]; traducirlos es redibujarlas.

## Del japonés

- [ ] `dialogo/1970#092`-`#094` (mapa de hablantes): el mapa las da a Evans como «segura», pero en japonés parecen tres voces: #092 «さてと、そろそろ寝るとするか» (masculina, llana), #093 «あら、もうこんな時間» («あら» suele ser femenino: ¿Marie Fowler?), #094 «やれやれ、今日も無事に過ごせましたね» (cortés, como Evans). Si #093 es de Marie, «Wow, look at the time.» no cambia en español, pero el mapa sí.

## De los lotes

(Nada por ahora.)
