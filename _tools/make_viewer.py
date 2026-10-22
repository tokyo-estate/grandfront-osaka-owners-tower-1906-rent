"""pdf/1906_{lang}.pdf をページ画像にして、スマホでもダウンロードにならず「開ける」ビューア pdf/view.html を作る"""
import glob, json, os, subprocess, sys
site = os.path.abspath(sys.argv[1]); P = f'{site}/pdf'; os.makedirs(f'{P}/pages', exist_ok=True)
for f in glob.glob(f'{P}/pages/*.jpg'): os.remove(f)
counts = {}
for l in ('ja', 'en', 'zh'):
    subprocess.run(['pdftoppm', '-r', '200', '-jpeg', '-jpegopt', 'quality=88,progressive=y', f'{P}/1906_{l}.pdf', f'{P}/pages/{l}'], check=True)
    fs = sorted(glob.glob(f'{P}/pages/{l}-*.jpg')); counts[l] = len(fs)
    for i, f in enumerate(fs, 1): os.rename(f, f'{P}/pages/{l}-{i:02d}.jpg')
L = {'ja': ['物件資料', 'PDFをダウンロード', 'サイトに戻る'], 'en': ['Brochure', 'Download PDF', 'Back to site'], 'zh': ['物业资料', '下载PDF', '返回网站']}
html = '''<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex, nofollow"><title>Grand Front Osaka Owners Tower 1906</title>
<style>:root{--gold:#c9a962}*{box-sizing:border-box;margin:0}html,body{background:#1a1c20}body{font-family:"Hiragino Sans","PingFang SC","Noto Sans JP",sans-serif;color:#eee}
.top{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:10px;padding:10px 14px;padding-top:calc(10px + env(safe-area-inset-top));background:rgba(16,17,20,.92);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);font-size:12px;letter-spacing:.08em}
.top .t{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#cfc9bd}
.top a{color:var(--gold);text-decoration:none;border:1px solid rgba(201,169,98,.6);border-radius:99px;padding:6px 12px;white-space:nowrap}
.pages{max-width:900px;margin:0 auto;padding:12px 10px 40px;display:grid;gap:12px}
.pages img{display:block;width:100%;height:auto;aspect-ratio:210/297;background:#2a2d33;box-shadow:0 6px 24px rgba(0,0,0,.45)}</style></head><body>
<div class="top"><a id="back" href="../">‹</a><div class="t" id="tt"></div><a id="dl" download>PDF</a></div><div class="pages" id="pages"></div>
<script>var C=__C__,L=__L__,V="__V__";var l=(location.search.match(/[?&]lang=(ja|en|zh)/)||[])[1]||"ja";document.documentElement.lang=l;
document.getElementById("tt").textContent="Grand Front Osaka Owners Tower — 1906　"+L[l][0];var dl=document.getElementById("dl");dl.href="1906_"+l+".pdf?"+V;dl.textContent=L[l][1];
var bk=document.getElementById("back");bk.href="../?lang="+l;bk.title=L[l][2];
var box=document.getElementById("pages");for(var i=1;i<=C[l];i++){var im=new Image();im.src="pages/"+l+"-"+(i<10?"0":"")+i+".jpg?"+V;im.alt=L[l][0]+" "+i;im.loading=i<=2?"eager":"lazy";im.width=1654;im.height=2339;box.appendChild(im);}</script></body></html>'''
V = sys.argv[2] if len(sys.argv) > 2 else 'v1'
open(f'{P}/view.html', 'w', encoding='utf-8').write(html.replace('__C__', json.dumps(counts)).replace('__L__', json.dumps(L, ensure_ascii=False)).replace('__V__', V))
print('viewer ok', counts)
