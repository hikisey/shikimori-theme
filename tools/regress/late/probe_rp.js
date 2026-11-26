// node probe_rp.js page.html a.css b.css : размеры .related-poster img на планшете 1024 (isMobile), несколько замеров
const fs=require('fs');const pw=(()=>{try{return require('playwright-core')}catch(e){return require('/workspace/pw/node_modules/playwright-core')}})();const nc=require('/workspace/rf/netcache');
const [fx,...css]=process.argv.slice(2);
(async()=>{const b=await pw.chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
for(const c of css)for(const start of [1280,1024]){const ctx=await b.newContext({viewport:{width:start,height:start==1024?768:900},isMobile:start==1024,hasTouch:start==1024});const p=await ctx.newPage();await nc(p,{block:['image','font','media']});
 const h=fs.readFileSync(fx,'utf8').replace('<!--THEME-->','<style>'+fs.readFileSync(c,'utf8')+'</style>');
 await p.setContent(h,{waitUntil:'load',timeout:90000}).catch(()=>{});
 if(start==1280)await p.setViewportSize({width:1024,height:768});
 const r=[];for(const t of [0,300,2000]){await new Promise(x=>setTimeout(x,t));r.push(await p.evaluate(()=>[...document.querySelectorAll('a.related-poster img')].slice(0,6).map(i=>Math.round(i.getBoundingClientRect().width)).join(',')))}
 console.log(c,start,r.join(' | '));await ctx.close()}
await b.close()})();
