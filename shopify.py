# -*- coding: utf-8 -*-
"""
Fuentes Shopify. Exponen /products.json publico, sin clave y sin login.
Hoy: La Basilica Galeria (Barcelona), Casa de Subastas Odalys (Madrid/Caracas)
y The Oblist (Paris; robots.txt lo permite, revisado el 2026-10-06).

The Oblist tiene decenas de miles de productos, casi todos contemporaneos y
caros. Solo se leen sus colecciones vintage.

No son subastas: son precio fijo. Por eso el "coste total" es el precio tal cual,
sin prima de comprador. Se marcan con comision 0 para que el calculo no mienta.
"""
import html
import json
import warnings
warnings.simplefilter('ignore')
import re
import time
import urllib.request

from config import UA  # correo en config_local.py, fuera del repo

TIENDAS = {
    "labasilica": {
        "nombre": "La Basilica Galeria",
        "base": "https://labasilicagaleria.com",
        "ciudad": "Barcelona",
        "nota": "Vintage y diseno. Mediana ~190 EUR. Precio fijo, sin prima.",
    },
    "odalys": {
        "nombre": "Casa de Subastas Odalys",
        "base": "https://odalys.com",
        "ciudad": "Madrid / Caracas",
        "nota": "Arte venezolano. OJO: el 82 % esta fisicamente en Caracas.",
    },
    "oblist": {
        "nombre": "The Oblist",
        "base": "https://oblist.com",
        "ciudad": None,          # marketplace: cada vendedor envia desde su pais
        "nota": "Marketplace de diseno, Paris. Solo colecciones vintage.",
        "colecciones": ["vintage-furniture", "mid-century-modern-furniture",
                        "vintage-home-decor"],
        "tope": 900,             # lo demas no cabe en el presupuesto
    },
}

RE_DIM = re.compile(r"(\d{1,4}(?:[.,]\d+)?)\s*(?:x|X|×)\s*(\d{1,4}(?:[.,]\d+)?)"
                    r"(?:\s*(?:x|X|×)\s*(\d{1,4}(?:[.,]\d+)?))?\s*(cm|mm|m\b)?", re.I)


def _texto(h_):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h_ or ""))).strip()


def _lado_mayor(txt):
    mejor = 0.0
    for m in RE_DIM.finditer(txt or ""):
        f = {"mm": 0.1, "m": 100.0}.get((m.group(4) or "cm").lower(), 1.0)
        for g in (m.group(1), m.group(2), m.group(3)):
            if not g:
                continue
            try:
                mejor = max(mejor, float(g.replace(",", ".")) * f)
            except ValueError:
                pass
    return mejor if 3 < mejor < 2000 else 0.0


def rastrear(tienda_id, max_paginas=8, pausa=2.0):
    t = TIENDAS[tienda_id]
    print(f"\n=== {t['nombre']} (Shopify) ===")
    lotes, vistos = [], set()
    rutas = [f"/collections/{c}" for c in t.get("colecciones", [])] or [""]
    for ruta in rutas:
        lotes += _rastrear_ruta(t, tienda_id, ruta, max_paginas, pausa, vistos)
    print(f"  TOTAL {t['nombre']}: {len(lotes)}")
    return lotes


def _rastrear_ruta(t, tienda_id, ruta, max_paginas, pausa, vistos):
    lotes = []
    for p in range(1, max_paginas + 1):
        url = f"{t['base']}{ruta}/products.json?limit=250&page={p}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
        except Exception as e:
            print(f"  page {p}: {e}")
            break
        prods = data.get("products", [])
        print(f"  {ruta or '/'} p{p}: {len(prods)} productos")
        if not prods:
            break
        for pr in prods:
            v = (pr.get("variants") or [{}])[0]
            try:
                precio = float(v.get("price") or 0)
            except ValueError:
                precio = 0.0
            if precio <= 0 or pr.get("id") in vistos:
                continue
            if t.get("tope") and precio > t["tope"]:
                continue
            # agotado = vendido. Antes se marcaba como "no vendido", que es lo
            # contrario, y le daba puntos de oportunidad a lo que ya no existe.
            if not any(x.get("available", True) for x in pr.get("variants") or [{}]):
                continue
            vistos.add(pr.get("id"))
            cuerpo = _texto(pr.get("body_html"))
            ubic = ""
            mu = re.search(r"Ubicaci[oó]n:\s*([A-Za-zÁÉÍÓÚáéíóúñ ]{3,20})", cuerpo)
            if mu:
                ubic = mu.group(1).strip()
            titulo = pr.get("title", "")
            lado = _lado_mayor(cuerpo)
            medidas = ""
            if not lado:
                # "H75 × W44 × D32 cm", "Height 75cm / Width 66 cm": The Oblist
                from etsy import medidas_de_texto
                m = medidas_de_texto(cuerpo)
                vals = [v for v in (m.get("ancho"), m.get("fondo"), m.get("alto")) if v]
                if len(vals) >= 2:
                    medidas = " x ".join(str(v) for v in vals) + " cm"
                    lado = max(vals)
            lotes.append({
                "casa": tienda_id,
                "casa_nombre": t["nombre"],
                "lote": str(pr.get("id")),
                "titulo": titulo[:300],
                "texto": " . ".join(x for x in [titulo, medidas, pr.get("vendor") or "", cuerpo,
                                                " ".join(pr.get("tags") or [])] if x)[:1500],
                "salida": precio,
                "imagen": (pr.get("images") or [{}])[0].get("src"),
                "url": f"{t['base']}/products/{pr.get('handle')}",
                "origen": url,
                "no_vendido": False,
                "lado_mayor_cm": lado,
                "ubicacion": ubic or (t["ciudad"] if tienda_id == "labasilica" else None),
                "precio_fijo": True,
                "historico": False,
                "visto": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
            })
        time.sleep(pausa)
        if len(prods) < 250:
            break
    return lotes


if __name__ == "__main__":
    import sys
    from scraper import guardar
    ids = [a for a in sys.argv[1:] if a in TIENDAS] or list(TIENDAS)
    todo = []
    for i in ids:
        todo += rastrear(i)
    if todo:
        nuevos, total = guardar(todo)
        print(f"\nGuardados: {nuevos} nuevos, {total} en total.")
