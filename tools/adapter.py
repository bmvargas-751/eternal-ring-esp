"""Adaptador de Eternal Ring (PAL): el texto del juego en el formato común del
kit (source.jsonl) y de vuelta al juego.

Uso:
  python3 -I tools/adapter.py export CARPETA SALIDA.jsonl
  python3 -I tools/adapter.py roundtrip CARPETA
  python3 -I tools/adapter.py build ISO_ORIGINAL ISO_NUEVA [translation/]

CARPETA tiene ERDATA.BIN y SLES_500.51 sacados de la ISO original. `build`
copia la ISO, le pone las letras españolas (font_es.py) y escribe la
traducción (lo que falta queda en inglés).

Qué texto hay (TECH.md):
  dialogo/<entrada>#NNN     los 505 mensajes de los guiones de los escenarios
  objetos/<tabla>#NNN.nombre / .desc
                            magias, armas, objetos clave, objetos y gemas
                            (ERDATA, entrada 4; las armas también en 801–809)
  menus/exe#<desplazamiento> textos del ejecutable

Códigos (T-1): en los diálogos, cada palabra que no es una letra va como
{hex} (por ejemplo {108f8}, un color); en el ejecutable, _NNN (color), ~
(fuente grande) y los formatos %s, %3d...
"""
import json, os, re, shutil, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stage as S
import font_es

ENC = 'cp1252'

# --- diálogos ----------------------------------------------------------------

CODE = re.compile(r'\{([0-9a-f]+)\}')


def decode_words(codes):
    out = []
    for w in codes:
        if w == S.LINE:
            out.append('\n')
        elif 0x20 <= w < 0x100 and w not in (0x7b, 0x7d, 0x7f):
            try:
                out.append(bytes([w]).decode(ENC))
            except UnicodeDecodeError:
                out.append('{%x}' % w)
        else:
            out.append('{%x}' % w)
    return ''.join(out)


def encode_words(s):
    out, i = [], 0
    while i < len(s):
        m = CODE.match(s, i)
        if m:
            out.append(int(m.group(1), 16)); i = m.end(); continue
        ch = s[i]
        out.append(S.LINE if ch == '\n' else ch.encode(ENC)[0])
        i += 1
    return out


# --- campos de texto de largo fijo (descripciones y ejecutable) ----------------

def decode_field(b):
    t = b.decode(ENC)
    t = t.replace('\r\n', '\n')
    t = re.sub(r'\r', '{cr}', t)
    return t


def encode_field(s):
    s = s.replace('\n', '\r\n').replace('{cr}', '\r')
    return s.encode(ENC)


# Tablas de la entrada 4: (nombre, inicio, registro, registros,
# campo del nombre, inicio de la descripción, campo de la descripción).
# Los campos van en bytes con el \0; detrás vienen datos (TECH.md).
TABLES = [
    ('magia', 0x1a57d0, 0x100, 127, 0x18, 0x18, 0xa8),
    ('armas', 0x1ad7cc, 0x100, 9, 0x14, 0x14, 0xac),
    ('clave', 0x1ae714, 0x80, 8, 0x14, 0x14, 0x3e),
    ('objetos', 0x1b0014, 0x80, 20, 0x14, 0x14, 0x40),
    ('gemas', 0x1b2714, 0x80, 26, 0x18, 0x18, 0x64),
]
WEAPON_FILES = 801          # el arma k de la tabla está también en la entrada 801 + k
WEAPON_NAME, WEAPON_DESC = (0x3c, 0x10), (0x50, 0x40)

# Textos del ejecutable: zonas (desplazamientos del archivo) y lo que no se traduce.
EXE_RANGES = [(0x243ce0, 0x24a780), (0x255100, 0x255470), (0x256280, 0x256d60), (0x257540, 0x257c60),
              (0x25d558, 0x25d740)]
EXE_SKIP = re.compile(r'cdrom0|host0|\\|\.(PSS|ADX|BIN|ICO|IRX)|icon\.sys|BESLES|0123456789|'
                      r'^(MRing|ARing|Aring) Name$|^WeaponName$|^(PS2D|abcd)$')
EXE_CODE = re.compile(r'_[0-9]{3}|%[-+0-9.]*[sdifxXu]|~')
EXE_MAX = 79


class Field:
    """Un texto que se escribe en su lugar: (archivo, desplazamiento, campo)."""
    def __init__(self, key, places, note):
        self.key, self.places, self.note = key, places, note   # places: [(dónde, desplazamiento, campo)]


def _cstr(b, off, size):
    raw = b[off:off + size]
    return raw[:raw.index(b'\0')] if b'\0' in raw else None


