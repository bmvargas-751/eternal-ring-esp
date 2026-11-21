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

CODES = re.compile(r'\{[0-9a-f]+\}|\{cr\}|_[0-9]{3}|%[-+0-9.]*[sdifxXu]')
FONT = set(chr(c) for c in font_es.ORIGINAL) | set(font_es.NEW) | {' ', '\n'}
# En menús y descripciones, _ y @ son códigos de control: no se dibujan.

# T-3 (TECH.md): renglones y caracteres por renglón.
DIALOG_LINES, DIALOG_WIDTH, DIALOG_LAST = 4, 35, 32
DESC_WIDTH = 32


def encode(key, es):
    if key.startswith('dialogo/'):
        return bytes(len(adapter.encode_words(es)))
    return adapter.encode_field(es)


def missing_chars(key, es):
    return sorted({c for c in CODES.sub('', es) if c not in FONT})


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
    elif key.startswith('objetos/') and key.endswith('.desc'):
        for n, l in enumerate(lines, 1):
            if len(l) > DESC_WIDTH:
                out.append(('caja', 'T-3', 'renglón %d: %d caracteres, el máximo es %d' % (n, len(l), DESC_WIDTH)))
    elif key.startswith('menus/'):
        en = CODES.sub('', item['en'])
        if en != en.rstrip() and len(lines[0]) > len(en):
            out.append(('caja', 'T-3', 'campo de ancho fijo: %d caracteres, el original ocupa %d (con espacios)'
                        % (len(lines[0]), len(en))))
    return out
