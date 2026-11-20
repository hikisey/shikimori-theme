// node elshot.js style.css page.html out.png dev(pc|phone) selector [pad] [hoverSel]
const fs=require('fs');const pw=require('/workspace/pw/node_modules/playwright-core');const nc=require('./netcache');
const [css,pg,out,dev,sel,pad='20',hov]=process.argv.slice(2);
(async()=>{const b=await pw.chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--hide-scrollbars']});
const ctx=await b.newContext(dev==='phone'?{viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true}:{viewport:{width:1366,height:900}});
const p=await ctx.newPage();await nc(p,{block:['media']});
const h=fs.readFileSync(pg,'utf8').replace('<!--THEME-->','<style id="custom_css">'+fs.readFileSync(css,'utf8').replace(/<\/style/gi,'')+'</style>');
await p.setContent(h,{waitUntil:'load',timeout:90000}).catch(()=>{});await p.waitForTimeout(800);
const el=await p.$(sel);if(!el){console.log('no el');process.exit(1)}await el.scrollIntoViewIfNeeded();if(hov)await p.hover(hov);await p.waitForTimeout(400);
const bb=await el.boundingBox();const P=+pad;
await p.screenshot({path:out,clip:{x:Math.max(0,bb.x-P),y:Math.max(0,bb.y-P),width:bb.width+2*P,height:bb.height+2*P}});
console.log(JSON.stringify(bb));await b.close()})();
