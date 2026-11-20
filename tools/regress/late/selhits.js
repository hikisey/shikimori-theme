// node selhits.js sels.json files.txt out.json : для каждого селектора (без состояний) — на каких страницах находит
const pw=require('/workspace/pw/node_modules/playwright-core');const fs=require('fs'),path=require('path');
const sels=JSON.parse(fs.readFileSync(process.argv[2]));const files=fs.readFileSync(process.argv[3],'utf8').split('\n').filter(Boolean);
function san(s){return s.replace(/::?(before|after|first-line|first-letter)(?![\w-])/g,'').replace(/::[\w-]+(\([^)]*\))?/g,'').replace(/:(hover|focus|focus-visible|focus-within|active|visited|target|checked|indeterminate|placeholder-shown|autofill|-webkit-autofill|open)(?![\w-])/g,'').replace(/:-moz-[\w-]+/g,'').trim()||'*'}
(async()=>{const b=await pw.chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const ctx=await b.newContext({javaScriptEnabled:false});const p=await ctx.newPage();
 const S=sels.map(san);const hits=sels.map(()=>[]);
 for(const f of files){let h=fs.readFileSync(f,'utf8').replace(/<script[\s\S]*?<\/script>/gi,'').replace(/<link[^>]*>/gi,'').replace(/\ssrc=/gi,' data-src=').replace(/\ssrcset=/gi,' data-srcset=');
  await p.setContent(h,{waitUntil:'domcontentloaded'});
  const r=await p.evaluate(S=>{const hit=[];S.forEach((s,i)=>{try{if(document.querySelector(s))hit.push(i)}catch(e){}});return hit},S);
  for(const i of r)hits[i].push(path.basename(f));}
 fs.writeFileSync(process.argv[4],JSON.stringify(Object.fromEntries(sels.map((s,i)=>[s,hits[i]]))));await b.close()})();
