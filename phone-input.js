/* Mare Gastro telefon alani: site ve panel ayni kurali kullanir.
   Ciktisi her zaman E.164 bicimindedir (+905321234567).
   DATA satirlari scripts/build_phone_input.mjs ile uretilir. */
(function(){
var DATA='AD,376,,6,9;AE,971,0,6,12;AF,93,0,9,9;AG,1,1,10,10;AI,1,1,10,10;AL,355,0,6,9;AM,374,0,8,8;AO,244,,9,9;AR,54,0,10,11;AS,1,1,10,10;AT,43,0,6,13;AU,61,0,6,12;AW,297,,7,7;AZ,994,0,9,9;BA,387,0,8,9;BB,1,1,10,10;BD,880,0,6,10;BE,32,0,8,9;BF,226,,8,8;BG,359,0,6,12;BH,973,,8,8;BI,257,,8,8;BJ,229,,8,10;BL,590,0,9,9;BM,1,1,10,10;BN,673,,7,7;BO,591,0,8,9;BR,55,0,8,11;BS,1,1,10,10;BT,975,,7,8;BW,267,,7,10;BY,375,8,6,11;BZ,501,,7,11;CA,1,1,7,10;CC,61,0,6,12;CD,243,0,7,10;CF,236,,8,8;CG,242,,9,9;CH,41,0,9,12;CI,225,,10,10;CK,682,,6,5;CL,56,,9,11;CM,237,,8,9;CN,86,0,7,12;CO,57,0,8,11;CR,506,,8,10;CU,53,0,6,10;CV,238,,7,7;CW,599,,7,8;CX,61,0,6,12;CY,357,,8,8;CZ,420,,9,12;DE,49,0,6,15;DJ,253,,8,8;DK,45,,8,8;DM,1,1,10,10;DO,1,1,10,10;DZ,213,0,8,9;EC,593,0,8,11;EE,372,,7,10;EG,20,0,8,10;ER,291,0,7,7;ES,34,,9,9;ET,251,0,9,9;FI,358,0,6,12;FJ,679,,7,11;FK,500,,6,5;FM,691,,7,7;FO,298,,6,6;FR,33,0,9,9;GA,241,,7,8;GB,44,0,7,10;GD,1,1,10,10;GE,995,0,9,9;GF,594,0,9,9;GH,233,0,8,9;GI,350,,8,8;GL,299,,6,6;GM,220,,7,9;GN,224,,8,9;GP,590,0,9,9;GQ,240,,9,9;GR,30,,10,12;GT,502,,8,11;GU,1,1,10,10;GW,245,,7,9;GY,592,,7,7;HK,852,,6,11;HN,504,,8,11;HR,385,0,7,9;HT,509,,8,8;HU,36,06,8,9;ID,62,0,7,17;IE,353,0,7,10;IL,972,0,7,12;IN,91,0,8,13;IO,246,,7,7;IQ,964,0,8,10;IR,98,0,6,10;IS,354,,7,9;IT,39,,6,12;JM,1,1,10,10;JO,962,0,8,9;JP,81,0,8,17;KE,254,0,7,10;KG,996,0,9,10;KH,855,0,8,10;KI,686,0,6,8;KM,269,,7,7;KN,1,1,10,10;KP,850,0,8,10;KR,82,0,6,14;KW,965,,7,8;KY,1,1,10,10;KZ,7,8,10,10;LA,856,0,8,10;LB,961,0,7,8;LC,1,1,10,10;LI,423,0,7,9;LK,94,0,9,9;LR,231,0,7,9;LS,266,,8,8;LT,370,0,8,8;LU,352,,6,11;LV,371,,8,8;LY,218,0,9,9;MA,212,0,9,9;MC,377,0,8,9;MD,373,0,8,8;ME,382,0,8,9;MF,590,0,9,9;MG,261,0,9,9;MH,692,1,7,7;MK,389,0,8,8;ML,223,,8,8;MM,95,0,6,10;MN,976,0,8,10;MO,853,,7,8;MP,1,1,10,10;MQ,596,0,9,9;MR,222,,8,8;MS,1,1,10,10;MT,356,,8,8;MU,230,,7,10;MV,960,,7,10;MW,265,0,7,9;MX,52,,10,10;MY,60,0,8,10;MZ,258,,8,9;NA,264,0,8,9;NC,687,,6,6;NE,227,,8,8;NF,672,,6,6;NG,234,0,10,14;NI,505,,8,8;NL,31,0,6,11;NO,47,,6,8;NP,977,0,8,11;NR,674,,7,7;NU,683,,6,7;NZ,64,0,6,10;OM,968,,7,9;PA,507,,7,11;PE,51,0,8,9;PF,689,,6,9;PG,675,,7,8;PH,63,0,6,13;PK,92,0,8,12;PL,48,,6,10;PM,508,0,6,9;PR,1,1,10,10;PS,970,0,8,10;PT,351,,9,9;PW,680,,7,7;PY,595,0,6,11;QA,974,,7,11;RE,262,0,9,9;RO,40,0,6,9;RS,381,0,6,12;RU,7,8,10,10;RW,250,0,8,9;SA,966,0,9,10;SB,677,,6,7;SC,248,,7,7;SD,249,0,9,9;SE,46,0,6,12;SG,65,,8,11;SH,290,,6,5;SI,386,0,6,8;SK,421,0,6,9;SL,232,0,8,8;SM,378,,8,10;SN,221,,9,9;SO,252,0,6,9;SR,597,,6,7;SS,211,0,9,9;ST,239,,7,7;SV,503,,7,11;SX,1,1,10,10;SY,963,0,8,9;SZ,268,,8,9;TC,1,1,10,10;TD,235,,8,8;TG,228,,8,8;TH,66,0,8,13;TJ,992,,9,9;TK,690,,6,7;TL,670,,7,8;TM,993,8,8,8;TN,216,,8,8;TO,676,,6,7;TR,90,0,10,10;TT,1,1,10,10;TV,688,,6,7;TW,886,0,7,11;TZ,255,0,9,9;UA,380,0,9,10;UG,256,0,9,9;US,1,1,10,10;UY,598,0,6,13;UZ,998,,9,9;VA,39,,6,12;VC,1,1,10,10;VE,58,0,10,10;VG,1,1,10,10;VI,1,1,10,10;VN,84,0,7,10;VU,678,,6,7;WF,681,,6,9;WS,685,,6,10;YE,967,0,7,9;YT,262,0,9,9;ZA,27,0,6,10;ZM,260,0,9,9;ZW,263,0,7,10';
var FIRST=['TR','SA','KW','AE','QA','IQ','BH','OM','JO','RU','AZ','DE','NL','GB','FR','US'];
var C={},BY_DIAL={};
DATA.split(';').forEach(function(r){
  var p=r.split(',');
  C[p[0]]={iso:p[0],dial:p[1],trunk:p[2],min:+p[3],max:+p[4]};
  (BY_DIAL[p[1]]=BY_DIAL[p[1]]||[]).push(p[0]);
});
// Ayni kodu paylasan ulkelerde once buyuk olan secilir.
var MAIN={'1':'US','7':'RU','44':'GB','39':'IT','47':'NO','61':'AU','212':'MA','262':'RE','358':'FI','590':'GP','599':'CW'};
function flag(iso){return String.fromCodePoint(iso.charCodeAt(0)+127397,iso.charCodeAt(1)+127397);}
function latin(s){return String(s||'').replace(/[٠-٩]/g,function(d){return d.charCodeAt(0)-1632;}).replace(/[۰-۹]/g,function(d){return d.charCodeAt(0)-1776;});}
function digits(s){return latin(s).replace(/\D/g,'');}
function national(el){
  var c=C[el._mpIso],d=digits(el.value);
  if(d.indexOf(c.trunk)===0&&c.trunk&&(c.trunk==='0'||d.length>c.max))d=d.slice(c.trunk.length);
  return d;
}
function format(iso,d){
  if(iso!=='TR')return null;
  return [d.slice(0,3),d.slice(3,6),d.slice(6,8),d.slice(8,10)].filter(Boolean).join(' ');
}
function paint(el){
  var c=C[el._mpIso];
  el._mpLabel.textContent=flag(c.iso)+' +'+c.dial;
  el._mpSelect.value=c.iso;
  el.placeholder=c.iso==='TR'?'532 123 45 67':'123 456 7890';
}
function detect(el){
  var s=latin(el.value).trim();
  if(!/^(\+|00)/.test(s))return false;
  var d=s.replace(/\D/g,'').replace(/^00/,'');
  for(var n=1;n<=4&&n<=d.length;n++){
    var list=BY_DIAL[d.slice(0,n)];
    if(list){
      el._mpIso=list.indexOf(el._mpIso)>=0?el._mpIso:(MAIN[d.slice(0,n)]||list[0]);
      el.value=d.slice(n);
      paint(el);
      return true;
    }
  }
  return false;
}
function tidy(el){
  var waiting=/^\s*\+/.test(el.value)||/^\s*00/.test(el.value);
  if(waiting&&!detect(el))return;
  var iso=el._mpIso,d=digits(el.value);
  if(iso==='TR'&&d.length===12&&d.indexOf('90')===0)d=d.slice(2);
  if(iso==='TR'&&d.charAt(0)==='0')d=d.slice(1);
  var atEnd=el.selectionStart===null||el.selectionStart>=el.value.length;
  if(!atEnd)return;
  var f=format(iso,d.slice(0,10));
  el.value=f===null?latin(el.value).replace(/[^\d\s]/g,''):f;
}
function injectCss(){
  if(document.getElementById('mpCss'))return;
  var s=document.createElement('style');s.id='mpCss';
  s.textContent='.mp{display:flex;gap:8px;width:100%;direction:ltr}.mp input{flex:1;min-width:0;margin:0;text-align:left}.mp-cc{position:relative;flex:none;display:flex;align-items:center;gap:4px;width:auto;margin:0;white-space:nowrap;cursor:pointer}.mp-cc svg{width:10px;height:10px;opacity:.55}.mp-cc select{position:absolute;inset:0;width:100%;height:100%;opacity:0;margin:0;padding:0;border:0;cursor:pointer;font-size:16px}.mp-cc:focus-within{outline:2px solid currentColor;outline-offset:1px}';
  document.head.appendChild(s);
}
function mount(el,opts){
  if(!el||el._mpIso)return;
  opts=opts||{};
  injectCss();
  var lang=(document.documentElement.lang||'tr').slice(0,2),names=null;
  try{names=new Intl.DisplayNames([lang],{type:'region'});}catch(e){}
  var name=function(i){try{return names?names.of(i):i;}catch(e){return i;}};
  var rest=Object.keys(C).filter(function(i){return FIRST.indexOf(i)<0;}).sort(function(a,b){return name(a).localeCompare(name(b),lang);});
  var wrap=document.createElement('div');wrap.className='mp';
  var cc=document.createElement('label');cc.className='mp-cc '+(opts.ccClass||'');
  var label=document.createElement('span');
  var sel=document.createElement('select');sel.setAttribute('aria-label',opts.label||'Ülke kodu');
  sel.innerHTML=FIRST.concat(rest).map(function(i){return '<option value="'+i+'">'+flag(i)+' '+name(i)+' +'+C[i].dial+'</option>';}).join('');
  cc.appendChild(label);
  cc.insertAdjacentHTML('beforeend','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>');
  cc.appendChild(sel);
  el.parentNode.insertBefore(wrap,el);
  wrap.appendChild(cc);wrap.appendChild(el);
  el.type='tel';el.inputMode='tel';
  el._mpIso='TR';el._mpLabel=label;el._mpSelect=sel;
  paint(el);
  sel.addEventListener('change',function(){el._mpIso=sel.value;paint(el);tidy(el);el.focus();});
  el.addEventListener('input',function(){tidy(el);});
  if(el.value)tidy(el);
}
function valid(el){
  var c=C[el._mpIso],d=national(el);
  if(c.iso==='TR')return /^[2-58]\d{9}$/.test(d);
  return d.length>=c.min&&d.length<=c.max;
}
function value(el){return valid(el)?'+'+C[el._mpIso].dial+national(el):'';}
function set(el,v){
  el._mpIso='TR';el.value=v||'';paint(el);
  if(el.value)tidy(el);
}
window.MarePhone={mount:mount,valid:valid,value:value,set:set};
})();
