#!/usr/bin/env python3
"""Темы-варианты: themes/<slug>/site.css собирается из корневого site.css (тот же текст, импорты и
комментарии) с заменой значений палитры. Запускать после каждого изменения site.css и при выпуске
(после замены версии в site.css): python3 tools/build_themes.py
Обои темы лежат рядом (bg.webp ≤3840, bg_m.webp 1080×1920) и подключаются с raw.githubusercontent.com по тегу
версии из site.css (без @ в адресе), баннер профиля — banner.webp 2400×600 (широкий кадр тех же обоев, 4:1 под шапку 1200×300, чёткий на 4K)."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
# описание и источник обоев — для раздела «Готовые темы» в README
INFO = {
    "default": ("алая (по умолчанию)", "графит и алый акцент; это обычный <code>site.css</code> из корня репозитория.",
                "обои и баннер — как в основной теме; на скриншоте — профиль hikisey."),
    "neon": None, "torii": None, "moon": None, "lake": None,
}
DESC = {
    "neon": ("ночной квартал в неоне: тёплый тёмный фон и мятный акцент.",
             "обои «Neon Shallows», автор неизвестен (найдены на Pinterest и wallpapersden.com)."),
    "torii": ("ворота-тории в туманном лесу: зелёное стекло и шалфейный акцент.",
              "обои — автор неизвестен (Pinterest, Reddit «Serene Nature Torii Arch»), увеличены до 4K нейросетью Real-ESRGAN."),
    "moon": ("месяц в ночных облаках, на телефоне — вороны и газетная бумага; синее стекло и лунно-голубой акцент.",
             "облака — автор неизвестен (Pinterest), увеличены до 4K нейросетью Real-ESRGAN; вороны — Telegram-канал [@wallpaper_hd_svstmrn](https://t.me/wallpaper_hd_svstmrn)."),
    "lake": ("пагоды у туманного озера: графитовое стекло и серо-бирюзовый акцент.",
             "обои — qbuer (Midjourney), увеличены до 4K нейросетью Real-ESRGAN."),
}

THEMES = {
    "neon": ("неоновый квартал", {
        "accent": "96, 204, 146", "bg-color": "34, 21, 17", "bg-color-mobile": "30, 20, 17",
        "bg-zoom": "1", "bg-blur": "2px", "bg-dim": ".55",
        "profile-banner-position": "center",
        "glass": "18, 16, 17", "text": "238, 236, 234", "text-2": "180, 174, 172", "text-3": "146, 140, 138",
        "time-empty": "34, 30, 30",
    }),
    "torii": ("туманные тории", {
        "accent": "134, 196, 168", "bg-color": "54, 94, 80", "bg-color-mobile": "48, 86, 72",
        "bg-zoom": "1", "bg-dim": ".45",
        "profile-banner-position": "center",
        "glass": "16, 26, 24", "text": "234, 242, 238", "text-2": "172, 188, 182", "text-3": "140, 156, 150",
        "time-empty": "28, 40, 37",
    }),
    "moon": ("лунная ночь", {
        "accent": "150, 184, 236", "bg-color": "75, 95, 123", "bg-color-mobile": "62, 74, 92",
        "bg-zoom": "1", "bg-dim": ".4",
        "profile-banner-position": "center",
        "glass": "18, 24, 38", "text": "232, 238, 250", "text-2": "170, 182, 204", "text-3": "138, 150, 172",
        "time-empty": "30, 38, 54",
    }),
    "lake": ("туманное озеро", {
        "accent": "156, 186, 196", "bg-color": "93, 98, 99", "bg-color-mobile": "93, 98, 99",
        "bg-zoom": "1", "bg-dim": ".5",
        "profile-banner-position": "center",
        "glass": "22, 24, 27", "text": "236, 238, 238", "text-2": "176, 180, 182", "text-3": "144, 148, 150",
        "time-empty": "34, 37, 40",
    }),
}

def main():
    site = (ROOT / "site.css").read_text(encoding="utf-8")
    ver = re.search(r"/(v\d+\.\d+\.\d+)/css/part_01\.css", site).group(1)
    for slug, (name, vals) in THEMES.items():
        # с тегом версии, но без «@» (jsDelivr пишет тег через @, а Шикимори не показывает картинки с @ в адресе)
        cdn = f"https://raw.githubusercontent.com/Hikisey/shikimori-theme/{ver}/themes/{slug}"
        v = dict(vals)
        v["bg-image"] = f'url("{cdn}/bg.webp")'
        v["bg-image-mobile"] = f'url("{cdn}/bg_m.webp")'
        v["profile-banner"] = f'url("{cdn}/banner.webp")'
        s = site
        for k, val in v.items():
            s, n = re.subn(r"(\n    --%s: )[^;]*;" % re.escape(k), lambda m: m.group(1) + val + ";", s, count=1)
            if n != 1:
                sys.exit(f"нет переменной --{k} в site.css")
        s = s.replace("/* shiki glass " + ver + " —", f"/* shiki glass {ver}, тема «{name}» —", 1)
        out = ROOT / "themes" / slug / "site.css"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(s, encoding="utf-8")
        print(out.relative_to(ROOT), len(s.encode()), "байт")

def readme():
    """Раздел README между <!-- themes:start --> и <!-- themes:end -->: по сворачиваемому пункту на тему,
    внутри скриншоты ПК и телефона рядом и ещё один сворачиваемый блок «CSS-код» с полным site.css."""
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    a, b = "<!-- themes:start -->", "<!-- themes:end -->"
    if a not in text or b not in text:
        return
    out = [a, ""]
    for slug in ["default"] + list(THEMES):
        if slug == "default":
            name, desc, src = INFO["default"]
            css = (ROOT / "site.css").read_text(encoding="utf-8")
        else:
            name = THEMES[slug][0]
            desc, src = DESC[slug]
            css = (ROOT / "themes" / slug / "site.css").read_text(encoding="utf-8")
        out += [
            "<details>",
            f"<summary><b>{name}</b> — {desc}</summary>",
            "",
            "<table>",
            "  <tr>",
            f'    <td valign="top"><img src="themes/{slug}/preview-pc.webp" alt="{name}: компьютер"></td>',
            f'    <td valign="top" width="200"><img src="themes/{slug}/preview-phone.webp" width="180" alt="{name}: телефон"></td>',
            "  </tr>",
            "</table>",
            "",
            f"Источник: {src}",
            "",
            "<details>",
            "<summary>CSS-код</summary>",
            "",
            "```css",
            css.rstrip("\n"),
            "```",
            "",
            "</details>",
            "</details>",
            "",
        ]
    out.append(b)
    i, j = text.index(a), text.index(b) + len(b)
    path.write_text(text[:i] + "\n".join(out) + text[j:], encoding="utf-8")
    print("README.md: раздел тем обновлён")


if __name__ == "__main__":
    main()
    readme()
