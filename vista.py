# -*- coding: utf-8 -*-
"""
Genera datos/vista.html: la rejilla visual para escanear cientos de lotes rapido.

Decisiones que vienen del brief de Diego:
  - La imagen manda. Todo lo demas es cartela.
  - Puntuaciones SEPARADAS (gusto, oportunidad, logistica, confianza), nunca
    una sola nota opaca.
  - Lo desconocido se queda desconocido. No se inventa envio ni condicion.
  - El feedback se guarda y se exporta, para que vuelva al perfil.

La plantilla HTML vive en plantilla.py.
"""
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from casas import CASAS
from encargo import dimensiones
from plantilla import PLANTILLA
from puntuar import ranking
from scraper import DIR_DATOS


# --------------------------------------------------------------------------
# Puntuaciones separadas
# --------------------------------------------------------------------------
def escalar(v, tope):
    return max(0, min(100, round(100 * v / tope))) if tope else 0


def puntuaciones(l):
    gusto = escalar(l.get("puntos", 0), 20)

    # Oportunidad: no vendido, bajada de precio, salida baja. NUNCA decimos
    # "infravalorado" sin evidencia: eso necesita comparables de verdad.
    op, por_que = 0, []
    if l.get("no_vendido"):
        op += 30
        por_que.append("no se vendio")
    for r in l.get("razones", []):
        if "BAJO DE PRECIO" in r:
            op += 40
            por_que.append("ya bajo de precio")
    salida = l.get("salida") or 0
    if 0 < salida <= 150:
        op += 20
        por_que.append("salida baja")
    elif 150 < salida <= 400:
        op += 10
    if CASAS.get(l.get("casa"), {}).get("relanza_40") and l.get("no_vendido"):
        op += 15
        por_que.append("Segre relanza a -40 %")
    op = min(100, op)

    # Logistica: cuanto cuesta de verdad traerlo a casa
    log = 50
    casa = CASAS.get(l.get("casa"))
    if l.get("precio_fijo"):
        log += 20                       # tienda: sin prima ni plazo de retirada
    if casa:
        log += int((0.25 - casa["comision"]) * 200)
        if casa.get("almacenaje_dia"):
            log -= 10                   # penalizacion por retirada a reloj
    if (l.get("ubicacion") or "").lower().startswith("caracas"):
        log = 5                         # importacion desde Venezuela
    lado = l.get("lado_mayor_cm") or 0
    if lado >= 180:
        log -= 15                       # no entra en un coche
    log = max(0, min(100, log))

    # Confianza: cuanto nos fiamos de lo que hemos extraido
    conf = 30
    if l.get("lado_mayor_cm"):
        conf += 25
    if l.get("imagen"):
        conf += 15
    if len(l.get("texto") or "") > 200:
        conf += 15
    if l.get("banderas"):
        conf -= 10                      # el catalogo admite algo raro
    conf = max(0, min(100, conf))

    return {"gusto": gusto, "oportunidad": op, "logistica": log,
            "confianza": conf, "op_por_que": por_que}


MATERIALES = ["roble", "nogal", "teca", "palisandro", "pino", "haya", "cerezo",
              "caoba", "bronce", "marmol", "hierro", "acero", "laton", "ceramica",
              "cristal", "vidrio", "mimbre", "enea", "cuero", "formica", "metal"]
PERIODOS = [("1950", r"\b195\d|a[nñ]os 50\b|\b50s\b"), ("1960", r"\b196\d|a[nñ]os 60\b|\b60s\b"),
            ("1970", r"\b197\d|a[nñ]os 70\b|\b70s\b"), ("1980", r"\b198\d|a[nñ]os 80\b|\b80s\b"),
            ("s. XIX", r"s\.?\s*xix|siglo xix"), ("s. XVIII", r"s\.?\s*xviii|siglo xviii")]


def atributos(l):
    t = ((l.get("titulo") or "") + " " + (l.get("texto") or "")).lower()
    mats = [m for m in MATERIALES if m in t]
    per = [p for p, rx in PERIODOS if re.search(rx, t)]
    dims = dimensiones(l.get("texto") or "")
    return {
        "materiales": mats[:3],
        "periodo": per[0] if per else None,
        "dims": " x ".join(f"{v:.0f}" for v in dims[0]) + " cm" if dims else None,
        "ubicacion": l.get("ubicacion") or ("Madrid" if l.get("casa") in CASAS else None),
    }


def preparar(lotes):
    out = []
    for l in lotes:
        s = puntuaciones(l)
        a = atributos(l)
        c = l.get("coste") or {}
        out.append({
            "id": l["url"],
            "fuente": l["casa_nombre"],
            "lote": l.get("lote"),
            "titulo": (l.get("titulo") or "sin titulo")[:140],
            "salida": l.get("salida"),
            "total": c.get("total"),
            "recargo": c.get("recargo_pct"),
            "img": l.get("imagen"),
            "url": l["url"],
            "dims": a["dims"],
            "lado": round(l.get("lado_mayor_cm") or 0),
            "mats": a["materiales"],
            "periodo": a["periodo"],
            "donde": a["ubicacion"],
            "nov": bool(l.get("no_vendido")),
            "fijo": bool(l.get("precio_fijo")),
            "g": s["gusto"], "o": s["oportunidad"],
            "lg": s["logistica"], "cf": s["confianza"],
            "porque": l.get("razones", [])[:4],
            "riesgos": l.get("banderas", [])[:3],
            "avisos": l.get("avisos", [])[:1],
            "opq": s["op_por_que"],
        })
    return out


def construir(minimo=1):
    ruta = os.path.join(DIR_DATOS, "lotes.json")
    lotes = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else []
    datos = preparar(ranking(lotes, minimo=minimo))
    html = PLANTILLA.replace("__DATOS__", json.dumps(datos, ensure_ascii=False))
    html = html.replace("__FECHA__", datetime.now().strftime("%d/%m/%Y %H:%M"))
    html = html.replace("__TOTAL__", str(len(lotes)))
    salida = os.path.join(DIR_DATOS, "vista.html")
    with open(salida, "w", encoding="utf-8") as f:
        f.write(html)
    return salida, len(datos), len(lotes)


if __name__ == "__main__":
    minimo = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    ruta, mostrados, total = construir(minimo)
    print(f"{ruta}\n  {mostrados} lotes en la rejilla, de {total} leidos")
