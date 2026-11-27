# Plan

## Decisiones

Se cierran en la fase 0, porque son caras de cambiar después.

- **Variante:** español neutro (*tú*/*ustedes*, sin regionalismos de ningún país).
- **Original:** versión PAL europea en inglés (SLES-50051), imagen `Eternal Ring.iso`. [DECISIONS 2026-11-20]
- **Otra versión de apoyo:** la japonesa (SLPS-25001), solo para género, sujeto omitido y trato (E-1). [DECISIONS 2026-11-21]
- **Terminología oficial:** no hay traducción oficial al español del juego. *King's Field IV* PAL (`KF4_SPA.DAT`) se consulta solo como muestra de cómo traducía FromSoftware; no es fuente del glosario. [DECISIONS 2026-11-20]
- **Pruebas:** PCSX2; la traducción se instala con un parche xdelta sobre la imagen PAL. [DECISIONS 2026-11-20]
- **Sin spoilers:** los documentos, los commits y el chat nombran zonas o archivos, nunca hechos de la historia.
- **Contenido del repo:** solo la traducción y las herramientas propias; nunca archivos del juego.

## Fases

### Fase 0. Antes de empezar

- [x] Cerrar las decisiones de arriba con el usuario.
- [x] Revisar con el usuario la base de STYLE.md: lo que no aplique se borra. (Se dejan todas, 2026-11-20.)

### Fase 1. Prueba técnica

Antes de esto no se decide nada más.

- [x] Extraer los archivos del juego, a una carpeta fuera del repo. (`../local/eternal-ring/iso/`, 2026-11-20.)
- [x] Ubicar todo el texto. (2026-11-21: ejecutable, descripciones de `ERDATA.BIN`, los 505 mensajes en los guiones de 55 escenarios y los videos `TEXT0`/`TEXT1`; ver TECH.md. Letras españolas y mensajes más largos probados en PCSX2.)
- [x] Adaptador: exportar el texto al formato común (`source` de `loc.json`) e importarlo de vuelta. (`tools/adapter.py`, 2026-11-21; una ISO de `build` probada en PCSX2: menú, día, objeto y arma.)
- [x] Ida y vuelta idéntica: exportar e importar sin cambios da los mismos archivos. (`adapter.py roundtrip`: `ERDATA.BIN`, ejecutable y 55 guiones idénticos.)
- [x] Caracteres: si la fuente tiene las letras españolas, o cómo se agregan (T-5). (No las tiene; `tools/font_es.py` agrega 34 signos, también en la fuente chica, y los activa en las tres funciones de texto. Probado en PCSX2. La fuente grande no tiene acentos y no le hacen falta.)
- [x] Límites: bytes, ancho y renglones de cada tipo de texto (T-3, T-4), y sus chequeos en `hooks`. (`tools/hooks.py`; cuántos renglones entran en una descripción, en PENDING.md.)
- [x] Pseudolocalización: todo el texto más largo y con letras españolas, en el juego, para ver cortes y glifos que faltan. (`tools/pseudo.py` + `adapter.py build`, vista en PCSX2 el 2026-11-21: fuente grande sin acentos, ancho de lugares, títulos y descripciones, una zona más del ejecutable y las imágenes con texto; ver TECH.md.)
- [x] Imágenes con texto (botones, ON/OFF, «Time of Fire»…): ubicadas; si se traducen, en PENDING.md.
- [x] Completar TECH.md y `loc.json` (`codes`, `fixed_break`, `excluded`, `sections`). (2026-11-21. Fase 1 cerrada.)

### Fase 2. Inventario y presupuesto

- [x] Volumen por sección (`loc.py progress`). (2026-11-21: 1.183 textos, 7.483 palabras. Diálogos 505 líneas / 5.378 palabras; Magias, armas y objetos 324 / 1.380; Menús 354 / 725.)
- [x] Costo estimado por sección, antes de empezarla. (2026-11-21, con la referencia de METHOD.md: unos 43.000 tokens cada 250 líneas por agente; traductor, revisor y corrector pasan por todo, más editor y delicadas.)
  - Diálogos: unos 300.000 tokens (2 lotes; líneas largas, puede subir).
  - Magias, armas y objetos: unos 200.000 (2 lotes).
  - Menús: unos 150.000 (2 lotes; líneas de 2 palabras de media, probablemente menos).
  - Total: unos 650.000, sin contar glosario, fichas ni set de oro.

### Fase 3. Documentos

- [x] Glosario: el terminólogo propone las filas. (2026-11-21: 296 términos decididos por el usuario, bloque por bloque; no hay fuente oficial, todo es G-2.)
- [x] Fichas de personajes: el perfilador, antes de cada sección. (2026-11-21, Diálogos: 20 fichas, 2 voces y `characters/_mapa.md`. Género y turnos revisados con el japonés; sin marcar solo el diario de 1911 y la conciencia antigua. Las otras dos secciones no tienen personajes.)
- [x] DECISIONS.md y PENDING.md al día. (2026-11-21.)

### Fase 4. Set de oro

Obligatorio: sin él, `loc.py prepare` no arma lotes.

- [x] Elegir con el usuario los casos reales (al menos uno de cada tipo; mejor dos o tres). (2026-11-21: 21 casos, tres de cada tipo, en `golden.jsonl`.)
- [x] Aprobarlo (`loc.py golden approve`). (2026-11-21.)
- [x] Probar a los agentes (`loc.py golden prepare`, traductor, revisor y corrector, `loc.py golden score`) hasta que pase. (2026-11-21: 20 de 21 en la primera prueba; tras el cambio de prompt sobre el género de a quién se le habla, 21 de 21. Fase 4 cerrada.)

### Fase 5. Piloto

- [x] Un primer lote de cada tipo de texto con el equipo completo. (2026-11-22: diálogos 1901-1905, 89 líneas; magias #000-029, 60; menús, 60.)
- [x] Ajustar documentos y roles con lo que salga (y volver a pasar el set de oro si cambia un prompt). (2026-11-22: descripciones con 3 renglones, «Fire Dragon» separado en tres términos, excepción de «Mando» en E-12, tres arreglos del validador del kit; ningún prompt cambió, la prueba de oro sigue vigente. Fase 5 cerrada.)

### Fase 6. Traducción

- [x] Historia (505 diálogos). (2026-11-22: lotes piloto-dialogos, dialogos-1908-1917 y dialogos-1918-1990.)
- [x] Objetos y equipo (324: magias, armas, objetos y gemas). (2026-11-22: lotes piloto-objetos y objetos-resto.)
- [x] Interfaz (354 menús). (2026-11-22: lotes piloto-menus y menus-resto. Los textos que no entraban en su campo se movieron en el ejecutable: TECH, «Textos movidos».)

### Fase 7. Prueba en el juego

- [x] Jugar con la traducción completa y anotar cortes, cajas que se pasan, glifos que faltan y texto que quedó sin traducir. (2026-11-23: la 0.9.0 se colgaba al sonar la primera voz, porque los escenarios movidos pisaban `VOICEALL.ADX`; la 0.9.1 los pone en `DUMMY.OUT`. TECH, «Espacio en el disco». 2026-11-24: el juego se congelaba en el escenario 1973 porque el banco de sonido quedaba desalineado detrás del escenario; la 0.9.2 deja cada escenario en múltiplo de 16. TECH, «Escenarios». 2026-11-27: el usuario terminó el juego con la 0.9.3 sin errores nuevos; antes de la 1.0.0 se revisaron los nombres de magias y gemas con la guía de anillos, DECISIONS 2026-11-27.)

### Fase 8. Entrega

- [x] Instalador, registro de cambios y publicación. (2026-11-27: versión 1.0.0; los botones e imágenes con texto quedan en inglés, DECISIONS 2026-11-27.)
