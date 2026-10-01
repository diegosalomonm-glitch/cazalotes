# -*- coding: utf-8 -*-
"""
La plantilla HTML de la vista, separada para que vista.py quede legible.

Logica de diseno: sala de subastas. Fondo neutro de galeria, la fotografia
manda y ocupa, y los datos van en cartela pequena, como la etiqueta de pared
de un museo. Nada de tarjetas decoradas: el objeto es el protagonista.
"""

PLANTILLA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CazaLotes</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Archivo+Narrow:wght@400;600&display=swap">
<style>
:root{
  --fondo:#f2f1ee; --panel:#fff; --tinta:#16150f; --suave:#5d5a54;
  --linea:#dcd9d2; --acento:#8c2f22; --verde:#2d6149; --ambar:#775412;
  --ui:'Archivo',system-ui,-apple-system,sans-serif;
  --etq:'Archivo Narrow','Archivo',system-ui,sans-serif;
  --ancho:300px;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --fondo:#121210; --panel:#1b1a17; --tinta:#eeece6; --suave:#a8a39a;
  --linea:#2b2924; --acento:#d9705d; --verde:#6cb795; --ambar:#d2a44a;
  color-scheme:dark;
}}
:root[data-theme="dark"]{
  --fondo:#121210; --panel:#1b1a17; --tinta:#eeece6; --suave:#a8a39a;
  --linea:#2b2924; --acento:#d9705d; --verde:#6cb795; --ambar:#d2a44a;
  color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--fondo);color:var(--tinta);font-family:var(--ui);
  font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}

.barra{position:sticky;top:0;z-index:30;background:var(--fondo);
  border-bottom:1px solid var(--linea)}
.barra-in{display:flex;gap:10px;align-items:center;flex-wrap:wrap;
  padding:11px 20px;max-width:1700px;margin:0 auto}
.marca{font-weight:700;font-size:16px;letter-spacing:-.02em;margin:0 6px 0 0}
.marca em{font-style:normal;color:var(--acento)}
input,select,button{font:inherit;font-size:13px;color:inherit;background:var(--panel);
  border:1px solid var(--linea);border-radius:8px;padding:6px 10px}
input[type=range]{padding:0;border:0;background:none;width:108px;accent-color:var(--acento)}
button{cursor:pointer;transition:border-color .12s,background .12s}
button:hover{border-color:var(--suave)}
button.on{background:var(--acento);color:#fff;border-color:var(--acento)}
label.ctrl{display:flex;align-items:center;gap:6px;font-family:var(--etq);
  font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--suave)}
label.ctrl b{color:var(--tinta);font-variant-numeric:tabular-nums;min-width:52px}
.recuento{font-family:var(--etq);font-size:11.5px;letter-spacing:.05em;
  text-transform:uppercase;color:var(--suave);padding:0 20px 9px;
  max-width:1700px;margin:0 auto}
.recuento b{color:var(--tinta)}

.rejilla{display:grid;gap:18px;padding:20px;max-width:1700px;margin:0 auto;
  grid-template-columns:repeat(auto-fill,minmax(var(--ancho),1fr))}
.ficha{background:var(--panel);border:1px solid var(--linea);border-radius:3px;
  overflow:hidden;display:flex;flex-direction:column;cursor:pointer;
  transition:border-color .15s,transform .15s}
.ficha:hover{border-color:var(--suave);transform:translateY(-3px)}
.ficha:focus-visible{outline:2px solid var(--acento);outline-offset:3px}
.ficha.apagada{opacity:.22}
.lienzo{aspect-ratio:4/5;background:var(--fondo);position:relative;overflow:hidden}
.lienzo img{width:100%;height:100%;object-fit:cover;display:block;
  transition:transform .4s ease}
.ficha:hover .lienzo img{transform:scale(1.03)}
.lienzo img.pobre{filter:saturate(.8)}
.novale{display:flex;align-items:center;justify-content:center;height:100%;
  font-family:var(--etq);font-size:11px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--suave)}
.sellos{position:absolute;top:10px;left:10px;display:flex;flex-direction:column;
  gap:5px;align-items:flex-start}
.sello{font-family:var(--etq);font-size:10px;letter-spacing:.07em;
  text-transform:uppercase;padding:3px 8px;border-radius:2px;
  background:var(--tinta);color:var(--fondo)}