def read_sources(er, exe, er_off=0, exe_off=0):
    """Todo el texto: (lista de dicts del formato común, campos, diálogos)."""
    items, fields = [], []
    # Diálogos
    dialogs = []
    for n, st in S.stages(er, er_off):
        off, ins = S.script(st)
        for k, (i, p, codes) in enumerate(S.messages(ins)):
            key = 'dialogo/%d#%03d' % (n, k)
            en = decode_words(codes)
            assert encode_words(en) == list(codes), key
            items.append({'key': key, 'en': en, 'max': 256, 'note': 'diálogo, escenario %d' % n})
            dialogs.append((key, n, i))
    # Tablas de la entrada 4 (y copias de las armas)
    e4 = S.entry_offset(er, 4, er_off)
    er.seek(er_off + e4); b4 = er.read(0x1b8000)
    for name, start, stride, count, nsize, doff, dsize in TABLES:
        for r in range(count):
            a = start + r * stride
            nm = _cstr(b4, a, nsize)
            if not nm or not all(0x20 <= c < 0x7f for c in nm):
                continue
            for part, off, size, extra in (('nombre', a, nsize, WEAPON_NAME), ('desc', a + doff, dsize, WEAPON_DESC)):
                orig = _cstr(b4, off, size)
                if orig is None:
                    continue
                places = [('er', e4 + off, size)]
                if name == 'armas':
                    wo = S.entry_offset(er, WEAPON_FILES + r, er_off)
                    er.seek(er_off + wo + extra[0]); wb = er.read(extra[1])
                    if _cstr(wb, 0, extra[1]) == orig:
                        places.append(('er', wo + extra[0], extra[1]))
                key = 'objetos/%s#%03d.%s' % (name, r, part)
                fields.append(Field(key, places, ''))
                items.append({'key': key, 'en': decode_field(orig), 'max': min(p[2] for p in places) - 1,
                              'note': '%s de %s' % ('nombre' if part == 'nombre' else 'descripción', name)})
    # Ejecutable. Los textos están en registros de largo fijo (menús cada 0x50,
    # lugares cada 0x18...): el campo llega hasta el próximo byte que no es 0,
    # pero nunca más allá de la distancia a la cadena anterior ni a la siguiente
    # (así no pisa registros vacíos de la misma lista), y como mucho EXE_MAX.
    exe.seek(exe_off); e = exe.read()
    for lo, hi in EXE_RANGES:
        hits = []
        for m in re.finditer(rb'[\x20-\x7e]{2,}\x00', e[lo:hi]):
            a, end = lo + m.start(), lo + m.end() - 1
            j = re.search(rb'[A-Za-z_%]', e[a:end])
            if a % 4 and j and j.start() <= 3 and (a + j.start()) % 4 == 0 and e[a - 1] == 0 \
                    and not e[a:a + j.start()].isalnum():
                a += j.start()                     # bytes de un número pegados delante («`?Cain Morgan»)
            hits.append((a, end))
        for k, (a, end) in enumerate(hits):
            s = e[a:end].decode('ascii')
            if len(re.findall('[A-Za-z]', EXE_CODE.sub('', s))) < 2 or not s.strip() or EXE_SKIP.search(s):
                continue
            z = end
            while z < len(e) and e[z] == 0:
                z += 1
            size = z - a
            if k + 1 < len(hits):
                size = min(size, hits[k + 1][0] - a)
            if k > 0:
                size = min(size, max(a - hits[k - 1][0], end - a + 1))
            size = min(size, EXE_MAX + 1)
            key = 'menus/exe#%06x' % a
            fields.append(Field(key, [('exe', a, size)], ''))
            items.append({'key': key, 'en': s, 'max': size - 1, 'note': 'ejecutable, campo de %d bytes' % (size - 1)})
    return items, fields, dialogs


# --- de vuelta al juego ------------------------------------------------------------

def write_fields(fields, texts, er, exe, er_off, exe_off, errors):
    for f in fields:
        es = texts[f.key]
        b = encode_field(es)
        for where, off, size in f.places:
            if len(b) + 1 > size:
                errors.append('%s: %d bytes, el campo admite %d' % (f.key, len(b), size - 1))
                continue
            fh, base = (er, er_off) if where == 'er' else (exe, exe_off)
            fh.seek(base + off); fh.write(b + b'\0')


