// node dropframes.js style.css page.html out_prefix dev(pc|tab|phone) "openJS" clipSel t1,t2,... [pad] [reduce]
// Открывает меню скриптом openJS (например, добавляет .active), ставит все анимации/переходы страницы
// на паузу и снимает кадры в моменты t (мс от начала) — видно, как появляются меню и его тень.
// clipSel — элемент меню; кадр = его рамка + pad со всех сторон (тень видна).
const fs=require('fs');const pw=(()=>{try{return require('playwright-core')}catch(e){return require('/workspace/pw/node_modules/playwright-core')}})();const nc=require('/workspace/rf/netcache');
const [css,pg,out,dev,openJS,sel,ts,pad='60',reduce]=process.argv.slice(2);
const D={pc:{viewport:{width:1366,height:900}},tab:{viewport:{width:1024,height:768},isMobile:true,hasTouch:true},phone:{viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true}};
(async()=>{const b=await pw.chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--hide-scrollbars']});
const o=Object.assign({},D[dev]||D.pc);if(reduce)o.reducedMotion='reduce';const ctx=await b.newContext(o);const p=await ctx.newPage();await nc(p,{block:['media']});
await p.setContent(fs.readFileSync(pg,'utf8').replace('<!--THEME-->','<style id="custom_css">'+fs.readFileSync(css,'utf8').replace(/<\/style/gi,'')+'</style>'),{waitUntil:'load',timeout:90000}).catch(()=>{});
await p.waitForTimeout(800);
await p.evaluate(()=>{for(const a of document.getAnimations())a.finish?.()});
await p.evaluate(openJS);
await p.evaluate(()=>{window.__an=document.getAnimations();for(const a of window.__an)a.pause()});
const el=await p.$(sel);if(!el){console.log('no el');process.exit(1)}
for(const t of ts.split(',').map(Number)){
  await p.evaluate(t=>{for(const a of window.__an)a.currentTime=t},t);await p.waitForTimeout(60);
  const bb=await el.boundingBox();const P=+pad;
  await p.screenshot({path:`${out}_${String(t).padStart(3,'0')}ms.png`,clip:{x:Math.max(0,bb.x-P),y:Math.max(0,bb.y-10),width:bb.width+2*P,height:bb.height+P+10}});
}
console.log(JSON.stringify(await p.evaluate(()=>window.__an.map(a=>[a.constructor.name,a.animationName||a.transitionProperty,a.effect?.target?.className?.toString().slice(0,40)]))));await b.close()})();
