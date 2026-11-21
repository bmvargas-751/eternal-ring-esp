"""Letras españolas para la fuente de los diálogos de Eternal Ring (PAL).

La fuente de 1 byte (77 signos de 16×24 a 8 bits, se ven las 12 columnas de la
izquierda) no tiene á é í ó ú ü ñ ¿ ¡ « ». Este script:
  - arma esos signos a partir de las letras del propio juego;
  - los guarda en las casillas de relleno del final de la fuente japonesa de
    2 bytes (sin uso en el PAL), que quedan justo antes de los signos ASCII:
    el signo de índice -k está en ASCII - k × 0x180;
  - cambia en el ejecutable la cadena de comparaciones de la función 0x179e60
    (0x17a088 a 0x17a1c4) por una tabla de 256 bytes: código Latin-1 → índice
    del signo (con signo; 0x7f = no se dibuja).

Uso: python3 -I font_es.py --preview ERDATA.BIN vista.png   (no cambia nada)
     python3 -I font_es.py ERDATA.BIN SLES_500.51 [vista.png]
     python3 -I font_es.py --iso IMAGEN.iso [vista.png]
Los dos archivos se cambian en su lugar.
"""
import struct, sys

FONT = 0x4e8090            # desplazamiento de la fuente en ERDATA.BIN (entrada 4)
ASCII = FONT + 0xb1b00     # primer signo de 1 byte
GLYPH = 0x180              # 16 × 24, 8 bits
W, H = 16, 24
EXE_BASE = 0xff000         # dirección = desplazamiento + 0xff000
PATCH_AT = 0x17a088        # inicio de la cadena de comparaciones
TABLE_AT = 0x17a0c0        # tabla de 256 bytes (dentro de la cadena, que ya no se usa)
CHAIN_END = 0x17a1c8       # bne t0, v0 (=1): se dibuja si t0 == 1
SKIP = 0x7f
ER_LBA = 0x6a1

# Mapa original del juego (de la cadena de comparaciones).
ORIGINAL = {}
for i in range(10): ORIGINAL[0x30 + i] = i
for i in range(26): ORIGINAL[0x41 + i] = 10 + i; ORIGINAL[0x61 + i] = 36 + i
for k, c in enumerate(".,()!?'\""):
    ORIGINAL[ord(c)] = 62 + k
ORIGINAL.update({ord('^'): 70, ord('-'): 70, ord(':'): 71, ord('&'): 72, ord('%'): 73,
                 ord('['): 74, ord(']'): 75, ord('/'): 76})

NEW = 'áéíóúüñÁÉÍÓÚÜÑ¿¡«»'      # índices -1, -2, ...


def idx(c):
    return ORIGINAL[ord(c)]


def get(font, c):
    o = idx(c) * GLYPH
    g = font[o:o + GLYPH]
    return [list(g[r * W:(r + 1) * W]) for r in range(H)]


def stamp(g, art, top, left):
    """Pinta un dibujo (filas de dígitos hex, '.' = vacío) sobre el signo."""
    for r, line in enumerate(art):
        for c, ch in enumerate(line):
            if ch != '.':
                g[top + r][left + c] = max(g[top + r][left + c], int(ch, 16) * 17)


def clear(g, r0, r1):
    for r in range(r0, r1):
        g[r] = [0] * W


def squash(g, src0, src1, dst0, dst1):
    """Comprime en vertical las filas src0..src1-1 en dst0..dst1-1 (mayúsculas)."""
    rows = [row[:] for row in g]
    n, m = src1 - src0, dst1 - dst0
    out = []
    for j in range(m):
        a, b = src0 + j * n / m, src0 + (j + 1) * n / m
        acc = [0.0] * W
        r = a
        while r < b - 1e-9:
            nxt = min(b, int(r) + 1)
            for c in range(W):
                acc[c] += rows[int(r)][c] * (nxt - r)
            r = nxt
        out.append([min(255, round(v * m / n)) for v in acc])
    clear(g, src0, src1)
    for j in range(m):
        g[dst0 + j] = out[j]


def visible(g):
    for row in g:
        for c in range(12, W):
            row[c] = 0
    return g


