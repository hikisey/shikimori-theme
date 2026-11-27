#!/usr/bin/env python3
"""Темы-варианты: themes/<slug>/site.css собирается из корневого site.css (тот же текст, импорты и
комментарии) с заменой значений палитры. Запускать после каждого изменения site.css и при выпуске
(после замены версии в site.css): python3 tools/build_themes.py
Палитру темы по умолчанию (DEFAULT) скрипт пишет и в сам корневой site.css. Скриншот темы — preview.webp
(компьютер и телефон одной картинкой, tools/preview_pair.py).
Обои темы лежат рядом (bg.webp ≤3840, bg_m.webp 1080×1920) и подключаются с raw.githubusercontent.com по тегу
версии из site.css (без @ в адресе), баннер профиля — banner.webp 2400×600 (широкий кадр тех же обоев, 4:1 под шапку 1200×300, чёткий на 4K)."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Тема по умолчанию (корневой site.css) — «лунная ночь» (с v1.7.21). Её значения build_themes.py пишет и в
# корневой site.css, и в themes/moon/site.css. Прежняя алая тема — themes/crimson/.
DEFAULT = "moon"

# Полная палитра, от которой считаются все темы (значения прежней алой темы по умолчанию).
# У каждой темы ниже — только отличия; в site.css темы пишутся все переменные из BASE.
BASE = {
    "accent": "232, 108, 108", "bg-color": "151, 128, 128", "bg-color-mobile": "167, 148, 145",
    "bg-zoom": "1.08", "bg-blur": "0px", "bg-blur-mobile": "1.5px", "bg-dim": ".5",
    "profile-banner-position": "center",
    "glass": "30, 34, 42", "glass-blur": "5px",
    "text": "236, 240, 247", "text-2": "170, 178, 192", "text-3": "140, 148, 160",
    "time-empty": "34, 38, 46",
}

# описание и источник обоев — для раздела «Готовые темы» в README
DESC = {
    "moon": ("месяц в ночных облаках, на телефоне — вороны и газетная бумага; синее стекло и лунно-голубой акцент.",
             "облака — автор неизвестен (Pinterest), увеличены до 4K нейросетью Real-ESRGAN; вороны — Telegram-канал [@wallpaper_hd_svstmrn](https://t.me/wallpaper_hd_svstmrn)."),
    "crimson": ("графит и алый акцент; до v1.7.21 это была тема по умолчанию.",
                "обои — как в прежней основной теме; баннер — Pinterest, автор неизвестен."),
    "neon": ("ночной квартал в неоне: тёплый тёмный фон и мятный акцент.",
             "обои «Neon Shallows», автор неизвестен (найдены на Pinterest и wallpapersden.com)."),
    "torii": ("ворота-тории в туманном лесу: зелёное стекло и шалфейный акцент.",
              "обои — автор неизвестен (Pinterest, Reddit «Serene Nature Torii Arch»), увеличены до 4K нейросетью Real-ESRGAN."),
    "lake": ("пагоды у туманного озера: графитовое стекло и серо-бирюзовый акцент.",
             "обои — qbuer (Midjourney), увеличены до 4K нейросетью Real-ESRGAN."),
    "purple": ("фиолетовое ночное небо и баннер «Пурпурные облака»: фиолетовое стекло и сиреневый акцент.",
               "обои «Sublime purple night sky» — Vincentiu Solomon, баннер «Purple and pink cloudy sky» — Jeremy Bishop (оба Unsplash, CC0)."),
}

THEMES = {
    "moon": ("лунная ночь", {
        "accent": "150, 184, 236", "bg-color": "75, 95, 123", "bg-color-mobile": "62, 74, 92",
        "bg-zoom": "1", "bg-dim": ".4",
        "glass": "18, 24, 38", "text": "232, 238, 250", "text-2": "170, 182, 204", "text-3": "138, 150, 172",
        "time-empty": "30, 38, 54",
    }),
    "crimson": ("алая", {}),
    "neon": ("неоновый квартал", {
        "accent": "96, 204, 146", "bg-color": "34, 21, 17", "bg-color-mobile": "30, 20, 17",
        "bg-zoom": "1", "bg-blur": "2px", "bg-dim": ".55",
        "glass": "18, 16, 17", "text": "238, 236, 234", "text-2": "180, 174, 172", "text-3": "146, 140, 138",
        "time-empty": "34, 30, 30",
    }),
    "torii": ("туманные тории", {
        "accent": "134, 196, 168", "bg-color": "54, 94, 80", "bg-color-mobile": "48, 86, 72",
        "bg-zoom": "1", "bg-dim": ".45",
        "glass": "16, 26, 24", "text": "234, 242, 238", "text-2": "172, 188, 182", "text-3": "140, 156, 150",
        "time-empty": "28, 40, 37",
    }),
    "lake": ("туманное озеро", {
        "accent": "156, 186, 196", "bg-color": "93, 98, 99", "bg-color-mobile": "93, 98, 99",
        "bg-zoom": "1", "bg-dim": ".5",
        "glass": "22, 24, 27", "text": "236, 238, 238", "text-2": "176, 180, 182", "text-3": "144, 148, 150",
        "time-empty": "34, 37, 40",
    }),
    "purple": ("фиолетовое небо", {
        "accent": "186, 122, 255", "bg-color": "64, 30, 66", "bg-color-mobile": "62, 32, 64",
        "bg-blur": "2px", "bg-dim": ".38", "glass": "30, 18, 40", "glass-blur": "8px",
        "text": "240, 236, 247", "text-2": "178, 168, 196",
    }),
}


def values(slug, ver):
    # с тегом версии, но без «@» (jsDelivr пишет тег через @, а Шикимори не показывает картинки с @ в адресе)
    cdn = f"https://raw.githubusercontent.com/Hikisey/shikimori-theme/{ver}/themes/{slug}"
    v = dict(BASE)
    v.update(THEMES[slug][1])
    v["bg-image"] = f'url("{cdn}/bg.webp")'
    v["bg-image-mobile"] = f'url("{cdn}/bg_m.webp")'
    v["profile-banner"] = f'url("{cdn}/banner.webp")'
    return v


def apply(s, v):
    for k, val in v.items():
        s, n = re.subn(r"(\n    --%s: )[^;]*;" % re.escape(k), lambda m: m.group(1) + val + ";", s, count=1)
        if n != 1:
            sys.exit(f"нет переменной --{k} в site.css")
    return s


def main():
    path = ROOT / "site.css"
    site = path.read_text(encoding="utf-8")
    ver = re.search(r"/(v\d+\.\d+\.\d+)/css/part_01\.css", site).group(1)
    # корневой site.css = тема по умолчанию
    site = apply(site, values(DEFAULT, ver))
    path.write_text(site, encoding="utf-8")
    print("site.css: палитра темы по умолчанию —", THEMES[DEFAULT][0])
    for slug, (name, _) in THEMES.items():
        s = apply(site, values(slug, ver))
        s = s.replace("/* shiki glass " + ver + " —", f"/* shiki glass {ver}, тема «{name}» —", 1)
        out = ROOT / "themes" / slug / "site.css"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(s, encoding="utf-8")
        print(out.relative_to(ROOT), len(s.encode()), "байт")


def readme():
    """Раздел README между <!-- themes:start --> и <!-- themes:end -->: на каждую тему заголовок, описание,
    скриншот (компьютер и телефон одной картинкой, всегда виден) и сворачиваемый блок с полным site.css."""
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    a, b = "<!-- themes:start -->", "<!-- themes:end -->"
    if a not in text or b not in text:
        return
    out = [a, ""]
    for slug in THEMES:
        name = THEMES[slug][0]
        desc, src = DESC[slug]
        if slug == DEFAULT:
            title = f"{name} (по умолчанию)"
            note = "Это обычный <code>site.css</code> из корня репозитория (раздел «Установка»)."
        else:
            title, note = name, ""
        css = (ROOT / "themes" / slug / "site.css").read_text(encoding="utf-8")
        out += [
            f"### {title}",
            "",
            f"{desc[0].upper() + desc[1:]} {note}".rstrip(),
            "",
            # компьютер и телефон — одной картинкой (tools/preview_pair.py): одинаковой высоты
            # и в одном масштабе и на компьютере, и в мобильном GitHub
            f'<img src="themes/{slug}/preview.webp" width="100%" alt="{name}: компьютер и телефон">',
            "",
            f"<sub>Источник: {src}</sub>",
            "",
            "<details>",
            f"<summary>CSS-код темы «{name}»</summary>",
            "",
            "```css",
            css.rstrip("\n"),
            "```",
            "",
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
