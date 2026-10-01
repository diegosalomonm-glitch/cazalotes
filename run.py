# -*- coding: utf-8 -*-
"""
Pasada diaria. Uso:
    .venv/bin/python run.py              todas las casas
    .venv/bin/python run.py salaretiro   una sola
    .venv/bin/python run.py --informe    sin rastrear, solo puntuar lo guardado
"""
import json
import warnings
warnings.simplefilter('ignore')
import os
import sys

from casas import CASAS
from scraper import DIR_DATOS, ParadaTotal, guardar, rastrear_casa
from puntuar import ficha, ranking


def cargar():
    ruta = os.path.join(DIR_DATOS, "lotes.json")
    if not os.path.exists(ruta):
        return []
    return json.load(open(ruta, encoding="utf-8"))


def main():
    args = [a for a in sys.argv[1:]]
    solo_informe = "--informe" in args
    con_hist = "--historico" in args
    casas = [a for a in args if a in CASAS] or list(CASAS)
    if con_hist:
        print("Incluyendo el archivo historico: esto tarda horas.")

    if not solo_informe:
        todos = []
        for cid in sorted(casas, key=lambda c: CASAS[c]["prioridad"]):
            try:
                todos += rastrear_casa(cid, con_historico=con_hist)
            except ParadaTotal as e:
                print(f"\n!! PARADA TOTAL en {cid}: {e}")
                print("   No reintentes en bucle. Revisa robots.txt y avisa.")
            except Exception as e:
                print(f"  fallo en {cid}: {type(e).__name__}: {e}")
        if todos:
            nuevos, total = guardar(todos)
            print(f"\nGuardados: {nuevos} nuevos, {total} en total.")

    lotes = cargar()
    if not lotes:
        print("\nSin datos todavia.")
        return

    top = ranking(lotes)
    print("\n" + "=" * 78)
    print(f"  {len(top)} lotes encajan con tu perfil, de {len(lotes)} vistos")
    print("=" * 78)
    for l in top[:25]:
        print()
        print(ficha(l))

    rebajados = [l for l in top if any("BAJO DE PRECIO" in r for r in l["razones"])]
    if rebajados:
        print("\n\n### HAN BAJADO DE PRECIO DESDE LA ULTIMA PASADA")
        for l in rebajados:
            print(ficha(l))


if __name__ == "__main__":
    main()
