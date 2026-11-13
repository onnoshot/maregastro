// Mare Gastro - rezervasyon formu (ana sayfa /tr/ ve /rezervasyon.html ortak kullanir).
// Formun HTML'i sayfada (#reservation), trackEvent/MarePhone sayfa basinda tanimli olmali.
if(typeof window.escHtml!=='function')window.escHtml=function(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')};
if(typeof window.goTo!=='function')window.goTo=function(id){var el=document.querySelector(id);if(el)el.scrollIntoView({behavior:'smooth',block:'start'})};
/* ── ETKİNLİK BİLGİ İKONU ── */
let EVENTS_CACHE=[];
let UPCOMING_CACHE=[];
function eventOccursOnDate(ev,iso){
  if(Array.isArray(ev.excludedDates)&&ev.excludedDates.includes(iso))return false;
  if(ev.recurring&&Array.isArray(ev.recurDays)&&ev.recurDays.length){
    if(iso<ev.date)return false;
    if(ev.endDate&&iso>ev.endDate)return false;
    const d=new Date(iso+'T00:00:00');
    return ev.recurDays.includes(d.getDay());
  }
  if(ev.endDate){
    if(iso<ev.date||iso>ev.endDate)return false;
    return new Date(iso+'T00:00:00').getDay()!==1;
  }
  return ev.date===iso;
}
function nextOccurrenceIso(ev,fromIso){
  const excluded=iso=>Array.isArray(ev.excludedDates)&&ev.excludedDates.includes(iso);
  if(ev.recurring&&Array.isArray(ev.recurDays)&&ev.recurDays.length){
    const startIso=ev.date>fromIso?ev.date:fromIso;
    if(ev.endDate&&startIso>ev.endDate)return null;
    const d0=new Date(startIso+'T00:00:00');
    for(let i=0;i<14;i++){
      const d=new Date(d0.getFullYear(),d0.getMonth(),d0.getDate()+i);
      const iso=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
      if(ev.endDate&&iso>ev.endDate)return null;
      if(ev.recurDays.includes(d.getDay())&&!excluded(iso))return iso;
    }
    return null;
  }
  if(ev.endDate){
    const startIso=ev.date>fromIso?ev.date:fromIso;
    if(startIso>ev.endDate)return null;
    const d0=new Date(startIso+'T00:00:00');
    for(let i=0;i<8;i++){
      const d=new Date(d0.getFullYear(),d0.getMonth(),d0.getDate()+i);
      const iso=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
      if(iso>ev.endDate)return null;
      if(d.getDay()!==1&&!excluded(iso))return iso;
    }
    return null;
  }
  return (ev.date>=fromIso&&!excluded(ev.date))?ev.date:null;
}
async function loadUpcomingEvents(){
  try{
    const r=await fetch('/api/events',{cache:'no-store'});
    const j=await r.json();
    const todayIso=new Date().toISOString().slice(0,10);
    EVENTS_CACHE=(j.items||[]).filter(e=>e.recurring||(e.endDate?e.endDate>=todayIso:e.date>=todayIso));
    UPCOMING_CACHE=EVENTS_CACHE.map(e=>{
      const occ=nextOccurrenceIso(e,todayIso);
      return occ?{...e,date:occ}:null;
    }).filter(Boolean).sort((a,b)=>a.date.localeCompare(b.date)||(a.time||'').localeCompare(b.time||''));
    if(UPCOMING_CACHE.length){
      document.getElementById('evInfoBtn').style.display='inline-flex';
      renderEvPopover();
    }
    if(typeof renderMiniCal==='function')renderMiniCal();
  }catch(e){}
}
function renderEvPopover(){
  document.getElementById('evPopList').innerHTML=UPCOMING_CACHE.map(e=>{
    const d=new Date(e.date+'T00:00:00');
    const dateFmt=d.toLocaleDateString('tr-TR',{day:'numeric',month:'long'});
    return `<div class="ev-pop-item">
      <div class="ev-pop-date">${dateFmt}${e.time?' · '+escHtml(e.time):''}</div>
      <div class="ev-pop-title">${escHtml(e.title)}</div>
      ${e.description?`<div class="ev-pop-desc">${escHtml(e.description)}</div>`:''}
    </div>`;
  }).join('');
}
function toggleEvPopover(force){
  const pop=document.getElementById('evPopover');
  pop.classList.toggle('show', force!==undefined?force:!pop.classList.contains('show'));
}
document.addEventListener('click',(e)=>{
  const btn=document.getElementById('evInfoBtn'), pop=document.getElementById('evPopover');
  if(!btn||!pop)return;
  if(!btn.contains(e.target)&&!pop.contains(e.target))pop.classList.remove('show');
});
loadUpcomingEvents();

/* ── MİNİ TAKVİM (tarih seçici) ── */
const MC_MONTHS=['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
const mcToday0=(()=>{const d=new Date();d.setHours(0,0,0,0);return d})();
let mcYear=mcToday0.getFullYear(), mcMonth=mcToday0.getMonth();
// Panelden kapatilan gunler (/api/closed-days): tum masalar dolu, secilemez.
let CLOSED_DAYS=new Set();
const MC_FULL_MSG='Bu tarihte tüm masalarımız rezerve edildi, lütfen başka bir tarih seçin.';
const MC_FULL_TIP='Tüm masalar rezerve edildi';
function mcFullDay(){showErr('err1',MC_FULL_MSG,'full');closeMcDetail();}
async function loadClosedDays(){
  try{
    const r=await fetch('/api/closed-days',{cache:'no-store'});
    const j=await r.json();
    CLOSED_DAYS=new Set(j.days||[]);
    const sel=document.getElementById('rdate');
    if(sel.value&&CLOSED_DAYS.has(sel.value))sel.value='';
    renderMiniCal();
  }catch(e){}
  applyDeepDate();
}
// /rezervasyon sayfasindaki takvimden gelen ?tarih=YYYY-MM-DD: gunu secip saat/kisi adimina gec.
function applyDeepDate(){
  if(applyDeepDate.done)return;applyDeepDate.done=true;
  let iso='';try{iso=(new URLSearchParams(location.search)).get('tarih')||'';}catch(e){}
  if(!/^\d{4}-\d{2}-\d{2}$/.test(iso))return;
  const d=new Date(iso+'T00:00:00');
  if(isNaN(d)||d<mcToday0||d.getDay()===1)return;
  mcYear=d.getFullYear();mcMonth=d.getMonth();renderMiniCal();
  if(CLOSED_DAYS.has(iso)){mcFullDay();}else{mcSelectDay(iso);gS(2);}
  // motion.js (Lenis) yuklenip goTo'yu degistirdikten sonra kaydir; gec yerlesim kaymasina karsi bir kez daha.
  const jump=()=>{try{window.goTo('#reservation')}catch(e){document.getElementById('reservation').scrollIntoView()}};
  const go=()=>{setTimeout(jump,450);setTimeout(()=>{const r=document.getElementById('reservation').getBoundingClientRect();if(Math.abs(r.top)>140)jump();},2300);};
  if(document.readyState==='complete')go();else window.addEventListener('load',go,{once:true});
}
const ICON_SVGS={
  star:'<path d="M12 2.5l2.2 5.3 5.7.5-4.3 3.8 1.3 5.6-4.9-3-4.9 3 1.3-5.6-4.3-3.8 5.7-.5z"/>',
  sparkle:'<path d="M12 3l1.3 4.7L18 9l-4.7 1.3L12 15l-1.3-4.7L6 9l4.7-1.3z"/>',
  music:'<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
  headphones:'<path d="M3 14v-2a9 9 0 0118 0v2"/><rect x="1.5" y="13" width="4.5" height="8" rx="2"/><rect x="18" y="13" width="4.5" height="8" rx="2"/>',
  wine:'<path d="M7 3h10l-1 9a4 4 0 01-8 0z"/><line x1="12" y1="12" x2="12" y2="20"/><line x1="8" y1="21" x2="16" y2="21"/>',
  utensils:'<path d="M6 2v8a2 2 0 002 2v10"/><path d="M6 2v6"/><path d="M10 2v6"/><path d="M17 2c-2.5 0-3.5 2.5-3.5 6 0 2.5 1 4 3.5 4v10"/>',
  gift:'<rect x="3" y="9" width="18" height="4" rx="1"/><rect x="4" y="13" width="16" height="8" rx="1"/><line x1="12" y1="9" x2="12" y2="21"/><path d="M12 9c-1-2.5-4-3-4.5-1S9 9 12 9zM12 9c1-2.5 4-3 4.5-1S15 9 12 9z"/>',
};
function iconSvg(key,sw){return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${sw||1.6}" stroke-linecap="round" stroke-linejoin="round">${ICON_SVGS[key]||ICON_SVGS.star}</svg>`;}
function mcIso(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}
function mcShift(n){
  mcMonth+=n;if(mcMonth<0){mcMonth=11;mcYear--}if(mcMonth>11){mcMonth=0;mcYear++}
  closeMcDetail();
  document.getElementById('mcGrid').classList.toggle('back',n<0);
  renderMiniCal();
}
function renderMiniCal(){
  document.getElementById('mcLabel').textContent=MC_MONTHS[mcMonth]+' '+mcYear;
  const first=new Date(mcYear,mcMonth,1);
  const startOffset=(first.getDay()+6)%7;
  const daysInMonth=new Date(mcYear,mcMonth+1,0).getDate();
  const gridStart=new Date(mcYear,mcMonth,1-startOffset);
  const selVal=document.getElementById('rdate').value;
  const totalCells=Math.ceil((startOffset+daysInMonth)/7)*7;
  let html='';
  for(let i=0;i<totalCells;i++){
    const d=new Date(gridStart.getFullYear(),gridStart.getMonth(),gridStart.getDate()+i);
    const iso=mcIso(d);
    const cls=['mc-day'];
    if(d.getMonth()!==mcMonth)cls.push('off');
    if(d.getTime()===mcToday0.getTime())cls.push('today');
    if(selVal===iso)cls.push('sel');
    const dayEvents=(EVENTS_CACHE||[]).filter(e=>eventOccursOnDate(e,iso)).sort((a,b)=>(a.recurring?1:0)-(b.recurring?1:0));
    const dotsHtml=dayEvents.length?`<div class="mc-day-dots">${dayEvents.slice(0,3).map(e=>
      `<span class="mc-day-dot" style="background:${e.color||'#C8A96E'}"></span>`
    ).join('')}</div>`:'';
    const isClosedDay=d.getDay()===1;
    if(d>=mcToday0&&!isClosedDay&&CLOSED_DAYS.has(iso)){cls.push('disabled','full');html+=`<div class="${cls.join(' ')}" title="${MC_FULL_TIP}"><button type="button" class="mc-daynum mc-full" aria-disabled="true" onclick="mcFullDay()">${d.getDate()}</button>${dotsHtml}</div>`;}
    else if(d<mcToday0||isClosedDay){cls.push('disabled');html+=`<div class="${cls.join(' ')}"${isClosedDay?' title="Pazartesi günleri kapalıyız"':''}><span class="mc-daynum">${d.getDate()}</span>${dotsHtml}</div>`;}
    else html+=`<div class="${cls.join(' ')}"><button type="button" class="mc-daynum" data-iso="${iso}" onclick="mcSelectDay('${iso}')">${d.getDate()}</button>${dotsHtml}</div>`;
  }
  document.getElementById('mcGrid').innerHTML=html;
}
let igEmbedPromise=null;
function loadInstagramEmbed(){
  if(window.instgrm)return Promise.resolve();
  if(igEmbedPromise)return igEmbedPromise;
  igEmbedPromise=new Promise((resolve)=>{
    const s=document.createElement('script');
    s.async=true;s.src='https://www.instagram.com/embed.js';
    s.onload=()=>resolve();s.onerror=()=>resolve();
    document.body.appendChild(s);
  });
  return igEmbedPromise;
}
function mcShowDetail(iso,idx){
  const list=(EVENTS_CACHE||[]).filter(e=>eventOccursOnDate(e,iso)).sort((a,b)=>(a.recurring?1:0)-(b.recurring?1:0));
  const ev=list[idx];
  if(!ev)return;
  const color=ev.color||'#C8A96E';
  const iconEl=document.getElementById('mcDetailIcon');
  iconEl.innerHTML=iconSvg(ev.icon||'star');
  iconEl.style.background=color+'26';
  iconEl.style.color=color;
  const d=new Date(iso+'T00:00:00');
  document.getElementById('mcDetailDate').textContent=d.toLocaleDateString('tr-TR',{day:'numeric',month:'long'})+(ev.time?' · '+ev.time:'');
  document.getElementById('mcDetailTitle').textContent=ev.title;
  const descEl=document.getElementById('mcDetailDesc');
  descEl.textContent=ev.description||'';
  descEl.style.display=ev.description?'block':'none';

  const switcher=document.getElementById('mcDetailSwitcher');
  if(list.length>1){
    switcher.innerHTML=list.map((e,i)=>`<button type="button" class="mc-switch-dot ${i===idx?'on':''}" style="background:${e.color||'#C8A96E'}" onclick="mcShowDetail('${iso}',${i})" aria-label="${escHtml(e.title)}"></button>`).join('');
    switcher.classList.add('show');
  } else switcher.classList.remove('show');

  const igEl=document.getElementById('mcDetailIg');
  if(ev.instagram_url){
    igEl.innerHTML=`<blockquote class="instagram-media" data-instgrm-permalink="${ev.instagram_url}" data-instgrm-version="14" style="margin:0;width:100%"></blockquote>`;
    igEl.classList.add('show');
    loadInstagramEmbed().then(()=>{ if(window.instgrm)window.instgrm.Embeds.process(); });
  } else {
    igEl.innerHTML='';igEl.classList.remove('show');
  }
  document.getElementById('mcEventDetail').classList.add('show');
}
function closeMcDetail(){ document.getElementById('mcEventDetail').classList.remove('show'); }
function mcSelectDay(iso){
  document.getElementById('rdate').value=iso;
  clearErr('err1');
  document.querySelectorAll('.mc-day.sel').forEach(el=>el.classList.remove('sel'));
  const btn=document.querySelector(`.mc-daynum[data-iso="${iso}"]`);
  if(btn){
    btn.closest('.mc-day').classList.add('sel');
    btn.classList.remove('mc-pop');void btn.offsetWidth;btn.classList.add('mc-pop');
  }
  const dayEvents=(EVENTS_CACHE||[]).filter(e=>eventOccursOnDate(e,iso)).sort((a,b)=>(a.recurring?1:0)-(b.recurring?1:0));
  if(dayEvents.length)mcShowDetail(iso,0);
  else closeMcDetail();
}
renderMiniCal();
loadClosedDays();

/* ── SAAT LİSTESİ (09:00–00:00) ── */
const TIME_SLOTS=(()=>{const out=[];for(let h=9;h<24;h++){out.push(String(h).padStart(2,'0')+':00');out.push(String(h).padStart(2,'0')+':30');}out.push('00:00');return out;})();
document.getElementById('timeList').innerHTML=TIME_SLOTS.map(t=>`<button type="button" class="tpill" onclick="selTime(this,'${t}')">${t}</button>`).join('');
(()=>{const def=document.querySelector('.time-list .tpill[onclick*="19:00"]');if(def)def.scrollIntoView({block:'nearest'});})();

/* ── REZERVASYON ── */
let selTime_val='',guestCount=2,selKon_val='',curStep=1;

function selTime(btn,val){
  document.querySelectorAll('.time-list .tpill').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');selTime_val=val;
  const label=document.getElementById('timeDdText');
  label.textContent=val;label.classList.add('picked');
  toggleTimeDd(false);
}
function toggleTimeDd(force){
  const list=document.getElementById('timeList'), trig=document.getElementById('timeDdTrigger');
  const show=force!==undefined?force:!list.classList.contains('show');
  list.classList.toggle('show',show);
  trig.classList.toggle('open',show);
}
document.addEventListener('click',(e)=>{
  const trig=document.getElementById('timeDdTrigger'), list=document.getElementById('timeList');
  if(!trig||!list)return;
  if(!trig.contains(e.target)&&!list.contains(e.target)){list.classList.remove('show');trig.classList.remove('open');}
});
function adjG(d){
  guestCount=Math.max(1,Math.min(20,guestCount+d));
  const el=document.getElementById('gNum');
  el.style.transform='scale(1.4)';el.style.opacity='.6';
  setTimeout(()=>{el.style.transform='scale(1)';el.style.opacity='1'},220);
  el.textContent=guestCount;
  const note=document.getElementById('gNote');
  if(note){
    if(guestCount>=10)note.textContent='Özel organizasyon — ekibimiz sizinle iletişime geçecek';
    else if(guestCount===1)note.textContent='Yalnız bir deneyim için hoş geldiniz';
    else note.textContent=guestCount+' kişilik masanız hazırlanacak';
  }
}
function selK(card,val){
  document.querySelectorAll('.kopt').forEach(k=>k.classList.remove('on'));
  card.classList.add('on');selKon_val=val;
}
(function(){
  const vids=document.querySelectorAll('.about-right video.alazy');
  if(!vids.length)return;
  const io=new IntersectionObserver((entries)=>{
    entries.forEach(en=>{
      const v=en.target;
      if(en.isIntersecting){
        const s=v.querySelector('source');
        if(s&&s.dataset.src){s.src=s.dataset.src;delete s.dataset.src;v.load();}
        v.play().catch(()=>{});
      }else{
        v.pause();
      }
    });
  },{rootMargin:'200px 0px',threshold:.1});
  vids.forEach(v=>io.observe(v));
})();
function showErr(id,msg,code){
  trackEvent('form_error',{event_label:id});
  // Hangi kontrolde takildigi GA4'te ozel boyut olmadan gorunsun diye ayri olay adi.
  if(code)trackEvent('form_error_'+code,{event_label:id});
  const el=document.getElementById(id);
  el.textContent=msg;el.classList.add('show');
  el.classList.remove('shk');void el.offsetWidth;el.classList.add('shk');
}
function clearErr(id){document.getElementById(id).classList.remove('show')}
function gS(n){
  if(n===2){
    clearErr('err1');
    if(!document.getElementById('rdate').value){showErr('err1','Lütfen bir tarih seçin.','date');return}
    const selD=new Date(document.getElementById('rdate').value+'T00:00:00');
    if(selD.getDay()===1){showErr('err1','Pazartesi günleri kapalıyız, lütfen başka bir tarih seçin.','monday');return}
    if(CLOSED_DAYS.has(document.getElementById('rdate').value)){showErr('err1',MC_FULL_MSG,'full');return}
  }
  if(n===3){
    clearErr('err2');
    if(!selTime_val){showErr('err2','Lütfen bir saat seçin.','time');return}
    if(!document.getElementById('rName').value.trim()){showErr('err2','Lütfen ad soyad girin.','name');return}
    const phoneVal=document.getElementById('rPhone').value.trim();
    if(!phoneVal){showErr('err2','Lütfen telefon numaranızı girin.','phone');return}
    if(!MarePhone.valid(document.getElementById('rPhone'))){showErr('err2','Lütfen geçerli bir telefon numarası girin.','phone_invalid');return}
    if(!selKon_val){showErr('err2','Lütfen konaklama tercihini seçin.','stay');return}
    const d=document.getElementById('rdate').value;
    const fmt=new Date(d).toLocaleDateString('tr-TR',{day:'numeric',month:'long',year:'numeric'});
    document.getElementById('sD').textContent=fmt;
    document.getElementById('sT').textContent=selTime_val;
    document.getElementById('sG').textContent=guestCount+' Kişi';
    document.getElementById('sK').textContent=selKon_val;
  }
  trackEvent('reservation_step_view',{step:n});
  document.querySelectorAll('.rstep').forEach(s=>s.classList.toggle('back',n<curStep));
  curStep=n;
  document.querySelectorAll('.rstep').forEach(s=>s.classList.remove('on'));
  document.getElementById('rs'+n).classList.add('on');
  for(let i=1;i<=3;i++){
    const d=document.getElementById('pd'+i);
    d.classList.remove('active','done');
    if(i<n){d.classList.add('done');document.getElementById('ps'+i).classList.remove('curstep')}
    else if(i===n){d.classList.add('active');document.getElementById('ps'+i).classList.add('curstep')}
    else{document.getElementById('ps'+i).classList.remove('curstep')}
  }
  for(let i=1;i<=2;i++)document.getElementById('pl'+i).classList.toggle('done',i<n);
}
// ── ZİYARETÇİ KANALI (rezervasyon kaynağı: Instagram/Google/Doğrudan...) ──
function mareRef(){try{return sessionStorage.getItem('mare_ref')||document.referrer||'';}catch(e){return document.referrer||'';}}
function deriveChannel(){
  try{
    var p=new URLSearchParams(location.search);
    var us=(p.get('utm_source')||'').toLowerCase();
    var m={instagram:'Instagram',ig:'Instagram',facebook:'Facebook',fb:'Facebook',meta:'Facebook',google:'Google',
      youtube:'YouTube',yt:'YouTube',tiktok:'TikTok',pinterest:'Pinterest',twitter:'X',x:'X',linkedin:'LinkedIn',
      whatsapp:'WhatsApp',wa:'WhatsApp',email:'E-posta',newsletter:'E-posta',mail:'E-posta'};
    if(us)return m[us]||(us.charAt(0).toUpperCase()+us.slice(1));
    if(p.get('gclid')||p.get('gbraid')||p.get('wbraid')||p.get('gad_source'))return 'Google';
    var ref=mareRef(),h='';try{h=new URL(ref).hostname.replace(/^www\./,'').toLowerCase();}catch(e){}
    if(!ref||h===location.hostname.replace(/^www\./,''))return 'Doğrudan';
    var hm=[['instagram','Instagram'],['google','Google'],['bing','Bing'],['facebook','Facebook'],['fb.','Facebook'],
      ['youtube','YouTube'],['t.co','X'],['twitter','X'],['x.com','X'],['tiktok','TikTok'],['pinterest','Pinterest'],
      ['linkedin','LinkedIn'],['whatsapp','WhatsApp'],['wa.me','WhatsApp'],['yandex','Yandex'],['duckduckgo','DuckDuckGo']];
    for(var i=0;i<hm.length;i++)if(h.indexOf(hm[i][0])>=0)return hm[i][1];
    return 'Yönlendirme';
  }catch(e){return 'Doğrudan';}
}
var MARE_CHANNEL=(function(){try{var s=sessionStorage.getItem('mare_ch');if(s)return s;var c=deriveChannel();sessionStorage.setItem('mare_ch',c);return c;}catch(e){return deriveChannel();}})();
// ── UCRETLI (REKLAM) / UCRETSIZ (ORGANIK) ──
// 'paid' = reklamdan geldi, 'organic' = ucretsiz. Sadece guvenilir reklam sinyallerine
// bakariz: reklam platformlarinin click-id'leri ve utm_medium. fbclid BILINCLI olarak
// listede DEGIL — Facebook/Instagram onu organik gonderi linklerine de ekliyor, paid
// sanip yanlis sayardik. Reklam linklerine utm_medium (cpc / paid_social vb.) eklenmezse
// o ziyaret organik sayilir.
function derivePaidClass(){
  try{
    var p=new URLSearchParams(location.search);
    var ids=['gclid','gbraid','wbraid','dclid','msclkid','ttclid','twclid'];
    for(var i=0;i<ids.length;i++)if(p.get(ids[i]))return 'paid';
    var med=(p.get('utm_medium')||'').toLowerCase().replace(/[^a-z]/g,'');
    var paid=['cpc','ppc','paid','paidsocial','paidsearch','paidmedia','cpm','cpv','cpa','display','banner','retargeting','remarketing','ads','ad','adwords','sponsored'];
    if(med&&paid.indexOf(med)>=0)return 'paid';
    return 'organic';
  }catch(e){return 'organic';}
}
var MARE_PAID=(function(){try{var s=sessionStorage.getItem('mare_paid');if(s==='paid'||s==='organic')return s;var v=derivePaidClass();sessionStorage.setItem('mare_paid',v);return v;}catch(e){return derivePaidClass();}})();
var MARE_UTM_MEDIUM=(function(){try{return (new URLSearchParams(location.search)).get('utm_medium')||'';}catch(e){return '';}})();
// Ilk gelis bilgisi: ziyaretci sayfa degistirse de reklam ve kampanya kaynagi kaybolmasin.
var MARE_FT=(function(){var empty={source:'',medium:'',campaign:'',term:'',landing:'',click:'',ref:''};try{var s=sessionStorage.getItem('mare_ft');if(s)return JSON.parse(s);var p=new URLSearchParams(location.search),ids=['gclid','gbraid','wbraid','dclid','msclkid','ttclid','twclid','fbclid'],click='';for(var i=0;i<ids.length;i++)if(p.get(ids[i])){click=ids[i];break}var v={source:p.get('utm_source')||'',medium:p.get('utm_medium')||'',campaign:p.get('utm_campaign')||p.get('gad_campaignid')||'',term:p.get('utm_term')||'',landing:location.pathname,click:click,ref:mareRef().indexOf(location.hostname)<0?mareRef():''};sessionStorage.setItem('mare_ft',JSON.stringify(v));return v;}catch(e){return empty;}})();
(function(){var seen={};function once(n){if(seen[n])return;seen[n]=1;trackEvent(n);}var d=document.getElementById('rdate');if(d&&d.parentElement)d.parentElement.addEventListener('click',function(){once('form_start');});document.addEventListener('focusin',function(e){if(e.target&&e.target.id==='rName')once('form_details_start');});})();
let rezSending=false;
// Rezervasyon tarihi hangi dil sayfasindan gonderilirse gonderilsin HER ZAMAN
// Turkce bicimde kaydedilmeli -- panel.maregastro.com'daki takvim/rapor ayristiricisi
// sadece Turkce ay adlarini taniyor. Intl'den bagimsiz, elle bicimlendirme kullaniliyor.
const MARE_TR_AYLAR=['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
function mareTrDateFmt(iso){const p=iso.split('-');const y=+p[0],m=+p[1],dd=+p[2];return dd+' '+MARE_TR_AYLAR[m-1]+' '+y;}
function submitReservation(a){
  if(rezSending)return false;
  const name=document.getElementById('rName').value.trim();
  const phone=MarePhone.value(document.getElementById('rPhone'));
  const email=document.getElementById('rEmail').value.trim();
  if(!name){showErr('err2','Lütfen ad soyad girin.','name');return false}
  if(!phone){showErr('err2','Lütfen telefon numaranızı girin.','phone');return false}
  const d=document.getElementById('rdate').value;
  const fmt=mareTrDateFmt(d);
  const msg=`Merhaba, Mare Gastro rezervasyon talebim:\n\nAd Soyad: ${name}\nTelefon: ${phone}${email?'\nE-posta: '+email:''}\n\nTarih: ${fmt}\nSaat: ${selTime_val}\nKişi Sayısı: ${guestCount}\nKonaklama: ${selKon_val}\n\nOnayınızı bekliyorum.`;
  a.href=`https://wa.me/905323540888?text=${encodeURIComponent(msg)}`;
  rezSending=true;
  a.classList.add('sending');
  trackEvent('reservation_submit_click',{channel:MARE_CHANNEL,konaklama:selKon_val,guests:guestCount});
  trackEvent('whatsapp_click',{event_label:'reservation_confirm'});
  fetch('/api/reservation',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({name,phone,email,date:fmt,time:selTime_val,guests:guestCount,konaklama:selKon_val,
      channel:MARE_CHANNEL,adPaid:MARE_PAID,utmMedium:MARE_FT.medium,referrer:(MARE_FT.ref||document.referrer||''),utm:MARE_FT.source,campaign:MARE_FT.campaign,term:MARE_FT.term,landing:MARE_FT.landing,click:MARE_FT.click})}).catch(()=>{});
  const suc=document.getElementById('rezSuccess');if(suc)suc.classList.add('show');
  setTimeout(()=>{rezSending=false;a.classList.remove('sending')},2500);
  return true;
}

