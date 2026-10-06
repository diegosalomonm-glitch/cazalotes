# -*- coding: utf-8 -*-
"""
Etsy, por su API oficial (Open API v3). App "personal-vintage-finder",
acceso personal aprobado el 2026-10-02.

Credenciales en config_local.py (fuera del repo):
    ETSY_KEYSTRING     = "..."
    ETSY_SHARED_SECRET = "..."
Etsy exige las dos en la cabecera: x-api-key: <keystring>:<shared_secret>.

Lo que obligan sus condiciones de API (etsy.com/legal/api) y como se cumple:
  - "no mostraras contenido de Etsy con mas de 24 horas de antiguedad"
    -> los anuncios van a datos/etsy.json, que se SOBRESCRIBE en cada pasada.
       Nada se acumula. vista.py ignora el archivo si tiene mas de 24 h.
  - "no lo guardaras mas de lo razonablemente necesario"
    -> lo mismo: un archivo, la ultima pasada, nada mas.
  - limite de 5 peticiones por segundo y 5.000 al dia
    -> una peticion cada 0,25 s y tope duro de 400 por pasada.
  - el aviso de marca va al pie de la pagina (plantilla.py).

Uso:
    .venv/bin/python etsy.py              busquedas del perfil
    .venv/bin/python etsy.py "comoda blanca"   una busqueda suelta
"""
import json
import os
import re
import sys
import time
import warnings
from datetime import datetime, timezone

warnings.simplefilter("ignore")
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scraper import DIR_DATOS

API = "https://openapi.etsy.com/v3/application"
ARCHIVO = os.path.join(DIR_DATOS, "etsy.json")
PAUSA = 0.25
TOPE_PETICIONES = 400

# Conversion APROXIMADA a euros solo para poder filtrar por tope. En la ficha se
# muestra siempre el precio original con su moneda. Revisar de vez en cuando.
A_EUR = {"EUR": 1.0, "USD": 0.86, "GBP": 1.17, "CAD": 0.62, "AUD": 0.57,
         "SEK": 0.088, "DKK": 0.134, "CHF": 1.07, "PLN": 0.234, "NOK": 0.083}

UE = {"ES", "PT", "FR", "IT", "DE", "NL", "BE", "LU", "AT", "IE", "DK", "SE", "FI",
      "PL", "CZ", "SK", "HU", "SI", "HR", "RO", "BG", "GR", "CY", "MT", "EE", "LV", "LT"}

# when_made de Etsy -> etiqueta legible y si es vintage de verdad
EPOCA = {
    "made_to_order": ("hecho por encargo", False), "2020_2026": ("2020s", False),
    "2020_2025": ("2020s", False), "2010_2019": ("2010s", False),
    "2007_2009": ("2007-2009", False), "before_2007": ("antes de 2007", True),
    "2000_2006": ("2000s", True), "1990s": ("1990s", True), "1980s": ("1980s", True),
    "1970s": ("1970s", True), "1960s": ("1960s", True), "1950s": ("1950s", True),
    "1940s": ("1940s", True), "1930s": ("1930s", True), "1920s": ("1920s", True),
    "1910s": ("1910s", True), "1900s": ("1900s", True), "1800s": ("s. XIX", True),
    "1700s": ("s. XVIII", True), "before_1700": ("antes de 1700", True),
}

# Busquedas del perfil. Etsy es sobre todo en ingles: van en ingles.
BUSQUEDAS = [
    # su lista mas grande en Wallapop: flexos
    "anglepoise lamp", "jielde lamp", "vintage task lamp", "articulated wall lamp",
    "industrial desk lamp vintage",
    # segunda: sillas
    "mid century chair", "bentwood chair vintage", "cesca chair", "danish teak chair",
    # almacenaje italiano mid-century (la referencia del Ico Parisi)
    "teak sideboard", "mid century dresser", "italian sideboard 60s",
    # escultura y bustos, lo que busca ahora
    "bronze bust", "brutalist sculpture", "marble sculpture vintage",
    # disenadores que salieron de sus favoritos y de La Basilica
    "ico parisi", "kazuhide takahama", "gio ponti", "joe colombo", "carlo hauner",
    "pino melis", "harvey guzzini",
    # estetica Shaker/Judd/Barragan y lo raro
    "shaker furniture", "space age", "postmodern lamp", "brutalist lamp",
    # arte venezolano ingenuo
    "venezuelan art", "naive painting venezuela",
]


def credenciales():
    try:
        import config_local as c
    except ImportError:
        return None, "falta config_local.py"
    k = getattr(c, "ETSY_KEYSTRING", "") or ""
    s = getattr(c, "ETSY_SHARED_SECRET", "") or ""
    if not k:
        return None, "falta ETSY_KEYSTRING en config_local.py"
    if not s:
        return None, ("falta ETSY_SHARED_SECRET en config_local.py. Copialo de "
                      "etsy.com/developers (icono del ojo) y pegalo como "
                      'ETSY_SHARED_SECRET = "..."')
    return f"{k}:{s}", None


class Etsy:
    def __init__(self, cabecera):
        self.s = requests.Session()
        self.s.headers.update({"x-api-key": cabecera, "Accept": "application/json"})
        self.n = 0
        self._ult = 0.0

    def get(self, ruta, **params):
        if self.n >= TOPE_PETICIONES:
            raise RuntimeError(f"tope de {TOPE_PETICIONES} peticiones por pasada")
        espera = PAUSA - (time.time() - self._ult)
        if espera > 0:
            time.sleep(espera)
        for intento in range(3):
            self._ult = time.time()
            self.n += 1
            r = self.s.get(API + ruta, params=params, timeout=30)
            if r.status_code == 429:
                time.sleep(5 * (intento + 1))
                continue
            if r.status_code in (401, 403):
                raise PermissionError(f"Etsy {r.status_code}: {r.text[:160]}")
            r.raise_for_status()
            return r.json()
        raise RuntimeError("Etsy sigue devolviendo 429")


