(() => {
  'use strict';
  const app=document.querySelector('#app');
  const sessionKey='geojade-challenge-v1',historyKey='geojade-challenge-history-v1';
  const continentViews={América:'0 35 430 420',Europa:'455 80 175 175',Asia:'555 55 440 355',África:'425 180 255 285',Oceanía:'710 250 290 245'};
  let session=null,storageOK=true;
  const read=(k,f)=>{try{return JSON.parse(localStorage.getItem(k))||f}catch{return f}};
  const write=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch{storageOK=false}};
  const erase=k=>{try{localStorage.removeItem(k)}catch{storageOK=false}};
  const bind=(id,fn)=>document.getElementById(id)?.addEventListener('click',fn);
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function shuffle(arr){const a=[...arr];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
  function valid(s){return s&&window.CHALLENGES[s.challenge]&&Array.isArray(s.questions)&&s.questions.length===window.CHALLENGES[s.challenge].length&&Number.isInteger(s.index)&&s.index>=0&&s.index<s.questions.length&&Array.isArray(s.answers)&&s.answers.length>=s.index}
  function notice(){return storageOK?'':'<p class="notice">El navegador no permitió guardar el avance. Mantén esta página abierta para terminar el reto.</p>'}

  function home(){
    const saved=read(sessionKey,null);session=valid(saved)?saved:null;
    const cards=Object.entries(window.CHALLENGES).map(([id,c])=>`<button class="challenge-card ${id==='abu'?'abu-card':''}" data-challenge="${id}">${id==='abu'?'<img src="abu-profesor.webp" alt="Abu, profesor de geografía">':`<span class="challenge-icon">${c.icon}</span>`}<span><strong>${esc(c.title)}</strong><small>${esc(c.subtitle)}</small><em>${c.length} preguntas</em></span></button>`).join('');
    app.innerHTML=`<section class="challenge-hero"><p class="eyebrow">ELIGE TU PRÓXIMA MISIÓN</p><h1>Retos cortos,<br><em>mapas grandes.</em></h1><p class="lead">Cada expedición es independiente. Puedes repetirla y las preguntas cambiarán.</p>${session?`<button class="primary" id="resume">Continuar ${esc(window.CHALLENGES[session.challenge].title)}</button>`:''}</section><section class="challenge-grid">${cards}</section>${notice()}${historyBlock()}`;
    document.querySelectorAll('[data-challenge]').forEach(b=>b.addEventListener('click',()=>start(b.dataset.challenge)));
    bind('resume',render);
  }

  function historyBlock(){
    const h=read(historyKey,[]);if(!Array.isArray(h)||!h.length)return '';
    return `<section class="panel history"><h2>Bitácora de retos</h2>${h.slice(0,6).map(r=>`<div class="row"><span>${esc(r.title)}</span><strong>${r.score} / ${r.total}</strong></div>`).join('')}</section>`;
  }

  function start(id){
    const c=window.CHALLENGES[id];
    session={id:Date.now()+'-'+Math.random().toString(36).slice(2),challenge:id,index:0,answers:[],questions:shuffle(c.questions).slice(0,c.length).map(q=>({...q,options:shuffle(q.options)}))};
    write(sessionKey,session);render();
  }

  function worldMap(q){
    const view=q.mapType==='america'?'0 35 430 420':continentViews[q.continent]||'0 0 1000 500';
    const paths=Object.entries(window.MAP_PATHS).map(([code,path])=>`<path class="country ${code===q.mapCode?'target':''}" d="${path}"></path>`).join('');
    const center=window.MAP_CENTERS[q.mapCode],marker=center?`<circle class="locator" cx="${center[0]}" cy="${center[1]}" r="${q.continent==='Europa'?4:8}"></circle>`:'';
    return `<div class="map-wrap focused"><svg class="world-map" viewBox="${view}" role="img" aria-label="Mapa ampliado con un país resaltado">${paths}${marker}</svg><p class="map-key">País marcado</p></div>`;
  }
  function mexicoMap(q){
    const paths=Object.entries(window.MEXICO_PATHS).map(([code,path])=>`<path class="country mexico-state ${code===q.mexicoCode?'target':''}" d="${path}"></path>`).join('');
    const c=window.MEXICO_CENTERS[q.mexicoCode];
    return `<div class="map-wrap mexico-wrap"><svg class="world-map" viewBox="0 0 800 500" role="img" aria-label="Mapa político de México con una entidad resaltada">${paths}<circle class="locator" cx="${c[0]}" cy="${c[1]}" r="7"></circle></svg><p class="map-key">Entidad marcada</p></div>`;
  }
  function oceanMap(q){
    const paths=Object.values(window.MAP_PATHS).map(path=>`<path class="country" d="${path}"></path>`).join('');
    return `<div class="map-wrap"><svg class="world-map" viewBox="0 0 1000 500" role="img" aria-label="Mapamundi con un océano señalado">${paths}<circle class="ocean-pulse" cx="${q.mapPoint[0]}" cy="${q.mapPoint[1]}" r="14"></circle></svg><p class="map-key ocean-key">Punto señalado</p></div>`;
  }
  function visual(q){
    if(q.mapType==='continent'||q.mapType==='america')return worldMap(q);
    if(q.mapType==='mexico')return mexicoMap(q);
    if(q.mapType==='ocean')return oceanMap(q);
    if(q.mapType==='player')return `<figure class="player-card"><img src="${esc(q.photo)}" alt="Fotografía de ${esc(q.player)}"><figcaption>${esc(q.player)} · Mundial 2026</figcaption></figure>`;
    if(q.abu)return `<div class="abu-strip"><img src="abu-profesor.webp" alt="Abu, profesor de geografía"><p><strong>Abu pregunta…</strong><br>Piénsalo bien: puede haber una pequeña trampa.</p></div>`;
    return '';
  }

  function score(){return session.answers.filter(a=>a.correct).length}
  function render(){
    const c=window.CHALLENGES[session.challenge],q=session.questions[session.index],a=session.answers[session.index],total=session.questions.length;
    app.innerHTML=`<div class="topline"><span class="badge">${c.icon} ${esc(c.title)}</span><span><strong>${session.index+1}</strong> de ${total} · <strong>${score()}</strong> puntos</span><button class="quiet" id="exit">Retos</button></div><div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="${total}" aria-valuenow="${session.answers.length}"><div style="width:${session.answers.length/total*100}%"></div></div><section class="panel question-panel"><h1 class="question" id="question" tabindex="-1">${esc(q.text)}</h1>${visual(q)}<div class="choices">${q.options.map((o,i)=>`<button id="choice${i}" class="choice ${a?(o===q.answer?'correct':o===a.selected?'wrong':''):''}" ${a?'disabled':''}><span class="letter">${'ABCD'[i]}</span><span>${esc(o)}${a&&o===q.answer?' · Correcta':a&&o===a.selected?' · Tu respuesta':''}</span></button>`).join('')}</div><div aria-live="polite">${a?feedback(q,a,total):''}</div></section>${notice()}`;
    q.options.forEach((o,i)=>bind('choice'+i,()=>choose(o)));bind('next',next);bind('exit',home);document.getElementById('question').focus();
  }
  function feedback(q,a,total){return `<div class="feedback ${a.correct?'':'error'}"><strong>${a.correct?'¡Correcto!':'Buena jugada, pero Abu tenía otra respuesta.'}</strong><p>${a.correct?'':`La respuesta es <b>${esc(q.answer)}</b>. `}${esc(q.explanation)}</p></div><button class="primary next" id="next">${session.index===total-1?'Ver resultado':'Siguiente'} →</button>`}
  function choose(selected){if(session.answers[session.index])return;const q=session.questions[session.index];session.answers.push({selected,correct:selected===q.answer});write(sessionKey,session);render();document.getElementById('next').focus()}
  function next(){if(!session.answers[session.index])return;if(session.index===session.questions.length-1){finish();return}session.index++;write(sessionKey,session);render()}
  function finish(){
    const c=window.CHALLENGES[session.challenge],n=score(),total=session.questions.length;let h=read(historyKey,[]);if(!Array.isArray(h))h=[];
    if(!h.some(r=>r.id===session.id)){h.unshift({id:session.id,title:c.title,score:n,total});write(historyKey,h.slice(0,20))}erase(sessionKey);
    app.innerHTML=`<section class="panel result-panel">${session.challenge==='abu'?'<img class="abu-result" src="abu-profesor.webp" alt="Abu, profesor de geografía">':''}<p class="eyebrow">RETO COMPLETADO</p><h1>${n===total?'¡Expedición perfecta!':n>=Math.ceil(total*.7)?'¡Gran exploradora!':'Cada mapa nuevo cuenta.'}</h1><div class="bigscore">${n}<span> / ${total}</span></div><p>${esc(c.title)} · ${Math.round(n/total*100)}% de aciertos</p><div class="actions"><button class="primary" id="again">Repetir reto</button><button class="quiet" id="home">Elegir otro</button></div></section>`;
    bind('again',()=>start(session.challenge));bind('home',home);window.scrollTo(0,0);
  }
  home();
})();
