#!/usr/bin/env python3
"""Скриншоты компьютера и телефона — одной картинкой одинаковой высоты (для README).
Отдельные <img> в таблице GitHub масштабирует по-разному: на компьютере телефон выходил выше скриншота ПК,
а в мобильном GitHub — огромным. Одна картинка с width="100%" везде в одном масштабе.
python3 tools/preview_pair.py pc.png phone.png out.webp [высота=900]"""
import sys
from PIL import Image

def pair(pc_path, phone_path, out, h=900, gap=24):
    pc = Image.open(pc_path).convert("RGB")
    ph = Image.open(phone_path).convert("RGB")
    pc = pc.resize((round(pc.width * h / pc.height), h), Image.LANCZOS)
    ph = ph.resize((round(ph.width * h / ph.height), h), Image.LANCZOS)
    im = Image.new("RGBA", (pc.width + gap + ph.width, h), (0, 0, 0, 0))  # промежуток прозрачный: и светлая, и тёмная тема GitHub
    im.paste(pc, (0, 0))
    im.paste(ph, (pc.width + gap, 0))
    im.save(out, "webp", quality=82, method=6)
    print(out, im.size)

if __name__ == "__main__":
    a = sys.argv[1:]
    pair(a[0], a[1], a[2], int(a[3]) if len(a) > 3 else 900)
