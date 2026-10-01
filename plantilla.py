# -*- coding: utf-8 -*-
"""
Plantilla HTML de la vista.

SISTEMA DE DISENO
-----------------
No sale de mirar los pines de Diego: su exportacion de Pinterest no trae
imagenes, solo URLs y nombres de tablero. Sale de lo que si esta documentado:

  Barragan   -> planos grandes de color saturado, muro y sombra, no "acento
                sobre crema". El color es arquitectura, no adorno.
  Shaker     -> nada decorativo que no sea estructural. Lineas rectas, union
                visible, proporcion precisa.
  Judd       -> repeticion exacta, cajas identicas, el intervalo importa tanto
                como el objeto.
  Su 50/50 maximalista-minimalista -> el fondo calla, la pieza grita.

Traduccion: la barra es un PLANO de color (muro de Barragan). La rejilla es una
retícula estricta de cajas identicas (Judd) sobre yeso neutro. Cero sombras,
cero degradados, cero esquinas redondeadas blandas: los cantos son rectos
porque en Shaker la union se ve.
"""

PLANTILLA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CazaLotes</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=Archivo+Narrow:wght@400;600&display=swap">
<style>
:root{
  --yeso:#eceae4; --caja:#fff; --tinta:#14130f; --gris:#5d5a54; --borde:#d6d2c9;
  --muro:#2e4a52;          /* el plano de color de la barra */
  --muro-tinta:#f3f1ea;
  --rosa:#a8423b;          /* accion y alerta */
  --verde:#2d6149; --ocre:#775412;
  --ui:'Archivo',system-ui,-apple-system,sans-serif;
  --etq:'Archivo Narrow','Archivo',system-ui,sans-serif;
  --ancho:300px;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --yeso:#14130f; --caja:#1c1a16; --tinta:#eeece6; --gris:#a8a39a; --borde:#2d2a24;
  --muro:#1d3238; --muro-tinta:#dfe6e5;
  --rosa:#d9705d; --verde:#6cb795; --ocre:#d2a44a;
  color-scheme:dark;
}}
:root[data-theme="dark"]{
  --yeso:#14130f; --caja:#1c1a16; --tinta:#eeece6; --gris:#a8a39a; --borde:#2d2a24;
  --muro:#1d3238; --muro-tinta:#dfe6e5;
  --rosa:#d9705d; --verde:#6cb795; --ocre:#d2a44a;
  color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--yeso);color:var(--tinta);font-family:var(--ui);
  font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}

/* ---- el muro ---- */
.muro{position:sticky;top:0;z-index:30;background:var(--muro);color:var(--muro-tinta)}
.muro-in{display:flex;gap:10px;align-items:center;flex-wrap:wrap;
  padding:13px 22px;max-width:1700px;margin:0 auto}
.marca{font-weight:800;font-size:17px;letter-spacing:-.03em;margin:0 10px 0 0;
  text-transform:uppercase}
.marca em{font-style:normal;opacity:.55}
.muro input,.muro select,.muro button{font:inherit;font-size:13px;
  color:var(--muro-tinta);background:rgba(255,255,255,.09);
  border:1px solid rgba(255,255,255,.22);border-radius:0;padding:6px 10px}
.muro input::placeholder{color:var(--muro-tinta);opacity:.55}
.muro select option{color:var(--tinta);background:var(--caja)}
.muro button{cursor:pointer}
.muro button:hover{background:rgba(255,255,255,.17)}
.muro button.on{background:var(--muro-tinta);color:var(--muro);border-color:var(--muro-tinta)}
.cuenta{font-family:var(--etq);font-size:11.5px;letter-spacing:.07em;
  text-transform:uppercase;padding:0 22px 11px;max-width:1700px;margin:0 auto;
  opacity:.75}
.cuenta b{opacity:1;font-weight:600}

/* ---- panel de busqueda ---- */
.panel{background:var(--caja);border-bottom:1px solid var(--borde)}
.panel-in{max-width:1700px;margin:0 auto;padding:18px 22px 20px;
  display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(215px,1fr))}
.grupo{display:flex;flex-direction:column;gap:7px;min-width:0}
.grupo h3{margin:0;font-family:var(--etq);font-size:11px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--gris);font-weight:600}
.panel input,.panel select{font:inherit;font-size:13px;color:var(--tinta);
  background:var(--yeso);border:1px solid var(--borde);border-radius:0;padding:7px 9px;
  width:100%}
