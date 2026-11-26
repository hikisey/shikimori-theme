const fs=require('fs');const pw=(()=>{try{return require('playwright-core')}catch(e){return require('/workspace/pw/node_modules/playwright-core')}})();const nc=require('/workspace/rf/netcache');
const [fx,...css]=process.argv.slice(2);
(async()=>{const b=await pw.chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
for(const c of css){for(const start of [1280,1920]){const ctx=await b.newContext({viewport:{width:start,height:900}});const p=await ctx.newPage();await nc(p,{block:['image','font','media']});
 const h=fs.readFileSync(fx,'utf8').replace('<!--THEME-->','<style>'+fs.readFileSync(c,'utf8')+'</style>');
 await p.setContent(h,{waitUntil:'load',timeout:90000}).catch(()=>{});
 if(start==1280)await p.setViewportSize({width:1920,height:900});
 const r=[];for(const t of [0,200,1000]){await new Promise(x=>setTimeout(x,t));r.push(await p.evaluate(()=>{const e=document.querySelector('section.l-page');const s=getComputedStyle(e);return s.marginLeft+' w='+s.width+' iw='+innerWidth}))}
 console.log(c,start,r.join(' | '));await ctx.close()}}
await b.close()})();
