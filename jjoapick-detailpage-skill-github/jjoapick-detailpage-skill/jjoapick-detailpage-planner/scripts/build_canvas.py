#!/usr/bin/env python3
"""Design(캔버스) 유형용 상세페이지 와이어프레임 생성기.

사용법: python build_canvas.py spec.json <출력 루트 폴더>
  - spec.json은 build_wireframe.py와 같은 형식(sections[{type, bg, blocks:[{m: ...}]}])
  - <루트>/project/ 아래에 아트보드(.dc.html)와 canvas.json을 만든다.
  - 결과 규칙: 가로 860 · 세로 1200 이상 · 여백 40 · 글자 22~82px · 보드 간격 0 · 이미지는 검은 박스
  - 만든 파일은 Design 유형의 절차대로 Artifact로 올린다(canvas.json은 마지막).
"""
import datetime
import sys
from pathlib import Path
import json, html, re
E = html.escape
FF = "font-family:'Noto Sans KR',sans-serif"
FONT = '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;800&display=swap" rel="stylesheet">'
TONE = {"bg0": "#fff", "bg1": "#f1f1f1", "bg2": "#dcdcdc", "dark": "#222", "photo": "#111"}

def page(title, h, bgkey, body, bglabel=None):
    dark = bgkey in ("dark", "photo")
    if bgkey == "photo":
        root = (f"position:relative;width:860px;height:{h}px;box-sizing:border-box;background:#111;color:#fff;{FF};"
                "display:flex;flex-direction:column;align-items:center;justify-content:center;gap:32px;padding:120px 40px")
        tag = (f'<div style="position:absolute;left:16px;top:16px;background:#fff;color:#111;font-size:22px;line-height:1.4;'
               f'padding:4px 12px">[BG IMG] 전체 배경 연출 이미지 · {E(bglabel or "연출 컷 설명 입력")}</div>')
    else:
        root = (f"width:860px;height:{h}px;box-sizing:border-box;background:{TONE[bgkey]};color:{'#fff' if dark else '#111'};{FF};"
                "display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:32px;padding:80px 40px")
        tag = ""
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
{tag}{body}
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
            f'text-align:center;padding:24px;box-sizing:border-box;font-size:22px;line-height:1.45;flex-shrink:0">{E(label)}</div>')
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
    out = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px">{ico(150)}'
                  f'<div style="font-size:22px;font-weight:700;text-align:center;color:{fg(d)}">{E(i)}</div></div>' for i in items)
    return f'<div style="width:100%;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">{out}</div>'
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
            f'font-size:22px;flex-shrink:0">[IMG] {E(label)} · 1:1{pills}</div>')
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
                  '<div style="font-size:22px;color:#555">★★★★★ · [작성자 입력]</div>'
                  f'<div style="font-size:32px;font-weight:700;line-height:1.35;color:#111">{E(t)}</div>'
                  f'<div style="font-size:26px;line-height:1.6;color:#333">{E(x)}</div></div>' for t, x in items)
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:20px">{out}</div>'
def checklist(items):
    out = "".join('<div style="width:100%;box-sizing:border-box;display:flex;align-items:center;gap:20px;background:#fff;border:2px solid #bbb;border-radius:999px;padding:18px 32px">'
                  '<div style="width:56px;height:56px;border-radius:50%;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-size:28px;flex-shrink:0">✓</div>'
                  f'<div style="font-size:26px;line-height:1.5;color:#111">{E(t)}</div></div>' for t in items)
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:16px">{out}</div>'
def cert_grid(n, d=False):
    return photo_grid(3, [(f"인증서·특허 {i + 1}", "[인증 번호·증빙 확인]") for i in range(n)], "3:4", d)
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
            f'border-bottom:3px solid {fg(d)}">{cols}</div>{bd_}</div>' + foot(note or "[비교 기준·출처 입력]", d) + foot("막대 높이는 샘플 비율입니다", d))