.sello.rojo{background:var(--acento);color:#fff}
.sello.gris{background:var(--suave);color:var(--fondo)}

.cartela{padding:13px 14px 14px;display:flex;flex-direction:column;gap:8px;flex:1}
.cifra{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap}
.cifra b{font-size:21px;font-weight:600;letter-spacing:-.025em;
  font-variant-numeric:tabular-nums}
.cifra span{font-family:var(--etq);font-size:11px;color:var(--suave);letter-spacing:.03em}
.nombre{font-size:13.5px;line-height:1.38;display:-webkit-box;-webkit-line-clamp:2;
  -webkit-box-orient:vertical;overflow:hidden}
.tecnicos{font-family:var(--etq);font-size:11px;letter-spacing:.03em;
  color:var(--suave);display:flex;gap:9px;flex-wrap:wrap}
.tecnicos i{font-style:normal}
.medidor{display:flex;gap:3px;margin-top:1px}
.m{flex:1;min-width:0}
.m i{display:block;height:2px;background:var(--linea);border-radius:1px}
.m i span{display:block;height:100%;border-radius:1px;background:var(--acento)}
.m.op i span{background:var(--verde)}
.m u{display:block;font-family:var(--etq);font-size:9px;letter-spacing:.05em;
  text-transform:uppercase;color:var(--suave);text-decoration:none;margin-top:3px}
.motivo{font-size:11.5px;line-height:1.4;color:var(--verde)}
.alerta{font-size:11.5px;line-height:1.4;color:var(--acento)}

.votos{display:flex;gap:3px;margin-top:auto;padding-top:9px}
.v{flex:1;min-height:38px;padding:5px 0;font-size:16px;line-height:1;
  text-align:center;border-radius:4px;background:transparent;
  border:1px solid transparent}
.v:hover{background:var(--fondo)}
.v.on{background:var(--acento);border-color:var(--acento)}

.velo{position:fixed;inset:0;z-index:60;background:rgba(10,9,7,.74);
  display:flex;align-items:center;justify-content:center;padding:24px}
.hoja{position:relative;background:var(--panel);border-radius:4px;max-width:1150px;
  width:100%;max-height:92vh;overflow:auto;display:grid;grid-template-columns:1.2fr .8fr}
.hoja .foto{background:var(--fondo);display:flex;align-items:center;
  justify-content:center;min-height:320px;padding:22px}
.hoja .foto img{max-width:100%;max-height:78vh;object-fit:contain}
.hoja .info{padding:26px 28px;display:flex;flex-direction:column;gap:14px;min-width:0}
.hoja h2{font-size:19px;line-height:1.3;margin:0;font-weight:600;text-wrap:balance}
.hoja .precio{font-size:30px;font-weight:600;letter-spacing:-.03em;
  font-variant-numeric:tabular-nums}
.hoja .precio em{font-style:normal;font-size:13px;font-weight:400;color:var(--suave);
  font-family:var(--etq);margin-left:8px}
dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:6px 16px;font-size:13px}
dt{font-family:var(--etq);font-size:11px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--suave);white-space:nowrap}
dd{margin:0;min-width:0;overflow-wrap:anywhere}
.caja{border-left:2px solid var(--linea);padding:3px 0 3px 12px;font-size:13px;line-height:1.5}
.caja.bien{border-color:var(--verde);color:var(--verde)}
.caja.mal{border-color:var(--acento);color:var(--acento)}
.caja.ojo{border-color:var(--ambar);color:var(--ambar)}
.acciones{display:flex;gap:9px;margin-top:auto;padding-top:6px;flex-wrap:wrap}
.btn{text-decoration:none;padding:9px 16px;border-radius:7px;font-size:13px;
  font-weight:500;border:1px solid var(--linea);color:var(--tinta);background:var(--panel)}