.medidas{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.medidas label{display:flex;flex-direction:column;gap:3px;font-family:var(--etq);
  font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--gris)}
.fichas{display:flex;flex-wrap:wrap;gap:5px}
.chip{font-family:var(--etq);font-size:11px;letter-spacing:.04em;padding:5px 10px;
  border:1px solid var(--borde);background:var(--yeso);color:var(--tinta);
  cursor:pointer;border-radius:0;min-height:30px}
.chip.on{background:var(--tinta);color:var(--yeso);border-color:var(--tinta)}
.ayuda{font-size:11.5px;color:var(--gris);line-height:1.45}
.panel .acc{display:flex;gap:7px;flex-wrap:wrap;align-items:flex-end}
.panel .acc button{font-family:var(--ui);font-size:13px;padding:8px 14px;
  border:1px solid var(--borde);background:var(--yeso);cursor:pointer;border-radius:0}
.panel .acc button.primaria{background:var(--rosa);border-color:var(--rosa);color:#fff}

/* ---- reticula ---- */
.rejilla{display:grid;gap:20px;padding:22px;max-width:1700px;margin:0 auto;
  grid-template-columns:repeat(auto-fill,minmax(var(--ancho),1fr))}
.ficha{background:var(--caja);border:1px solid var(--borde);overflow:hidden;
  display:flex;flex-direction:column;cursor:pointer;transition:border-color .12s}
.ficha:hover{border-color:var(--tinta)}
.ficha:focus-visible{outline:2px solid var(--rosa);outline-offset:2px}
.ficha.apagada{opacity:.2}
.lienzo{aspect-ratio:4/5;background:var(--yeso);position:relative;overflow:hidden}
.lienzo img{width:100%;height:100%;object-fit:cover;display:block}
.lienzo img.pobre{filter:saturate(.75)}
.novale{display:flex;align-items:center;justify-content:center;height:100%;
  font-family:var(--etq);font-size:11px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--gris)}
.sellos{position:absolute;top:0;left:0;display:flex;flex-direction:column;align-items:flex-start}
.sello{font-family:var(--etq);font-size:10px;letter-spacing:.08em;
  text-transform:uppercase;padding:4px 9px;background:var(--tinta);color:var(--yeso)}
.sello.rosa{background:var(--rosa);color:#fff}
.sello.gris{background:var(--gris);color:var(--yeso)}

.cartela{padding:13px 14px 14px;display:flex;flex-direction:column;gap:8px;flex:1}
.cifra{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap}
.cifra b{font-size:21px;font-weight:600;letter-spacing:-.025em;
  font-variant-numeric:tabular-nums}
.cifra span{font-family:var(--etq);font-size:11px;color:var(--gris);letter-spacing:.03em}
.nombre{font-size:13.5px;line-height:1.38;display:-webkit-box;-webkit-line-clamp:2;
  -webkit-box-orient:vertical;overflow:hidden}
.tecnicos{font-family:var(--etq);font-size:11px;letter-spacing:.03em;
  color:var(--gris);display:flex;gap:9px;flex-wrap:wrap}
.tecnicos i{font-style:normal}
.medidor{display:flex;gap:4px;margin-top:1px}
.m{flex:1;min-width:0}
.m i{display:block;height:2px;background:var(--borde)}
.m i span{display:block;height:100%;background:var(--tinta)}
.m.op i span{background:var(--verde)}
.m u{display:block;font-family:var(--etq);font-size:9px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--gris);text-decoration:none;margin-top:3px}
.motivo{font-size:11.5px;line-height:1.4;color:var(--verde)}
.alerta{font-size:11.5px;line-height:1.4;color:var(--rosa)}
.votos{display:flex;gap:4px;margin-top:auto;padding-top:9px}
.v{flex:1;min-height:38px;font-size:16px;line-height:1;text-align:center;
  background:transparent;border:1px solid transparent;cursor:pointer;border-radius:0}
.v:hover{background:var(--yeso)}
.v.on{background:var(--tinta);border-color:var(--tinta)}

/* ---- detalle ---- */
.velo{position:fixed;inset:0;z-index:60;background:rgba(8,8,6,.8);
  display:flex;align-items:center;justify-content:center;padding:26px}
.hoja{position:relative;background:var(--caja);max-width:1150px;width:100%;
  max-height:92vh;overflow:auto;display:grid;grid-template-columns:1.2fr .8fr}
