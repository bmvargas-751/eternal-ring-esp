"""Letras y signos españoles para la fuente de Eternal Ring (PAL).

La fuente de 1 byte (77 signos de 16×24 a 8 bits, se ven las 12 columnas de la
izquierda) no tiene letras españolas ni varios signos. Este script:
  - arma los signos de NEW a partir de las letras del propio juego o dibujados
    a mano;
  - los guarda en las casillas de relleno del final de la fuente japonesa de
    2 bytes (sin uso en el PAL), que quedan justo antes de los signos ASCII:
    el signo de índice -k está en ASCII - k × 0x180;
  - en el ejecutable, cambia la cadena de comparaciones (carácter → índice del
    signo) de las tres funciones que dibujan texto por una búsqueda en una
    tabla de 256 bytes (índice con signo; 0x7f = no se dibuja), y en las dos
    que leen cadenas de bytes apaga el desvío a la fuente japonesa (byte
    ≥ 0x80 = primer byte de Shift-JIS), que el texto PAL no usa.

Codificación del juego: Windows-1252, un carácter por palabra (diálogos) o por
byte (menús y descripciones).

Uso: python3 -I font_es.py --preview ERDATA.BIN vista.png   (no cambia nada)
     python3 -I font_es.py ERDATA.BIN SLES_500.51 [vista.png]
     python3 -I font_es.py --iso IMAGEN.iso [vista.png]
Los archivos se cambian en su lugar.
"""
import struct, sys

FONT = 0x4e8090            # desplazamiento de la fuente en ERDATA.BIN (entrada 4)
ASCII = FONT + 0xb1b00     # primer signo de 1 byte
GLYPH = 0x180              # 16 × 24, 8 bits
W, H = 16, 24
EXE_BASE = 0xff000         # dirección = desplazamiento + 0xff000
TABLE_AT = 0x17a0c0        # tabla de 256 bytes (dentro de la cadena de los diálogos)
SKIP = 0x7f
ER_LBA = 0x6a1
ENCODING = 'cp1252'

# Las tres cadenas de comparaciones: (inicio, salto final "bne t0, v0(=1)",
# primera palabra original). Al entrar, v1 = carácter & 0xff; al salir tienen que
# quedar s1 = índice, t0 = 1 si se dibuja, v0 = 1 y v1 sin tocar.
CHAINS = [
    (0x17a088, 0x17a1c8, 0x2465ffd0),   # diálogos, función 0x179e60 (palabras)
    (0x177d24, 0x177e80, 0x2c42000a),   # cadenas de bytes, función 0x177b20
    (0x1784e4, 0x178640, 0x2c42000a),   # cadenas de bytes, función 0x1782f0
]
# "beq v0, zero" después de "andi v0, byte, 0x80": pasa a "beq zero, zero".
SJIS = [(0x177be8, 0x10400038), (0x1783b0, 0x10400038)]

# Mapa original del juego (de la cadena de comparaciones).
ORIGINAL = {}
for i in range(10): ORIGINAL[0x30 + i] = i
for i in range(26): ORIGINAL[0x41 + i] = 10 + i; ORIGINAL[0x61 + i] = 36 + i
for k, c in enumerate(".,()!?'\""):
    ORIGINAL[ord(c)] = 62 + k
ORIGINAL.update({ord('^'): 70, ord('-'): 70, ord(':'): 71, ord('&'): 72, ord('%'): 73,
                 ord('['): 74, ord(']'): 75, ord('/'): 76})

# Índices -1, -2, ... (no cambiar el orden: los primeros 18 ya se probaron).
NEW = 'áéíóúüñÁÉÍÓÚÜÑ¿¡«»' + '“”‘’—…ºª°' + ';+=*<>#'


def idx(c):
    return ORIGINAL[ord(c)]


def get(font, c):
    o = idx(c) * GLYPH
    g = font[o:o + GLYPH]
    return [list(g[r * W:(r + 1) * W]) for r in range(H)]


def empty():
    return [[0] * W for _ in range(H)]