.btn.fuerte{background:var(--acento);border-color:var(--acento);color:#fff}
.cerrar{position:absolute;top:16px;right:18px;width:34px;height:34px;border-radius:50%;
  font-size:16px;line-height:1;display:flex;align-items:center;justify-content:center;z-index:2}
.paso{position:fixed;top:50%;transform:translateY(-50%);width:42px;height:42px;
  border-radius:50%;font-size:17px;z-index:61;display:flex;align-items:center;
  justify-content:center}
.paso.izq{left:14px} .paso.der{right:14px}
.nada{padding:70px 20px;text-align:center;color:var(--suave);font-family:var(--etq);
  letter-spacing:.05em;text-transform:uppercase;font-size:12px}

@media(max-width:860px){ .hoja{grid-template-columns:1fr;max-height:88vh}
  .hoja .foto{min-height:0} .hoja .foto img{max-height:46vh} .paso{display:none} }
@media(pointer:coarse){ .v{min-height:44px} }
@media(max-width:560px){ :root{--ancho:150px} .rejilla{gap:11px;padding:12px}
  .barra-in{padding:10px 14px} .recuento{padding:0 14px 8px} .velo{padding:0}
  .hoja{border-radius:0;max-height:100vh;height:100%} }
@media (prefers-reduced-motion:reduce){ *{transition:none!important} }
</style></head><body>

<header class="barra"><div class="barra-in">
  <h1 class="marca">Caza<em>Lotes</em></h1>
  <input id="q" aria-label="Buscar por texto" placeholder="buscar&hellip;" style="flex:1;min-width:120px">
  <select id="fuente" aria-label="Filtrar por fuente"><option value="">todas las fuentes</option></select>
  <label class="ctrl">hasta <b id="pmax">600 &euro;</b>
    <input type="range" id="precio" aria-label="Precio maximo en euros" min="0" max="3000" step="25" value="600"></label>
  <label class="ctrl">ancho <b id="amax">&mdash;</b>
    <input type="range" id="ancho" aria-label="Ancho maximo en centimetros" min="0" max="300" step="10" value="0"></label>
  <select id="orden" aria-label="Ordenar resultados">
    <option value="g">por gusto</option><option value="o">por oportunidad</option>
    <option value="lg">por log&iacute;stica</option><option value="cf">por confianza</option>
    <option value="precio">por precio</option>
  </select>
  <button id="solonov">sin vender</button>
  <button id="nitidas">solo n&iacute;tidas</button>
  <button id="ocultano">ocultar descartados</button>
  <button id="densidad" data-d="1">tama&ntilde;o</button>
  <button id="exportar">exportar votos</button>
</div>
<div class="recuento"><b id="cuenta">0</b> de __TOTAL__ lotes &middot; __FECHA__
  <span id="pobres"></span></div></header>

<main id="rejilla" class="rejilla" aria-label="Lotes encontrados"></main>
<div id="nada" class="nada" hidden>Nada encaja con estos filtros</div>
<div id="velo" class="velo" hidden></div>

<script>
const DATOS = __DATOS__;
const K='cazalotes.votos', KP='cazalotes.pobres';
let votos={}, pobres={};
try{ votos=JSON.parse(localStorage.getItem(K)||'{}'); }catch(e){}
try{ pobres=JSON.parse(localStorage.getItem(KP)||'{}'); }catch(e){}
function guardar(){ try{ localStorage.setItem(K,JSON.stringify(votos));
  localStorage.setItem(KP,JSON.stringify(pobres)); }catch(e){} }
const $=s=>document.querySelector(s);
const VOTOS=[['3','❤️'],['2','👍'],['1','😐'],
             ['0','👎'],['x','🚫']];
const ANCHOS=[220,300,400];
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,
  c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let visibles=[];

$('#fuente').innerHTML+=[...new Set(DATOS.map(d=>d.fuente))].sort()
  .map(f=>'<option>'+esc(f)+'</option>').join('');

function med(v,e,op){
  return '<div class="m'+(op?' op':'')+'"><i><span style="width:'+v+'%"></span></i><u>'+e+' '+v+'</u></div>';
}

function ficha(d,i){
  const v=votos[d.id];
  const img=d.img
    ? '<img loading="lazy" src="'+esc(d.img)+'" alt="'+esc(d.titulo)+'" data-id="'+esc(d.id)+'">'
    : '<div class="novale">sin fotografía</div>';
  const sellos=(d.nov?'<span class="sello rojo">no vendido</span>':'')
    +(pobres[d.id]?'<span class="sello gris">foto pobre</span>':'');
  const tec=[d.dims,d.periodo,(d.mats||[]).slice(0,2).join(' · '),d.donde]
    .filter(Boolean).map(x=>'<i>'+esc(x)+'</i>').join('');
  const real=(d.total&&Math.round(d.total)!==Math.round(d.salida))
    ? '<span>→ '+Math.round(d.total)+' € real</span>'
    : (d.fijo?'<span>precio final</span>':'');
  return '<article class="ficha'+(v==='x'||v==='0'?' apagada':'')+'" data-i="'+i+'" tabindex="0">'
    +'<div class="lienzo">'+img+'<div class="sellos">'+sellos+'</div></div>'
    +'<div class="cartela">'
    +'<div class="cifra"><b>'+(d.salida!=null?Math.round(d.salida)+' €':'—')+'</b>'+real+'</div>'
    +'<div class="nombre">'+esc(d.titulo)+'</div>'
    +'<div class="tecnicos">'+tec+'<i>'+esc(d.fuente)+'</i></div>'
    +'<div class="medidor">'+med(d.g,'gusto')+med(d.o,'oport',1)+med(d.lg,'logís')+med(d.cf,'conf')+'</div>'
    +(d.porque.length?'<div class="motivo">'+esc(d.porque.slice(0,2).join(' · '))+'</div>':'')
    +(d.riesgos.length?'<div class="alerta">'+esc(d.riesgos[0])+'</div>':'')
    +'<div class="votos">'+VOTOS.map(p=>'<button class="v'+(v===p[0]?' on':'')
        +'" data-v="'+p[0]+'" data-id="'+esc(d.id)+'">'+p[1]+'</button>').join('')+'</div>'
    +'</div></article>';
}

function pintar(){
  const q=$('#q').value.toLowerCase().trim(), fu=$('#fuente').value;
  const pm=+$('#precio').value, am=+$('#ancho').value, ord=$('#orden').value;
  const soloNov=$('#solonov').classList.contains('on');
  const soloNit=$('#nitidas').classList.contains('on');
  const ocultar=$('#ocultano').classList.contains('on');
  visibles=DATOS.filter(function(d){
    if(q&&!(d.titulo+' '+d.fuente+' '+(d.mats||[]).join(' ')).toLowerCase().includes(q))return false;
    if(fu&&d.fuente!==fu)return false;
    if(pm&&d.salida!=null&&d.salida>pm)return false;
    if(am&&d.lado&&d.lado>am)return false;
    if(soloNov&&!d.nov)return false;
    if(soloNit&&pobres[d.id])return false;
    if(ocultar&&(votos[d.id]==='x'||votos[d.id]==='0'))return false;
    return true;
  }).sort(function(a,b){
    return ord==='precio' ? (a.salida==null?1e9:a.salida)-(b.salida==null?1e9:b.salida)
                          : b[ord]-a[ord];
  });
  $('#rejilla').innerHTML=visibles.map(ficha).join('');
  $('#nada').hidden=visibles.length>0;
  $('#cuenta').textContent=visibles.length;
  $('#pmax').textContent=pm?pm+' €':'sin tope';
  $('#amax').textContent=am?am+' cm':'—';
  const np=Object.keys(pobres).length;
  $('#pobres').textContent=np?' · '+np+' con foto de baja resolución':'';
}

document.addEventListener('load',function(e){
  const im=e.target;
  if(im.tagName!=='IMG'||!im.dataset.id)return;
  if(im.naturalWidth&&im.naturalWidth<340){
    pobres[im.dataset.id]=im.naturalWidth;
    im.classList.add('pobre');
    const s=im.closest('.lienzo').querySelector('.sellos');
    if(s&&!s.querySelector('.gris'))
      s.insertAdjacentHTML('beforeend','<span class="sello gris">foto pobre</span>');
    guardar();
  }
},true);

let actual=-1;
function detalle(i){
  actual=i; const d=visibles[i]; if(!d)return;
  const v=votos[d.id];
  const filas=[['fuente',d.fuente],['lote',d.lote],['medidas',d.dims],
    ['periodo',d.periodo],['materiales',(d.mats||[]).join(', ')],['dónde',d.donde],
    ['salida',d.salida!=null?Math.round(d.salida)+' €':null],
    ['coste real',d.total?Math.round(d.total)+' € ('+(d.recargo||0)+' % encima)':null]]
    .filter(p=>p[1]).map(p=>'<dt>'+esc(p[0])+'</dt><dd>'+esc(p[1])+'</dd>').join('');
  $('#velo').innerHTML='<div class="hoja" role="dialog" aria-modal="true" aria-label="'+esc(d.titulo)+'" tabindex="-1">'
    +'<div class="foto">'+(d.img?'<img src="'+esc(d.img)+'" alt="'+esc(d.titulo)+'">'
        :'<div class="novale">sin fotografía</div>')+'</div>'
    +'<div class="info">'
    +'<button class="cerrar" id="x" aria-label="Cerrar">✕</button>'
    +'<div class="precio">'+(d.salida!=null?Math.round(d.salida)+' €':'—')
    +((d.total&&Math.round(d.total)!==Math.round(d.salida))
        ?'<em>'+Math.round(d.total)+' € puestos en casa</em>'
        :(d.fijo?'<em>precio final</em>':''))+'</div>'
    +'<h2>'+esc(d.titulo)+'</h2>'
    +'<dl>'+filas+'</dl>'
    +'<div class="medidor">'+med(d.g,'gusto')+med(d.o,'oport',1)+med(d.lg,'logís')+med(d.cf,'conf')+'</div>'
    +(d.porque.length?'<div class="caja bien">'+esc(d.porque.join(' · '))+'</div>':'')
    +(d.opq.length?'<div class="caja bien">oportunidad: '+esc(d.opq.join(', '))+'</div>':'')
    +d.riesgos.map(r=>'<div class="caja mal">'+esc(r)+'</div>').join('')
    +d.avisos.map(a=>'<div class="caja ojo">'+esc(a)+'</div>').join('')
    +(pobres[d.id]?'<div class="caja ojo">La foto del catálogo mide '+pobres[d.id]
        +' px de ancho. Pide fotos mejores antes de decidir.</div>':'')
    +'<div class="votos">'+VOTOS.map(p=>'<button class="v'+(v===p[0]?' on':'')
        +'" data-v="'+p[0]+'" data-id="'+esc(d.id)+'">'+p[1]+'</button>').join('')+'</div>'
    +'<div class="acciones">'
    +'<a class="btn fuerte" href="'+esc(d.url)+'" target="_blank" rel="noopener">Ver en '+esc(d.fuente)+'</a>'
    +'<button class="btn" id="sig">Siguiente →</button></div>'
    +'</div></div>'
    +'<button class="paso izq" id="ant" aria-label="Anterior">←</button>'
    +'<button class="paso der" id="des" aria-label="Siguiente">→</button>';
  $('#velo').hidden=false; document.body.style.overflow='hidden';
  const h=$('.hoja'); if(h) h.focus();
}
function cerrar(){ $('#velo').hidden=true; document.body.style.overflow=''; actual=-1; }
function mover(n){ const i=actual+n; if(i>=0&&i<visibles.length)detalle(i); }

document.addEventListener('click',function(e){
  const bv=e.target.closest('.v');
  if(bv){ e.stopPropagation();
    const id=bv.dataset.id,k=bv.dataset.v;
    if(votos[id]===k) delete votos[id]; else votos[id]=k;
    guardar(); const abierto=actual; pintar(); if(abierto>=0)detalle(abierto); return; }
  if(e.target.closest('#x')||e.target.id==='velo'){ cerrar(); return; }
  if(e.target.closest('#sig')||e.target.closest('#des')){ mover(1); return; }
  if(e.target.closest('#ant')){ mover(-1); return; }
  const f=e.target.closest('.ficha');
  if(f&&!e.target.closest('a')) detalle(+f.dataset.i);
});
document.addEventListener('keydown',function(e){
  if($('#velo').hidden){
    if(e.key==='Enter'&&document.activeElement&&document.activeElement.classList.contains('ficha'))
      detalle(+document.activeElement.dataset.i);
    return; }
  if(e.key==='Escape')cerrar();
  if(e.key==='ArrowRight')mover(1);
  if(e.key==='ArrowLeft')mover(-1);
});

['q','fuente','precio','ancho','orden'].forEach(function(id){
  $('#'+id).addEventListener('input',pintar); });
['solonov','nitidas','ocultano'].forEach(function(id){
  $('#'+id).addEventListener('click',function(e){
    e.currentTarget.classList.toggle('on'); pintar(); }); });
$('#densidad').addEventListener('click',function(e){
  const n=(+e.currentTarget.dataset.d+1)%3;
  e.currentTarget.dataset.d=n;
  document.documentElement.style.setProperty('--ancho',ANCHOS[n]+'px'); });
$('#exportar').addEventListener('click',function(){
  const ix={}; DATOS.forEach(d=>{ ix[d.id]=d; });
  const nombres={'3':'love','2':'like','1':'maybe','0':'no','x':'nunca'};
  const out=Object.keys(votos).map(function(id){
    return {voto:nombres[votos[id]], titulo:ix[id]&&ix[id].titulo,
            fuente:ix[id]&&ix[id].fuente, salida:ix[id]&&ix[id].salida, url:id}; });
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([JSON.stringify(out,null,1)],{type:'application/json'}));
  a.download='votos.json'; a.click(); });

pintar();
</script></body></html>
"""