.hoja .foto{background:var(--yeso);display:flex;align-items:center;
  justify-content:center;min-height:320px;padding:24px}
.hoja .foto img{max-width:100%;max-height:78vh;object-fit:contain}
.hoja .info{padding:26px 28px;display:flex;flex-direction:column;gap:14px;min-width:0}
.hoja h2{font-size:19px;line-height:1.3;margin:0;font-weight:600;text-wrap:balance}
.hoja .precio{font-size:31px;font-weight:600;letter-spacing:-.03em;
  font-variant-numeric:tabular-nums}
.hoja .precio em{font-style:normal;font-size:13px;font-weight:400;color:var(--gris);
  font-family:var(--etq);margin-left:8px}
dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:6px 16px;font-size:13px}
dt{font-family:var(--etq);font-size:11px;letter-spacing:.07em;text-transform:uppercase;
  color:var(--gris);white-space:nowrap}
dd{margin:0;min-width:0;overflow-wrap:anywhere}
.caja{border-left:3px solid var(--borde);padding:3px 0 3px 12px;font-size:13px;line-height:1.5}
.caja.bien{border-color:var(--verde);color:var(--verde)}
.caja.mal{border-color:var(--rosa);color:var(--rosa)}
.caja.ojo{border-color:var(--ocre);color:var(--ocre)}
.acciones{display:flex;gap:9px;margin-top:auto;padding-top:6px;flex-wrap:wrap}
.btn{text-decoration:none;padding:10px 17px;font-size:13px;font-weight:500;
  border:1px solid var(--borde);color:var(--tinta);background:var(--caja);
  cursor:pointer;border-radius:0}
