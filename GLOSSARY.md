# Glosario

Términos fijos de la traducción. La guía de estilo está en [STYLE.md](STYLE.md).

## Reglas

- **G-1** Si la serie tiene una traducción oficial al español (otro juego, el anime, un manual), los términos que comparte con este juego llevan el nombre oficial. Se toma solo el término; el registro es siempre el de esta traducción. Completar en el PLAN cuál es la fuente oficial, o borrar esta regla si no hay. [IVA]
- **G-2** Lo propio de este juego se decide aquí. Hasta que esté decidido, el término va a [PENDING.md](PENDING.md) con una propuesta. [IVA]
- **G-3** Un término de esta tabla se usa igual en todo el juego. `loc.py check` avisa cuando el original lo tiene y la traducción no (`glosario`). [Encargo §6]

## Cómo se arma

1. El terminólogo revisa los candidatos (los de la fuente oficial, si hay, y los términos de sistema del juego) y propone las filas: *oficial* si es el mismo término, o *por decidir* si significa otra cosa en este juego.
2. Las filas *oficial* entran a la tabla. Las *por decidir* van a [PENDING.md](PENDING.md) para que las decida el usuario.

## Términos

Por sección. *Oficial* (G-1) o *decidido* por el usuario (G-2), con fecha. `loc.py` lee toda tabla cuya cabecera empiece por `| Inglés |`.

