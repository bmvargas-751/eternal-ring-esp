# Pendientes

La cola del usuario: lo que ninguna regla cubre, las líneas delicadas con su solución provisional, los términos por decidir y los choques entre documentos. Nada de esto cambia el texto hasta que el usuario lo decide.

Formato: `- [ ] \`clave\` (rol, motivo): «fragmento» → «propuesta». Por qué.` `loc.py findings` agrega aquí, solo, los hallazgos sin regla de cada lote. Lo decidido pasa a DECISIONS.md y se borra de aquí.

## Para la prueba en el juego

Se deciden al ver la pantalla.

- [ ] `menus/exe#256360`, `#256370`, `#256380`, `#256390` (prueba técnica, ordinal del día): «%3dst day», «%3dnd day», «%3drd day», «%3dth day» → «%3d.er día», «%3d.º día», «%3d.er día», «%3d.º día». El juego elige la variante como en inglés (st para 1, 21, 31…; nd para 2, 22…; rd para 3, 23…; th para el resto, incluidos 11, 12 y 13), así que el 13 saldría «13.º día» en vez de «13.er día». «Día %3d» se vio bien en PCSX2 y evita el problema; el campo admite 15 bytes. `%3d` deja espacios delante del número.

- [ ] Descripciones de magias, armas y objetos (T-3): se traducen con hasta 3 renglones [DECISIONS 2026-11-22]. Ver en el juego (fase 7) que el 3.º renglón se dibuja dentro del recuadro; si no, se recortan a 2 las que usen 3.
- [ ] Imágenes con texto (prueba técnica): OK, CANCEL, SELECT, RETURN, USE, SHORTCUT, INFO., CHANGE, ON/OFF, STEREO/MONO, MIN/MAX, «Time of Fire» son texturas. ¿Se traducen (editar imágenes) o quedan en inglés, como los videos `TEXT0`/`TEXT1` mientras tanto?
- [ ] Títulos de 7 letras (prueba técnica, T-3): en el ejecutable, 0x25d558–0x25d740, los campos son de 8 bytes («Options» → «Ajustes» entra; «Opciones», no). Si alguno necesita más, hay que mover la cadena y corregir sus referencias en el código. «Options» → «Opciones» (8) en 0x25d678 ya lo necesita [DECISIONS 2026-11-21].
- [ ] Lista corta de lugares (T-3; [DECISIONS 2026-11-21]): en el ejecutable, 0x24a540–0x24a760, campos de 7 a 17 bytes. Se mueven las cadenas y se corrigen sus referencias en el código, para que cada lugar use su forma completa del glosario. Junto con los títulos de 7 letras.
  **Hoy bloquea el armado:** con la traducción al 100 %, `adapter.py build` no arma la ISO hasta mover estas cadenas y la de «Opciones»: 15 lugares de la lista corta pasan de su campo («Desconocido» 11/7, «Biblioteca» 10/7, «Ruinas de la Mina» 17/10…) y «Opciones» 8/7. Hay que hacerlo antes de la fase 7.

- [ ] `menus/exe#256430` (set de oro, T-3): «_665MP Used: %s%s» → «_665MP usado:%s%s». El original termina el rótulo en espacio («MP Used: », 9 caracteres), y el chequeo lo toma como campo de ancho fijo: «MP usado: » mide 10. El traductor quitó el espacio para que pase. Ver en el juego si con el espacio el valor se corre o se corta; si entra, se vuelve a poner. Igual con «_665MP Used: --» (#256448).

- [ ] Rótulos de menú más largos que el original (piloto, T-3; caben en los bytes, falta ver si entran en pantalla): `243d30` «DARK» → «OSCURIDAD»; `243edc` «Summon Magic» → «Magia de invocación»; `243ef0` «Change attrib.» → «Cambio de atributo»; `243f60` «_882Mag Splitting» → «_882División de magia»; `243f80` «_882Fire weapon» → «_882Arma con fuego»; `243fc0` «_882Reduce MP used» → «_882Reduce el MP usado»; `243fe0` «_882Avoid death» → «_882Evita la muerte»; `244000` «_882Magic Following» → «_882Magia con seguimiento»; `244040` «_882Slow time» → «_882Ralentiza el tiempo»; `244060` «_882Up walk SPD» → «_882Más velocidad al andar»; `2440a0` «_882Recover sight» → «_882Recupera la vista». «OSCURIDAD» va en la fuente grande, junto a los demás elementos. Si alguno se corta o se encima, se abrevia.

- [ ] Menús del lote menus-resto más largos que el original (T-3; caben en los bytes, falta verlos en pantalla): `2562f0`, `256430`, `256578`, `2566d8`, `2567b0`, `256838`, `256af8`, `256b80`, `256c10`, `256c60`, `257540`, `257958`, `257968`, `25d5e8`. También las cabeceras de gemas `256468` «Cant» y `256490` «(Tienes)» (las columnas pueden desalinearse) y los mensajes centrados sobre 39 caracteres `255100`, `255128`, `255150`.
- [ ] `menus/exe#2566c8` «acquired.» → «Se obtuvo.» y `#2566d8` «Can't hold» → «No puedes tener» (lote menus-resto): sin ver qué va delante o detrás en pantalla. «No puedes llevar» sonaría mejor, pero no entra en 15 bytes. Ver en el juego.
- [ ] Abreviaturas forzadas por el ancho (lote menus-resto), que se arreglan solas si se mueven las cadenas (ver «Lista corta de lugares»): `24a5c0`/`24a5e0` «Sant. Agua S1/S2» (glosario «Sant. del Agua S1/S2», 17 bytes en 15), `24a620` «B. Escarpado 1», `24a660` «Valle Desechos 1», `256c30` «MEMORY CARD Ran. 1» (la 2 sí dice «Ranura 2»), `25d718`/`25d720` «Cargar»/«Guardar» sin «¿ ?» (campos de 7).

## Del japonés

- [ ] `dialogo/1970#092`-`#094` (mapa de hablantes): el mapa las da a Evans como «segura», pero en japonés parecen tres voces: #092 «さてと、そろそろ寝るとするか» (masculina, llana), #093 «あら、もうこんな時間» («あら» suele ser femenino: ¿Marie Fowler?), #094 «やれやれ、今日も無事に過ごせましたね» (cortés, como Evans). Si #093 es de Marie, «Wow, look at the time.» no cambia en español, pero el mapa sí.

## De los lotes

- [ ] `objetos/magia#062`, `#064`, `#077` (lote objetos-resto, duda del revisor, sin regla): «the Earth» → «la Tierra», con mayúscula como el elemento. En español «la Tierra» suena a planeta; «la tierra» (el suelo, la naturaleza) también serviría.
- [ ] `objetos/magia#080` «luz» y `#090` «oscuridad» (resistencias, lote objetos-resto): en minúscula, mientras los atributos van «Luz»/«Oscuridad». El original es irregular («light»/«Dark»). ¿Se unifican con mayúscula?
- [ ] «fuerza y Agua» (`magia#015`, `#035`, `#055`, `#075`): «fuerza» en minúscula por el glosario y el elemento en mayúscula; el contraste se ve raro. Unificarlo cambia el glosario.
- [ ] `menus/exe#257bf8` «No saved data.» → «No hay datos.» (lote menus-resto, duda del revisor): «Sin guardados.» (14 bytes) conserva el «saved».
- [ ] `menus/exe#256448` «_665MP usado:--» (lote menus-resto): sin espacio por el límite de 15; «_665MP us.: --» cabe y va igual que `256508` «(MP us.:  )». Junto con `256430` de «Para la prueba en el juego».