def stamp(g, art, top, left):
    """Pinta un dibujo (filas de dígitos hex, '.' = vacío) sobre el signo."""
    for r, line in enumerate(art):
        for c, ch in enumerate(line):
            if ch != '.':
                g[top + r][left + c] = max(g[top + r][left + c], int(ch, 16) * 17)


def clear(g, r0, r1):
    for r in range(r0, r1):
        g[r] = [0] * len(g[r])


def squash(g, src0, src1, dst0, dst1):
    """Comprime en vertical las filas src0..src1-1 en dst0..dst1-1 (mayúsculas)."""
    rows = [row[:] for row in g]
    n, m = src1 - src0, dst1 - dst0
    w = len(rows[0])
    out = []
    for j in range(m):
        a, b = src0 + j * n / m, src0 + (j + 1) * n / m
        acc = [0.0] * w
        r = a
        while r < b - 1e-9:
            nxt = min(b, int(r) + 1)
            for c in range(w):
                acc[c] += rows[int(r)][c] * (nxt - r)
            r = nxt
        out.append([min(255, round(v * m / n)) for v in acc])
    for r in range(src0, src1):
        g[r] = [0] * w
    for j in range(m):
        g[dst0 + j] = out[j]


def visible(g):
    for row in g:
        for c in range(12, W):
            row[c] = 0
    return g


def rot180(g):
    g = visible([row[:] for row in g])
    return [[g[H - 1 - y][11 - x] if x < 12 else 0 for x in range(W)] for y in range(H)]


def mirror(g):
    return [[row[11 - x] if x < 12 else 0 for x in range(W)] for row in g]


# Dibujos (valores hex de intensidad). Renglón base: fila 19; mayúsculas desde la 3.
ACUTE = ['...5fb',
         '..cf8.',
         '.8f8..',
         '4d4...']
ACUTE_CAP = ['..5fb',
             '.cf6.',
             '8d4..']
TILDE = ['.8fd6..b',
         'e9.4dc6f',
         '7....9b2']
TILDE_CAP = ['.8fd5.a',
             'e8.5dcf',
             '6...7a2']
DIER = ['ff..ff',
        'ff..ff']
DIER_CAP = ['dd..dd',
            '77..77']
GUILL_L = ['....5d..5d',
           '...5f8.5f8',
           '..5f8.5f8.',
           '.4fa.4fa..',
           '..5f8.5f8.',
           '...5f8.5f8',
           '....5d..5d']
COMMA = ['441',            # la coma del juego (filas 18 a 23)
         'ff4',
         'ff4',
         '3d.',
         '96.',
         '3..']
DOT = ['44',
       'ff',
       'ff']
ORD_O = ['.6dd6.',
         '5f55f5',
         'c8..8c',
         'c8..8c',
         '5f55f5',
         '.6dd6.',
         '......',
         'ffffff']
ORD_A = ['.7dd6.',
         '.4..e8',
         '.8dde8',
         'e7..e8',
         '9fccf9',
         '......',
         '......',
         'ffffff']
DEGREE = ['.6dd6.',
          'd6..6d',
          'd6..6d',
          '.6dd6.']
PLUS = ['....f7....'] * 4 + ['ffffffffff', '7777ff7777'] + ['....f7....'] * 4
EQUALS = ['7777777777',
          'ffffffffff',
          '..........',
          '..........',
          '7777777777',
          'ffffffffff']
STAR = ['....ff....',
        'e8..ff..8e',
        '3cfdffdfc3',
        '...cffc...',
        '..cf77fc..',
        '.cf4..4fc.',
        '.44....44.']
LESS = ['........4c',
        '......5ff8',
        '....5ff8..',
        '..5ff8....',
        '5ff8......',
        '5ff8......',
        '..5ff8....',
        '....5ff8..',
        '......5ff8',
        '........4c']
HASH = ['...c6..c6.',
        '...c6..c6.',
        '..2f3.2f3.',
        '..6c..6c..',
        'cffffffffc',
        '..b7..b7..',
        '..d5..d5..',
        '.1f2.1f2..',
        'cffffffffc',
        '.6c..6c...',
        '.a8..a8...',
        '.c6..c6...']


