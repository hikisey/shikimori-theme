// [AT=center] node hovershift.js style.css page.html dev selector [n]  (курсор у шапки или, с AT=center, в центре)  — для первых n элементов selector: высота и положение
// детей до наведения и под курсором; печатает элементы, которые сдвинулись или изменили размер (наведение двигает вёрстку)
const fs=require('fs');const pw=(()=>{try{return require('playwright-core')}catch(e){return require('/workspace/pw/node_modules/playwright-core')}})();const nc=require('/workspace/rf/netcache');
const [css,pg,dev,sel,n='3']=process.argv.slice(2);
const D={pc:{viewport:{width:1366,height:900}},pc1920:{viewport:{width:1920,height:1000}},tab:{viewport:{width:1024,height:768}}};
(async()=>{const b=await pw.chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const ctx=await b.newContext(D[dev]||D.pc);const p=await ctx.newPage();await nc(p,{block:['media']});
await p.setContent(fs.readFileSync(pg,'utf8').replace('<!--THEME-->','<style id="custom_css">'+fs.readFileSync(css,'utf8').replace(/<\/style/gi,'')+'</style>'),{waitUntil:'load',timeout:90000}).catch(()=>{});
await p.addStyleTag({content:'*,*::before,*::after{transition-duration:0s!important;animation-duration:0s!important}'});await p.waitForTimeout(600);
const snap=i=>p.evaluate(([sel,i])=>{const e=document.querySelectorAll(sel)[i];const o={};let k=0;for(const x of [e,...e.querySelectorAll('*')]){if(x.closest('aside.buttons, .item-mobile')){k++;continue}const r=x.getBoundingClientRect();o[k++]=[x.tagName+'.'+(x.className?.toString()||'').split(' ')[0],Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height),getComputedStyle(x).display]}return o},[sel,i]);
const cnt=await p.evaluate(s=>document.querySelectorAll(s).length,sel);let bad=0;
for(let i=0;i<Math.min(+n,cnt);i++){const els=await p.$$(sel);await els[i].scrollIntoViewIfNeeded();await p.mouse.move(1,1);await p.waitForTimeout(150);const a=await snap(i);
 const bb=await els[i].boundingBox();await p.mouse.move(bb.x+bb.width/2,process.env.AT==='center'?bb.y+bb.height/2:bb.y+20);await p.waitForTimeout(250);const h=await snap(i);
 for(const k in a){const x=a[k],y=h[k];if(!y)continue;if(x[5]!==y[5]&&!(x[3]==0&&y[3]==0)){bad++;if(bad<15)console.log('#'+i,x[0],'display',x[5],'->',y[5],y.slice(1,5).join(','))}else if(x[5]!=='none'&&y[5]!=='none'&&(x[1]!=y[1]||x[2]!=y[2]||x[3]!=y[3]||x[4]!=y[4])){bad++;if(bad<15)console.log('#'+i,x[0],'rest',x.slice(1,5).join(','),'hover',y.slice(1,5).join(','))}}}
console.log(sel,'elements',cnt,'checked',Math.min(+n,cnt),'shifted',bad);await b.close()})();