def percent_bars(items, d=False):
    out = ""
    for it in items:
        m = re.search(r"\d+(?:\.\d+)?", str(it.get("value", "")))
        v = max(0, min(100, float(m.group()))) if m else 80
        out += (f'<div style="width:100%;display:flex;flex-direction:column;gap:6px"><div style="font-size:26px;line-height:1.5;color:{bd(d)}">{E(it.get("label", ""))}</div>'
                f'<div style="height:28px;background:{"#444" if d else "#dcdcdc"}"><div style="width:{v}%;height:100%;background:{"#fff" if d else "#111"}"></div></div>'
                f'<div style="font-size:22px;color:{mu(d)}">{E(it.get("value") or "[실제 수치 입력]")}</div></div>')
    return f'<div style="width:100%;display:flex;flex-direction:column;gap:20px">{out}</div>'
def lineup(items, d=False):
    return photo_grid(3, [(i, i) for i in items], "3:4", d)

SIZE = {"xl": 82, "lg": 64, "md": 48}
ROW = {"hero": True, "brand": True}
VIS_TYPES = {"hero", "brand"}
LABEL = {"hero": "Hero", "trust": "Trust", "pain": "Pain", "cause": "Cause", "point": "Point", "proof": "Proof", "howto": "How-to",
         "review": "Review", "why": "Why", "brand": "Brand", "info": "Info", "notice": "Notice", "maker": "Maker", "section": "Section"}


