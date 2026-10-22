#!/bin/bash
# index.html（日英中切替入り）から A4 の PDF 版を日英中で作り直す → pdf/1906_{ja,en,zh}.pdf ＋ スマホ用ビューア pdf/view.html
# 日本語本文を直したら: _グランフロント大阪_i18n/make_gfo1906.py を直す → python3 _グランフロント大阪_i18n/apply_gfo.py → これ → _deploy.sh
set -e
cd "$(dirname "$0")"
node _tools/ovl_images.mjs "$PWD"                                   # 重ね文字付きの図を言語別画像に
for f in $(ls img/s01_structure_??.png img/u00_plan2d_??.png 2>/dev/null); do python3 -c "from PIL import Image;Image.open('$f').convert('RGB').save('${f%.png}.jpg',quality=88)"; rm "$f"; done
python3 /Users/leetenki/AI_share/.claude/skills/property-site/scripts/make_pdf_brochure.py "$PWD" --name 1906
V=$(grep -o 'view.html?lang=ja&v=[0-9a-z]*' index.html | head -1 | sed 's/.*&//')
python3 _tools/make_viewer.py "$PWD" "$V"
ls -la pdf/*.pdf