def build(font):
    out = {}
    for low, up, art in (('a', 'A', 'acute'), ('e', 'E', 'acute'), ('i', 'I', 'acute'),
                         ('o', 'O', 'acute'), ('u', 'U', 'acute'), ('u', 'U', 'dier'),
                         ('n', 'N', 'tilde')):
        g = get(font, low)
        if low == 'i':
            clear(g, 2, 7)                       # se quita el punto
        if art == 'acute':
            stamp(g, ACUTE, 3, 4 if low != 'i' else 3)
        elif art == 'dier':
            stamp(g, DIER, 4, 3)
        else:
            stamp(g, TILDE, 4, 2)
        lowc = {'acute': 'áéíóú', 'dier': 'ü', 'tilde': 'ñ'}[art]
        out[lowc['aeiou'.index(low)] if art == 'acute' else lowc] = g

        G = get(font, up)
        squash(G, 3, 20, 5, 20)                  # 17 filas → 15, deja lugar arriba
        if art == 'acute':
            stamp(G, ACUTE_CAP, 0, 5)
        elif art == 'dier':
            stamp(G, DIER_CAP, 1, 3)
        else:
            stamp(G, TILDE_CAP, 1, 2)
        upc = {'acute': 'ÁÉÍÓÚ', 'dier': 'Ü', 'tilde': 'Ñ'}[art]
        out[upc['AEIOU'.index(up)] if art == 'acute' else upc] = G

    out['¿'] = rot180(get(font, '?'))
    out['¡'] = rot180(get(font, '!'))
    gl = empty()
    stamp(gl, GUILL_L, 9, 1)
    out['«'] = gl
    out['»'] = mirror(gl)

    # Comillas curvas: la coma del juego, arriba.
    g = empty(); stamp(g, COMMA, 2, 2); stamp(g, COMMA, 2, 6); out['”'] = g
    g = empty(); stamp(g, COMMA, 2, 4); out['’'] = g
    # Las de apertura son las de cierre giradas, en la misma altura.
    for close, open_ in (('”', '“'), ('’', '‘')):
        r = rot180(out[close])                   # quedan abajo: se suben
        top = min(y for y in range(H) if any(r[y][:12]))
        top0 = min(y for y in range(H) if any(out[close][y][:12]))
        r = r[top - top0:] + [[0] * W for _ in range(top - top0)]
        out[open_] = r
    g = empty(); stamp(g, ['777777777777', 'ffffffffffff'], 10, 0); out['—'] = g
    g = empty()
    for c in (1, 5, 9):
        stamp(g, DOT, 18, c)
    out['…'] = g
    g = empty(); stamp(g, ORD_O, 3, 3); out['º'] = g
    g = empty(); stamp(g, ORD_A, 3, 3); out['ª'] = g
    g = empty(); stamp(g, DEGREE, 2, 3); out['°'] = g

    g = visible(get(font, ':'))
    clear(g, 12, H)
    stamp(g, COMMA, 16, 5)
    out[';'] = g
    g = empty(); stamp(g, PLUS, 8, 1); out['+'] = g
    g = empty(); stamp(g, EQUALS, 10, 1); out['='] = g
    g = empty(); stamp(g, STAR, 5, 1); out['*'] = g
    g = empty(); stamp(g, LESS, 8, 1); out['<'] = g
    out['>'] = mirror(g)
    g = empty(); stamp(g, HASH, 5, 1); out['#'] = g
    assert set(out) == set(NEW), set(NEW) ^ set(out)
    return {c: visible(g) for c, g in out.items()}


# --- fuente chica (modo angosto) -------------------------------------------
# Celdas de 16×16 a 8 bits guardadas de abajo hacia arriba, con dos signos de
# 8 columnas cada una (índice par a la izquierda). El signo de índice i está en
# la celda NARROW + piso(i / 2): el parche de 0x177f8c cambia el redondeo hacia
# cero por el piso, para que los índices negativos caigan en las celdas de
# relleno de la fuente japonesa chica que están justo antes.
NARROW = FONT + 0xba000 + 0x4c2 * 0x100
NW, NH = 8, 16
NARROW_PATCH = (0x177f8c, 0x001127c2, 0x0000202d)   # srl a0, s1, 31 → daddu a0, zero, zero

