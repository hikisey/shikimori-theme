// node probe_img.js page.html a.css b.css : ширины .body > a.b-image и img до и после прокрутки к ним (ленивые картинки)
const fs=require('fs');const pw=(()=>{try{return require('playwright-core')}catch(e){return require('/workspace/pw/node_modules/playwright-core')}})();const nc=require('/workspace/rf/netcache');
const [fx,...css]=process.argv.slice(2);
(async()=>{const b=await pw.chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
for(const c of css){const ctx=await b.newContext({viewport:{width:1280,height:900}});const p=await ctx.newPage();await nc(p,{block:['image','font','media']});
 await p.setContent(fs.readFileSync(fx,'utf8').replace('<!--THEME-->','<style>'+fs.readFileSync(c,'utf8')+'</style>'),{waitUntil:'load',timeout:90000}).catch(()=>{});
 const m=()=>p.evaluate(()=>[...document.querySelectorAll('.body > a.b-image')].map(a=>getComputedStyle(a).width+'/'+getComputedStyle(a.querySelector('img')).width).join(','));
 const r=[await m()];await p.evaluate(()=>document.querySelector('.body > a.b-image').scrollIntoView());await new Promise(x=>setTimeout(x,1500));r.push(await m());
 console.log(c,r.join(' | после прокрутки: '));await ctx.close()}
await b.close()})();