| Inglés | Español | Fuente | Nota |
|---|---|---|---|
| Eternal Ring | Anillo Eterno | decidido [DECISIONS 2026-11-21] | En los textos; el logo y los videos no se tocan. |
| HP | HP | decidido [DECISIONS 2026-11-21] | |
| MP | MP | decidido [DECISIONS 2026-11-21] | |
| EXP | EXP | decidido [DECISIONS 2026-11-21] | |
| God's child | el hijo de Dios | decidido [DECISIONS 2026-11-21] | También «God-child» y «the child of God». |
| Sealed | Magia sellada | decidido [DECISIONS 2026-11-21] | Estado. El cartel de 1912#000 («Sealed by magic.») va «Tiene un sello mágico.» [DECISIONS 2026-11-22]; el de 1975#000 («Sealed.»), «Sellado.». |
| Cursed | Maldición | decidido [DECISIONS 2026-11-21] | Estado. |
| Poisoned | Veneno | decidido [DECISIONS 2026-11-21] | Estado. |
| Paralyzed | Parálisis | decidido [DECISIONS 2026-11-21] | Estado. |
| Fire Dragon Fang | Colm. dragón fuego | decidido [DECISIONS 2026-11-21] | Objeto; campo de 19 bytes. |
| Earth Dragon Fang | Colm. dragón tierra | decidido [DECISIONS 2026-11-21] | Objeto; 19/19 bytes. |
| Air Dragon Fang | Colm. dragón aire | decidido [DECISIONS 2026-11-21] | Objeto; «aire» como el original (E-61). |
| Water Dragon Fang | Colm. dragón agua | decidido [DECISIONS 2026-11-21] | Objeto. |
| Gold Dragon Fang | Colm. dragón oro | decidido [DECISIONS 2026-11-21] | Objeto. |
| Silver Dragon Fang | Colm. dragón plata | decidido [DECISIONS 2026-11-21] | Objeto. |
| Elder Dragon Fang | Colm. dragón mayor | decidido [DECISIONS 2026-11-21] | Objeto. |
| Dark | Oscuridad | decidido [DECISIONS 2026-11-21] | Elemento. En la pantalla de estado (fuente grande, 6 letras como mucho y sin punto): «OSCUR» [DECISIONS 2026-11-24]. |
| Blizzard | Ventisca | decidido [DECISIONS 2026-11-21] | Magia. |
| Snowstorm Plain | Llano de la Nevada | decidido [DECISIONS 2026-11-21] | Lugar; 18 caracteres visibles. |
| Poison | Veneno | decidido [DECISIONS 2026-11-21] | Magia; el estado «Poisoned» también es «Veneno». |
| Research Team HQ | Base de Invest. | decidido [DECISIONS 2026-11-21] | Lugar. |
| [ON] | [Sí] | decidido [DECISIONS 2026-11-21] | Menú de opciones. |
| [OFF] | [No] | decidido [DECISIONS 2026-11-21] | Menú de opciones. |
| Options | Opciones | decidido [DECISIONS 2026-11-21] | En `menus/exe#25d678` (7 bytes) hay que mover la cadena. |
| Settings | Ajustes | decidido [DECISIONS 2026-11-21] | |
| Fire | Fuego | decidido [DECISIONS 2026-11-21] | Elemento; «FUEGO» en la fuente grande. |
| Earth | Tierra | decidido [DECISIONS 2026-11-21] | Elemento; «TIERRA» en la fuente grande. |
| Wind | Viento | decidido [DECISIONS 2026-11-21] | Elemento; «VIENTO» en la fuente grande. |
| Water | Agua | decidido [DECISIONS 2026-11-21] | Elemento; «AGUA» en la fuente grande. |
| Light | Luz | decidido [DECISIONS 2026-11-21] | Elemento; «LUZ» en la fuente grande. |
| STR | FUE | decidido [DECISIONS 2026-11-21] | Atributo de fuerza, en la fuente grande; en las descripciones, «Strength» → «fuerza», pero «Fuerza» con mayúscula cuando se nombra como atributo junto a un elemento («los atributos Fuerza y Fuego») [DECISIONS 2026-11-22]. |
| Neutral | Neutro | decidido [DECISIONS 2026-11-21] |  |
| Attrib. | Atrib. | decidido [DECISIONS 2026-11-21] | «attribute» → «atributo»; «Basic Attrib.» → «Atrib. básico»; «Overall Attrib.» → «Atrib. total». |
| Fire Magic | magia de fuego | decidido [DECISIONS 2026-11-21] | Igual con agua, viento y tierra; minúscula a media frase. |
| Magic Ring | anillo mágico | decidido [DECISIONS 2026-11-21] | Forma corta «Mag Ring» → «An. mágico». |
| Attribution Ring | anillo de atributo | decidido [DECISIONS 2026-11-21] | Forma corta «Attr Ring» → «An. atrib.». En el menú del altar: «Anillo de atrib.» [DECISIONS 2026-11-24]. |
| Elements | Elementos | decidido [DECISIONS 2026-11-21] | Categoría de anillos. |
| Attack Magic | Magia de ataque | decidido [DECISIONS 2026-11-21] | Categoría de anillos. |
| Assist Magic | Magia de apoyo | decidido [DECISIONS 2026-11-21] | Categoría de anillos. |
| Summon Magic | Magia de invocación | decidido [DECISIONS 2026-11-21] | Categoría de anillos. |
| Change attrib. | Cambio de atributo | decidido [DECISIONS 2026-11-21] | Categoría de anillos. |
| Add special ability | Añade hab. especial | decidido [DECISIONS 2026-11-21] | Categoría de anillos; 19/19 bytes. |
| Gems | gemas | decidido [DECISIONS 2026-11-21] | «Mag Gems» → «Gemas mágicas». En la columna del menú principal (10 caracteres, junto a «An. mágico»): «Gemas mág.» [DECISIONS 2026-11-22]. |
| Combine | Combinar | decidido [DECISIONS 2026-11-21] | «Combination» → «combinación». |
| MP used | MP usado | decidido [DECISIONS 2026-11-21] | También «MP usage». |
| Level | Nivel | decidido [DECISIONS 2026-11-21] | «LEVEL» → «NIVEL»; «Lvl.1» → «Nv.1». |
| NEXT | SIG | decidido [DECISIONS 2026-11-21] | Experiencia para el siguiente nivel; la fuente grande no tiene punto. |
| caster | el usuario | decidido [DECISIONS 2026-11-21] | Quien lanza la magia, en las descripciones. |
| Fireball | Bola de fuego | decidido [DECISIONS 2026-11-21] | Magia. |
| Fire Wall | Muro de fuego | decidido [DECISIONS 2026-11-21] | Magia. |
| Floating Bomb | Bomba flotante | decidido [DECISIONS 2026-11-21] | Magia. |
| Bomber | Bombardeo | decidido [DECISIONS 2026-11-21] | Magia. |
| Silence | Silencio | decidido [DECISIONS 2026-11-21] | Magia. |
| Weaken | Debilitar | decidido [DECISIONS 2026-11-21] | Magia. |
| Alter Fire | Alterar fuego | decidido [DECISIONS 2026-11-21] | Magia. |
| Deplete | Agotar | decidido [DECISIONS 2026-11-21] | Magia. |
| Fiery Avenger | Vengador ígneo | decidido [DECISIONS 2026-11-21] | Magia. |
| Fire Dragon | Dragón de fuego | decidido [DECISIONS 2026-11-22] | Nombre de la magia (magia#009). En los diálogos, «a Fire Dragon» es la criatura: ver «fire dragon». |
| fire dragon | dragón de fuego | decidido [DECISIONS 2026-11-22] | La criatura en que se convirtieron los solcianos (diálogos 1909#007, 1912#039, 1915#016, 1916#008; en japonés «火竜»), en minúscula aunque el inglés la escriba «Fire Dragon». |
| Great Fire Dragon | Gran Dragón de fuego | decidido [DECISIONS 2026-11-22] | El ser que invoca la magia, solo en su descripción: «Invoca al Gran Dragón de fuego…». |
| Great Water Dragon | Gran Dragón de agua | decidido [DECISIONS 2026-11-22] | Descripción de la magia «Dragón de agua». |
| Great Wind Dragon | Gran Dragón de viento | decidido [DECISIONS 2026-11-22] | Descripción de la magia «Dragón de viento». |
| Great Earth Dragon | Gran Dragón de tierra | decidido [DECISIONS 2026-11-22] | Descripción de la magia «Dragón de tierra». |
| Great Light Dragon | Gran Dragón de luz | decidido [DECISIONS 2026-11-22] | Descripción de la magia «Dragón de luz». |
| Great Dark Dragon | Gran Dragón oscuro | decidido [DECISIONS 2026-11-22] | Descripción de la magia «Dragón oscuro». |
| Ring of Heat | Anillo de calor | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Flame | Anillo de llamas | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Inferno | Anillo del infierno | decidido [DECISIONS 2026-11-21] | Magia. |
| Wind Heat | Calor de viento | decidido [DECISIONS 2026-11-21] | Magia. |
| Earth Heat | Calor de tierra | decidido [DECISIONS 2026-11-21] | Magia. |
| Sword Heat | Espada de calor | decidido [DECISIONS 2026-11-21] | Magia. |
| Water Heat | Calor de agua | decidido [DECISIONS 2026-11-21] | Magia. |
| Animated Sword | Espada animada | decidido [DECISIONS 2026-11-21] | Magia. |
| Power of Branch | Poder de ramificación | decidido [DECISIONS 2026-11-21] | Magia. Como nombre del anillo (19 caracteres como mucho): «Poder de ramific.» [DECISIONS 2026-11-24]. |
| Burn Edge | Filo ardiente | decidido [DECISIONS 2026-11-21] | Magia. |
| Ice Needle | Aguja de hielo | decidido [DECISIONS 2026-11-21] | Magia. |
| Ice Wall | Muro de hielo | decidido [DECISIONS 2026-11-21] | Magia. |
| Ice Trap | Trampa de hielo | decidido [DECISIONS 2026-11-21] | Magia. |
| Healing Water | Agua curativa | decidido [DECISIONS 2026-11-21] | Magia. |
| Curing Water | Agua sanadora | decidido [DECISIONS 2026-11-21] | Magia. |
| Unpoison | Antídoto | decidido [DECISIONS 2026-11-21] | Magia. |
| Purify | Purificar | decidido [DECISIONS 2026-11-21] | Magia. |
| Projectile | Proyectil | decidido [DECISIONS 2026-11-21] | Magia. |
| Water Dragon | Dragón de agua | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Rain | Anillo de lluvia | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Sea | Anillo de mar | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Abyss | Anillo del abismo | decidido [DECISIONS 2026-11-21] | Magia. |
| Wind Rain | Lluvia de viento | decidido [DECISIONS 2026-11-21] | Magia. |
| Earth Rain | Lluvia de tierra | decidido [DECISIONS 2026-11-21] | Magia. |
| Sword Rain | Espada de lluvia | decidido [DECISIONS 2026-11-21] | Magia. |
| Fire Rain | Lluvia de fuego | decidido [DECISIONS 2026-11-21] | Magia. |
| Fortune | Fortuna | decidido [DECISIONS 2026-11-21] | Magia. |
| Enlightenment | Iluminación | decidido [DECISIONS 2026-11-21] | Magia. |
| Sacrifice | Sacrificio | decidido [DECISIONS 2026-11-21] | Magia. |
| Wind Cutter | Cuchilla de viento | decidido [DECISIONS 2026-11-21] | Magia. |
| Sonic | Sónico | decidido [DECISIONS 2026-11-21] | Magia. |
| Tornado | Tornado | decidido [DECISIONS 2026-11-21] | Magia. |
| Vortex | Vórtice | decidido [DECISIONS 2026-11-21] | Magia. |
| Turbulence | Turbulencia | decidido [DECISIONS 2026-11-21] | Magia. |
| Confusion | Confusión | decidido [DECISIONS 2026-11-21] | Magia. |
| Invisible | Invisible | decidido [DECISIONS 2026-11-21] | Magia. |
| Bind | Atadura | decidido [DECISIONS 2026-11-21] | Magia. |
| Spear | Lanza | decidido [DECISIONS 2026-11-21] | Magia. |
| Wind Dragon | Dragón de viento | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Breeze | Anillo de brisa | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Gust | Anillo de ráfaga | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Storm | Anillo de tormenta | decidido [DECISIONS 2026-11-21] | Magia. |
| Fire Breeze | Brisa de fuego | decidido [DECISIONS 2026-11-21] | Magia. |
| Water Breeze | Brisa de agua | decidido [DECISIONS 2026-11-21] | Magia. |
| Sword Breeze | Espada de brisa | decidido [DECISIONS 2026-11-21] | Magia. |
| Earth Breeze | Brisa de tierra | decidido [DECISIONS 2026-11-21] | Magia. |
| Power of Seek | Poder de búsqueda | decidido [DECISIONS 2026-11-21] | Magia. |
| Clarity | Claridad | decidido [DECISIONS 2026-11-21] | Magia. |
| Power of Time | Poder del tiempo | decidido [DECISIONS 2026-11-21] | Magia. |
| Material Arrow | Flecha material | decidido [DECISIONS 2026-11-21] | Magia. |
| Upheaval | Sacudida | decidido [DECISIONS 2026-11-21] | Magia. |
| Mist | Niebla | decidido [DECISIONS 2026-11-21] | Magia. |
| Earth Heal | Cura de tierra | decidido [DECISIONS 2026-11-21] | Magia. |
| Protect | Protección | decidido [DECISIONS 2026-11-21] | Magia. |
| Imprisonment | Encarcelamiento | decidido [DECISIONS 2026-11-21] | Magia. |
| Orbiter | Órbita | decidido [DECISIONS 2026-11-21] | Magia. |
| Earthy Axe | Hacha de tierra | decidido [DECISIONS 2026-11-21] | Magia. |
| Earth Dragon | Dragón de tierra | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Stone | Anillo de piedra | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Rock | Anillo de roca | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Nature | Anillo de la naturaleza | decidido [DECISIONS 2026-11-21] | Magia. Como nombre del anillo: «Anillo de natur.» [DECISIONS 2026-11-24]. |
| Fire Stone | Piedra de fuego | decidido [DECISIONS 2026-11-21] | Magia. |
| Water Stone | Piedra de agua | decidido [DECISIONS 2026-11-21] | Magia. |
| Sword Stone | Espada de piedra | decidido [DECISIONS 2026-11-21] | Magia. |
| Wind Stone | Piedra de viento | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Insight | Anillo de perspicacia | decidido [DECISIONS 2026-11-21] | Magia. Como nombre del anillo: «Anillo de perspic.» [DECISIONS 2026-11-24]. |
| Power of Growth | Poder de crecimiento | decidido [DECISIONS 2026-11-21] | Magia. Como nombre del anillo: «Poder de crecim.» [DECISIONS 2026-11-24]. |
| True Sight | Visión verdadera | decidido [DECISIONS 2026-11-21] | Magia. |
| Divine | Divinidad | decidido [DECISIONS 2026-11-21] | Magia. |
| Thunder | Trueno | decidido [DECISIONS 2026-11-21] | Magia. |
| Holy Flash | Destello sagrado | decidido [DECISIONS 2026-11-21] | Magia. |
| Absorb | Absorción | decidido [DECISIONS 2026-11-21] | Magia. |
| Bless | Bendición | decidido [DECISIONS 2026-11-21] | Magia. |
| Light Dragon | Dragón de luz | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Light | Anillo de luz | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Shine | Anillo de brillo | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Glare | Anillo de fulgor | decidido [DECISIONS 2026-11-21] | Magia. |
| Create Life | Crear vida | decidido [DECISIONS 2026-11-21] | Magia. |
| Banishment | Destierro | decidido [DECISIONS 2026-11-21] | Magia. |
| Dark Thunder | Trueno oscuro | decidido [DECISIONS 2026-11-21] | Magia. |
| Dark Flash | Destello oscuro | decidido [DECISIONS 2026-11-21] | Magia. |
| Guardian | Guardián | decidido [DECISIONS 2026-11-21] | Magia. |
| Dark Stop | Bloqueo oscuro | decidido [DECISIONS 2026-11-21] | Magia. |
| Dark Dragon | Dragón oscuro | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Shadow | Anillo de sombra | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Night | Anillo de noche | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Chaos | Anillo del caos | decidido [DECISIONS 2026-11-21] | Magia. |
| Dark Pact | Pacto oscuro | decidido [DECISIONS 2026-11-21] | Magia. |
| Ring of Magic | Anillo de magia | decidido [DECISIONS 2026-11-21] | Magia. |
| Small Sword | Espada pequeña | decidido [DECISIONS 2026-11-21] | Arma. |
| Knife | Cuchillo | decidido [DECISIONS 2026-11-21] | Arma. |
| Cinquedea | Cinquedea | decidido [DECISIONS 2026-11-21] | Arma. |
| Stiletto | Estilete | decidido [DECISIONS 2026-11-21] | Arma. |
| Rapier | Estoque | decidido [DECISIONS 2026-11-21] | Arma. |
| Hunting Sword | Espada de caza | decidido [DECISIONS 2026-11-21] | Arma. |
| Eternal Sword | Espada Eterna | decidido [DECISIONS 2026-11-21] | Arma. |
| Kaizer Knuckle | Manopla Kaizer | decidido [DECISIONS 2026-11-21] | Arma. |
| King's Scroll | Pergamino del rey | decidido [DECISIONS 2026-11-21] | Objeto clave. |
| Weapon Form | Solicitud de arma | decidido [DECISIONS 2026-11-21] | Objeto clave. |
| Bracelet | Brazalete | decidido [DECISIONS 2026-11-21] | Objeto clave. |
| Water Key | Llave de agua | decidido [DECISIONS 2026-11-21] | Objeto clave. |
| Fire Key | Llave de fuego | decidido [DECISIONS 2026-11-21] | Objeto clave. |
| Wind Key | Llave de viento | decidido [DECISIONS 2026-11-21] | Objeto clave. |
| Earth Key | Llave de tierra | decidido [DECISIONS 2026-11-21] | Objeto clave. |
| Golden Grass | Hierba dorada | decidido [DECISIONS 2026-11-21] | Objeto. |
| Golden Flower | Flor dorada | decidido [DECISIONS 2026-11-21] | Objeto. |
| Golden Fruit | Fruto dorado | decidido [DECISIONS 2026-11-21] | Objeto. |
| Magic Stone | Piedra mágica | decidido [DECISIONS 2026-11-21] | Objeto. |
| Magic Crystal | Cristal mágico | decidido [DECISIONS 2026-11-21] | Objeto. |
| Magic Jewel | Joya mágica | decidido [DECISIONS 2026-11-21] | Objeto. |
| Dragon Scale | Escama de dragón | decidido [DECISIONS 2026-11-21] | Objeto. |
| Dragon Egg | Huevo de dragón | decidido [DECISIONS 2026-11-21] | Objeto. |
| Rat's Tail | Cola de rata | decidido [DECISIONS 2026-11-21] | Objeto. |
| Golden Seed | Semilla dorada | decidido [DECISIONS 2026-11-21] | Objeto. |
| Sahagin's Thorn | Espina de Sahagin | decidido [DECISIONS 2026-11-21] | Objeto. |
| Cockatrice Feather | Pluma de cocatriz | decidido [DECISIONS 2026-11-21] | Objeto. |
| Dragon Potion | Poción de dragón | decidido [DECISIONS 2026-11-21] | Objeto. |
| Glowing Gem | Gema incandescente | decidido [DECISIONS 2026-11-21] | Gema. |
| Leaf Gem | Gema de hoja | decidido [DECISIONS 2026-11-21] | Gema. |
| Feather Gem | Gema de pluma | decidido [DECISIONS 2026-11-21] | Gema. |
| Watery Gem | Gema acuosa | decidido [DECISIONS 2026-11-21] | Gema. |
| Flame Gem | Gema de llama | decidido [DECISIONS 2026-11-21] | Gema. |
| Tree Gem | Gema de árbol | decidido [DECISIONS 2026-11-21] | Gema. |
| Winged Gem | Gema alada | decidido [DECISIONS 2026-11-21] | Gema. |
| Waterfall Gem | Gema de cascada | decidido [DECISIONS 2026-11-21] | Gema. |
| Lava Gem | Gema de lava | decidido [DECISIONS 2026-11-21] | Gema. |
| Forest Gem | Gema de bosque | decidido [DECISIONS 2026-11-21] | Gema. |
| Cloudy Gem | Gema nubosa | decidido [DECISIONS 2026-11-21] | Gema. |
| Sea Gem | Gema de mar | decidido [DECISIONS 2026-11-21] | Gema. |
| Sunbeam Gem | Gema de rayo solar | decidido [DECISIONS 2026-11-21] | Gema. |
| Dead Gem | Gema muerta | decidido [DECISIONS 2026-11-21] | Gema. |
| Phoenix Gem | Gema de fénix | decidido [DECISIONS 2026-11-21] | Gema. |
| Mountain Gem | Gema de montaña | decidido [DECISIONS 2026-11-21] | Gema. |
| Tornado Gem | Gema de tornado | decidido [DECISIONS 2026-11-21] | Gema. |
| Iceberg Gem | Gema de iceberg | decidido [DECISIONS 2026-11-21] | Gema. |
| Divine Gem | Gema divina | decidido [DECISIONS 2026-11-21] | Gema. |
| Ritual Gem | Gema ritual | decidido [DECISIONS 2026-11-21] | Gema. |
| Fire Dragon Gem | Gema dragón de fuego | decidido [DECISIONS 2026-11-21] | Gema. Como nombre (19 caracteres como mucho): «Gema drag. de fuego» [DECISIONS 2026-11-24]. |
| Earth Dragon Gem | Gema dragón de tierra | decidido [DECISIONS 2026-11-21] | Gema. Como nombre: «Gema drag. tierra» [DECISIONS 2026-11-24]. |
| Wind Dragon Gem | Gema dragón de viento | decidido [DECISIONS 2026-11-21] | Gema. Como nombre: «Gema drag. viento» [DECISIONS 2026-11-24]. |
| Water Dragon Gem | Gema dragón de agua | decidido [DECISIONS 2026-11-21] | Gema. |
| Light Dragon Gem | Gema dragón de luz | decidido [DECISIONS 2026-11-21] | Gema. |
| Dark Dragon Gem | Gema dragón oscuro | decidido [DECISIONS 2026-11-21] | Gema. |
| Red door | Puerta roja | decidido [DECISIONS 2026-11-21] | Cartel; igual «Blue door» → «Puerta azul», «Green door» → «Puerta verde», «Yellow door» → «Puerta amarilla». |
| Golden Fields | Campos Dorados | decidido [DECISIONS 2026-11-21] |  |
| Golden Trees | Árboles Dorados | decidido [DECISIONS 2026-11-21] |  |
| Unknown | Desconocido | decidido [DECISIONS 2026-11-21] | Descripción de las gemas; también lugares sin nombre. |
| Cliff Forest | Bosque Escarpado | decidido [DECISIONS 2026-11-21] | Lugar; «Cliff Forest 1» → «Bosque Escarpado 1». |
| Water Shrine | Santuario del Agua | decidido [DECISIONS 2026-11-21] | Lugar; «shrine» → «santuario» también en los diálogos. «Water Shrine B1/B2» → «Sant. del Agua S1/S2». |
| Worshipping Area | Zona de Culto | decidido [DECISIONS 2026-11-21] | Lugar. |
| Disposal Valley | Valle de Desechos | decidido [DECISIONS 2026-11-21] | Lugar; «Disposal Valley 1» → «Valle de Desechos 1». |
| Tree Hideout | Refugio del Árbol | decidido [DECISIONS 2026-11-21] | Lugar. |
| Southern Hideout | Refugio del Sur | decidido [DECISIONS 2026-11-21] | Lugar. |
| Limestone Cave | Cueva de Caliza | decidido [DECISIONS 2026-11-21] | Lugar. |
| Mine Ruins | Ruinas de la Mina | decidido [DECISIONS 2026-11-21] | Lugar. |
| Iron Mill | Fundición | decidido [DECISIONS 2026-11-21] | Lugar. |
| River of Lava | Río de Lava | decidido [DECISIONS 2026-11-21] | Lugar. |
| Magic Laboratory | Laboratorio Mágico | decidido [DECISIONS 2026-11-21] | Lugar. |
| Ruins | Ruinas | decidido [DECISIONS 2026-11-21] | Lugar. |
| Library | Biblioteca | decidido [DECISIONS 2026-11-21] | Lugar. |
| Underground Lake | Lago Subterráneo | decidido [DECISIONS 2026-11-21] | Lugar. |
| Tower of Storms | Torre de Tormentas | decidido [DECISIONS 2026-11-21] | Lugar. |
| Eternal Dimension | Dimensión Eterna | decidido [DECISIONS 2026-11-21] | Lugar. |
| Sealed Labyrinth | Laberinto Sellado | decidido [DECISIONS 2026-11-21] | Lugar. |
| N.Shore of Island | Costa Norte | decidido [DECISIONS 2026-11-21] | Lugar. |
| Waterfall Cavern | Caverna de Cascada | decidido [DECISIONS 2026-11-21] | Lugar. |
| Forgotten Dais | Estrado Olvidado | decidido [DECISIONS 2026-11-21] | Lugar. |
| Warehouse | almacén | decidido [DECISIONS 2026-11-21] | Lugar del campamento (descripción y diálogos). |
| Cain Morgan | Cain Morgan | decidido [DECISIONS 2026-11-21] | Protagonista; sin tilde. |
| Lyla Satin | Lyla Satin | decidido [DECISIONS 2026-11-21] | También «Lyla». |
| Soulus | Soulus | decidido [DECISIONS 2026-11-21] |  |
| Nell Grey | Nell Grey | decidido [DECISIONS 2026-11-21] | También «Nell». |
| Matthew D. Ross III | Matthew D. Ross III | decidido [DECISIONS 2026-11-21] |  |
| Azabar Duhrin | Azabar Duhrin | decidido [DECISIONS 2026-11-21] |  |
| Gil Grey | Gil Grey | decidido [DECISIONS 2026-11-21] |  |
| Lyn Grey | Lyn Grey | decidido [DECISIONS 2026-11-21] |  |
| Evans | Evans | decidido [DECISIONS 2026-11-21] |  |
| Wallace | Wallace | decidido [DECISIONS 2026-11-21] |  |
| Marie Fowler | Marie Fowler | decidido [DECISIONS 2026-11-21] |  |
| Marcus | Marcus | decidido [DECISIONS 2026-11-21] |  |
| Solcia | Solcia | decidido [DECISIONS 2026-11-21] | Gentilicio «solciano(s)»; «the Solcian people» → «el pueblo solciano». |
| Eilsia | Eilsia | decidido [DECISIONS 2026-11-21] | Gentilicio «eilsiano(s)». |
| Aldine | Aldine | decidido [DECISIONS 2026-11-21] | Gentilicio «aldiniano(s)»; «the Aldines» → «los aldinianos»; «the Aldine army» → «el ejército de Aldine». |
| Heingaria | Heingaria | decidido [DECISIONS 2026-11-21] | Gentilicio «heingariano»; «Heingarian emblem» → «emblema heingariano». |
| the Guardians | los Guardianes | decidido [DECISIONS 2026-11-21] | Grupo; la magia «Guardian» es «Guardián». |
| the elders | los ancianos | decidido [DECISIONS 2026-11-21] |  |
| retinue | séquito | decidido [DECISIONS 2026-11-21] |  |
| research team | equipo de investigación | decidido [DECISIONS 2026-11-21] | «team leader» → «jefe del equipo». |
| captain | capitán | decidido [DECISIONS 2026-11-21] | Minúscula: cargo. |
| assistant captain | subcapitán | decidido [DECISIONS 2026-11-21] |  |
| sir | caballero | decidido [DECISIONS 2026-11-21] | Trato del árbol cortés al protagonista (en japonés «騎士さま»): «Thank you, sir.» → «Gracias, caballero.» |
| King of Aldine | rey de Aldine | decidido [DECISIONS 2026-11-21] | «the King» → «el rey»; minúscula: cargo. |
| magician | mago | decidido [DECISIONS 2026-11-21] | «'Great Magician'» → «Gran Mago», entre comillas « » (E-58); «the ancient magician» → «el mago antiguo». |
| Eternal Power | Poder Eterno | decidido [DECISIONS 2026-11-21] |  |
| the Eternal cage | la jaula eterna | decidido [DECISIONS 2026-11-21] |  |
| Eternity | la eternidad | decidido [DECISIONS 2026-11-21] |  |
| the mainland | el continente | decidido [DECISIONS 2026-11-21] | También «continent». |
| the water gate | la compuerta | decidido [DECISIONS 2026-11-21] |  |
| emblem | emblema | decidido [DECISIONS 2026-11-21] |  |
| curse | maldición | decidido [DECISIONS 2026-11-21] | «cursed» → «maldito/a». |
| Gravestone | Lápida | decidido [DECISIONS 2026-11-21] | Cartel. |
| Tombstone | Tumba | decidido [DECISIONS 2026-11-21] | Cartel. |
| Inventory | Inventario | decidido [DECISIONS 2026-11-21] |  |
| Equipment | Equipo | decidido [DECISIONS 2026-11-21] |  |
| Status | Estado | decidido [DECISIONS 2026-11-21] |  |
| Items | Objetos | decidido [DECISIONS 2026-11-21] |  |
| Rings | Anillos | decidido [DECISIONS 2026-11-21] | «Ring» → «Anillo». |
| Weapons | Armas | decidido [DECISIONS 2026-11-21] |  |
| Sound | Sonido | decidido [DECISIONS 2026-11-21] |  |
| Controller | Mando | decidido [DECISIONS 2026-11-21] | «Controller Configuration» → «Configuración del mando». Decidido por el usuario frente a «control» (E-12). |
| Collection | Colección | decidido [DECISIONS 2026-11-21] |  |
| End | Salir | decidido [DECISIONS 2026-11-21] | Menú principal. |
| Use | Usar | decidido [DECISIONS 2026-11-21] |  |
| Back | Volver | decidido [DECISIONS 2026-11-21] |  |
| Cancel | Cancelar | decidido [DECISIONS 2026-11-21] |  |
| Reset | Reiniciar | decidido [DECISIONS 2026-11-21] | En el altar (botón △, unas 6 letras antes del ícono siguiente): «Quitar», que saca las gemas puestas [DECISIONS 2026-11-24]. |
| Yes | Sí | decidido [DECISIONS 2026-11-21] |  |
| No | No | decidido [DECISIONS 2026-11-21] |  |
| Load | Cargar | decidido [DECISIONS 2026-11-21] |  |
| Save | Guardar | decidido [DECISIONS 2026-11-21] |  |
| Load Data | Cargar partida | decidido [DECISIONS 2026-11-21] | «Load Data - » → «Cargar - ». |
| Save Data | Guardar partida | decidido [DECISIONS 2026-11-21] | «Save Data - » → «Guardar - ». |
| MEMORY CARD(PS2) | MEMORY CARD(PS2) | decidido [DECISIONS 2026-11-21] | Como el original. |
| Slot | ranura | decidido [DECISIONS 2026-11-21] |  |
| Type | Tipo | decidido [DECISIONS 2026-11-21] | «Type-A» → «Tipo A». |
| Item | Objeto | decidido [DECISIONS 2026-11-21] |  |
| Weapon | Arma | decidido [DECISIONS 2026-11-21] |  |
| Empty | Vacío | decidido [DECISIONS 2026-11-21] |  |
| NO EQUIP | SIN EQUIPO | decidido [DECISIONS 2026-11-21] |  |
| -- Unequipped -- | -- Sin equipar -- | decidido [DECISIONS 2026-11-21] |  |
| QTY Owned | Tienes | decidido [DECISIONS 2026-11-21] | También «Owned». |
| Vibration | Vibración | decidido [DECISIONS 2026-11-21] |  |
| Sensitivity | Sensibilidad | decidido [DECISIONS 2026-11-21] |  |
| Analog button | botón analógico | decidido [DECISIONS 2026-11-21] | «_577Botón analóg.» donde no entra. |
| BGM | música | decidido [DECISIONS 2026-11-21] | «Vol. de música». |
| Sound-Effect | efectos | decidido [DECISIONS 2026-11-21] | «Volumen de efectos». |
| Stereo | Estéreo | decidido [DECISIONS 2026-11-21] |  |
| Mono | Mono | decidido [DECISIONS 2026-11-21] |  |
| Always | Siempre | decidido [DECISIONS 2026-11-21] | «Not Always» → «No siempre». |
| Level up! | ¡Sube de nivel! | decidido [DECISIONS 2026-11-21] |  |
| Chief Medic | jefa médica | decidido [DECISIONS 2026-11-21] | Marie Fowler. |
