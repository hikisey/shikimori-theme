// node probe_l.js style.css page.html dev 'js expression returning JSON'
const fs=require('fs');const pw=require('/workspace/pw/node_modules/playwright-core');const nc=require('./netcache');
const [css,pg,dev,expr]=process.argv.slice(2);
(async()=>{const b=await pw.chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const ctx=await b.newContext(dev==='phone'?{viewport:{width:390,height:844},isMobile:true,hasTouch:true}:{viewport:{width:1366,height:900}});
const p=await ctx.newPage();await nc(p,{block:['media','image']});
const h=fs.readFileSync(pg,'utf8').replace('<!--THEME-->','<style id="custom_css">'+fs.readFileSync(css,'utf8').replace(/<\/style/gi,'')+'</style>');
await p.setContent(h,{waitUntil:'load',timeout:90000}).catch(()=>{});await p.waitForTimeout(500);
console.log(JSON.stringify(await p.evaluate(expr),null,1));await b.close()})();
