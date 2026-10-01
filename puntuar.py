# -*- coding: utf-8 -*-
"""
Puntua cada lote contra el perfil de Diego y le pone banderas.

No decide: ordena y avisa. La decision final es de Diego, en la exposicion previa.
Eso sale de la unica cosa en la que coincidieron el marchante suizo, el subastador
y el manual: nadie serio puja sin ver la pieza o pedir el informe de estado.
"""
import re
import unicodedata

import perfil
from casas import CASAS, coste_total


def _encaja(clave, texto):
    """
    Subcadena normal, salvo claves cortas o con digitos ("40s", "60s"), donde
    exigimos limite de palabra. Sin esto, "40s" aparece dentro de cualquier
    numero y lo ensucia todo.
    """
    if len(clave) <= 4 or any(c.isdigit() for c in clave):
        return re.search(r"(?<![a-z0-9])" + re.escape(clave) + r"(?![a-z0-9])", texto) is not None
    return clave in texto


def limpiar(s):
    """Minusculas y sin tildes, para que 'oleo' encuentre 'óleo'."""
    s = (s or "").lower()
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def puntuar(lote):
    txt = limpiar(lote.get("titulo", "") + " " + lote.get("texto", ""))
    pts = 0
    razones, banderas, avisos = [], [], []

    # --- artistas por nombre: la senal mas fuerte
    for a in perfil.ARTISTAS:
        if limpiar(a) in txt:
            es_alcanzable = a in perfil.ARTISTAS_ALCANZABLES
            es_venezolano = a in perfil.ARTISTAS_VENEZOLANOS
            pts += 8 if es_venezolano else (6 if es_alcanzable else 4)
            razones.append(f"ARTISTA: {a}")
            for clave, aviso in perfil.AVISOS_POR_ARTISTA.items():
                if clave in limpiar(a):
                    avisos.append(aviso)

    # --- gusto
    for k, peso in perfil.GUSTA.items():
        if _encaja(limpiar(k), txt):
            pts += peso
            if peso >= 3:
                razones.append(k)

    # --- rechazo
    descartado = False
    for k, peso in perfil.NO_GUSTA_FUERTE.items():
        if _encaja(limpiar(k), txt):
            pts += peso
            banderas.append(f"NO: {k}")
            if peso <= -4:
                descartado = True
    for k, peso in perfil.NO_GUSTA_SUAVE.items():
        if _encaja(limpiar(k), txt):
            pts += peso

    # --- gran formato: su gusto y la ineficiencia del mercado apuntan igual
    lado = lote.get("lado_mayor_cm") or 0
    if lado >= 150:
        pts += perfil.BONUS_MUY_GRANDE
        razones.append(f"GRAN FORMATO {lado:.0f} cm")
    elif lado >= perfil.GRAN_FORMATO_CM:
        pts += perfil.BONUS_GRAN_FORMATO
        razones.append(f"formato grande {lado:.0f} cm")

    # --- lectura del catalogo: lo que la casa esta diciendo en su codigo
    for formula, significado in perfil.GRADOS_ATRIBUCION.items():
        if formula in txt:
            banderas.append(f"'{formula.strip()}' = {significado}")
            pts -= 2

    # --- firma: multiplica el precio por 3 o 4
    if any(f in txt for f in perfil.FIRMA_MALA):
        banderas.append("FIRMA EN PLANCHA: leelo como SIN FIRMA, vale como estampa decorativa")
        pts -= 3
    elif any(f in txt for f in perfil.FIRMA_BUENA):
        pts += 2
        razones.append("firmado a lapiz")

    # --- lote reciclado: no se vendio, luego es negociable o va a bajar
    if lote.get("no_vendido"):
        razones.append("NO VENDIDO: candidato a rebaja")
        pts += 2
        if CASAS.get(lote["casa"], {}).get("relanza_40"):
            banderas.append("Segre relanza a -40 %: espera en vez de comprar ahora")

    # --- bajada de precio ya detectada entre pasadas
    hist = lote.get("historico_salida") or []
    for h in hist:
        if h["a"] < h["de"]:
            baja = 100 * (1 - h["a"] / h["de"])
            razones.append(f"BAJO DE PRECIO {baja:.0f} % ({h['de']:.0f} -> {h['a']:.0f} EUR)")
            pts += 4

    # --- presupuesto
    salida = lote.get("salida") or 0
    fuera_presupuesto = False
    if salida and salida > perfil.PRECIO_MAX:
        if salida <= perfil.PRECIO_MAX_ESTIRANDO and pts >= 12:
            banderas.append(f"Por encima de presupuesto ({salida:.0f} EUR) pero encaja mucho")
        else:
            fuera_presupuesto = True
    if salida and salida < perfil.PRECIO_MIN:
        pts -= 1

    lote["puntos"] = pts
    lote["razones"] = razones
    lote["banderas"] = banderas
    lote["avisos"] = avisos
    lote["descartado"] = descartado or fuera_presupuesto

    if salida:
        _, desglose = coste_total(salida, lote["casa"])
        lote["coste"] = desglose
    return lote


def ranking(lotes, minimo=4):
    lotes = [l for l in lotes if not l.get("historico")]
    puntuados = [puntuar(dict(l)) for l in lotes]
    vivos = [l for l in puntuados if not l["descartado"] and l["puntos"] >= minimo]
    return sorted(vivos, key=lambda l: (-l["puntos"], l.get("salida") or 0))


def ficha(l):
    """Una ficha legible, con el coste real y no solo el martillo."""
    out = []
    out.append(f"[{l['puntos']:+3d}] {l['casa_nombre']} lote {l.get('lote') or '?'}")
    out.append(f"      {l['titulo'][:95]}")
    c = l.get("coste")
    if c:
        out.append(f"      salida {c['martillo']:.0f} EUR  ->  TOTAL REAL {c['total']:.0f} EUR "
                   f"(+{c['recargo_pct']:.0f} %)  sin contar transporte")
    if l["razones"]:
        out.append(f"      a favor: {', '.join(l['razones'][:5])}")
    for b in l["banderas"][:3]:
        out.append(f"      OJO: {b}")
    for a in l["avisos"][:1]:
        out.append(f"      AVISO: {a}")
    out.append(f"      {l['url']}")
    return "\n".join(out)
