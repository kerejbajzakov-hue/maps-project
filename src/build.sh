#!/usr/bin/env bash
# Пересобрать сайт, постеры и лист QR-кодов.
#   BASE_URL — адрес сайта, на который ведут QR (по умолчанию GitHub Pages этого репозитория)
# Нужны: Python 3 + requirements.txt, Node.js + playwright, шрифт Nunito в системе.
set -e
cd "$(dirname "$0")"
export PHOTO_DIR=../photos
# сайт с галереей фото (фото лежат отдельными файлами в /photos)
PHOTOS=files STANDALONE=1 OUT=../index.html python3 build_app.py
pdf() { python3 - "$1" "$2" <<'PY'
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from PIL import Image
W, H = landscape(A3)
c = canvas.Canvas(sys.argv[1], pagesize=(W, H)); c.drawImage("poster_hi.png", 0, 0, W, H); c.save()
if sys.argv[2] != "-":
    im = Image.open("poster_hi.png").convert("RGB"); im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(sys.argv[2])
PY
}
# постер с фото
PHOTOS=1 python3 poster_clay.py && node render_poster.js && pdf ../poster/poster-A3-photos.pdf ../poster/poster-preview.png
# постер с иллюстрациями
PHOTOS=0 python3 poster_clay.py && node render_poster.js && pdf ../poster/poster-A3.pdf -
python3 make_qr_sheet.py
rm -f poster_clay.html poster_hi.png
echo "Готово: index.html, poster/"
