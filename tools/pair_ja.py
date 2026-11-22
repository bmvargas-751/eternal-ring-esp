#!/usr/bin/env python3
"""Empareja los diálogos ingleses con los japoneses (versión de apoyo, E-1).

Las claves no coinciden: el japonés tiene mensajes que el inglés no tiene (y al
revés), así que se alinea escenario por escenario con programación dinámica
(nombres, códigos, signos y largo) y se corrige a mano con MANUAL.

Uso:
    python3 -I tools/pair_ja.py ORIGINAL.jsonl DIALOGOS-JA.jsonl SALIDA.jsonl [--show ESCENARIO...]

SALIDA tiene una línea por clave inglesa: {"key": ..., "ja_key": ..., "ja": ...};
sin pareja, «ja» es null.
"""
import json
import re
import sys
from collections import defaultdict

NAMES = [
    ("lyla", "ライラ"), ("solcia", "ソルシア"), ("eternal ring", "エターナルリング"),
    ("aldin", "アルダイン"), ("homunculus", "ホムンクルス"), ("eilsia", "エイルシア"),
    ("heingaria", "ヘインガリア"), ("grey", "グレイ"), ("evans", "エバンス"),
    ("wallace", "ウォレス"), ("marie", "マリー"), ("fowler", "ファウラー"),
    ("marcus", "マークス"), ("matthew", "マシュー"), ("juno", "ユノー"),
    ("pendant", "ペンダント"), ("soulus", "ソウルス"),
]
CODE = re.compile(r"\{[0-9a-f]+\}")

# Correcciones a mano: clave inglesa -> clave japonesa (o None si no tiene pareja).
# Revisadas leyendo los dos textos, escenario por escenario (2026-11-21).
def _d(n):
    return f"dialogo/{n}"


MANUAL = {
    # 1905: el japonés #056 («あんた、よくあの森を通れたもんだぜ») no está en inglés.
    _d("1905#056"): _d("1905#057"), _d("1905#057"): _d("1905#058"),
    _d("1905#058"): _d("1905#059"), _d("1905#059"): _d("1905#060"),
    # 1916: los japoneses #002-004 son solo puntos; el inglés #012 y #018-020 van corridos.
    _d("1916#002"): None, _d("1916#003"): None,
    _d("1916#012"): _d("1916#013"), _d("1916#018"): _d("1916#019"),
    _d("1916#019"): _d("1916#020"), _d("1916#020"): _d("1916#021"),
    # 1921: el inglés repite «Lyla...» y agrega líneas que el japonés no tiene.
    _d("1921#004"): _d("1921#004"), _d("1921#007"): None,
    # 1990: el japonés #007-028 (cómo se forjan los anillos) no está en inglés.
    **{_d(f"1990#{i:03d}"): _d(f"1990#{i:03d}") for i in range(7)},
    **{_d(f"1990#{i:03d}"): _d(f"1990#{i + 22:03d}") for i in range(7, 21)},
    # 1901: «not much time left» (#007) no está en japonés; «find Lyla» (#008) es el japonés #007;
    # el japonés #008 («ワガハラカラヨ», «hermanos míos») no está en inglés.
    _d("1901#007"): None, _d("1901#008"): _d("1901#007"),
    # 1980: repite el texto del agonizante de 1901, que en japonés solo está en 1901.
    **{_d(f"1980#{i:03d}"): _d(f"1901#{i - 1:03d}") for i in range(1, 8)},
    _d("1980#008"): None, _d("1980#009"): _d("1901#007"), _d("1980#010"): _d("1901#007"),
}


def feats(text, ja):
    t = text.lower()
    f = {"codes": CODE.findall(text)}
    f["names"] = {n for n, k in NAMES if (k in text if ja else n in t)}
    f["q"] = ("？" in text or "?" in text)
    f["ex"] = ("！" in text or "!" in text)
    body = CODE.sub("", text)
    f["len"] = len(body) * (2.6 if ja else 1.0)
    return f


def score(a, b):
    s = 0.0
    s += 3 * len(a["names"] & b["names"]) - 1.5 * len(a["names"] ^ b["names"])
    s += 3 if a["codes"] == b["codes"] else -3
    s += 0.5 if a["q"] == b["q"] else -0.5
    s += 0.3 if a["ex"] == b["ex"] else -0.3
    la, lb = max(a["len"], 1), max(b["len"], 1)
    s += 1.5 - 2.0 * abs(la - lb) / max(la, lb)
    return s


def align(en, ja, gap=-1.0):
    n, m = len(en), len(ja)
    fe = [feats(x["en"], False) for x in en]
    fj = [feats(x["ja"], True) for x in ja]
    D = [[0.0] * (m + 1) for _ in range(n + 1)]
    P = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        D[i][0], P[i][0] = D[i - 1][0] + gap, "e"
    for j in range(1, m + 1):
        D[0][j], P[0][j] = D[0][j - 1] + gap, "j"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            opts = [(D[i - 1][j - 1] + score(fe[i - 1], fj[j - 1]), "d"),
                    (D[i - 1][j] + gap, "e"), (D[i][j - 1] + gap, "j")]
            D[i][j], P[i][j] = max(opts)
    i, j, out = n, m, []
    while i or j:
        p = P[i][j]
        if p == "d":
            out.append((en[i - 1], ja[j - 1])); i -= 1; j -= 1
        elif p == "e":
            out.append((en[i - 1], None)); i -= 1
        else:
            out.append((None, ja[j - 1])); j -= 1
    return out[::-1]


def scene(key):
    return key.split("/")[1].split("#")[0]


def main():
    args = sys.argv[1:]
    show = set()
    if "--show" in args:
        k = args.index("--show")
        show = set(args[k + 1:])
        args = args[:k]
    src, jap, dst = args
    en, ja = defaultdict(list), defaultdict(list)
    for line in open(src, encoding="utf-8"):
        it = json.loads(line)
        if it["key"].startswith("dialogo/"):
            en[scene(it["key"])].append(it)
    jtext = {}
    for line in open(jap, encoding="utf-8"):
        it = json.loads(line)
        ja[scene(it["key"])].append(it)
        jtext[it["key"]] = it["ja"]
    rows = []
    for s in sorted(en):
        pairs = align(en[s], ja.get(s, []))
        if s in show or "all" in show:
            print(f"=== {s}")
            for e, j in pairs:
                el = e["key"].split("#")[1] if e else "----"
                jl = j["key"].split("#")[1] if j else "----"
                et = (e["en"] if e else "").replace("\n", " ")[:70]
                jt = (j["ja"] if j else "").replace("\n", " ")[:40]
                print(f"{el} {jl} | {et:70} | {jt}")
        for e, j in pairs:
            if not e:
                continue
            jk = j["key"] if j else None
            if e["key"] in MANUAL:
                jk = MANUAL[e["key"]]
            rows.append({"key": e["key"], "ja_key": jk, "ja": jtext.get(jk) if jk else None})
    with open(dst, "w", encoding="utf-8") as w:
        for r in rows:
            w.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} claves; {sum(r['ja'] is not None for r in rows)} con japonés -> {dst}")


if __name__ == "__main__":
    main()
