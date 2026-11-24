"""Chequeos propios de Eternal Ring para loc.py (ver loc.json, «hooks»).

  encode(key, es)        lo que ocupa el texto en el juego, para «max» (T-4):
                         en los diálogos, una palabra por carácter o código
                         (el búfer admite 256); en el resto, bytes Windows-1252
                         con \\r\\n como salto de línea.
  missing_chars(key, es) los caracteres que la fuente no tiene (T-5).
  check(key, item, es)   el ancho de la caja (T-3).
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adapter
import font_es

CODES = re.compile(r'\{[0-9a-f]+\}|\{cr\}|_[0-9]{3}|%[-+0-9.]*[sdifxXu]|~')
FONT = set(chr(c) for c in font_es.ORIGINAL) | set(font_es.NEW) | {' ', '\n'}
# En menús y descripciones, _ y @ son códigos de control: no se dibujan.

# T-3 (TECH.md): renglones y caracteres por renglón.
DIALOG_LINES, DIALOG_WIDTH, DIALOG_LAST = 4, 35, 32
DESC_WIDTH = 30             # 32 en una prueba, 30 en otra: el seguro
DESC_LINES = 2              # la ventana de objeto obtenido muestra 2 [DECISIONS 2026-11-24]
NAME_MAX = 19               # la lista de anillos copia el nombre en 20 bytes, con el \0
PLACE_WIDTH = 18            # nombre del lugar en la pantalla de estado
PLACES = (0x249940, 0x24a2a0)
MENU_GROWTH = 1.25          # resto del ejecutable: aviso si crece más (se revisa en el juego)

# Fuente grande (FIRE, EARTH..., LEVEL, H P, EXP, NEXT): solo tiene lo de la
# tabla del ejecutable en 0x243d60; lo demás sale como «0».
BIG_FONT = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ()[]!?+-/* ')
BIG = [(0x243ce0, 0x243d50), (0x25d570, 0x25d5c8)]


def exe_offset(key):
    return int(key.split('#')[1], 16) if key.startswith('menus/exe#') else None


def big_font(key):
    o = exe_offset(key)
    return o is not None and any(a <= o < b for a, b in BIG)


def encode(key, es):
    if key.startswith('dialogo/'):
        return bytes(len(adapter.encode_words(es)))
    return adapter.encode_field(es)


def missing_chars(key, es):
    font = BIG_FONT if big_font(key) else FONT
    return sorted({c for c in CODES.sub('', es) if c not in font})


def check(key, item, es):
    out = []
    lines = CODES.sub('', es).rstrip('\n').split('\n')
    if key.startswith('dialogo/'):
        if len(lines) > DIALOG_LINES:
            out.append(('caja', 'T-3', '%d renglones; la caja muestra %d' % (len(lines), DIALOG_LINES)))
        for n, l in enumerate(lines, 1):
            lim = DIALOG_LAST if n == DIALOG_LINES else DIALOG_WIDTH
            if len(l) > lim:
                out.append(('caja', 'T-3', 'renglón %d: %d caracteres, el máximo es %d' % (n, len(l), lim)))
    elif key.startswith('objetos/') and key.endswith('.nombre'):
        if len(lines[0]) > NAME_MAX:
            out.append(('caja', 'T-3', 'nombre: %d caracteres, la lista muestra %d' % (len(lines[0]), NAME_MAX)))
    elif key.startswith('objetos/') and key.endswith('.desc'):
        if len(lines) > DESC_LINES:
            out.append(('caja', 'T-3', '%d renglones; la ventana de objeto obtenido muestra %d' % (len(lines), DESC_LINES)))
        for n, l in enumerate(lines, 1):
            if len(l) > DESC_WIDTH:
                out.append(('caja', 'T-3', 'renglón %d: %d caracteres, el máximo es %d' % (n, len(l), DESC_WIDTH)))
    elif key.startswith('menus/'):
        en = CODES.sub('', item['en'])
        o = exe_offset(key)
        if en != en.rstrip():
            if len(lines[0]) > len(en):
                out.append(('caja', 'T-3', 'campo de ancho fijo: %d caracteres, el original ocupa %d (con espacios)'
                            % (len(lines[0]), len(en))))
        elif PLACES[0] <= o < PLACES[1]:
            if len(lines[0]) > PLACE_WIDTH:
                out.append(('caja', 'T-3', 'lugar: %d caracteres, la pantalla de estado muestra %d'
                            % (len(lines[0]), PLACE_WIDTH)))
        elif len(lines[0]) > max(len(en) * MENU_GROWTH, len(en) + 2):
            out.append(('caja', 'T-3', '%d caracteres, el original %d: ver en el juego si entra'
                        % (len(lines[0]), len(en))))
    return out
