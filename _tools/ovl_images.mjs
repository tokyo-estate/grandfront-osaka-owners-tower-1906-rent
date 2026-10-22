// サイトの重ね文字付き図（#ovl-st 構造図 / #ovl-plan 2D間取図）を言語別の画像に書き出す（PDF 用）
import { chromium } from '/Users/leetenki/AI_share/_tools/node_modules/playwright/index.mjs';
const site=process.argv[2]; const b=await chromium.launch({channel:'chrome'});
const T=[['ovl-st','img/s01_structure',2],['ovl-plan','img/u00_plan2d',3]];
for (const lang of ['ja','en','zh']) for (const [id,base,dsf] of T) {
  const p=await b.newPage({viewport:{width:1280,height:900},deviceScaleFactor:dsf}); await p.goto('file://'+site+'/index.html?lang='+lang);
  await p.addStyleTag({content:'.rv,.zoom img{opacity:1!important;transform:none!important}'});
  await p.evaluate(()=>document.querySelectorAll('img').forEach(i=>i.loading='eager')); await p.evaluate(()=>document.fonts.ready);
  const el=p.locator('#'+id); if(!(await el.count())){ await p.close(); continue; } await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(500);
  await el.screenshot({path:`${site}/${base}_${lang}.png`}); await p.close(); }
await b.close(); console.log('ovl images ok');