# Dibujos (valores hex de intensidad).
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

    for src, dst in (('?', '¿'), ('!', '¡')):
        g = visible(get(font, src))
        r = [[g[H - 1 - y][11 - x] if x < 12 else 0 for x in range(W)] for y in range(H)]
        out[dst] = r
    gl = [[0] * W for _ in range(H)]
    stamp(gl, GUILL_L, 9, 1)
    out['«'] = gl
    out['»'] = [[row[11 - x] if x < 12 else 0 for x in range(W)] for row in gl]
    return {c: visible(g) for c, g in out.items()}


def table():
    t = [SKIP] * 256
    for code, i in ORIGINAL.items():
        t[code] = i
    for k, c in enumerate(NEW):
        t[ord(c.encode('latin-1'))] = (-1 - k) & 0xff
    return bytes(t)


def code():
    hi = (TABLE_AT + 0x8000) >> 16
    lo = TABLE_AT & 0xffff
    br = (CHAIN_END - (PATCH_AT + 0x18 + 4)) // 4
    words = [
        0x3c020000 | hi,           # lui   v0, hi(tabla)
        0x00431021,                # addu  v0, v0, v1      (v1 = carácter & 0xff)
        0x80510000 | lo,           # lb    s1, lo(tabla)(v0)
        0x2402007f,                # addiu v0, zero, 0x7f
        0x02224026,                # xor   t0, s1, v0
        0x0008402b,                # sltu  t0, zero, t0    (t0 = 1 si se dibuja)
        0x10000000 | br,           # b     0x17a1c8
        0x24020001,                # addiu v0, zero, 1
    ]
    words += [0] * ((TABLE_AT - PATCH_AT) // 4 - len(words))
    blob = struct.pack('<%dI' % len(words), *words) + table()
    blob += bytes(CHAIN_END - PATCH_AT - len(blob))
    assert len(blob) == CHAIN_END - PATCH_AT
    return blob


def apply(er, er_off, exe, exe_off):
    er.seek(er_off + FONT)
    font_all = er.read(0xb1b00 + 77 * GLYPH)
    font = font_all[0xb1b00:]
    glyphs = build(font)
    # La zona que se pisa tiene que ser relleno de la fuente japonesa (o ya
    # tener estos mismos signos, si el script se corre dos veces).
    lowest = 0xb1b00 - len(NEW) * GLYPH
    filler = font_all[0x800 + 1259 * 0x240:0x800 + 1260 * 0x240]
    j0 = (lowest - 0x800) // 0x240
    fresh = all(font_all[0x800 + j * 0x240:0x800 + (j + 1) * 0x240] == filler for j in range(j0, 1260))
    mine = font_all[lowest:0xb1b00] == b''.join(bytes(sum(glyphs[c], [])) for c in reversed(NEW))
    assert fresh or mine, 'la zona de los signos nuevos no es relleno'
    for k, c in enumerate(NEW):
        er.seek(er_off + ASCII - (k + 1) * GLYPH)
        er.write(bytes(sum(glyphs[c], [])))
    exe.seek(exe_off + PATCH_AT - EXE_BASE)
    old = exe.read(4)
    assert old in (b'\xd0\xff\x65\x24', struct.pack('<I', 0x3c020000 | ((TABLE_AT + 0x8000) >> 16))), old.hex()
    exe.seek(exe_off + PATCH_AT - EXE_BASE)
    exe.write(code())
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
    chars = list(NEW)
    base = 'aeiouunAEIOUUN?!""'
    img = Image.new('L', (len(chars) * 14 + 2, 2 * 26 + 2), 50)
    for k, c in enumerate(chars):
        src = visible(get(font, base[k]))
        for g, y in ((src, 1), (glyphs[c], 27)):
            t = Image.frombytes('L', (W, H), bytes(sum(g, []))).crop((0, 0, 12, H))
            img.paste(t, (2 + k * 14, y))
    img.resize((img.width * 5, img.height * 5), Image.NEAREST).save(path)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == '--preview':           # solo mira: ERDATA.BIN (o la ISO) y la imagen
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
    print('listo:', len(NEW), 'signos y la tabla en', hex(TABLE_AT))