ACUTE_N = ['..6d', '.a8.']
ACUTE_CAP_N = ['..5d', '.ba.', '6...']
DIER_N = ['d..d', '5..5']
DIER_CAP_N = ['c..c']
TILDE_N = ['.8d8.b', 'b5.8d5']
TILDE_CAP_N = ['.8d8.b', 'b5.8d5']


def nget(small, i):
    c = small[(i // 2) * 0x100:(i // 2 + 1) * 0x100]
    x0 = (i % 2) * NW
    return [list(c[r * 16 + x0:r * 16 + x0 + NW]) for r in range(NH)][::-1]


def nvisible(g):
    for row in g:
        row[7] = 0
    return g


def shrink(g):
    """Signo grande (12×24 visibles) → chico (7×16): mayúsculas de las filas
    3–19 a las 3–13, promediando el área."""
    sx, sy = 12 / 7, 17 / 11
    out = [[0] * NW for _ in range(NH)]
    for y in range(NH):
        y0, y1 = 3 + (y - 3) * sy, 3 + (y - 2) * sy
        for x in range(7):
            x0, x1 = x * sx, (x + 1) * sx
            acc = 0.0
            for by in range(max(0, int(y0)), min(H, int(y1) + 1)):
                wy = min(y1, by + 1) - max(y0, by)
                if wy <= 0: continue
                for bx in range(int(x0), min(12, int(x1) + 1)):
                    wx = min(x1, bx + 1) - max(x0, bx)
                    if wx > 0: acc += g[by][bx] * wx * wy
            out[y][x] = min(255, round(acc / (sx * sy) * 1.15))
    return out


def build_narrow(small, big):
    nidx = lambda c: ORIGINAL[ord(c)]
    out = {}
    for low, up, art in (('a', 'A', 'acute'), ('e', 'E', 'acute'), ('i', 'I', 'acute'),
                         ('o', 'O', 'acute'), ('u', 'U', 'acute'), ('u', 'U', 'dier'),
                         ('n', 'N', 'tilde')):
        g = nget(small, nidx(low))
        if low == 'i':
            clear(g, 2, 6)
        {'acute': lambda: stamp(g, ACUTE_N, 3, 2 if low != 'i' else 1), 'dier': lambda: stamp(g, DIER_N, 3, 2),
         'tilde': lambda: stamp(g, TILDE_N, 3, 1)}[art]()
        G = nget(small, nidx(up))
        squash(G, 3, 15, 5, 15)
        {'acute': lambda: stamp(G, ACUTE_CAP_N, 2, 2), 'dier': lambda: stamp(G, DIER_CAP_N, 3, 2),
         'tilde': lambda: stamp(G, TILDE_CAP_N, 2, 1)}[art]()
        if art == 'acute':
            out['áéíóú'['aeiou'.index(low)]] = g
            out['ÁÉÍÓÚ'['AEIOU'.index(up)]] = G
        else:
            out[{'dier': 'ü', 'tilde': 'ñ'}[art]] = g
            out[{'dier': 'Ü', 'tilde': 'Ñ'}[art]] = G
    for src, dst in (('?', '¿'), ('!', '¡')):
        g = nvisible(nget(small, nidx(src)))
        out[dst] = [[g[NH - 1 - y][6 - x] if x < 7 else 0 for x in range(NW)] for y in range(NH)]
    for c in NEW:
        if c not in out:
            out[c] = shrink(big[c])
    return {c: nvisible(g) for c, g in out.items()}


def narrow_cells(glyphs, cells):
    """Escribe los signos chicos (índices -1, -2, ...) en una copia de las celdas."""
    cells = bytearray(cells)
    lo = -((len(NEW) + 1) // 2)          # primera celda (relativa a NARROW)
    for k, c in enumerate(NEW):
        i = -1 - k
        ci = (i // 2) - lo
        x0 = (i % 2) * NW
        rows = glyphs[c][::-1]
        for r in range(NH):
            assert len(rows[r]) == NW, c
            cells[ci * 0x100 + r * 16 + x0:ci * 0x100 + r * 16 + x0 + NW] = bytes(rows[r])
    assert len(cells) == (len(NEW) + 1) // 2 * 0x100
    return bytes(cells)


def code(c):
    return c.encode(ENCODING)[0]


def table():
    t = [SKIP] * 256
    for k, i in ORIGINAL.items():
        t[k] = i
    for k, c in enumerate(NEW):
        assert t[code(c)] == SKIP, c
        t[code(c)] = (-1 - k) & 0xff
    return bytes(t)


def lookup(start, end):
    """La búsqueda en la tabla, del tamaño exacto de la cadena que reemplaza."""
    hi = (TABLE_AT + 0x8000) >> 16
    lo = TABLE_AT & 0xffff
    br = (end - (start + 0x18 + 4)) // 4
    words = [
        0x3c020000 | hi,           # lui   v0, hi(tabla)
        0x00431021,                # addu  v0, v0, v1      (v1 = carácter & 0xff)
        0x80510000 | lo,           # lb    s1, lo(tabla)(v0)
        0x2402007f,                # addiu v0, zero, 0x7f
        0x02224026,                # xor   t0, s1, v0
        0x0008402b,                # sltu  t0, zero, t0    (t0 = 1 si se dibuja)
        0x10000000 | br,           # b     end
        0x24020001,                # addiu v0, zero, 1
    ]
    blob = struct.pack('<%dI' % len(words), *words)
    if start < TABLE_AT < end:
        blob += bytes(TABLE_AT - start - len(blob)) + table()
    # El resto de la cadena queda como está (código muerto): stage.py usa una
    # parte para su propio parche.
    assert len(blob) <= end - start
    return blob


def patch_exe(exe, exe_off):
    def word(addr):
        exe.seek(exe_off + addr - EXE_BASE)
        return struct.unpack('<I', exe.read(4))[0]
    for start, end, orig in CHAINS:
        blob = lookup(start, end)
        assert word(start) in (orig, struct.unpack('<I', blob[:4])[0]), hex(start)
        exe.seek(exe_off + start - EXE_BASE)
        exe.write(blob)
    addr, orig, new = NARROW_PATCH
    assert word(addr) in (orig, new), hex(addr)
    exe.seek(exe_off + addr - EXE_BASE)
    exe.write(struct.pack('<I', new))
    for addr, orig in SJIS:
        assert word(addr) in (orig, orig & ~0x03e00000), hex(addr)
        exe.seek(exe_off + addr - EXE_BASE)
        exe.write(struct.pack('<I', orig & ~0x03e00000))     # rs = zero


def apply(er, er_off, exe, exe_off):
    er.seek(er_off + FONT)
    font_all = er.read(0xb1b00 + 77 * GLYPH)
    font = font_all[0xb1b00:]
    glyphs = build(font)
    # Cada casilla japonesa que se pisa tiene que ser relleno (todas iguales a
    # la última) o tener ya estos signos, si el script se corre dos veces.
    lowest = 0xb1b00 - len(NEW) * GLYPH
    mine = font_all[lowest:0xb1b00] == b''.join(bytes(sum(glyphs[c], [])) for c in reversed(NEW))
    filler = font_all[0x800 + 1259 * 0x240:0x800 + 1260 * 0x240]
    j0 = (lowest - 0x800) // 0x240
    fresh = all(font_all[0x800 + j * 0x240:0x800 + (j + 1) * 0x240] == filler for j in range(j0, 1260))
    assert fresh or mine, 'la zona de los signos nuevos no es relleno'
    # Fuente chica: las celdas que se pisan tienen que ser relleno (cajas de
    # dos variantes: la de la celda anterior y la de la última) o tener ya
    # estos signos.
    n = (len(NEW) + 1) // 2
    er.seek(er_off + NARROW - (n + 1) * 0x100)
    before = er.read((n + 1) * 0x100)
    er.seek(er_off + NARROW)
    small = er.read(39 * 0x100)
    nglyphs = build_narrow(small, glyphs)
    cells = before[0x100:]
    new_cells = narrow_cells(nglyphs, cells)
    boxes = {before[:0x100], before[-0x100:]}
    fresh = all(cells[k * 0x100:(k + 1) * 0x100] in boxes for k in range(n))
    assert fresh or cells == new_cells, 'la zona de los signos chicos no es relleno'
    # Recién ahora se escribe.
    for k, c in enumerate(NEW):
        er.seek(er_off + ASCII - (k + 1) * GLYPH)
        er.write(bytes(sum(glyphs[c], [])))
    er.seek(er_off + NARROW - n * 0x100)
    er.write(new_cells)
    patch_exe(exe, exe_off)
    return font, glyphs


def iso_file(iso, name):
    """LBA y tamaño de un archivo del directorio raíz de la ISO."""
    iso.seek(16 * 2048 + 156)
    root = iso.read(34)
    lba, size = struct.unpack('<I', root[2:6])[0], struct.unpack('<I', root[10:14])[0]
    iso.seek(lba * 2048)
    d = iso.read(size)
    i = 0
    while i < len(d):
        n = d[i]
        if n == 0:
            i = (i // 2048 + 1) * 2048
            continue
        nm = d[i + 33:i + 33 + d[i + 32]].decode('ascii', 'replace')
        if nm.split(';')[0] == name:
            return struct.unpack('<I', d[i + 2:i + 6])[0], struct.unpack('<I', d[i + 10:i + 14])[0]
        i += n
    raise KeyError(name)


def preview(font, glyphs, path):
    from PIL import Image
    per = 18
    rows = (len(NEW) + per - 1) // per
    img = Image.new('L', (per * 14 + 2, rows * 26 + 2), 50)
    for k, c in enumerate(NEW):
        t = Image.frombytes('L', (W, H), bytes(sum(glyphs[c], []))).crop((0, 0, 12, H))
        img.paste(t, (2 + (k % per) * 14, 1 + (k // per) * 26))
    img.resize((img.width * 5, img.height * 5), Image.NEAREST).save(path)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == '--preview-narrow':
        f = open(args[1], 'rb')
        f.seek(ASCII); font = f.read(77 * GLYPH)
        f.seek(NARROW); small = f.read(39 * 0x100)
        ng = build_narrow(small, build(font))
        from PIL import Image
        img = Image.new('L', (len(NEW) * 10 + 2, 2 * 18 + 2), 50)
        base = 'aeiouunAEIOUUN?!' + '"' * 18
        for k, c in enumerate(NEW):
            for g, y in ((nget(small, ORIGINAL[ord(base[k])]), 1), (ng[c], 19)):
                t = Image.frombytes('L', (NW, NH), bytes(sum(g, []))).crop((0, 0, 7, NH))
                img.paste(t, (2 + k * 10, y))
        img.resize((img.width * 6, img.height * 6), Image.NEAREST).save(args[2])
        sys.exit()
    if args[0] == '--preview':
        f = open(args[1], 'rb')
        off = ER_LBA * 2048 if args[1].lower().endswith('.iso') else 0
        f.seek(off + ASCII)
        font = f.read(77 * GLYPH)
        preview(font, build(font), args[2])
        sys.exit()
    if args[0] == '--iso':
        f = open(args[1], 'r+b')
        exe_lba, _ = iso_file(f, 'SLES_500.51')
        er_lba, _ = iso_file(f, 'ERDATA.BIN')
        assert er_lba == ER_LBA
        font, glyphs = apply(f, er_lba * 2048, f, exe_lba * 2048)
        rest = args[2:]
    else:
        font, glyphs = apply(open(args[0], 'r+b'), 0, open(args[1], 'r+b'), 0)
        rest = args[2:]
    if rest:
        preview(font, glyphs, rest[0])
    print('listo:', len(NEW), 'signos; tabla en', hex(TABLE_AT))
