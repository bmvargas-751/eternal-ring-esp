"""Escenarios y guiones de Eternal Ring (PAL): leerlos y reescribirlos con
mensajes de otro largo.

Cómo está hecho (TECH.md):
  - ERDATA.BIN 0x3d40: tabla de 16 escenarios {sector, sectores}; el LBA del
    disco es 0x6a1 + 0x10 + sector. Se cargan enteros en RAM 0x55ca80.
  - Cabecera del escenario: +0 tamaño total, +4 tamaño del guion, +8 y +0xc en
    0 en los 16 (sin uso). En 0x138..0x154, ocho desplazamientos a secciones.
  - El guion no tiene desplazamiento propio: el juego recorre las secciones en
    orden (0x117xxx) y el guion es la que sigue a las de objetos; la siguiente
    empieza en guion + tamaño. Por eso no puede crecer en su lugar.

Lo que hace este módulo para que un guion crezca sin mover nada:
  - el guion nuevo va al final del escenario; su desplazamiento, en la
    cabecera +8, y su tamaño, en +0xc. El viejo queda donde está y +4 no se
    toca: el juego lo usa para calcular dónde empieza la sección siguiente;
  - parche del ejecutable en 0x1175fc: si cabecera+8 no es 0, el puntero al
    guion es cabecera + cabecera[+8] (código en 0x178620, en la cadena de
    comparaciones que font_es.py deja sin uso);
  - el escenario entero va al final de ERDATA.BIN (sector alineado) y su fila
    de la tabla apunta ahí; el tamaño de ERDATA.BIN en el directorio de la ISO
    se agranda para cubrirlo.
"""
import struct

ER_LBA = 0x6a1
STAGE_TABLE = 0x3d40
STAGES = 16
SECTOR = 0x800
EXE_BASE = 0xff000
HOOK = 0x1175fc            # lw v0, 4(a0) ; sw s7, 0x14(v1)
CAVE = 0x178620

LINE = 0x40000             # salto de línea en un mensaje
MSG, JUMP, COND, EXPR = 0x19d, 0x197, 0x192, 0x196


def u32(b, o):
    return struct.unpack_from('<I', b, o)[0]


def table(er, er_off=0):
    er.seek(er_off + STAGE_TABLE)
    return [struct.unpack('<II', er.read(8)) for _ in range(STAGES)]


def read_stage(er, n, er_off=0):
    s, c = table(er, er_off)[n]
    er.seek(er_off + (s + 0x10) * SECTOR)
    size = struct.unpack('<I', er.read(4))[0]
    er.seek(er_off + (s + 0x10) * SECTOR)
    return er.read(size)


# --- bytecode -------------------------------------------------------------

def isize(w):
    """Tamaño de una instrucción en palabras, o None si no es válida."""
    op, lo = w >> 16, w & 0xffff
    if op == MSG: return 2 + lo
    if op == EXPR: return 1 + lo
    if op == COND: return 2 + ((lo >> 8) & 0xff) * 5
    if op in (0x190, 0x191, 0x194, 0x195, JUMP): return 1
    if op < 0x190 or op in (0x193, 0x198, 0x199, 0x19a, 0x19b, 0x19c):
        return None if lo > 40 else 1 + 2 * lo
    return None


def walk(b, start, size):
    """Lista de (desplazamiento, palabras) o None si no cubre justo `size`."""
    out, o, end = [], start, start + size
    while o < end:
        n = isize(u32(b, o))
        if n is None or o + 4 * n > end:
            return None
        out.append((o, list(struct.unpack_from('<%dI' % n, b, o))))
        o += 4 * n
    return out


def find_script(stage):
    """Desplazamiento del guion original dentro del escenario."""
    size = u32(stage, 4)
    hits = []
    for o in range(0, len(stage) - size + 1, 4):
        if u32(stage, o) >> 16 == 0x190 and walk(stage, o, size) is not None:
            hits.append(o)
    assert len(hits) == 1, [hex(h) for h in hits]
    return hits[0]


def script(stage):
    """El guion en uso: el reubicado (cabecera +8 y +0xc) si lo hay, si no el original."""
    if u32(stage, 8):
        off, size = u32(stage, 8), u32(stage, 0xc)
    else:
        off, size = find_script(stage), u32(stage, 4)
    return off, walk(stage, off, size)


def messages(ins):
    """Los mensajes como (índice de instrucción, parámetro, lista de códigos)."""
    return [(i, w[1], w[2:]) for i, (o, w) in enumerate(ins) if w[0] >> 16 == MSG]


def text(codes):
    return ''.join('\n' if c == LINE else bytes([c]).decode('cp1252') if c < 0x100 else '{%x}' % c
                   for c in codes)