.btn.fuerte{background:var(--rosa);border-color:var(--rosa);color:#fff}
.cerrar{position:absolute;top:0;right:0;width:40px;height:40px;font-size:16px;
  border:0;background:var(--tinta);color:var(--yeso);cursor:pointer;z-index:2}
.paso{position:fixed;top:50%;transform:translateY(-50%);width:44px;height:44px;
  font-size:17px;z-index:61;border:0;background:var(--tinta);color:var(--yeso);
  cursor:pointer}
.paso.izq{left:0} .paso.der{right:0}
.nada{padding:70px 20px;text-align:center;color:var(--gris);font-family:var(--etq);
  letter-spacing:.08em;text-transform:uppercase;font-size:12px}

@media(pointer:coarse){ .v{min-height:44px} .chip{min-height:40px} }
@media(max-width:860px){ .hoja{grid-template-columns:1fr;max-height:88vh}
  .hoja .foto{min-height:0} .hoja .foto img{max-height:46vh} .paso{display:none} }
@media(max-width:560px){ :root{--ancho:150px} .rejilla{gap:11px;padding:12px}
  .muro-in{padding:11px 14px} .cuenta{padding:0 14px 9px} .panel-in{padding:14px}
  .velo{padding:0} .hoja{max-height:100vh;height:100%} }
@media (prefers-reduced-motion:reduce){ *{transition:none!important} }
</style></head><body>

<header class="muro"><div class="muro-in">
  <h1 class="marca">Caza<em>Lotes</em></h1>
  <input id="q" aria-label="Buscar por texto" placeholder="buscar por texto&hellip;" style="flex:1;min-width:120px">
  <select id="fuente" aria-label="Filtrar por fuente"><option value="">todas las fuentes</option></select>
  <select id="orden" aria-label="Ordenar resultados">
    <option value="g">por gusto</option><option value="o">por oportunidad</option>
    <option value="lg">por log&iacute;stica</option><option value="cf">por confianza</option>
    <option value="precio">por precio</option>
  </select>
  <button id="abrir" aria-expanded="false">encargo</button>
  <button id="solonov">sin vender</button>
  <button id="nitidas">solo n&iacute;tidas</button>
  <button id="ocultano">ocultar descartados</button>
  <button id="densidad" data-d="1">tama&ntilde;o</button>
  <button id="exportar">exportar votos</button>
</div>
<div class="cuenta"><b id="num">0</b> de __TOTAL__ lotes &middot; __FECHA__<span id="pobres"></span></div></header>

<section class="panel" id="panel" hidden><div class="panel-in">
  <div class="grupo">
    <h3>Qu&eacute; busco</h3>
    <div class="fichas" id="tipos"></div>
    <p class="ayuda">Si no marcas nada, busca en todo.</p>
  </div>
  <div class="grupo">
    <h3>Medidas, en cent&iacute;metros</h3>
    <div class="medidas">
      <label>ancho m&aacute;x<input type="number" id="wmax" placeholder="220" min="0" step="5"></label>
      <label>alto m&aacute;x<input type="number" id="hmax" placeholder="200" min="0" step="5"></label>
      <label>fondo m&aacute;x<input type="number" id="dmax" placeholder="70" min="0" step="5"></label>
    </div>
    <label class="ayuda" style="display:flex;gap:7px;align-items:center">
      <input type="checkbox" id="puerta" style="width:auto">
      tiene que pasar por una puerta de
      <input type="number" id="puertacm" value="200" min="50" step="5" style="width:72px">
      cm
    </label>
    <p class="ayuda">Un lote sin medidas en el cat&aacute;logo no se descarta: sale marcado para que preguntes.</p>
  </div>
  <div class="grupo">
    <h3>Presupuesto</h3>
    <label class="ayuda">tope en euros, coste real con comisi&oacute;n incluida
      <input type="number" id="tope" placeholder="600" min="0" step="25"></label>
    <h3 style="margin-top:4px">Materiales</h3>
    <div class="fichas" id="mats"></div>
  </div>
  <div class="grupo">
    <h3>&Eacute;poca</h3>
    <div class="fichas" id="epocas"></div>
    <h3 style="margin-top:4px">Excluir palabras</h3>
    <input id="excluir" placeholder="dorado, tallado, ikea&hellip;">
    <div class="acc" style="margin-top:6px">
      <button class="primaria" id="aplicar">Buscar</button>
      <button id="limpiar">Limpiar</button>
      <button id="guardar">Guardar encargo</button>
      <select id="guardados" aria-label="Encargos guardados" style="min-width:130px"></select>
    </div>
  </div>
</div></section>

<main id="rejilla" class="rejilla" aria-label="Lotes encontrados"></main>
<div id="nada" class="nada" hidden>Nada encaja con este encargo</div>
<div id="velo" class="velo" hidden></div>

<script>
const DATOS = __DATOS__;
const K='cazalotes.votos', KP='cazalotes.pobres', KE='cazalotes.encargos';
let votos={}, pobres={}, encargos={};
try{ votos=JSON.parse(localStorage.getItem(K)||'{}'); }catch(e){}
try{ pobres=JSON.parse(localStorage.getItem(KP)||'{}'); }catch(e){}
try{ encargos=JSON.parse(localStorage.getItem(KE)||'{}'); }catch(e){}
function guardarTodo(){ try{
  localStorage.setItem(K,JSON.stringify(votos));
  localStorage.setItem(KP,JSON.stringify(pobres));
  localStorage.setItem(KE,JSON.stringify(encargos)); }catch(e){} }
const $=s=>document.querySelector(s);
const VOTOS=[['3','❤️'],['2','👍'],['1','😐'],
             ['0','👎'],['x','🚫']];
const ANCHOS=[220,300,400];
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,
  c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let visibles=[];

/* vocabulario del buscador: sinonimos reales de catalogo espanol */
const TIPOS={
 'almacenaje':['cajonera','comoda','aparador','armario','credenza','sideboard','chifonier','cajonero','mueble bajo','consola','vitrina'],
 'asiento':['silla','sillon','butaca','taburete','banqueta','sofa','canape','banco'],
 'mesa':['mesa','mesita','velador','escritorio','buro','mesa de centro','mesa de comedor'],
 'luz':['lampara','flexo','aplique','candelabro','farol','plafon','luminaria','quinque'],
 'escultura':['escultura','busto','talla','figura','relieve','estatua'],
 'pintura':['oleo','acuarela','pintura','lienzo','cuadro','gouache','temple'],
 'estanteria':['estanteria','libreria','balda','repisa'],
 'espejo':['espejo'],
 'alfombra':['alfombra','kilim','tapiz'],
 'ceramica':['ceramica','porcelana','jarron','loza','gres']
};
const MATS=['roble','nogal','teca','palisandro','pino','haya','bronce','marmol',
            'hierro','acero','laton','ceramica','cristal','cuero','mimbre','formica'];
const EPOCAS=['1950','1960','1970','1980','s. XIX','s. XVIII'];

function chips(cont,lista){
  $(cont).innerHTML=lista.map(x=>'<button class="chip" data-x="'+esc(x)+'">'+esc(x)+'</button>').join('');
}
chips('#tipos',Object.keys(TIPOS)); chips('#mats',MATS); chips('#epocas',EPOCAS);
document.addEventListener('click',e=>{
  const c=e.target.closest('.chip'); if(c){ c.classList.toggle('on'); }
});
const marcados=cont=>[...document.querySelectorAll(cont+' .chip.on')].map(c=>c.dataset.x);

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
  const sellos=(d.nov?'<span class="sello rosa">no vendido</span>':'')
    +(pobres[d.id]?'<span class="sello gris">foto pobre</span>':'')
    +(d.d3?'':'<span class="sello">sin medidas</span>');
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

function leerEncargo(){
  return {
    q:$('#q').value.toLowerCase().trim(),
    fuente:$('#fuente').value, orden:$('#orden').value,
    tipos:marcados('#tipos'), mats:marcados('#mats'), epocas:marcados('#epocas'),
    wmax:+$('#wmax').value||0, hmax:+$('#hmax').value||0, dmax:+$('#dmax').value||0,
    puerta:$('#puerta').checked?(+$('#puertacm').value||0):0,
    tope:+$('#tope').value||0,
    excluir:$('#excluir').value.toLowerCase().split(',').map(s=>s.trim()).filter(Boolean),
    nov:$('#solonov').classList.contains('on'),
    nit:$('#nitidas').classList.contains('on'),
    ocu:$('#ocultano').classList.contains('on')
  };
}

function cumple(d,E){
  const txt=(d.titulo+' '+(d.mats||[]).join(' ')+' '+d.fuente).toLowerCase();
  if(E.q&&!txt.includes(E.q))return false;
  if(E.fuente&&d.fuente!==E.fuente)return false;
  if(E.excluir.some(x=>txt.includes(x)))return false;
  if(E.tipos.length){
    const pal=E.tipos.flatMap(t=>TIPOS[t]||[]);
    if(!pal.some(p=>txt.includes(p)))return false;
  }
  if(E.mats.length&&!E.mats.some(m=>(d.mats||[]).includes(m)))return false;
  if(E.epocas.length&&!E.epocas.includes(d.periodo))return false;
  if(E.tope){ const c=d.total!=null?d.total:d.salida; if(c!=null&&c>E.tope)return false; }
  /* medidas: duras SOLO si el lote las declara. Sin medidas no se descarta. */
  if(d.d3&&d.d3.length){
    const o=[...d.d3].sort((a,b)=>b-a);
    if(E.wmax&&o[0]>E.wmax)return false;
    if(E.hmax&&o.length>1&&o[1]>E.hmax)return false;
    if(E.dmax&&o.length>2&&o[2]>E.dmax)return false;
    if(E.puerta&&o.length>1&&Math.min(o[0],o[1])>E.puerta)return false;
  }
  if(E.nov&&!d.nov)return false;
  if(E.nit&&pobres[d.id])return false;
  if(E.ocu&&(votos[d.id]==='x'||votos[d.id]==='0'))return false;
  return true;
}

function pintar(){
  const E=leerEncargo();
  visibles=DATOS.filter(d=>cumple(d,E)).sort((a,b)=>
    E.orden==='precio' ? (a.salida==null?1e9:a.salida)-(b.salida==null?1e9:b.salida)
                       : b[E.orden]-a[E.orden]);
  $('#rejilla').innerHTML=visibles.map(ficha).join('');
  $('#nada').hidden=visibles.length>0;
  $('#num').textContent=visibles.length;
  const np=Object.keys(pobres).length;
  $('#pobres').textContent=np?' · '+np+' con foto de baja resolución':'';
}

document.addEventListener('load',function(e){
  const im=e.target;
  if(im.tagName!=='IMG'||!im.dataset.id)return;
  if(im.naturalWidth&&im.naturalWidth<340){
    pobres[im.dataset.id]=im.naturalWidth; im.classList.add('pobre');
    const s=im.closest('.lienzo').querySelector('.sellos');
    if(s&&!s.querySelector('.gris'))
      s.insertAdjacentHTML('beforeend','<span class="sello gris">foto pobre</span>');
    guardarTodo();
  }
},true);

let actual=-1;
function detalle(i){
  actual=i; const d=visibles[i]; if(!d)return;
  const v=votos[d.id];
  const filas=[['fuente',d.fuente],['lote',d.lote],['medidas',d.dims||'no declaradas'],
    ['periodo',d.periodo],['materiales',(d.mats||[]).join(', ')],['dónde',d.donde],
    ['salida',d.salida!=null?Math.round(d.salida)+' €':null],
    ['coste real',d.total?Math.round(d.total)+' € ('+(d.recargo||0)+' % encima)':null]]
    .filter(p=>p[1]).map(p=>'<dt>'+esc(p[0])+'</dt><dd>'+esc(p[1])+'</dd>').join('');
  $('#velo').innerHTML='<div class="hoja" role="dialog" aria-modal="true" aria-label="'
    +esc(d.titulo)+'" tabindex="-1">'
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
    +(!d.d3?'<div class="caja ojo">El catálogo no da medidas. Pregunta antes de pujar.</div>':'')
    +(pobres[d.id]?'<div class="caja ojo">La foto del catálogo mide '+pobres[d.id]
        +' px de ancho. Pide fotos mejores.</div>':'')
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
    guardarTodo(); const ab=actual; pintar(); if(ab>=0)detalle(ab); return; }
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

$('#abrir').addEventListener('click',e=>{
  const p=$('#panel'); p.hidden=!p.hidden;
  e.currentTarget.classList.toggle('on',!p.hidden);
  e.currentTarget.setAttribute('aria-expanded',String(!p.hidden)); });
['q','fuente','orden'].forEach(id=>$('#'+id).addEventListener('input',pintar));
['solonov','nitidas','ocultano'].forEach(id=>$('#'+id).addEventListener('click',e=>{
  e.currentTarget.classList.toggle('on'); pintar(); }));
$('#aplicar').addEventListener('click',pintar);
$('#limpiar').addEventListener('click',()=>{
  ['wmax','hmax','dmax','tope','excluir','q'].forEach(id=>$('#'+id).value='');
  $('#puerta').checked=false;
  document.querySelectorAll('.chip.on').forEach(c=>c.classList.remove('on'));
  pintar(); });
$('#densidad').addEventListener('click',e=>{
  const n=(+e.currentTarget.dataset.d+1)%3; e.currentTarget.dataset.d=n;
  document.documentElement.style.setProperty('--ancho',ANCHOS[n]+'px'); });

/* encargos guardados */
function pintarGuardados(){
  $('#guardados').innerHTML='<option value="">encargos guardados…</option>'
    +Object.keys(encargos).map(n=>'<option>'+esc(n)+'</option>').join(''); }
$('#guardar').addEventListener('click',()=>{
  const n=prompt('Nombre del encargo'); if(!n)return;
  encargos[n]=leerEncargo(); guardarTodo(); pintarGuardados(); });
$('#guardados').addEventListener('change',e=>{
  const E=encargos[e.target.value]; if(!E)return;
  $('#q').value=E.q||''; $('#fuente').value=E.fuente||''; $('#orden').value=E.orden||'g';
  $('#wmax').value=E.wmax||''; $('#hmax').value=E.hmax||''; $('#dmax').value=E.dmax||'';
  $('#tope').value=E.tope||''; $('#excluir').value=(E.excluir||[]).join(', ');
  $('#puerta').checked=!!E.puerta; if(E.puerta)$('#puertacm').value=E.puerta;
  document.querySelectorAll('.chip').forEach(c=>c.classList.remove('on'));
  [['#tipos',E.tipos],['#mats',E.mats],['#epocas',E.epocas]].forEach(([sel,arr])=>
    (arr||[]).forEach(x=>{ const c=document.querySelector(sel+' .chip[data-x="'+x+'"]');
      if(c)c.classList.add('on'); }));
  ['solonov','nitidas','ocultano'].forEach((id,i)=>
    $('#'+id).classList.toggle('on',[E.nov,E.nit,E.ocu][i]));
  pintar(); });
pintarGuardados();

$('#exportar').addEventListener('click',function(){
  const ix={}; DATOS.forEach(d=>{ ix[d.id]=d; });
  const nombres={'3':'love','2':'like','1':'maybe','0':'no','x':'nunca'};
  const out=Object.keys(votos).map(id=>({voto:nombres[votos[id]],
    titulo:ix[id]&&ix[id].titulo, fuente:ix[id]&&ix[id].fuente,
    salida:ix[id]&&ix[id].salida, url:id}));
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([JSON.stringify(out,null,1)],{type:'application/json'}));
  a.download='votos.json'; a.click(); });

pintar();
</script></body></html>
"""
