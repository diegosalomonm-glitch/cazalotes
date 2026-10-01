# -*- coding: utf-8 -*-
"""
Duran carga sus lotes por AJAX (Laravel + token CSRF), asi que necesita su
propio adaptador. Sigue siendo navegacion publica anonima: no hay login.
"""
import re
import requests
from bs4 import BeautifulSoup

BASE = "https://www.duran-subastas.com"
from config import UA  # correo en config_local.py, fuera del repo


def sesion_con_token(ruta="/es/subastas-muebles"):
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9"})
    r = s.get(BASE + ruta, timeout=30)
    r.raise_for_status()
    m = re.search(r'name="csrf-token"\s+content="([^"]+)"', r.text)
    if not m:
        m = re.search(r'csrf[_-]?token["\']?\s*[:=]\s*["\']([A-Za-z0-9+/=]{20,})', r.text, re.I)
    return s, (m.group(1) if m else None), r.text


def pedir_lotes(s, token, ruta, pagina=1, extra=None):
    datos = {"page": pagina}
    if extra:
        datos.update(extra)
    h = {"X-Requested-With": "XMLHttpRequest", "Referer": BASE + ruta}
    if token:
        h["X-CSRF-TOKEN"] = token
        datos["_token"] = token
    r = s.post(BASE + "/es/GetAjaxLots", data=datos, headers=h, timeout=30)
    return r


if __name__ == "__main__":
    s, token, html = sesion_con_token()
    print("token:", (token or "NINGUNO")[:24])
    for pagina in (1,):
        r = pedir_lotes(s, token, "/es/subastas-muebles", pagina)
        print(f"  page {pagina}: HTTP {r.status_code}  bytes {len(r.text)}")
        txt = r.text
        print("  inicio:", txt[:260].replace("\n", " "))
        if r.status_code == 200 and len(txt) > 500:
            soup = BeautifulSoup(txt, "lxml")
            enlaces = [a["href"] for a in soup.find_all("a", href=True)
                       if "lote" in a["href"]]
            print(f"  enlaces de lote: {len(enlaces)}")
            for e in enlaces[:4]:
                print("   ", e)