def write_dialogs(dialogs, texts, en, er, er_off, er_size, errors):
    by_stage = {}
    for key, n, i in dialogs:
        if texts[key] != en[key]:
            by_stage.setdefault(n, {})[i] = key
    for n, changes in sorted(by_stage.items()):
        st = S.read_stage(er, n, er_off)
        off, ins = S.script(st)
        new = {}
        for i, key in changes.items():
            try:
                c = encode_words(texts[key])
            except UnicodeEncodeError as x:
                errors.append('%s: no se puede escribir %r' % (key, x.object[x.start:x.end])); continue
            if len(c) > 256:
                errors.append('%s: %d caracteres, el búfer admite 256' % (key, len(c))); continue
            new[i] = c
        st2 = S.with_script(st, S.rebuild(ins, new))
        er_size = S.place(er, n, st2, er_off, er_size)
    return er_size, len(by_stage)


def load_translation(path):
    out = {}
    if path and os.path.isdir(path):
        for root, _, files in os.walk(path):
            for fn in sorted(files):
                if fn.endswith('.jsonl'):
                    for line in open(os.path.join(root, fn), encoding='utf-8'):
                        if line.strip():
                            x = json.loads(line); out[x['key']] = x['es']
    return out


def build(iso_src, iso_out, tr_dir):
    shutil.copyfile(iso_src, iso_out)
    f = open(iso_out, 'r+b')
    pos, er_lba, er_size = S.iso_dir_entry(f, 'ERDATA.BIN')
    _, exe_lba, _ = S.iso_dir_entry(f, 'SLES_500.51')
    er_off, exe_off = er_lba * S.SECTOR, exe_lba * S.SECTOR
    items, fields, dialogs = read_sources(f, f, er_off, exe_off)
    en = {x['key']: x['en'] for x in items}
    tr = load_translation(tr_dir)
    unknown = sorted(set(tr) - set(en))
    texts = {k: tr.get(k, v) for k, v in en.items()}
    errors = ['clave desconocida: %s' % k for k in unknown]
    font_es.apply(f, er_off, f, exe_off)
    write_fields(fields, texts, f, f, er_off, exe_off, errors)
    er_size, moved = write_dialogs(dialogs, texts, en, f, er_off, er_size, errors)
    S.set_iso_size(f, 'ERDATA.BIN', er_size)
    S.patch_exe(f, exe_off)
    f.close()
    if errors:
        os.remove(iso_out)
        sys.exit('No se armó la ISO:\n  ' + '\n  '.join(errors))
    done = sum(1 for k in en if k in tr)
    print('%s: %d de %d textos traducidos, %d escenarios movidos al final de ERDATA' % (iso_out, done, len(en), moved))


def roundtrip(folder):
    """Escribe el original sobre una copia en memoria y comprueba que no cambie nada."""
    import io
    er_b = open(os.path.join(folder, 'ERDATA.BIN'), 'rb').read()
    exe_b = open(os.path.join(folder, 'SLES_500.51'), 'rb').read()
    er, exe = io.BytesIO(bytearray(er_b)), io.BytesIO(bytearray(exe_b))
    items, fields, dialogs = read_sources(er, exe)
    en = {x['key']: x['en'] for x in items}
    errors = []
    write_fields(fields, en, er, exe, 0, 0, errors)
    assert not errors, errors
    same_er, same_exe = er.getvalue() == er_b, exe.getvalue() == exe_b
    # Diálogos: todos los mensajes rearmados desde «en», con rebuild.
    same_dlg = True
    for n, st in S.stages(er):
        off, ins = S.script(st)
        new = {i: encode_words(en['dialogo/%d#%03d' % (n, k)]) for k, (i, p, c) in enumerate(S.messages(ins))}
        same_dlg &= S.rebuild(ins, new) == st[off:off + S.u32(st, 4)]
    kinds = {}
    for x in items:
        kinds[x['key'].split('/')[0]] = kinds.get(x['key'].split('/')[0], 0) + 1
    print('textos:', len(items), kinds)
    print('ERDATA igual:', same_er, '| ejecutable igual:', same_exe, '| guiones iguales:', same_dlg)
    return same_er and same_exe and same_dlg


def export(folder, out):
    er = open(os.path.join(folder, 'ERDATA.BIN'), 'rb')
    exe = open(os.path.join(folder, 'SLES_500.51'), 'rb')
    items, _, _ = read_sources(er, exe)
    with open(out, 'w', encoding='utf-8') as w:
        for x in items:
            w.write(json.dumps(x, ensure_ascii=False) + '\n')
    print(out, len(items), 'textos')


if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'export':
        export(*args)
    elif cmd == 'roundtrip':
        sys.exit(0 if roundtrip(*args) else 1)
    elif cmd == 'build':
        build(args[0], args[1], args[2] if len(args) > 2 else None)
    else:
        sys.exit(__doc__)
