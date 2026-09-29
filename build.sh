#!/usr/bin/env bash
# Пересобрать сайт, постер и лист QR-кодов.
#   BASE_URL — адрес сайта, на который ведут QR (по умолчанию GitHub Pages этого репозитория)
#   PHOTOS=1 — вставить реальные фото из src/photos/<id>.jpg (по умолчанию иллюстрации)
# Нужны: Python 3 + requirements.txt, Node.js + playwright, шрифт Nunito в системе.
set -e
cd "$(dirname "$0")"
STANDALONE=1 OUT=../index.html python3 build_app.py
python3 poster_clay.py
node render_poster.js
python3 - <<'PY'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from PIL import Image
W, H = landscape(A3)
c = canvas.Canvas("../poster/poster-A3.pdf", pagesize=(W, H)); c.drawImage("poster_hi.png", 0, 0, W, H); c.save()
im = Image.open("poster_hi.png").convert("RGB")
im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save("../poster/poster-preview.png")
PY
python3 make_qr_sheet.py
echo "Готово: index.html, poster/"
