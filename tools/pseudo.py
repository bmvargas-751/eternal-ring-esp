"""Pseudolocalización de Eternal Ring: una traducción falsa de todo el texto,
más larga y con letras españolas, para ver en el juego cortes, cajas que se
desbordan y signos que falten (PLAN, fase 1).

Uso: python3 -I tools/pseudo.py source.jsonl CARPETA_SALIDA
Después: python3 -I tools/adapter.py build ISO_ORIGINAL ISO_NUEVA CARPETA_SALIDA

Cada texto va entre [ ] (si falta el «]», se cortó), con a e i o u n → á é í
ó ú ñ, y se alarga con « ñ» hasta el límite que conocemos (TECH.md, T-3 y T-4):
  - diálogos: renglones de 35 caracteres (el 4.º, de 32), sin agregar renglones;
  - descripciones: renglones de 32, y un renglón más de prueba si cabe;
  - ejecutable: un 30 % más dentro del campo; los de ancho fijo (terminan en
    espacios) conservan el largo.
Los códigos quedan intactos.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hooks

ACC = str.maketrans('aeiounAEIOUN', 'áéíóúñÁÉÍÓÚÑ')
CODES = hooks.CODES


def accent(s):
    """Acentúa lo que no es código."""
    out, i = [], 0
    for m in CODES.finditer(s):
        out.append(s[i:m.start()].translate(ACC)); out.append(m.group()); i = m.end()
    out.append(s[i:].translate(ACC))
    return ''.join(out)


def width(s):
    return len(CODES.sub('', s))


def pad(line, limit):
    while width(line) + 2 <= limit:
        line += ' ñ'
    return line


def fits(key, item, es):
    if item.get('max') is not None and len(hooks.encode(key, es)) > item['max']:
        return False
    return not hooks.check(key, item, es)


def pseudo(item):
    key, en = item['key'], item['en']
    if key.startswith('menus/') and en != en.rstrip(' '):
        core = en.rstrip(' ')                        # ancho fijo: mismo largo
        if CODES.search(core) or len(core) <= 2:
            return accent(en)
        es = accent('[' + core[1:-1] + ']')
        return es + ' ' * (len(en) - len(es))
    body = en.rstrip('\n')
    trail = en[len(body):]                           # saltos al final, tal cual
    lines = [accent(l) for l in body.split('\n')]
    if key.startswith('dialogo/'):
        limits = [hooks.DIALOG_LAST if n == hooks.DIALOG_LINES else hooks.DIALOG_WIDTH
                  for n in range(1, len(lines) + 1)]
    elif key.endswith('.desc'):
        limits = [hooks.DESC_WIDTH] * len(lines)
    else:
        limits = [int(width(body) * 1.3 + 0.999) + 2]
    # el [ va al principio y el ] al final: cuentan en el primer y el último renglón
    lim = [l - (n == 0) - (n == len(lines) - 1) for n, l in enumerate(limits)]
    lines = [pad(l, m) for l, m in zip(lines, lim)]
    es = '[' + '\n'.join(lines) + ']' + trail
    if key.endswith('.desc'):
        extra = es[:len(es) - len(trail)] + '\n[3.er renglón de prueba]' + trail
        if fits(key, item, extra):
            es = extra
    while not fits(key, item, es) and ' ñ' in es:   # recortar el relleno si no entra
        i = es.rfind(' ñ'); es = es[:i] + es[i + 2:]
    if not fits(key, item, es):                      # sin corchetes, o como el original
        es = accent(en)
    return es


def main(src, out):
    items = [json.loads(l) for l in open(src, encoding='utf-8') if l.strip()]
    by_file, bad = {}, []
    for it in items:
        es = pseudo(it)
        if not fits(it['key'], it, es):
            bad.append(it['key'])
        by_file.setdefault(it['key'].rsplit('#', 1)[0], []).append({'key': it['key'], 'es': es})
    for f, rows in by_file.items():
        p = os.path.join(out, f + '.jsonl')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as w:
            for r in rows:
                w.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(len(items), 'textos en', out, '| fuera de límite (el original ya se pasa):', len(bad))
    for k in bad[:20]:
        print('  ', k)


if __name__ == '__main__':
    main(*sys.argv[1:])