def lines(t, per):
    return sum(max(1, -(-len(x) // per)) for x in str(t).split("\n"))


def render_block(b, d):
    m = b.get("m")
    g = b.get
    if m == "eyebrow": return eyebrow(g("text") or "POINT 01", d)
    if m == "headline": return headline(g("text") or "[제목 입력]", d, SIZE.get(g("size", "lg"), 64))
    if m == "sub": return sub(g("text") or "[서브 한 줄 입력]", d)
    if m == "body": return body(g("text") or "[본문 입력]", d)
    if m == "footnote": return foot(g("text") or "[각주 입력]", d)
    if m == "image":
        return gif(g("label") or "이미지", d) if g("gif") else image(g("label") or "이미지", g("ratio", "16:9"), d)
    if m == "badges": return badges(g("items") or ["[배지 입력]"] * 3, d)
    if m == "icon_row": return icon_row(g("items") or ["[특징]"] * 4, d)
    if m == "icon_cards": return icon_cards([(i.get("label", "LABEL"), i.get("text", "[문구 입력]")) for i in (g("items") or [{}] * 3)], d)
    if m == "check_grid": return check_grid(g("items") or ["[체크 포인트 입력]"] * 4, d)
    if m == "bubbles": return bubbles(g("items") or ["[고객 속마음 입력]"] * 4)
    if m == "photo_grid":
        cols = int(g("cols", 2))
        its = [((i.get("label") or "사진"), (i.get("caption") or "[캡션 입력]")) for i in (g("items") or [{}] * (cols * 2))]
        return photo_grid(cols, its, g("ratio", "1:1" if cols == 2 else "3:4"), d)
    if m == "chart": return chart(g("bars") or [{"label": "일반 제품", "value": 40}, {"label": "우리 제품", "value": 70, "hot": True}], g("badge"), g("note"), d)
    if m == "percent_bars": return percent_bars(g("items") or [{}] * 3, d)
    if m == "reviews": return reviews([(i.get("title", "[후기 제목 입력]"), i.get("text", "[실제 후기 입력]")) for i in (g("items") or [{}] * 3)])
    if m == "qa": return qa([(i.get("q", "[질문 입력]"), i.get("a", "[실제 답변 입력]")) for i in (g("items") or [{}] * 3)])
    if m == "spec_table": return spec_table(g("rows") or [["항목", "[실제 입력]"]] * 5)
    if m == "notice_rows": return notice_rows([(i.get("title", "안내"), i.get("text", "[실제 안내 입력]")) for i in (g("items") or [{}] * 3)])
    if m == "cert_grid": return cert_grid(int(g("n", 6)), d)
    if m == "callout": return callout(g("label") or "제품 도해 컷", g("items") or ["[특징 1]", "[특징 2]", "[특징 3]", "[특징 4]"])
    if m == "tip": return tip(g("text") or "[팁 입력]", d)
    if m == "claim": return claim(g("text") or "[강조 문구 입력]", g("items"), d)
    if m == "checklist": return checklist(g("items") or ["[선택 이유 입력]"] * 5)
    if m == "lineup": return lineup(g("items") or ["[제품 1]", "[제품 2]", "[제품 3]"], d)
    if m == "steps": return steps([(i.get("title", "[단계 제목]"), i.get("text", "[설명 입력]")) for i in (g("items") or [{}] * 3)])
    if m == "vs":
        L, R = g("left", {}), g("right", {})
        return vs(L.get("tag", "흔한 생각"), L.get("text", "[흔한 생각 입력]"), R.get("tag", "새로운 생각"), R.get("text", "[새로운 생각 입력]"), d)
    if m == "cta_band": return band(g("text") or "지금 구매하기 ▸", d)
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
        if g("gif"): return 439
        a, c = [float(x) for x in g("ratio", "16:9").split(":")]; return round(780 * c / a)
    if m == "badges": return 220
    if m == "icon_row": return 200
    if m == "icon_cards":
        its = g("items") or [{}] * 3
        return sum(56 + max(96, 33 + 8 + 42 * lines(i.get("text", "x"), 22)) for i in its) + 20 * (len(its) - 1)
    if m == "check_grid": return -(-len(g("items") or [0] * 4) // 2) * 230 + 16
    if m == "bubbles":
        its = g("items") or ["x"] * 4
        return sum(52 + 39 * lines(t, 20) for t in its) + 20 * (len(its) - 1) + 10
    if m == "photo_grid":
        cols = int(g("cols", 2)); its = g("items") or [{}] * (cols * 2); rows = -(-len(its) // cols)
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
    return 100


def needs_of(text):
    found = []
    for m in re.findall(r"\[[^\[\]]*\]", re.sub(r"<[^>]+>", "", html.unescape(text))):
        if re.search(r"입력|실제|확인", m) and not m.startswith(("[IMG", "[BG", "[GIF")) and m not in found:
            found.append(m)
    return found


def build(spec_path, out_root):
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
    y, order, report = 0, [], []
    for i, s in enumerate(secs, 1):
        typ = s.get("type", "section")
        visual = bool(s.get("photo")) or (typ in VIS_TYPES and s.get("photo", True))
        bgk = "photo" if visual else (s.get("bg") or ["bg0", "bg1"][(i - 1) % 2])
        d = bgk in ("dark", "photo")
        blocks = s.get("blocks", [])
        body_html = "".join(render_block(b, d) for b in blocks)
        h = sum(est(b, d) for b in blocks) + 32 * max(0, len(blocks) - 1) + (240 if visual else 160)
        h = max(1200, -(-(h + 40) // 20) * 20)
        fn = s.get("file") or ("Main.dc.html" if i == 1 else f"s{i:02d}-{typ}.dc.html")
        label = LABEL.get(typ, typ)
        gub = "비주얼" if visual else "정보"
        (proj / fn).write_text(page(label, h, bgk, body_html, s.get("bg_label")), encoding="utf-8")
        ent = dict(canvas["boards"].get(fn, {"w": 860}))
        ent.update({"x": 0, "y": y, "w": 860, "h": h, "title": f"P{i} {label} · {gub}"})
        canvas["boards"][fn] = ent
        order.append(fn)
        nd = needs_of(body_html)
        tx = f"P{i} {label} · {gub}"
        if s.get("theory"): tx += f"\n기획: {s['theory']}"
        if s.get("goal"): tx += f"\n목적: {s['goal']}"
        if s.get("note"): tx += f"\n메모: {s['note']}"
        if nd: tx += f"\n입력 필요 {len(nd)}: " + ", ".join(nd[:3]) + (" …" if len(nd) > 3 else "")
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
    print("글자 크기 22~82px 범위:", "모두 통과" if not sizes else f"위반 {sorted(sizes)}")
    print("파일(마지막에 canvas.json):", [fn for fn, _ in report] + ["canvas.json"])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python build_canvas.py spec.json <출력 루트 폴더>")
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])