def a_cm(v, unidad):
    if v in (None, 0):
        return None
    f = {"in": 2.54, "inches": 2.54, "ft": 30.48, "mm": 0.1, "m": 100.0}.get((unidad or "cm").lower(), 1.0)
    return round(float(v) * f)


def normalizar(l, tienda=None):
    precio = l.get("price") or {}
    try:
        valor = precio["amount"] / precio["divisor"]
    except (KeyError, ZeroDivisionError, TypeError):
        return None
    moneda = precio.get("currency_code", "EUR")
    eur = round(valor * A_EUR[moneda], 2) if moneda in A_EUR else None

    imgs = l.get("images") or []
    img = imgs[0] if imgs else {}

    u = l.get("item_dimensions_unit")
    w, h, d = a_cm(l.get("item_width"), u), a_cm(l.get("item_height"), u), a_cm(l.get("item_length"), u)
    medidas = [x for x in (w, h, d) if x]
    medidas_txt = (" x ".join(str(x) for x in medidas) + " cm") if len(medidas) >= 2 else ""

    epoca, vintage = EPOCA.get(l.get("when_made") or "", (None, None))
    pais = None
    if tienda:
        pais = (tienda.get("shop_location_country_iso") or tienda.get("country_iso") or "").upper() or None

    desc = re.sub(r"\s+", " ", l.get("description") or "").strip()
    mats = ", ".join(l.get("materials") or [])
    etiquetas = ", ".join(l.get("tags") or [])
    texto = " . ".join(x for x in [
        l.get("title") or "", medidas_txt, epoca or "", mats, etiquetas, desc[:900]] if x)

    avisos = []
    if vintage is False:
        avisos.append(f"NUEVO, no vintage ({epoca}): reproduccion o pieza actual")
    if pais and pais not in UE:
        avisos.append(f"envia desde {pais}: aduana e IVA de importacion aparte")
    if moneda != "EUR":
        avisos.append(f"precio en {moneda}; el valor en euros es aproximado")

    nombre_tienda = (tienda or {}).get("shop_name") or ""
    return {
        "casa": "etsy",
        "casa_nombre": "Etsy" + (f" · {nombre_tienda}" if nombre_tienda else ""),
        "lote": str(l.get("listing_id")),
        "titulo": (l.get("title") or "")[:300],
        "texto": texto[:1500],
        "salida": eur,
        "precio_original": f"{valor:.2f} {moneda}",
        "imagen": img.get("url_570xN"),
        "imagen_grande": img.get("url_fullxfull"),
        "url": (l.get("url") or "").split("?")[0],
        "origen": "etsy-api",
        "no_vendido": False,
        "lado_mayor_cm": max(medidas) if medidas else 0,
        "ubicacion": pais,
        "precio_fijo": True,
        "historico": False,
        "epoca_etsy": epoca,
        "vintage": vintage,
        "avisos_fuente": avisos,
        "visto": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def buscar(api, consulta, tope_eur=900, cuantos=100, solo_ue=False):
    params = {"keywords": consulta, "limit": min(cuantos, 100), "sort_on": "score",
              "max_price": tope_eur}
    if solo_ue:
        params["shop_location"] = "Spain"
    res = api.get("/listings/active", **params)
    return [r["listing_id"] for r in res.get("results", [])]


def detalles(api, ids):
    """Ficha completa con fotos y tienda, de 100 en 100."""
    out = []
    for i in range(0, len(ids), 100):
        trozo = ids[i:i + 100]
        res = api.get("/listings/batch", listing_ids=",".join(str(x) for x in trozo),
                      includes="Images,Shop")
        out += res.get("results", [])
    return out


def rastrear(consultas=None, tope_eur=900):
    cab, error = credenciales()
    if error:
        print("ETSY:", error)
        return []
    api = Etsy(cab)
    consultas = consultas or BUSQUEDAS
    ids, vistos = [], set()
    print(f"\n=== Etsy (API oficial) · {len(consultas)} busquedas ===")
    for q in consultas:
        try:
            nuevos = [x for x in buscar(api, q, tope_eur) if x not in vistos]
        except PermissionError as e:
            print("  ", e)
            return []
        vistos.update(nuevos)
        ids += nuevos
        print(f"  {len(nuevos):3d}  {q}")
    fichas = detalles(api, ids)
    lotes = [x for x in (normalizar(f, f.get("shop")) for f in fichas) if x]
    print(f"  TOTAL Etsy: {len(lotes)} anuncios · {api.n} peticiones (limite diario 5.000)")
    return lotes


def guardar(lotes):
    os.makedirs(DIR_DATOS, exist_ok=True)
    datos = {"obtenido": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "lotes": lotes}
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False)
    return ARCHIVO


def cargar_si_fresco(max_horas=24):
    """Devuelve los anuncios solo si tienen menos de 24 h (condiciones de Etsy)."""
    if not os.path.exists(ARCHIVO):
        return [], "sin datos de Etsy todavia"
    datos = json.load(open(ARCHIVO, encoding="utf-8"))
    t = datetime.fromisoformat(datos["obtenido"])
    horas = (datetime.now(timezone.utc) - t).total_seconds() / 3600
    if horas > max_horas:
        return [], f"datos de Etsy de hace {horas:.0f} h: caducados, vuelve a pasar etsy.py"
    return datos["lotes"], f"Etsy de hace {horas:.1f} h"


if __name__ == "__main__":
    extra = [a for a in sys.argv[1:] if not a.startswith("-")]
    lotes = rastrear(extra or None)
    if lotes:
        print("guardado en", guardar(lotes))
