#!/usr/bin/env python3
"""Design(캔버스) 유형용 상세페이지 와이어프레임 생성기.

사용법: python build_canvas.py spec.json <출력 루트 폴더>
  - spec.json은 build_wireframe.py와 같은 형식(sections[{type, bg, blocks:[{m: ...}]}])
  - <루트>/project/ 아래에 아트보드(.dc.html)와 canvas.json을 만든다.
  - 결과 규칙: 가로 860 · 세로 1200 이상 · 여백 40 · 글자 22~82px · 보드 간격 0 · 이미지는 검은 박스
  - 만든 파일은 Design 유형의 절차대로 Artifact로 올린다(canvas.json은 마지막).
"""
import datetime
import random
import sys
from pathlib import Path
import json, html, re
E = html.escape
FF = "font-family:'Noto Sans KR',sans-serif"
FONT = '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;800&display=swap" rel="stylesheet">'
TONE = {"bg0": "#fff", "bg1": "#f1f1f1", "bg2": "#dcdcdc", "dark": "#222", "photo": "#111"}

def page(title, h, bgkey, body, bglabel=None, valign="top", bar=""):
    dark = bgkey in ("dark", "photo")
    if bgkey == "photo":
        just = "flex-start" if valign == "top" else "center"
        pad = "96px 40px 40px" if valign == "top" else "120px 40px 96px"
        root = (f"position:relative;width:860px;height:{h}px;box-sizing:border-box;background:#111;color:#fff;{FF};"
                f"display:flex;flex-direction:column;align-items:center;justify-content:{just};gap:28px;padding:{pad}")
        tag = f'<div style="position:absolute;left:0;bottom:0;width:860px">{bar}</div>' if bar else ""
        body = body + tag
    else:
        root = (f"width:860px;height:{h}px;box-sizing:border-box;background:{TONE[bgkey]};color:{'#fff' if dark else '#111'};{FF};"
                "display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:32px;padding:80px 40px")
        tag = ""
        body = body + (bar or "")
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{E(title)}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONT}
<style>
body{{margin:0}}
a{{color:inherit}}
</style>
</helmet>
<div style="{root}">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":860,"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
"""

# ---- 색 규칙 (대비 4.5:1 이상)
def fg(d): return "#fff" if d else "#111"
def mu(d): return "#e6e6e6" if d else "#555"
def bd(d): return "#e6e6e6" if d else "#333"
def hl(s, d):
    c = "rgba(255,255,255,.28)" if d else "#cdcdcd"
    return re.sub(r"\*\*(.+?)\*\*", lambda m: f'<span style="background:{c};padding:0 8px">{m.group(1)}</span>', E(s))

# ---- 모듈
def eyebrow(t, d=False):
    return (f'<div style="font-size:22px;font-weight:700;letter-spacing:.06em;border:2px solid {fg(d)};border-radius:999px;'
            f'padding:4px 22px;color:{fg(d)}">{E(t)}</div>')
def headline(t, d=False, size=64):
    return (f'<h2 style="margin:0;width:100%;text-align:center;font-size:{size}px;line-height:1.25;font-weight:800;'
            f'color:{fg(d)};white-space:pre-line">{hl(t, d)}</h2>')
def sub(t, d=False):
    return f'<p style="margin:0;width:100%;text-align:center;font-size:32px;line-height:1.5;color:{mu(d)};white-space:pre-line">{E(t)}</p>'
def body(t, d=False, center=False):
    return (f'<p style="margin:0;width:100%;font-size:26px;line-height:1.6;color:{bd(d)};white-space:pre-line;'
            f'text-align:{"center" if center else "left"}">{E(t)}</p>')
def foot(t, d=False):
    return f'<p style="margin:0;width:100%;text-align:center;font-size:22px;line-height:1.5;color:{mu(d)}">{E(t)}</p>'
def box(label, h, w="100%", d=False):
    ol = "outline:2px solid #fff;outline-offset:-2px;" if d else ""
    return (f'<div style="width:{w};height:{h}px;background:#111;color:#fff;{ol}display:flex;align-items:center;justify-content:center;'
            f'text-align:center;padding:24px;box-sizing:border-box;font-size:22px;line-height:1.45;flex-shrink:0"></div>')   # 이미지 자리는 설명 글자 없는 검은 박스
def image(label, ratio="16:9", d=False):
    a, b = [float(x) for x in ratio.split(":")]
    return box(f"[IMG] {label} · {ratio}", round(780 * b / a), "780px", d)
def gif(label, d=False):
    return box(f"[GIF] {label} · 16:9", 439, "780px", d)
def badges(items, d=False, size=220):
    fs = 26 if size >= 220 else 24
    out = "".join(
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:#fff;color:#111;border:3px solid {"#fff" if d else "#111"};'
        f'display:flex;align-items:center;justify-content:center;text-align:center;font-size:{fs}px;font-weight:800;line-height:1.3;'
        f'padding:16px;box-sizing:border-box;white-space:pre-line">{E(i)}</div>' for i in items)
    return f'<div style="display:flex;gap:20px;justify-content:center">{out}</div>'
def ico(sz=96):
    return (f'<div style="width:{sz}px;height:{sz}px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;'
            f'font-size:22px;flex-shrink:0">ICON</div>')
def icon_row(items, d=False):
    n = len(items)
    cols = n if n <= 4 else (3 if n in (5, 6) else 4)
    isz = 150 if cols >= 4 else (200 if cols == 3 else 240)
    out = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px">{ico(isz)}'
                  f'<div style="font-size:22px;font-weight:700;text-align:center;color:{fg(d)}">{E(i)}</div></div>' for i in items)
    return f'<div style="width:100%;display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:16px;justify-items:center">{out}</div>'
def icon_cards(items, d=False):
    out = ""
    for lab, t in items:
        out += ('<div style="width:100%;box-sizing:border-box;border:2px solid #bbb;background:#fff;padding:28px;display:flex;gap:24px;align-items:center">'
                f'{ico()}<div style="display:flex;flex-direction:column;gap:8px;min-width:0"><div style="font-size:22px;font-weight:700;letter-spacing:.04em;color:#555">{E(lab)}</div>'
                f'<div style="font-size:26px;line-height:1.6;color:#333">{E(t)}</div></div></div>')
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:20px">{out}</div>'
def bubbles(items):
    out = ""
    for i, t in enumerate(items):
        side = "flex-end" if i % 2 else "flex-start"
        rad = "border-bottom-right-radius:8px" if i % 2 else "border-bottom-left-radius:8px"
        out += (f'<div style="max-width:82%;background:{"#c4c4c4" if i % 2 else "#dcdcdc"};color:#111;border-radius:40px;{rad};padding:26px 36px;'
                f'font-size:26px;line-height:1.5;align-self:{side};box-sizing:border-box">{E(t)}</div>')
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:20px">{out}</div>'
def photo_grid(cols, items, ratio, d=False):
    w = (780 - 16 * (cols - 1)) // cols
    a, b = [float(x) for x in ratio.split(":")]
    h = round(w * b / a)
    out = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px">{box(f"[IMG] {l} · {ratio}", h, "100%", d)}'
                  f'<div style="font-size:22px;line-height:1.4;text-align:center;color:{mu(d)}">{E(c)}</div></div>' for l, c in items)
    return f'<div style="width:100%;display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:16px">{out}</div>'
def callout(label, items):
    pos = ["left:16px;top:60px", "right:16px;top:60px", "left:16px;bottom:60px", "right:16px;bottom:60px"]
    pills = "".join(f'<div style="position:absolute;{pos[i]};background:#fff;color:#111;border:3px solid #111;border-radius:999px;padding:10px 22px;font-size:24px;font-weight:700">{E(t)}</div>'
                    for i, t in enumerate(items[:4]))
    return (f'<div style="position:relative;width:780px;height:780px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;'
            f'font-size:22px;flex-shrink:0">{pills}</div>')
def tip(t, d=False):
    return (f'<div style="width:100%;box-sizing:border-box;border:3px dashed {"#ccc" if d else "#666"};padding:28px;display:flex;flex-direction:column;gap:12px">'
            f'<div style="align-self:flex-start;font-size:22px;font-weight:700;border:2px solid {fg(d)};border-radius:999px;padding:2px 14px;color:{fg(d)}">TIP!</div>'
            f'<div style="font-size:26px;line-height:1.6;color:{bd(d)}">{E(t)}</div></div>')
def steps(items):
    out = ""
    for i, (t, x) in enumerate(items, 1):
        out += ('<div style="width:100%;display:flex;gap:24px;align-items:flex-start;border-bottom:2px solid #ddd;padding-bottom:24px">'
                f'{box(f"[IMG] STEP {i} 사용 컷 · 4:3", 285, "380px")}<div style="display:flex;flex-direction:column;gap:10px;min-width:0">'
                f'<div style="align-self:flex-start;font-size:22px;font-weight:700;border:2px solid #111;border-radius:999px;padding:2px 14px">STEP {i}</div>'
                f'<div style="font-size:32px;font-weight:700;line-height:1.35;color:#111">{E(t)}</div>'
                f'<div style="font-size:26px;line-height:1.6;color:#333">{E(x)}</div></div></div>')
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:24px">{out}</div>'
def vs(ltag, ltxt, rtag, rtxt, d=False):
    def card(tag, t, strong):
        if d:
            st = f"border:2px solid #fff;background:{'rgba(255,255,255,.2)' if strong else 'rgba(255,255,255,.08)'};color:#fff"
        else:
            st = "border:2px solid #111;background:#ececec;color:#111" if strong else "border:2px solid #bbb;background:#fff;color:#111"
        return (f'<div style="width:100%;box-sizing:border-box;{st};padding:28px;display:flex;flex-direction:column;gap:12px">'
                f'<div style="font-size:22px;font-weight:700;color:{mu(d) if not strong or d else "#555"}">{E(tag)}</div>'
                f'<div style="font-size:32px;font-weight:700;line-height:1.4;white-space:pre-line">{E(t)}</div></div>')
    return (f'<div style="width:100%;display:flex;flex-direction:column;gap:16px;align-items:center">{card(ltag, ltxt, False)}'
            f'<div aria-hidden="true" style="font-size:48px;line-height:1;color:{mu(d)}">↓</div>{card(rtag, rtxt, True)}</div>')
def reviews(items):
    out = "".join('<div style="width:100%;box-sizing:border-box;border:2px solid #bbb;background:#fff;padding:28px;display:flex;flex-direction:column;gap:10px">'
                  '<div style="font-size:22px;color:#555">★★★★★ · 구매 고객</div>'
                  f'<div style="font-size:32px;font-weight:700;line-height:1.35;color:#111">{E(t)}</div>'
                  f'<div style="font-size:26px;line-height:1.6;color:#333">{E(x)}</div></div>' for t, x in items)
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:20px">{out}</div>'
def checklist(items):
    out = "".join('<div style="width:100%;box-sizing:border-box;display:flex;align-items:center;gap:20px;background:#fff;border:2px solid #bbb;border-radius:999px;padding:18px 32px">'
                  '<div style="width:56px;height:56px;border-radius:50%;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-size:28px;flex-shrink:0">✓</div>'
                  f'<div style="font-size:26px;line-height:1.5;color:#111">{E(t)}</div></div>' for t in items)
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:16px">{out}</div>'
def cert_grid(n, d=False):
    return photo_grid(3, [(f"인증서·특허 {i + 1}", f"인증 자료 {i + 1}") for i in range(n)], "3:4", d)
def spec_table(rows):
    out = "".join(f'<div style="display:grid;grid-template-columns:220px minmax(0,1fr);gap:16px;border-bottom:2px solid #ddd;padding:18px 0;font-size:26px;line-height:1.5">'
                  f'<div style="font-weight:700;color:#111">{E(k)}</div><div style="color:#333">{E(v)}</div></div>' for k, v in rows)
    return f'<div style="width:100%;border-top:3px solid #111">{out}</div>'
def notice_rows(items):
    out = "".join('<div style="display:flex;gap:24px;align-items:center;border-bottom:2px solid #ddd;padding-bottom:20px">'
                  f'{ico()}<div style="display:flex;flex-direction:column;gap:8px;min-width:0"><div style="font-size:22px;font-weight:700;color:#111">{E(t)}</div>'
                  f'<div style="font-size:26px;line-height:1.6;color:#333">{E(x)}</div></div></div>' for t, x in items)
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:20px">{out}</div>'
def qa(items):
    out = "".join('<div style="border-bottom:2px solid #bbb;padding-bottom:20px;display:flex;flex-direction:column;gap:10px">'
                  f'<div style="font-size:32px;font-weight:700;line-height:1.35;color:#111">Q. {E(q)}</div>'
                  f'<div style="font-size:26px;line-height:1.6;color:#555">{E(a)}</div></div>' for q, a in items)
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:20px">{out}</div>'
def claim(t, items=None, d=True):
    ic = badges(items, d, 170) if items else ""
    return (f'<div style="width:100%;text-align:center;font-size:82px;font-weight:800;line-height:1.25;color:{fg(d)};white-space:pre-line">{E(t)}</div>{ic}')
def band(t, invert=False):
    st = "background:#fff;color:#111" if invert else "background:#111;color:#fff"
    return f'<div style="width:860px;box-sizing:border-box;{st};text-align:center;font-size:32px;font-weight:700;padding:36px 0;flex-shrink:0">{E(t)}</div>'


def check_grid(items, d=False):
    out = "".join('<div style="box-sizing:border-box;border:2px solid #bbb;background:#fff;padding:24px;display:flex;flex-direction:column;align-items:center;gap:12px">'
                  f'{ico()}<div style="font-size:26px;line-height:1.5;text-align:center;color:#111">{E(t)}</div></div>' for t in items)
    return f'<div style="width:100%;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px">{out}</div>'
def chart(bars, badge=None, note=None, d=False):
    hs = []
    for b in bars:
        m = re.search(r"\d+(?:\.\d+)?", str(b.get("value", "")))
        hs.append((float(m.group()) if m else 50, b))
    cols = "".join(f'<div style="display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:10px;width:200px;height:100%">'
                   f'<div style="width:100%;height:{int(v * 3.2)}px;background:{"#111" if b.get("hot") else "#bdbdbd"}"></div>'
                   f'<div style="font-size:22px;font-weight:700;color:{fg(d)}">{E(b.get("label", ""))}</div></div>' for v, b in hs)
    bd_ = (f'<div style="position:absolute;right:0;top:0;width:170px;height:170px;border-radius:50%;background:#fff;color:#111;border:3px solid #111;'
           f'display:flex;align-items:center;justify-content:center;text-align:center;font-size:24px;font-weight:800;padding:16px;box-sizing:border-box">{E(badge)}</div>') if badge else ""
    return (f'<div style="position:relative;width:100%;height:420px"><div style="display:flex;align-items:flex-end;justify-content:center;gap:40px;height:380px;'
            f'border-bottom:3px solid {fg(d)}">{cols}</div>{bd_}</div>' + foot(note or "", d) + foot("막대 높이는 샘플 비율입니다", d))
def percent_bars(items, d=False):
    out = ""
    for it in items:
        m = re.search(r"\d+(?:\.\d+)?", str(it.get("value", "")))
        v = max(0, min(100, float(m.group()))) if m else 80
        out += (f'<div style="width:100%;display:flex;flex-direction:column;gap:6px"><div style="font-size:26px;line-height:1.5;color:{bd(d)}">{E(it.get("label", ""))}</div>'
                f'<div style="height:28px;background:{"#444" if d else "#dcdcdc"}"><div style="width:{v}%;height:100%;background:{"#fff" if d else "#111"}"></div></div>'
                f'<div style="font-size:22px;color:{mu(d)}">{E(it.get("value") or "")}</div></div>')
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:20px">{out}</div>'
def lineup(items, d=False):
    return photo_grid(3, [(i, i) for i in items], "3:4", d)

# ======================= 레이아웃 모듈 (가로 분할·교차·이미지 위 글자 등) =======================
def _ratio_h(w, ratio):
    a, b = [float(x) for x in str(ratio).split(":")]
    return round(w * b / a)

def _split_row(side, label, ratio, eyebrow_t, title_t, text_t, items, d=False, iw=380):
    h = _ratio_h(iw, ratio)
    img_html = box(f"[IMG] {label} · {ratio}", h, f"{iw}px", d)
    col = ""
    if eyebrow_t:
        col += (f'<div style="align-self:flex-start;font-size:22px;font-weight:700;letter-spacing:.06em;border:2px solid {fg(d)};'
                f'border-radius:999px;padding:2px 14px;color:{fg(d)}">{E(eyebrow_t)}</div>')
    if title_t:
        col += (f'<div style="font-size:40px;font-weight:800;line-height:1.3;color:{fg(d)};white-space:pre-line">{hl(title_t, d)}</div>')
    if text_t:
        col += f'<div style="font-size:26px;line-height:1.6;color:{bd(d)};white-space:pre-line">{E(text_t)}</div>'
    for it in items or []:
        col += (f'<div style="display:flex;gap:12px;font-size:26px;line-height:1.5;color:{bd(d)}">'
                f'<span style="flex-shrink:0;width:12px;height:12px;background:{fg(d)};margin-top:12px"></span><span>{E(it)}</span></div>')
    direction = "row-reverse" if side == "right" else "row"
    return (f'<div style="width:100%;display:flex;flex-direction:{direction};gap:28px;align-items:center">{img_html}'
            f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:16px">{col}</div></div>')

def split(label, ratio="3:4", side="left", eyebrow_t=None, title_t=None, text_t=None, items=None, d=False):
    return _split_row(side, label, ratio, eyebrow_t, title_t, text_t, items, d)

def zigzag(items, d=False):
    rows = ""
    for i, it in enumerate(items):
        rows += _split_row("left" if i % 2 == 0 else "right", it.get("label", "이미지"), it.get("ratio", "3:4"),
                           it.get("eyebrow"), it.get("title"), it.get("text"), it.get("items"), d)
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:48px">{rows}</div>'

def overlay(label, ratio="1:1", title_t=None, sub_t=None, align="center", valign="middle", size=64, d=True):
    h = _ratio_h(780, ratio)
    just = {"top": "flex-start", "middle": "center", "bottom": "flex-end"}.get(valign, "center")
    ai = {"left": "flex-start", "center": "center", "right": "flex-end"}.get(align, "center")
    inner = ""
    if title_t:
        inner += (f'<div style="font-size:{size}px;font-weight:800;line-height:1.25;color:#fff;text-align:{align};white-space:pre-line">{hl(title_t, True)}</div>')
    if sub_t:
        inner += f'<div style="font-size:32px;line-height:1.5;color:#e6e6e6;text-align:{align};white-space:pre-line">{E(sub_t)}</div>'
    return (f'<div style="position:relative;width:780px;height:{h}px;background:#111;display:flex;flex-direction:column;justify-content:{just};'
            f'align-items:{ai};gap:16px;padding:56px 40px;box-sizing:border-box;flex-shrink:0">'
            f'{inner}</div>')

def circle_row(items, d=False):
    out = ""
    for it in items:
        out += ('<div style="width:240px;display:flex;flex-direction:column;align-items:center;gap:12px">'
                f'<div style="width:240px;height:240px;border-radius:50%;background:#111;color:#fff;{"border:3px solid #fff;" if d else ""}display:flex;align-items:center;justify-content:center;'
                f'text-align:center;padding:24px;box-sizing:border-box;font-size:22px;line-height:1.4"></div>'
                f'<div style="font-size:32px;font-weight:700;line-height:1.3;color:{fg(d)};text-align:center">{E(it.get("title", ""))}</div>'
                f'<div style="font-size:22px;line-height:1.5;color:{mu(d)};text-align:center">{E(it.get("text", ""))}</div></div>')
    return f'<div style="width:100%;display:flex;gap:30px;justify-content:center">{out}</div>'

def stat_rows(items, d=False):
    out = ""
    for it in items:
        out += (f'<div style="display:flex;gap:24px;align-items:flex-start;border-top:3px solid {fg(d)};padding:28px 0">'
                f'<div style="width:380px;flex-shrink:0;font-size:48px;font-weight:800;line-height:1.25;color:{fg(d)};white-space:pre-line">{E(it.get("claim", ""))}</div>'
                f'<div style="flex:1;min-width:0;font-size:22px;line-height:1.5;color:{mu(d)}">{E(it.get("data", ""))}</div></div>')
    return f'<div style="width:100%;border-bottom:3px solid {fg(d)}">{out}</div>'

def timeline(items, d=False):
    out = ""
    for i, it in enumerate(items, 1):
        out += (f'<div style="position:relative;display:flex;flex-direction:column;gap:8px">'
                f'<div style="position:absolute;left:-64px;top:0;width:44px;height:44px;border-radius:50%;background:{fg(d)};color:{"#111" if d else "#fff"};'
                f'display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700">{i}</div>'
                f'<div style="font-size:32px;font-weight:700;line-height:1.35;color:{fg(d)}">{E(it.get("title", ""))}</div>'
                f'<div style="font-size:26px;line-height:1.6;color:{bd(d)}">{E(it.get("text", ""))}</div></div>')
    return (f'<div style="position:relative;width:100%;box-sizing:border-box;padding-left:64px;display:flex;flex-direction:column;gap:40px">'
            f'<div style="position:absolute;left:20px;top:22px;bottom:30px;width:4px;background:{fg(d)}"></div>{out}</div>')

def numbered_list(items, d=False):
    out = ""
    for i, it in enumerate(items, 1):
        out += (f'<div style="display:flex;gap:28px;align-items:flex-start;border-bottom:2px solid {"#555" if d else "#ddd"};padding:28px 0">'
                f'<div style="width:110px;flex-shrink:0;font-size:64px;font-weight:800;line-height:1;color:{fg(d)}">{i:02d}</div>'
                f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:8px"><div style="font-size:32px;font-weight:700;line-height:1.35;color:{fg(d)}">{E(it.get("title", ""))}</div>'
                f'<div style="font-size:26px;line-height:1.6;color:{bd(d)}">{E(it.get("text", ""))}</div></div></div>')
    return f'<div style="width:100%;border-top:3px solid {fg(d)}">{out}</div>'

def ticker(items, invert=False):
    st = "background:#fff;color:#111;border-top:3px solid #111;border-bottom:3px solid #111" if invert else "background:#111;color:#fff"
    txt = "   ·   ".join(items)
    return (f'<div style="width:860px;box-sizing:border-box;{st};text-align:center;font-size:32px;font-weight:700;line-height:1.4;padding:28px 40px;flex-shrink:0">{E(txt)}</div>')

def quote(text_t, who=None, d=False):
    w = f'<div style="font-size:22px;color:{mu(d)};text-align:center">{E(who)}</div>' if who else ""
    return (f'<div style="width:100%;display:flex;flex-direction:column;align-items:center;gap:12px">'
            f'<div style="font-size:82px;font-weight:800;line-height:.8;color:{fg(d)}">“</div>'
            f'<div style="font-size:48px;font-weight:800;line-height:1.3;text-align:center;color:{fg(d)};white-space:pre-line">{E(text_t)}</div>{w}</div>')

def index_mark(text_t, d=False):
    return (f'<div style="width:100%;font-size:82px;font-weight:800;line-height:1;color:{fg(d)};border-bottom:4px solid {fg(d)};padding-bottom:12px">{E(text_t)}</div>')

def two_col(items, d=False):
    out = "".join(f'<div style="border-top:3px solid {fg(d)};padding-top:16px;display:flex;flex-direction:column;gap:8px">'
                  f'<div style="font-size:32px;font-weight:700;line-height:1.35;color:{fg(d)}">{E(it.get("title", ""))}</div>'
                  f'<div style="font-size:26px;line-height:1.6;color:{bd(d)}">{E(it.get("text", ""))}</div></div>' for it in items[:2])
    return f'<div style="width:100%;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px">{out}</div>'


# ======================= 항목 개수에 따라 레이아웃이 바뀌는 모듈 =======================
def _fmedia(it, mode, w, num=None, d=False, ratio="4:3"):
    """카드 위쪽 미디어: icon(검은 아이콘 박스) / image(검은 이미지 박스) / number(큰 번호)"""
    if mode == "image" or it.get("label"):
        h = _ratio_h(w, ratio)
        return box(f"[IMG] {it.get('label', '이미지')} · {ratio}", h, "100%", d)
    if mode == "number":
        return f'<div style="font-size:64px;font-weight:800;line-height:1;color:{fg(d)}">{num:02d}</div>'
    return ico(96)

def _fcard(it, i, w, mode, compact, d=False, ratio="4:3"):
    pad = 16 if compact else 24
    tsz, xsz = (28, 22) if compact else (32, 26)
    st = ("border:2px solid #666;background:#2e2e2e;color:#fff" if d else "border:2px solid #bbb;background:#fff;color:#111")
    return (f'<div style="box-sizing:border-box;{st};padding:{pad}px;display:flex;flex-direction:column;gap:12px;min-width:0">'
            f'{_fmedia(it, mode, w - 2 * pad - 4, i + 1, d, ratio)}'
            f'<div style="font-size:{tsz}px;font-weight:700;line-height:1.3;color:{"#fff" if d else "#111"};white-space:pre-line">{E(it.get("title", ""))}</div>'
            f'<div style="font-size:{xsz}px;line-height:1.55;color:{"#e6e6e6" if d else "#333"};white-space:pre-line">{E(it.get("text", ""))}</div></div>')

def _flead(it, mode, d=False):
    st = ("border:2px solid #fff;background:#2e2e2e;color:#fff" if d else "border:2px solid #111;background:#ececec;color:#111")
    if mode == "image" or it.get("label"):
        m = box(f"[IMG] {it.get('label', '이미지')} · 1:1", 240, "240px", d)
    else:
        m = ico(120)
    return (f'<div style="width:100%;box-sizing:border-box;{st};padding:24px;display:flex;gap:24px;align-items:center">{m}'
            f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:10px">'
            f'<div style="font-size:40px;font-weight:800;line-height:1.3;color:{"#fff" if d else "#111"};white-space:pre-line">{E(it.get("title", ""))}</div>'
            f'<div style="font-size:26px;line-height:1.6;color:{"#e6e6e6" if d else "#333"};white-space:pre-line">{E(it.get("text", ""))}</div></div></div>')

def _grid(cards, cols):
    return f'<div style="width:100%;display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:16px;align-items:stretch">{"".join(cards)}</div>'

def pick_feature_layout(n, avg_len):
    """항목 개수와 글 길이로 레이아웃을 고른다."""
    if n <= 1: return "lead"
    if n == 2: return "duo"
    if n == 3: return "trio" if avg_len <= 30 else "rows"
    if n == 4: return "grid2"
    if n == 5: return "lead2"
    if n == 6: return "grid3" if avg_len <= 30 else "grid2"
    if n == 7: return "lead3"
    if n == 8: return "grid2"
    return "rows"

def _avg_len(items):
    return sum(len(x.get("text", "")) for x in items) / max(1, len(items))

def feature_set(items, mode=None, layout=None, d=False):
    items = [({"title": x} if isinstance(x, str) else x) for x in (items or [{}, {}, {}])]
    n = len(items)
    lay = layout or pick_feature_layout(n, _avg_len(items))
    mode = mode or ("image" if n <= 3 else "icon")   # 항목이 적을수록 큰 사진으로 채운다
    if lay == "lead": return _flead(items[0], mode, d)
    if lay == "duo": return _grid([_fcard(x, i, 382, mode, False, d, "3:4") for i, x in enumerate(items)], 2)
    if lay == "trio": return _grid([_fcard(x, i, 249, mode, True, d, "3:4") for i, x in enumerate(items)], 3)
    if lay == "grid2": return _grid([_fcard(x, i, 382, mode, False, d) for i, x in enumerate(items)], 2)
    if lay == "grid3": return _grid([_fcard(x, i, 249, mode, True, d) for i, x in enumerate(items)], 3)
    if lay in ("lead2", "lead3"):
        cols = 2 if lay == "lead2" else 3
        w = 382 if cols == 2 else 249
        rest = [_fcard(x, i + 1, w, mode, cols == 3, d) for i, x in enumerate(items[1:])]
        return f'<div style="width:100%;display:flex;flex-direction:column;gap:16px">{_flead(items[0], mode, d)}{_grid(rest, cols)}</div>'
    # rows: 번호 리스트
    return numbered_list([{"title": x.get("title", ""), "text": x.get("text", "")} for x in items], d)

def _est_feature(items, mode, layout):
    items = [({"title": x} if isinstance(x, str) else x) for x in (items or [{}, {}, {}])]
    n = len(items)
    lay = layout or pick_feature_layout(n, _avg_len(items))
    mode = mode or ("image" if n <= 3 else "icon")
    def card_h(x, w, compact):
        pad = 16 if compact else 24
        inner = w - 2 * pad - 4
        ratio = "3:4" if lay in ("duo", "trio") else "4:3"
        media = _ratio_h(inner, ratio) if (mode == "image" or x.get("label")) else (64 if mode == "number" else 96)
        tl = lines(x.get("title", ""), 6 if compact else 11)
        xl = lines(x.get("text", ""), 8 if compact else 12)
        return 2 * pad + media + 12 + (36 if compact else 43) * tl + 12 + (34 if compact else 42) * xl + 8
    def lead_h(x):
        return 48 + max(240 if (mode == "image" or x.get("label")) else 120, 52 * lines(x.get("title", ""), 12) + 42 * lines(x.get("text", ""), 14) + 10)
    def grid_h(xs, cols, w, compact):
        rows = -(-len(xs) // cols)
        tot = 0
        for r in range(rows):
            tot += max(card_h(x, w, compact) for x in xs[r * cols:(r + 1) * cols])
        return tot + 16 * (rows - 1)
    if lay == "lead": return lead_h(items[0])
    if lay == "duo": return grid_h(items, 2, 382, False)
    if lay == "trio": return grid_h(items, 3, 249, True)
    if lay == "grid2": return grid_h(items, 2, 382, False)
    if lay == "grid3": return grid_h(items, 3, 249, True)
    if lay == "lead2": return lead_h(items[0]) + 16 + grid_h(items[1:], 2, 382, False)
    if lay == "lead3": return lead_h(items[0]) + 16 + grid_h(items[1:], 3, 249, True)
    return sum(max(80, 43 * lines(x.get("title", ""), 16) + 42 * lines(x.get("text", ""), 18) + 8) + 58 for x in items) + 10

def _auto_cols(n):
    return 1 if n <= 1 else (3 if n in (3, 6, 9) else 2)


# ======================= 비주얼 섹션 구성 요소: 로고 + 하단 픽토그램 바 =======================
def logo(text_t="LOGO", d=True):
    return (f'<div style="width:96px;height:96px;border:3px solid {fg(d)};border-radius:20px;display:flex;align-items:center;justify-content:center;'
            f'font-size:22px;font-weight:700;color:{fg(d)};flex-shrink:0">{E(text_t)}</div>')

def pictogram_bar(items):
    """하단 픽토그램 바: 칸 수 = 주요 특징 개수. 6칸까지 한 줄, 7~8칸은 4칸씩 두 줄."""
    items = [({"label": x} if isinstance(x, str) else x) for x in (items or [{}, {}, {}])]
    n = len(items)
    per = n if n <= 6 else 4
    rows = [items[i:i + per] for i in range(0, n, per)]
    out = ""
    for ri, row in enumerate(rows):
        cells = ""
        for ci, it in enumerate(row):
            line = "border-left:2px solid #bbb;" if ci else ""
            cells += (f'<div style="flex:1;min-width:0;box-sizing:border-box;{line}padding:24px 6px;display:flex;flex-direction:column;align-items:center;gap:10px">'
                      f'<div style="width:64px;height:64px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-size:22px">ICON</div>'
                      f'<div style="font-size:22px;line-height:1.35;color:#555;text-align:center">{E(it.get("label", ""))}</div>'
                      f'<div style="font-size:22px;font-weight:700;line-height:1.35;color:#111;text-align:center">{E(it.get("value", ""))}</div></div>')
        sep = "border-top:2px solid #bbb;" if ri else ""
        out += f'<div style="display:flex;width:860px;{sep}">{cells}</div>'
    return f'<div style="width:860px;background:#fff;color:#111">{out}</div>'

def _est_bar(items):
    n = len(items or [0] * 3); per = n if n <= 6 else 4
    return -(-n // per) * 190

# ======================= 빈칸·자리표시 검사 =======================
PH_RE = re.compile(r"\[[^\[\]]{1,40}\]")
REQ_TEXT = {"headline": ["text"], "sub": ["text"], "body": ["text"], "footnote": ["text"], "quote": ["text"], "tip": ["text"],
            "eyebrow": ["text"], "claim": ["text"], "cta_band": ["text"]}
REQ_ITEMS = {"icon_cards": ["label", "text"], "steps": ["title", "text"], "timeline": ["title", "text"], "numbered_list": ["title", "text"],
             "notice_rows": ["title", "text"], "two_col": ["title", "text"], "reviews": ["title", "text"], "feature_set": ["title", "text"],
             "features": ["title", "text"], "stat_rows": ["claim", "data"], "qa": ["q", "a"], "circle_row": ["title", "text"],
             "zigzag": ["title", "text"], "entries": ["title", "text"], "showcase": ["title", "text"], "pictogram_bar": ["label", "value"], "photo_grid": ["caption"]}
REQ_LIST = ["icon_row", "bubbles", "checklist", "badges", "ticker", "lineup"]

def validate(spec):
    """모든 글자 자리는 문장으로 채워야 한다. 대괄호 자리표시나 빈 텍스트를 찾아 목록으로 돌려준다."""
    warns = []
    def walk(v, path):
        if isinstance(v, str):
            if PH_RE.search(v): warns.append(f"{path}: 자리표시 {PH_RE.findall(v)}")
        elif isinstance(v, dict):
            for k, x in v.items(): walk(x, f"{path}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v): walk(x, f"{path}[{i}]")
    for si, sec in enumerate(spec.get("sections") or [], 1):
        for bi, b in enumerate(sec.get("blocks") or [], 1):
            m = b.get("m"); where = f"P{si} {sec.get('type', '')} 블록{bi}({m})"
            walk({k: v for k, v in b.items() if k != "label"}, where)
            for key in REQ_TEXT.get(m, []):
                if not str(b.get(key, "")).strip(): warns.append(f"{where}: '{key}' 텍스트가 비어 있음")
            if m in REQ_ITEMS:
                its = b.get("items") or []
                if not its: warns.append(f"{where}: items가 비어 있음")
                for ii, it in enumerate(its, 1):
                    for key in REQ_ITEMS[m]:
                        if not (isinstance(it, dict) and str(it.get(key, "")).strip()): warns.append(f"{where}: 항목{ii}의 '{key}'가 비어 있음")
            if m in REQ_LIST and not [x for x in (b.get("items") or []) if str(x).strip()]: warns.append(f"{where}: items가 비어 있음")
            if m == "spec_table":
                for ri, row in enumerate(b.get("rows") or [], 1):
                    if len(row) < 2 or not str(row[1]).strip(): warns.append(f"{where}: {ri}행 값이 비어 있음")
            if m in ("split", "overlay") and not (b.get("title") or b.get("text") or b.get("sub")): warns.append(f"{where}: 글이 없음")
    return warns

# ======================= 무작위 레이아웃 선택: entries 모듈 =======================
# 내용(항목)은 한 번만 쓰고, 레이아웃 패턴은 생성할 때마다 무작위로 정한다.
PATTERN_NAME = {"cards": "카드 격자", "zigzag": "좌우 교차", "timeline": "세로 타임라인", "numbered": "큰 번호 리스트",
                "circles": "원형 사진", "datarows": "데이터 행", "photogrid": "사진 그리드", "splitlist": "가로 분할 + 목록",
                "duo": "2열 대비", "checklist": "체크 목록", "overlaycards": "이미지 위 글자 + 카드"}
PATTERNS = list(PATTERN_NAME)

def _applicable(p, n, kind, avg, b):
    if p == "cards": return 2 <= n <= 8
    if p == "zigzag": return 2 <= n <= 4
    if p == "timeline": return 2 <= n <= 5 and kind in ("steps", "features", "reasons")
    if p == "numbered": return 2 <= n <= 6
    if p == "circles": return n == 3
    if p == "datarows": return 2 <= n <= 5 and kind in ("features", "prices", "options", "reasons")
    if p == "photogrid": return 2 <= n <= 6
    if p == "splitlist": return 2 <= n <= 5
    if p == "duo": return n == 2
    if p == "checklist": return 3 <= n <= 6 and avg <= 34 and kind in ("features", "reasons", "options")
    if p == "overlaycards": return 2 <= n <= 4 and bool(b.get("lead_title"))
    return False

def expand_entries(b, rng, used, last):
    """entries 블록을 구체 모듈 목록으로 바꾼다. 돌려주는 값: (패턴, 블록 목록)"""
    items = [({"title": x} if isinstance(x, str) else dict(x)) for x in (b.get("items") or [])]
    n = len(items); kind = b.get("kind", "features")
    avg = sum(len(i.get("text", "")) for i in items) / max(1, n)
    allow = b.get("allow") or PATTERNS
    cand = [x for x in allow if x in PATTERN_NAME and _applicable(x, n, kind, avg, b)] or [x for x in PATTERNS if _applicable(x, n, kind, avg, b)] or ["cards"]
    pinned = b.get("pattern") if b.get("pattern") in PATTERN_NAME else None
    pref = [x for x in cand if x != last and x not in used] or [x for x in cand if x != last] or cand
    pat = pinned or rng.choice(pref)
    lab = lambda i: i.get("label") or i.get("title", "이미지")
    if pat == "cards":
        blocks = [{"m": "feature_set", "items": items, "style": rng.choice([None, None, "icon"])}]
    elif pat == "zigzag":
        blocks = [{"m": "zigzag", "items": [{"label": lab(i), "ratio": rng.choice(["3:4", "1:1"]), "title": i.get("title", ""), "text": i.get("text", ""), "items": i.get("points")} for i in items]}]
    elif pat == "timeline":
        blocks = [{"m": "timeline", "items": [{"title": i.get("title", ""), "text": i.get("text", "")} for i in items]}]
    elif pat == "numbered":
        blocks = [{"m": "numbered_list", "items": [{"title": i.get("title", ""), "text": i.get("text", "")} for i in items]}]
    elif pat == "circles":
        blocks = [{"m": "circle_row", "items": [{"label": lab(i), "title": i.get("title", ""), "text": i.get("text", "")} for i in items]}]
    elif pat == "datarows":
        blocks = [{"m": "stat_rows", "items": [{"claim": i.get("title", ""), "data": i.get("text", "")} for i in items]}]
    elif pat == "photogrid":
        blocks = [{"m": "photo_grid", "ratio": rng.choice(["1:1", "3:4"]), "items": [{"label": lab(i), "caption": i.get("title", "") + (" · " + i["text"] if i.get("text") else "")} for i in items]}]
    elif pat == "splitlist":
        blocks = [{"m": "split", "label": b.get("image_label") or lab(items[0]), "ratio": rng.choice(["3:4", "1:1"]), "side": rng.choice(["left", "right"]),
                   "title": b.get("lead_title"), "text": b.get("lead_text"),
                   "items": [i.get("title", "") + (" — " + i["text"] if i.get("text") else "") for i in items]}]
    elif pat == "duo":
        blocks = [{"m": "two_col", "items": [{"title": i.get("title", ""), "text": i.get("text", "")} for i in items]}]
    elif pat == "checklist":
        blocks = [{"m": "checklist", "items": [i.get("title", "") + (" — " + i["text"] if i.get("text") else "") for i in items]}]
    else:  # overlaycards
        blocks = [{"m": "overlay", "label": b.get("image_label") or lab(items[0]), "ratio": rng.choice(["4:5", "1:1"]), "title": b.get("lead_title"),
                   "sub": b.get("lead_text"), "size": "md", "align": "center", "valign": rng.choice(["middle", "bottom"])},
                  {"m": "feature_set", "items": items}]
    if b.get("lead_image"):
        li = {"m": "image", "label": b["lead_image"], "ratio": rng.choice(["3:2", "16:9"]), "bleed": True}
        blocks = [li] + blocks if rng.random() < 0.5 else blocks + [li]
    return pat, blocks

SIZE = {"xl": 82, "lg": 64, "md": 48}
ROW = {"hero": True, "brand": True}
VIS_TYPES = {"hero", "brand"}
LABEL = {"hero": "Hero", "trust": "Trust", "pain": "Pain", "cause": "Cause", "point": "Point", "proof": "Proof", "howto": "How-to",
         "review": "Review", "why": "Why", "brand": "Brand", "info": "Info", "notice": "Notice", "maker": "Maker", "offer": "Offer", "option": "Option", "compare": "Compare", "story": "Story", "section": "Section"}


def lines(t, per):
    return sum(max(1, -(-len(x) // per)) for x in str(t).split("\n"))


def render_block(b, d):
    m = b.get("m")
    g = b.get
    if m == "eyebrow": return eyebrow(g("text") or "POINT 01", d)
    if m == "headline": return headline(g("text") or "", d, SIZE.get(g("size", "lg"), 64))
    if m == "sub": return sub(g("text") or "", d)
    if m == "body": return body(g("text") or "", d)
    if m == "footnote": return foot(g("text") or "", d)
    if m == "image":
        if g("bleed"):
            h = _ratio_h(860, g("ratio", "16:9"))
            return box(("[GIF] " if g("gif") else "[IMG] ") + (g("label") or "이미지") + f" · {g('ratio', '16:9')} · 전체 폭", h, "860px", d)
        return gif(g("label") or "이미지", d) if g("gif") else image(g("label") or "이미지", g("ratio", "16:9"), d)
    if m == "badges": return badges(g("items") or ["[배지 입력]"] * 3, d)
    if m == "icon_row": return icon_row(g("items") or ["[특징]"] * 4, d)
    if m == "icon_cards": return icon_cards([(i.get("label", "LABEL"), i.get("text", "[문구 입력]")) for i in (g("items") or [{}] * 3)], d)
    if m == "check_grid": return check_grid(g("items") or ["[체크 포인트 입력]"] * 4, d)
    if m == "bubbles": return bubbles(g("items") or ["[고객 속마음 입력]"] * 4)
    if m == "photo_grid":
        cols = int(g("cols") or _auto_cols(len(g("items") or [0] * 4)))
        its = [((i.get("label") or "사진"), (i.get("caption") or "")) for i in (g("items") or [{}] * (cols * 2))]
        return photo_grid(cols, its, g("ratio", "1:1" if cols == 2 else "3:4"), d)
    if m == "chart": return chart(g("bars") or [{"label": "일반 제품", "value": 40}, {"label": "우리 제품", "value": 70, "hot": True}], g("badge"), g("note"), d)
    if m == "percent_bars": return percent_bars(g("items") or [{}] * 3, d)
    if m == "reviews": return reviews([(i.get("title", "[후기 제목 입력]"), i.get("text", "[실제 후기 입력]")) for i in (g("items") or [{}] * 3)])
    if m == "qa": return qa([(i.get("q", "[질문 입력]"), i.get("a", "[실제 답변 입력]")) for i in (g("items") or [{}] * 3)])
    if m == "spec_table": return spec_table(g("rows") or [["항목", "[실제 입력]"]] * 5)
    if m == "notice_rows": return notice_rows([(i.get("title", "안내"), i.get("text", "[실제 안내 입력]")) for i in (g("items") or [{}] * 3)])
    if m == "cert_grid": return cert_grid(int(g("n", 6)), d)
    if m == "callout": return callout(g("label") or "제품 도해 컷", g("items") or ["[특징 1]", "[특징 2]", "[특징 3]", "[특징 4]"])
    if m == "tip": return tip(g("text") or "", d)
    if m == "claim": return claim(g("text") or "", g("items"), d)
    if m == "checklist": return checklist(g("items") or ["[선택 이유 입력]"] * 5)
    if m == "lineup": return lineup(g("items") or ["[제품 1]", "[제품 2]", "[제품 3]"], d)
    if m == "steps": return steps([(i.get("title", "[단계 제목]"), i.get("text", "[설명 입력]")) for i in (g("items") or [{}] * 3)])
    if m == "vs":
        L, R = g("left", {}), g("right", {})
        return vs(L.get("tag", "흔한 생각"), L.get("text", "[흔한 생각 입력]"), R.get("tag", "새로운 생각"), R.get("text", "[새로운 생각 입력]"), d)
    if m == "cta_band": return band(g("text") or "지금 구매하기 ▸", d)
    if m in ("feature_set", "features"): return feature_set(g("items"), g("style"), g("layout"), d)
    if m == "logo": return logo(g("text") or "LOGO", d)
    if m == "pictogram_bar": return pictogram_bar(g("items"))
    if m == "split": return split(g("label") or "이미지", g("ratio", "3:4"), g("side", "left"), g("eyebrow"), g("title"), g("text"), g("items"), d)
    if m == "zigzag": return zigzag(g("items") or [{}, {}, {}], d)
    if m == "overlay": return overlay(g("label") or "이미지", g("ratio", "1:1"), g("title"), g("sub"), g("align", "center"), g("valign", "middle"), SIZE.get(g("size", "lg"), 64), True)
    if m == "circle_row": return circle_row(g("items") or [{}, {}, {}], d)
    if m == "stat_rows": return stat_rows(g("items") or [{}, {}, {}], d)
    if m == "timeline": return timeline(g("items") or [{}, {}, {}], d)
    if m == "numbered_list": return numbered_list(g("items") or [{}, {}, {}], d)
    if m == "ticker": return ticker(g("items") or ["[키워드 1]", "[키워드 2]", "[키워드 3]"], g("invert", False))
    if m == "quote": return quote(g("text") or "", g("who"), d)
    if m == "index": return index_mark(g("text") or "01", d)
    if m == "two_col": return two_col(g("items") or [{}, {}], d)
    return ""


def est(b, d):
    """모듈 높이 추정(px). 잘리지 않게 넉넉하게 잡는다."""
    m, g = b.get("m"), b.get
    if m == "eyebrow": return 44
    if m == "headline":
        s = SIZE.get(g("size", "lg"), 64); per = {82: 9, 64: 12, 48: 16}[s]
        return int(lines(g("text") or "x", per) * s * 1.25) + 6
    if m == "sub": return 48 * lines(g("text") or "x", 24)
    if m == "body": return 42 * lines(g("text") or "x", 30)
    if m == "footnote": return 33 * lines(g("text") or "x", 35)
    if m == "image":
        if g("bleed"): return _ratio_h(860, g("ratio", "16:9"))
        if g("gif"): return 439
        a, c = [float(x) for x in g("ratio", "16:9").split(":")]; return round(780 * c / a)
    if m == "badges": return 220
    if m == "icon_row":
        n = len(g("items") or [0] * 4); cols = n if n <= 4 else (3 if n in (5, 6) else 4); isz = 150 if cols >= 4 else (200 if cols == 3 else 240)
        return -(-n // cols) * (isz + 12 + 66 + 16)
    if m == "icon_cards":
        its = g("items") or [{}] * 3
        return sum(56 + max(96, 33 + 8 + 42 * lines(i.get("text", "x"), 22)) for i in its) + 20 * (len(its) - 1)
    if m == "check_grid": return -(-len(g("items") or [0] * 4) // 2) * 230 + 16
    if m == "bubbles":
        its = g("items") or ["x"] * 4
        return sum(52 + 39 * lines(t, 20) for t in its) + 20 * (len(its) - 1) + 10
    if m == "photo_grid":
        cols = int(g("cols") or _auto_cols(len(g("items") or [0] * 4))); its = g("items") or [{}] * (cols * 2); rows = -(-len(its) // cols)
        w = (780 - 16 * (cols - 1)) // cols; a, c = [float(x) for x in g("ratio", "1:1" if cols == 2 else "3:4").split(":")]
        return rows * (round(w * c / a) + 12 + 66) + 16 * (rows - 1)
    if m == "chart": return 420 + 66 + 32
    if m == "percent_bars": return len(g("items") or [0] * 3) * 120
    if m == "reviews":
        its = g("items") or [{}] * 3
        return sum(56 + 33 + 10 + 43 * lines(i.get("title", "x"), 20) + 10 + 42 * lines(i.get("text", "x"), 30) for i in its) + 20 * (len(its) - 1) + 20
    if m == "qa":
        its = g("items") or [{}] * 3
        return sum(43 * lines(i.get("q", "x"), 20) + 10 + 42 * lines(i.get("a", "x"), 30) + 24 for i in its) + 20 * (len(its) - 1) + 10
    if m == "spec_table": return sum(40 * lines(v, 22) + 38 for k, v in (g("rows") or [["a", "b"]] * 5)) + 10
    if m == "notice_rows":
        its = g("items") or [{}] * 3
        return sum(max(96, 33 + 8 + 42 * lines(i.get("text", "x"), 22)) + 24 for i in its) + 20 * (len(its) - 1) + 10
    if m == "cert_grid": return -(-int(g("n", 6)) // 3) * (332 + 12 + 66) + 16
    if m == "callout": return 780
    if m == "tip": return 56 + 36 + 12 + 42 * lines(g("text") or "x", 28) + 10
    if m == "claim": return int(lines(g("text") or "x", 9) * 82 * 1.25) + (170 + 32 if g("items") else 0)
    if m == "checklist":
        its = g("items") or ["x"] * 5
        return sum(92 if len(t) <= 22 else 124 for t in its) + 16 * (len(its) - 1)
    if m == "lineup": return 332 + 12 + 66
    if m == "steps": n = len(g("items") or [0] * 3); return n * 309 + 24 * (n - 1)
    if m == "vs": return 2 * (56 + 33 + 12 + 43 * 2) + 48 + 32
    if m == "cta_band": return 108
    if m == "logo": return 96
    if m == "pictogram_bar": return _est_bar(g("items"))
    if m in ("feature_set", "features"): return _est_feature(g("items"), g("style"), g("layout"))
    if m in ("split", "zigzag"):
        its = g("items") if m == "zigzag" else [b]
        tot = 0
        for it in (its or [{}] * 3):
            src = it if m == "zigzag" else {"ratio": g("ratio", "3:4"), "title": g("title"), "text": g("text"), "items": g("items"), "eyebrow": g("eyebrow")}
            ih = _ratio_h(380, src.get("ratio", "3:4"))
            th = (44 if src.get("eyebrow") else 0) + (52 * lines(src.get("title") or "", 9) if src.get("title") else 0) \
                 + (42 * lines(src.get("text") or "", 13) if src.get("text") else 0) + sum(42 * lines(x, 13) + 8 for x in (src.get("items") or []))
            tot += max(ih, th + 40)
        return tot + (48 * (len(g("items") or []) - 1) if m == "zigzag" else 0)
    if m == "overlay": return _ratio_h(780, g("ratio", "1:1"))
    if m == "circle_row":
        its = g("items") or [{}] * 3
        return 240 + 12 + 44 + 33 * max(lines(i.get("text", "x"), 10) for i in its) + 30
    if m == "stat_rows":
        its = g("items") or [{}] * 3
        return sum(max(62 * lines(i.get("claim", "x"), 8), 33 * lines(i.get("data", "x"), 16)) + 62 for i in its) + 10
    if m == "timeline":
        its = g("items") or [{}] * 3
        return sum(43 * lines(i.get("title", "x"), 20) + 42 * lines(i.get("text", "x"), 22) + 8 for i in its) + 40 * (len(its) - 1) + 20
    if m == "numbered_list":
        its = g("items") or [{}] * 3
        return sum(max(80, 43 * lines(i.get("title", "x"), 16) + 42 * lines(i.get("text", "x"), 18) + 8) + 58 for i in its) + 10
    if m == "ticker": return 104
    if m == "quote": return 82 + 62 * lines(g("text") or "x", 14) + 40 + (33 if g("who") else 0)
    if m == "index": return 110
    if m == "two_col":
        its = (g("items") or [{}, {}])[:2]
        return max(43 * lines(i.get("title", "x"), 11) + 42 * lines(i.get("text", "x"), 12) + 40 for i in its)
    return 100


def needs_of(text):
    found = []
    for m in re.findall(r"\[[^\[\]]*\]", re.sub(r"<[^>]+>", "", html.unescape(text))):
        if re.search(r"입력|실제|확인", m) and not m.startswith(("[IMG", "[BG", "[GIF")) and m not in found:
            found.append(m)
    return found


def build(spec_path, out_root, seed=None):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    secs = spec.get("sections") or []
    if not secs:
        raise SystemExit("sections가 비어 있습니다.")
    proj = Path(out_root) / "project"
    proj.mkdir(parents=True, exist_ok=True)
    cj = proj / "canvas.json"
    if cj.exists():
        canvas = json.loads(cj.read_text(encoding="utf-8"))
    else:
        canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
                  "title": spec.get("title") or "상세페이지 와이어프레임", "launch": {"view": "canvas"},
                  "pages": [], "boards": {}, "order": [], "notes": {}, "designSystems": []}
    warns = validate(spec)
    seed = seed if seed is not None else spec.get("seed")
    if seed is None: seed = random.SystemRandom().randrange(1, 1000000)
    rng = random.Random(int(seed)); used_pat = set(); last_pat = None; pat_report = []
    sample_secs = []
    y, order, report, thin = 0, [], [], []
    for i, s in enumerate(secs, 1):
        typ = s.get("type", "section")
        visual = bool(s.get("photo")) or (typ in VIS_TYPES and s.get("photo", True))
        bgk = "photo" if visual else (s.get("bg") or ["bg0", "bg1"][(i - 1) % 2])
        d = bgk in ("dark", "photo")
        blocks = []
        auto_names = []
        for bk in s.get("blocks", []):
            if bk.get("m") in ("entries", "showcase"):
                pat, newb = expand_entries(bk, rng, used_pat, last_pat)
                used_pat.add(pat); last_pat = pat; auto_names.append(PATTERN_NAME[pat]); blocks += newb
            else:
                blocks.append(bk)
        if auto_names:
            pat_report.append(f"P{i} {LABEL.get(typ, typ)}: " + " + ".join(auto_names))
            if not s.get("layout"): s = dict(s); s["layout"] = " + ".join(auto_names) + " (무작위)"
        valign = s.get("valign", "top") if visual else "top"
        bar_blocks = [bk for bk in blocks if bk.get("m") == "pictogram_bar"]
        main_blocks = [bk for bk in blocks if bk.get("m") != "pictogram_bar"]
        bar_html = render_block(bar_blocks[-1], d) if bar_blocks else ""
        body_html = "".join(render_block(bk, d) for bk in main_blocks)
        content = sum(est(bk, d) for bk in main_blocks) + 28 * max(0, len(main_blocks) - 1)
        bar_h = est(bar_blocks[-1], d) if bar_blocks else 0
        if visual and valign == "top":
            # 상단에 카피, 아래에는 연출 이미지가 보이는 빈 공간, 맨 아래에 픽토그램 바
            h = max(1400, 96 + content + 560 + bar_h)
        else:
            h = content + 32 * max(0, len(main_blocks) - 1) + (240 if visual else 160) + (0 if visual else bar_h)
            if h < 1000: thin.append(f"P{i} {LABEL.get(typ, typ)}")
            h = max(1200, h + 40)
        if s.get("h"): h = int(s["h"])
        h = -(-h // 20) * 20
        fn = s.get("file") or ("Main.dc.html" if i == 1 else f"s{i:02d}-{typ}.dc.html")

        label = LABEL.get(typ, typ)
        gub = "비주얼" if visual else "정보"
        (proj / fn).write_text(page(label, h, bgk, body_html, s.get("bg_label"), valign, bar_html), encoding="utf-8")
        ent = dict(canvas["boards"].get(fn, {"w": 860}))
        ent.update({"x": 0, "y": y, "w": 860, "h": h, "title": f"P{i} {label} · {gub}"})
        canvas["boards"][fn] = ent
        order.append(fn)
        nd = list(s.get("check") or [])
        smp = list(s.get("sample") or [])
        if smp: sample_secs.append(f"P{i} {LABEL.get(typ, typ)}: " + " / ".join(smp))
        warns += [f"P{i} {label}: 렌더 결과에 자리표시 {x}" for x in PH_RE.findall(re.sub(r"<[^>]+>", "", html.unescape(body_html))) if not x.startswith(("[IMG", "[GIF", "[BG"))]
        tx = f"P{i} {label} · {gub}"
        if s.get("layout"): tx += f"\n레이아웃: {s['layout']}"
        if s.get("theory"): tx += f"\n기획: {s['theory']}"
        if s.get("goal"): tx += f"\n목적: {s['goal']}"
        if s.get("note"): tx += f"\n메모: {s['note']}"
        if smp: tx += "\n샘플 값 교체: " + " / ".join(smp)
        if nd: tx += "\n확인 필요: " + " / ".join(nd)
        note = dict(canvas["notes"].get(f"n{i}", {}))
        note.update({"x": 940, "y": y, "w": 300, "size": "s", "fill": "gray", "text": tx})
        canvas["notes"][f"n{i}"] = note
        report.append((fn, h))
        y += h  # 간격 0: 한 장의 긴 상세페이지처럼 이어 붙임
    canvas["order"] = order
    cj.write_text(json.dumps(canvas, ensure_ascii=False, indent=1), encoding="utf-8")
    sizes = set()
    for fn, _ in report:
        for m in re.findall(r"font-size:(\d+)px", (proj / fn).read_text(encoding="utf-8")):
            if not 22 <= int(m) <= 82:
                sizes.add((fn, m))
    print(f"{len(report)}개 아트보드 생성, 전체 높이 {y}px")
    if warns:
        print(f"⚠ 빈칸·자리표시 {len(warns)}곳 — 모두 문장으로 채운 뒤 다시 생성하세요")
        for w in warns: print("  -", w)
    else:
        print("빈칸·자리표시 검사: 통과")
    print("글자 크기 22~82px 범위:", "모두 통과" if not sizes else f"위반 {sorted(sizes)}")
    print(f"레이아웃 시드: {seed} (같은 시드를 주면 같은 배치로 다시 만들어집니다)")
    for x in pat_report: print("  레이아웃 -", x)
    if sample_secs:
        print("샘플 값이 들어간 곳(실제 근거로 교체 필요):")
        for x in sample_secs: print("  -", x)
    if thin: print("⚠ 내용이 짧아 하단이 비어 보이는 섹션:", ", ".join(thin), "→ 전체 폭 이미지, zigzag 항목, 추가 모듈로 채우세요")
    print("파일(마지막에 canvas.json):", [fn for fn, _ in report] + ["canvas.json"])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python build_canvas.py spec.json <출력 루트 폴더>")
        sys.exit(1)
    _seed = None
    if "--seed" in sys.argv:
        _seed = int(sys.argv[sys.argv.index("--seed") + 1])
    build(sys.argv[1], sys.argv[2], _seed)
