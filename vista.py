# -*- coding: utf-8 -*-
"""
Genera datos/vista.html: la rejilla visual para escanear cientos de lotes rapido.

Decisiones que vienen del brief de Diego:
  - La imagen manda. Todo lo demas es secundario.
  - Puntuaciones SEPARADAS (gusto, oportunidad, logistica, confianza), nunca
    una sola nota opaca.
  - Lo desconocido se queda desconocido. No se inventa envio ni condicion.
  - El feedback se guarda y se exporta, para que vuelva al perfil.
"""
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from casas import CASAS
from encargo import dimensiones
from puntuar import ranking
from scraper import DIR_DATOS


# --------------------------------------------------------------------------
# Puntuaciones separadas
# --------------------------------------------------------------------------
def escalar(v, tope):
    return max(0, min(100, round(100 * v / tope))) if tope else 0


def puntuaciones(l):
    gusto = escalar(l.get("puntos", 0), 20)

    # Oportunidad: no vendido, bajada de precio, atribucion floja pero objeto
    # fisico interesante. NUNCA decimos "infravalorado" sin evidencia.
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
    open(salida, "w", encoding="utf-8").write(html)
    return salida, len(datos), len(lotes)


PLANTILLA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CazaLotes</title>
<style>
:root{
  --papel:#faf8f4; --tinta:#1a1a1a; --suave:#6e6a62; --linea:#e2ddd3;
  --acento:#8a5a2b; --verde:#2f6b4f; --rojo:#9c3b2e; --tarjeta:#fff;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --papel:#171614; --tinta:#eceae6; --suave:#9a958c; --linea:#2e2b27;
  --acento:#c8935e; --verde:#6fbf96; --rojo:#e0806f; --tarjeta:#201e1b;
}}
:root[data-theme="dark"]{
  --papel:#171614; --tinta:#eceae6; --suave:#9a958c; --linea:#2e2b27;
  --acento:#c8935e; --verde:#6fbf96; --rojo:#e0806f; --tarjeta:#201e1b;
}
*{box-sizing:border-box}
body{margin:0;background:var(--papel);color:var(--tinta);
  font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
header{position:sticky;top:0;z-index:20;background:var(--papel);
  border-bottom:1px solid var(--linea);padding:12px 16px}
.fila{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
h1{font-size:17px;margin:0 14px 0 0;font-weight:700;letter-spacing:-.01em}
.meta{color:var(--suave);font-size:12.5px}
input,select,button{font:inherit;color:inherit;background:var(--tarjeta);
  border:1px solid var(--linea);border-radius:7px;padding:5px 9px}
input[type=range]{padding:0;background:none;border:none;width:120px}
button{cursor:pointer}
button.on{background:var(--acento);color:#fff;border-color:var(--acento)}
.rejilla{display:grid;gap:14px;padding:16px;
  grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.c{background:var(--tarjeta);border:1px solid var(--linea);border-radius:11px;
  overflow:hidden;display:flex;flex-direction:column;transition:.12s}
.c:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.09)}
.c.no{opacity:.28}
.foto{aspect-ratio:1;background:var(--papel);position:relative;overflow:hidden}
.foto img{width:100%;height:100%;object-fit:cover;display:block}
.sinfoto{display:flex;align-items:center;justify-content:center;height:100%;
  color:var(--suave);font-size:12px}
.cinta{position:absolute;top:8px;left:8px;background:var(--rojo);color:#fff;
  font-size:10.5px;padding:2px 7px;border-radius:20px;letter-spacing:.02em}
.cuerpo{padding:11px 12px 12px;display:flex;flex-direction:column;gap:7px;flex:1}
.precio{font-size:19px;font-weight:700;letter-spacing:-.02em}
.precio small{font-size:11.5px;font-weight:400;color:var(--suave)}
.tit{font-size:13px;line-height:1.35;max-height:3.6em;overflow:hidden}
.datos{font-size:11.5px;color:var(--suave);display:flex;gap:7px;flex-wrap:wrap}
.barras{display:flex;gap:4px;margin-top:2px}
.b{flex:1;text-align:center;font-size:9.5px;color:var(--suave)}
.b i{display:block;height:3px;border-radius:2px;background:var(--linea);margin-bottom:3px}
.b i span{display:block;height:100%;border-radius:2px;background:var(--acento)}
.b.v i span{background:var(--verde)}
.porque{font-size:11px;color:var(--verde);line-height:1.35}
.riesgo{font-size:11px;color:var(--rojo);line-height:1.35}
.pie{display:flex;gap:4px;align-items:center;margin-top:auto;padding-top:8px}
.voto{flex:1;padding:4px 0;font-size:14px;line-height:1;text-align:center;border-radius:6px}
.ver{font-size:11px;text-decoration:none;color:var(--acento);padding:4px 7px;
  border:1px solid var(--linea);border-radius:6px;white-space:nowrap}
.vacio{padding:60px 20px;text-align:center;color:var(--suave)}
@media(max-width:600px){ .rejilla{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
  gap:10px;padding:12px} h1{width:100%} }
</style></head><body>

<header>
  <div class="fila">
    <h1>CazaLotes</h1>
    <input id="q" placeholder="buscar…" style="flex:1;min-width:130px">
    <select id="fuente"><option value="">todas las fuentes</option></select>
    <label class="meta">hasta <b id="pmax">600</b> €
      <input type="range" id="precio" min="0" max="3000" step="25" value="600"></label>
    <label class="meta">ancho máx <b id="amax">—</b>
      <input type="range" id="ancho" min="0" max="300" step="10" value="0"></label>
    <select id="orden">
      <option value="g">gusto</option><option value="o">oportunidad</option>
      <option value="lg">logística</option><option value="cf">confianza</option>
      <option value="precio">precio</option>
    </select>
    <button id="solonov">sin vender</button>
    <button id="ocultano">ocultar descartados</button>
    <button id="exportar">exportar votos</button>
  </div>
  <div class="fila meta" style="margin-top:7px">
    <span id="cuenta"></span> · __TOTAL__ lotes leídos · __FECHA__
  </div>
</header>

<div id="rejilla" class="rejilla"></div>
<div id="vacio" class="vacio" hidden>Nada encaja con estos filtros.</div>

<script>
const DATOS = __DATOS__;
const K = 'cazalotes.votos';
let votos = {};
try { votos = JSON.parse(localStorage.getItem(K) || '{}'); } catch(e) { votos = {}; }
const guardar = () => { try { localStorage.setItem(K, JSON.stringify(votos)); } catch(e){} };

const $ = s => document.querySelector(s);
const VOTOS = [['3','❤️'],['2','👍'],['1','😐'],['0','👎'],['x','🚫']];

const fuentes = [...new Set(DATOS.map(d => d.fuente))].sort();
$('#fuente').innerHTML += fuentes.map(f => `<option>${f}</option>`).join('');

const esc = s => String(s==null?'':s).replace(/[&<>"]/g, c =>
  ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function barra(v, etq, verde){
  return `<div class="b${verde?' v':''}"><i><span style="width:${v}%"></span></i>${etq} ${v}</div>`;
}

function tarjeta(d){
  const v = votos[d.id];
  const img = d.img
    ? `<img loading="lazy" src="${esc(d.img)}" alt="">`
    : `<div class="sinfoto">sin foto</div>`;
  const datos = [d.dims, d.periodo, (d.mats||[]).join(', '), d.donde]
    .filter(Boolean).map(x => `<span>${esc(x)}</span>`).join('');
  const total = d.total && d.total !== d.salida
    ? ` <small>→ ${Math.round(d.total)} € real</small>` : (d.fijo ? ' <small>precio final</small>' : '');
  return `<div class="c${v==='x'||v==='0'?' no':''}" data-id="${esc(d.id)}">
    <div class="foto">${img}${d.nov?'<span class="cinta">no vendido</span>':''}</div>
    <div class="cuerpo">
      <div class="precio">${d.salida!=null?Math.round(d.salida)+' €':'—'}${total}</div>
      <div class="tit">${esc(d.titulo)}</div>
      <div class="datos">${datos}<span>${esc(d.fuente)}</span></div>
      <div class="barras">${barra(d.g,'gusto')}${barra(d.o,'oport',1)}${barra(d.lg,'logís')}${barra(d.cf,'conf')}</div>
      ${d.porque.length?`<div class="porque">${esc(d.porque.join(' · '))}</div>`:''}
      ${d.riesgos.length?`<div class="riesgo">⚠ ${esc(d.riesgos.join(' · '))}</div>`:''}
      ${d.avisos.length?`<div class="riesgo">${esc(d.avisos[0])}</div>`:''}
      <div class="pie">
        ${VOTOS.map(([k,e])=>`<button class="voto${v===k?' on':''}" data-v="${k}">${e}</button>`).join('')}
        <a class="ver" href="${esc(d.url)}" target="_blank" rel="noopener">ver</a>
      </div>
    </div></div>`;
}

function pintar(){
  const q = $('#q').value.toLowerCase().trim();
  const fu = $('#fuente').value;
  const pm = +$('#precio').value;
  const am = +$('#ancho').value;
  const ord = $('#orden').value;
  const soloNov = $('#solonov').classList.contains('on');
  const ocultar = $('#ocultano').classList.contains('on');

  let f = DATOS.filter(d => {
    if (q && !(d.titulo+' '+d.fuente+' '+(d.mats||[]).join(' ')).toLowerCase().includes(q)) return false;
    if (fu && d.fuente !== fu) return false;
    if (pm && d.salida != null && d.salida > pm) return false;
    if (am && d.lado && d.lado > am) return false;
    if (soloNov && !d.nov) return false;
    if (ocultar && (votos[d.id]==='x' || votos[d.id]==='0')) return false;
    return true;
  });
  f.sort((a,b) => ord==='precio' ? (a.salida??1e9)-(b.salida??1e9) : b[ord]-a[ord]);

  $('#rejilla').innerHTML = f.map(tarjeta).join('');
  $('#vacio').hidden = f.length > 0;
  $('#cuenta').textContent = `${f.length} mostrados`;
  $('#pmax').textContent = pm || '∞';
  $('#amax').textContent = am ? am+' cm' : '—';
}

$('#rejilla').addEventListener('click', e => {
  const b = e.target.closest('.voto'); if (!b) return;
  const id = b.closest('.c').dataset.id, k = b.dataset.v;
  if (votos[id] === k) delete votos[id]; else votos[id] = k;
  guardar(); pintar();
});

['q','fuente','precio','ancho','orden'].forEach(id =>
  $('#'+id).addEventListener('input', pintar));
['solonov','ocultano'].forEach(id => $('#'+id).addEventListener('click', e => {
  e.target.classList.toggle('on'); pintar();
}));

$('#exportar').addEventListener('click', () => {
  const porId = Object.fromEntries(DATOS.map(d => [d.id, d]));
  const salida = Object.entries(votos).map(([id, v]) => ({
    voto: {'3':'love','2':'like','1':'maybe','0':'no','x':'nunca'}[v],
    titulo: porId[id]?.titulo, fuente: porId[id]?.fuente,
    salida: porId[id]?.salida, url: id
  }));
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(salida, null, 1)],
    {type:'application/json'}));
  a.download = 'votos.json'; a.click();
});

pintar();
</script></body></html>
"""


if __name__ == "__main__":
    minimo = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    ruta, mostrados, total = construir(minimo)
    print(f"{ruta}\n  {mostrados} lotes en la rejilla, de {total} leidos")
