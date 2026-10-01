# -*- coding: utf-8 -*-
"""
COMPARABLES: contesta "¿esto esta barato?" en vez de solo "¿esto me gusta?".

Fuente: datos/historico.json, el archivo de subastas pasadas de Alcala
(27.000 lotes). Es la fuente primaria y publicada por la propia casa, que es
la via limpia que salio de la investigacion legal.

AVISO METODOLOGICO, importante: lo que guardamos del historico es el PRECIO DE
SALIDA, no el de remate. No es lo mismo. Una salida de 300 EUR dice lo que la
casa pedia, no lo que alguien pago. Sirve para comparar peticiones entre si,
que ya es mucho, pero NO es una base de precios rematados. Para eso hacen falta
mas pasadas anotando que se vendio y que no.
"""
import json
import os
import re
import statistics
import unicodedata
from collections import Counter

from scraper import DIR_DATOS

VACIAS = set("""de la el los las un una y o en con para por sobre su sus del al
cm x s siglo xix xx xviii xvii mm aprox approx medidas decorado decorada
madera con como que mas muy dos tres sin segun estilo""".split())


def norm(s):
    s = (s or "").lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", s)


def palabras(texto):
    return [w for w in norm(texto).split() if len(w) > 3 and w not in VACIAS]


def cargar_historico():
    ruta = os.path.join(DIR_DATOS, "historico.json")
    if not os.path.exists(ruta):
        return []
    return json.load(open(ruta, encoding="utf-8"))


def _indice(hist):
    idx = {}
    for i, l in enumerate(hist):
        for w in set(palabras(l.get("titulo", "") + " " + l.get("texto", "")[:300])):
            idx.setdefault(w, []).append(i)
    return idx


_CACHE = {}


def comparables(lote, hist=None, idx=None, minimo=3, tope=60):
    """Busca lotes historicos que compartan vocabulario con este."""
    if hist is None:
        if "hist" not in _CACHE:
            h = cargar_historico()
            _CACHE["hist"] = h
            _CACHE["idx"] = _indice(h)
        hist, idx = _CACHE["hist"], _CACHE["idx"]

    claves = set(palabras(lote.get("titulo", "") + " " + lote.get("texto", "")[:300]))
    if not claves:
        return [], {}

    votos = Counter()
    for w in claves:
        for i in idx.get(w, []):
            votos[i] += 1

    sel = [(n, hist[i]) for i, n in votos.most_common(tope * 3) if n >= minimo]
    sel = sel[:tope]
    precios = [c.get("salida") for _, c in sel if c.get("salida")]
    precios = [p for p in precios if p > 0]

    resumen = {}
    if len(precios) >= 4:
        precios_o = sorted(precios)
        resumen = {
            "n": len(precios_o),
            "min": precios_o[0],
            "p25": statistics.quantiles(precios_o, n=4)[0] if len(precios_o) >= 4 else precios_o[0],
            "mediana": statistics.median(precios_o),
            "p75": statistics.quantiles(precios_o, n=4)[2] if len(precios_o) >= 4 else precios_o[-1],
            "max": precios_o[-1],
        }
        salida = lote.get("salida") or 0
        if salida and resumen["mediana"]:
            resumen["ratio"] = salida / resumen["mediana"]
            if salida <= resumen["p25"]:
                resumen["veredicto"] = "POR DEBAJO del cuartil bajo"
            elif salida >= resumen["p75"]:
                resumen["veredicto"] = "por encima del cuartil alto"
            else:
                resumen["veredicto"] = "en el rango normal"
    return sel, resumen


def informe(lote, sel, resumen):
    out = []
    t = (lote.get("titulo") or "")[:80]
    out.append(f"\n{t}")
    out.append(f"  salida {lote.get('salida', 0):.0f} EUR  ({lote['casa_nombre']})")
    if not resumen:
        out.append(f"  comparables insuficientes ({len(sel)} parecidos). Sin veredicto.")
        return "\n".join(out)
    r = resumen
    out.append(f"  {r['n']} comparables historicos")
    out.append(f"     min {r['min']:.0f} · p25 {r['p25']:.0f} · MEDIANA {r['mediana']:.0f} "
               f"· p75 {r['p75']:.0f} · max {r['max']:.0f} EUR")
    if "veredicto" in r:
        out.append(f"  -> {r['veredicto']}  ({r['ratio']:.2f}x la mediana)")
    out.append("  parecidos:")
    for n, c in sel[:4]:
        out.append(f"     {c.get('salida', 0):>6.0f} EUR  [{n} palabras]  {(c.get('titulo') or '')[:66]}")
    return "\n".join(out)


if __name__ == "__main__":
    import encargo
    hist = cargar_historico()
    print(f"Historico cargado: {len(hist)} lotes\n{'=' * 78}")
    for l in encargo.buscar(encargo.CAJONERA_DORMITORIO):
        sel, res = comparables(l)
        print(informe(l, sel, res))
