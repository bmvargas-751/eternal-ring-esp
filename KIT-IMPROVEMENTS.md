# Mejoras para el kit

Lo que se vio al usar el kit con Eternal Ring y que **no** se cambió: el kit solo se toca por errores graves (decisión del usuario, 2026-11-22). Cada punto dice qué pasó, dónde y una propuesta. Se juntan aquí para hacerlas de una vez, con el visto bueno del usuario y una nueva prueba del set de oro si alguna toca un prompt.

## Validador (`tools/lockit/checks.py`)

- **Diminutivos y formas derivadas del glosario.** «Fireball → Bola de fuego»: «Invoca una bolita de fuego.» (magia#000.desc, decisión del usuario) da G-3, porque «bola» tiene 4 letras y se busca literal. Propuesta: aceptar diminutivos en *-ita/-ito* de las palabras cortas, o un mecanismo para aceptar un aviso (ver abajo).
- **Avisos aceptados.** Un aviso que el usuario acepta (como el anterior) sigue saliendo en cada `check` y en `checks.jsonl`, y el revisor tiene que adivinar que es decisión. Propuesta: un archivo del proyecto (`accepted.jsonl`, `{key, check, motivo}`) que `check` respete y que se cite en DECISIONS.
- **Aviso de crecimiento en menús (T-3).** En los rótulos del ejecutable el aviso «N caracteres, el original M: ver en el juego» es informativo, pero cuenta como aviso sin resolver y empuja al traductor a recortar. Propuesta: separar los avisos «a ver en el juego» de los que obligan a corregir.

## Set de oro (`golden.py`)

- **Los casos de revisión no pasan por el validador.** O-6 tenía un renglón de 37 caracteres (la caja admite 35) y nadie lo notó hasta que el revisor lo mencionó como duda. Propuesta: `golden status` corre `check` sobre el `es` de los casos `intacta`, `rara-correcta` (deben pasar limpios).
- **El contexto de los casos no trae la versión de apoyo.** `make_item` agrega `ja` a la línea, no a las de `context`. Propuesta: agregarlo también al contexto, para que el revisor vea el japonés de la línea anterior.

## Flujo del lote

- **Decisiones del usuario sobre un lote.** Para aplicar un cambio que decide el usuario hubo que inventar un hallazgo `U-n` en `approved.jsonl` y un `edits.jsonl` a mano. Propuesta: `loc.py decide NOMBRE CLAVE "texto"` que registre el cambio con su motivo (y lo lleve a DECISIONS).
- **Hallazgos descartados por el usuario.** Para descartar un hallazgo (el «Mando» → «Control» del corrector, que contradecía una excepción del glosario) se vació el archivo de hallazgos. Propuesta: `loc.py findings NOMBRE --drop C-1 "motivo"`, que deje constancia.
- **Rehacer un lote ya revisado.** Al cambiar una regla a mitad de lote (3 renglones en las descripciones) hubo que borrar los hallazgos viejos a mano antes de volver a revisar. Propuesta: `loc.py view` avisa si hay hallazgos más viejos que la traducción vigente.

## Prompts de los agentes

- **El traductor fuerza frases para callar un aviso.** En el piloto reformuló tres líneas («Usar el anillo te permitirá…», «hacia el continente») solo por un falso positivo. Se resolvió diciéndolo en el encargo de cada lote. Propuesta: una línea en `loc-translator`: «Si un aviso te obliga a una frase peor, no la fuerces: déjala natural y explícalo en el informe».
- **El corrector no ve las excepciones del glosario.** Lee solo el español y marcó «Mando» por E-12, que el glosario exceptúa. Se resolvió nombrando la excepción en STYLE E-12. Propuesta: que el corrector consulte el glosario antes de marcar un término por E-12/E-13.
- **El corrector no lee fichas.** En la segunda prueba de oro no marcó el tuteo del árbol cortés (O-19); lo atrapó el revisor. No es grave (el revisor cubre trato), pero conviene que el corrector lea el mapa de hablantes o que la línea traiga el hablante.
- **Hablante en cada línea.** El original no trae `speaker`; el mapa está en `characters/_mapa.md` y cada agente lo busca. Propuesta: un campo opcional en `loc.json` (archivo `{key, speaker}`) que `make_item` agregue, igual que la versión de apoyo.