def codes(s):
    out = []
    for ch in s:
        out.append(LINE if ch == '\n' else ch.encode('cp1252')[0])
    return out


def rebuild(ins, new_msgs):
    """Arma el guion con los mensajes cambiados ({índice: códigos}) y corrige
    los saltos 0x197 (pc = pc + 4 + desplazamiento × 4)."""
    words = []
    for i, (o, w) in enumerate(ins):
        if i in new_msgs:
            c = new_msgs[i]
            w = [(MSG << 16) | len(c), w[1]] + list(c)
        words.append(w)
    new_off, pos = {}, 0
    for (o, _), w in zip(ins, words):
        new_off[o] = pos
        pos += 4 * len(w)
    for (o, _), w in zip(ins, words):
        if w[0] >> 16 == JUMP:
            d = w[0] & 0xffff
            d -= 0x10000 if d & 0x8000 else 0
            target = o + 4 + 4 * d
            nd = (new_off[target] - new_off[o] - 4) // 4
            assert -0x8000 <= nd < 0x8000
            w[0] = (JUMP << 16) | (nd & 0xffff)
    return b''.join(struct.pack('<%dI' % len(w), *w) for w in words)


def with_script(stage, blob):
    """Escenario con el guion nuevo al final (alineado a 16) y la cabecera al día."""
    base = bytearray(stage[:u32(stage, 8)] if u32(stage, 8) else stage)
    base += bytes(-len(base) % 16)
    off = len(base)
    base += blob
    struct.pack_into('<I', base, 0, len(base))
    struct.pack_into('<II', base, 8, off, len(blob))
    return bytes(base)


# --- disco y ejecutable ----------------------------------------------------

def place(er, n, stage, er_off=0, er_size=None):
    """Escribe el escenario al final de ERDATA (o donde ya estaba reubicado, si
    cabe) y actualiza la tabla. Devuelve el nuevo tamaño de ERDATA."""
    t = table(er, er_off)
    s, c = t[n]
    need = (len(stage) + SECTOR - 1) // SECTOR
    need += -need % 0x10
    end_sector = er_size // SECTOR
    if s + 0x10 + c == end_sector and s + 0x10 >= max(x + 0x10 + y for i, (x, y) in enumerate(t) if i != n):
        start = s + 0x10                       # ya es el último: se reescribe ahí
    else:
        start = end_sector
    er.seek(er_off + start * SECTOR)
    er.write(stage + bytes(need * SECTOR - len(stage)))
    er.seek(er_off + STAGE_TABLE + 8 * n)
    er.write(struct.pack('<II', start - 0x10, need))
    return max(er_size, (start + need) * SECTOR)


def patch_exe(exe, exe_off):
    def put(addr, words):
        exe.seek(exe_off + addr - EXE_BASE)
        exe.write(struct.pack('<%dI' % len(words), *words))

    def get(addr):
        exe.seek(exe_off + addr - EXE_BASE)
        return struct.unpack('<I', exe.read(4))[0]
    j = lambda a: 0x08000000 | (a >> 2)
    hook = [j(CAVE), 0x8c820004]               # j cave ; lw v0, 4(a0)
    cave = [0x8c880008,                        # lw    t0, 8(a0)
            0x00884821,                        # addu  t1, a0, t0
            0x02e0502d,                        # daddu t2, s7, zero
            0x0128500b,                        # movn  t2, t1, t0
            0xac6a0014,                        # sw    t2, 0x14(v1)
            j(HOOK + 8),                       # j     0x117604
            0]                                 # nop
    assert [get(HOOK), get(HOOK + 4)] in ([0x8c820004, 0xac770014], hook), hex(get(HOOK))
    put(HOOK, hook)
    put(CAVE, cave)


def iso_dir_entry(iso, name):
    """(posición del registro, LBA, tamaño) de un archivo del directorio raíz."""
    iso.seek(16 * SECTOR + 156)
    root = iso.read(34)
    lba, size = u32(root, 2), u32(root, 10)
    iso.seek(lba * SECTOR)
    d = iso.read(size)
    i = 0
    while i < len(d):
        n = d[i]
        if n == 0:
            i = (i // SECTOR + 1) * SECTOR
            continue
        nm = d[i + 33:i + 33 + d[i + 32]].decode('ascii', 'replace')
        if nm.split(';')[0] == name:
            return lba * SECTOR + i, u32(d, i + 2), u32(d, i + 10)
        i += n
    raise KeyError(name)


def set_iso_size(iso, name, size):
    pos, lba, old = iso_dir_entry(iso, name)
    iso.seek(pos + 10)
    iso.write(struct.pack('<I', size) + struct.pack('>I', size))
