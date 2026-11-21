"""Diálogos de la versión japonesa (SLPS-25001), solo de apoyo (STYLE E-1).

Uso: python3 -I tools/ja.py ISO_JAPONESA SALIDA.jsonl

Escribe {key, ja} por mensaje, con las mismas claves que el adaptador
(dialogo/<escenario>#NNN). El número de mensajes no coincide siempre con el
inglés (ver TECH.md). El texto japonés no es Shift-JIS: cada carácter es el
índice de un signo de la fuente (`(alto - 1) * 42 + (bajo - 1)`), y
tools/ja_glyphs.txt dice qué signo es cada índice (transcrito a mano, 20 por
renglón).
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stage as S  # noqa: E402

GLYPHS = ''.join(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ja_glyphs.txt'),
                      encoding='utf-8').read().split('\n'))


def char(c):
    if c == S.LINE:
        return '\n'
    if c >> 16:
        return '{%x}' % c
    hi, lo = (c >> 8) & 0xff, c & 0xff
    if hi:
        i = (hi - 1) * 42 + (lo - 1)
        return GLYPHS[i] if 0 <= i < len(GLYPHS) else '{%x}' % c
    return chr(lo)


def main(iso_path, out_path):
    iso = open(iso_path, 'rb')
    _, lba, size = S.iso_dir_entry(iso, 'ERDATA.BIN')
    iso.seek(lba * S.SECTOR)
    er = io.BytesIO(iso.read(size))
    n_msgs = 0
    with open(out_path, 'w', encoding='utf-8') as out:
        for n, stage in S.stages(er):
            _, ins = S.script(stage)
            for k, (_, _, codes) in enumerate(S.messages(ins)):
                out.write(json.dumps({'key': 'dialogo/%d#%03d' % (n, k),
                                      'ja': ''.join(char(c) for c in codes)}, ensure_ascii=False) + '\n')
                n_msgs += 1
    print('%s: %d mensajes' % (out_path, n_msgs))


if __name__ == '__main__':
    main(*sys.argv[1:])
