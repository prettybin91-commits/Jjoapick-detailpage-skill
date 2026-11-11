#!/usr/bin/env python3
"""상세페이지 와이어프레임 빌더 (Design 캔버스를 쓸 수 없을 때의 폴백, 글자를 클릭해 수정되는 HTML).

사용법: python build_wireframe.py spec.json out.html
스펙은 sections[{type, bg, blocks:[{m: 모듈이름, ...}]}] 형식. references/modules.md 참고.
섹션은 간격 없이 이어 붙어 한 장의 긴 상세페이지처럼 보인다(가로 860px 고정).
"""
import html
import json
import re
import sys
from pathlib import Path

W = 860
CW = 780  # 본문 폭 (좌우 여백 40)


def esc(s):
    return html.escape(str(s), quote=True)


def rich(s):
    out = esc(s)
    out = re.sub(r"\*\*(.+?)\*\*", r'<b class="hl">\1</b>', out)
    return out


def hgt(w, ratio):
    try:
        a, b = [float(x) for x in str(ratio).replace("/", ":").split(":")]
        return round(w * b / a)
    except Exception:
        return round(w * 9 / 16)


def num(v, default=60):
    m = re.search(r"\d+(?:\.\d+)?", str(v or ""))
    return (max(0, min(100, float(m.group()))), True) if m else (default, False)


def T(cls, v, label="문구 입력", tag="div"):
    if v:
        return f'<{tag} class="{cls}">{rich(v)}</{tag}>'
    return f'<{tag} class="{cls} phx">[{esc(label)}]</{tag}>'


def img(label, w=CW, ratio="16:9", h=None, cls=""):
    hh = h or hgt(w, ratio)
    return (f'<div class="img {cls}" style="width:{w}px;max-width:100%;height:{hh}px">'
            f'<span>{esc(label)}</span></div>')


# ------------------------------------------------------------------ 모듈
def m_eyebrow(m):
    return f'<div class="eyebrow">{esc(m.get("text") or "POINT 01")}</div>'


def m_headline(m):
    return f'<h2 class="h {m.get("size", "lg")}">{rich(m.get("text") or "[제목 입력]")}</h2>'


def m_sub(m):
    return T("sub", m.get("text"), "서브 한 줄 입력")


def m_body(m):
    return T("p", m.get("text"), "본문 입력")


def m_footnote(m):
    return T("fn", m.get("text"), "각주 입력")


def m_image(m):
    label = m.get("label") or "이미지"
    ratio = m.get("ratio", "16:9")
    pre = "[GIF] " if m.get("gif") else "[IMG] "
    return img(pre + label + f" · {ratio}", m.get("w", CW), ratio, m.get("h"))


def m_badges(m):
    items = m.get("items") or ["[배지 입력]"] * 3
    return '<div class="row-c">' + "".join(f'<div class="circle">{rich(i)}</div>' for i in items) + "</div>"


def m_icon_cards(m):
    out = ""
    for it in m.get("items") or [{}, {}, {}]:
        it = {"text": it} if isinstance(it, str) else it
        out += ('<div class="card row-l"><div class="ico"><span>ICON</span></div><div class="col-t">'
                f'{T("lab", it.get("label"), "영문 라벨")}{T("p", it.get("text"), "문구 입력")}</div></div>')
    return f'<div class="stack">{out}</div>'


def m_icon_row(m):
    items = m.get("items") or ["[특징]"] * 4
    return ('<div class="grid4">' + "".join(
        f'<div class="col-c"><div class="ico lg"><span>ICON</span></div><div class="lab c">{rich(i)}</div></div>'
        for i in items) + "</div>")


def m_check_grid(m):
    items = m.get("items") or ["[체크 포인트 입력]"] * 4
    return ('<div class="grid2">' + "".join(
        f'<div class="card col-c"><div class="ico"><span>ICON</span></div>{T("p c", i, "문구 입력")}</div>'
        for i in items) + "</div>")


def m_bubbles(m):
    out = ""
    for i, t in enumerate(m.get("items") or ["[고객 속마음 입력]"] * 4):
        out += f'<div class="bubble {"r" if i % 2 else "l"}">{rich(t)}</div>'
    return f'<div class="stack">{out}</div>'


def m_photo_grid(m):
    cols = int(m.get("cols", 2))
    items = m.get("items") or [{}] * (cols * 2)
    w = (CW - 16 * (cols - 1)) // cols
    ratio = m.get("ratio", "1:1" if cols == 2 else "3:4")
    out = ""
    for it in items:
        it = {"label": it} if isinstance(it, str) else it
        out += (f'<div class="col-c">{img("[IMG] " + (it.get("label") or "사진") + " · " + ratio, w, ratio)}'
                f'{T("cap", it.get("caption"), "캡션 입력")}</div>')
    return f'<div class="grid{cols}">{out}</div>'


def m_chart(m):
    bars = m.get("bars") or [{"label": "일반 제품", "value": 40}, {"label": "우리 제품", "value": 70, "hot": True}]
    out, sample = "", False
    for b in bars:
        v, ok = num(b.get("value"), 50)
        sample = sample or not ok
        out += (f'<div class="bar-c"><div class="bar {"hot" if b.get("hot") else ""}" style="height:{int(v * 3.2)}px"></div>'
                f'<div class="lab c">{esc(b.get("label", ""))}</div></div>')
    badge = f'<div class="circle sm">{rich(m["badge"])}</div>' if m.get("badge") else ""
    note = T("fn", m.get("note"), "비교 기준·출처 입력")
    smp = '<div class="fn">막대 높이는 샘플 비율입니다</div>' if sample or m.get("sample") else ""
    return f'<div class="chart">{badge}<div class="bars">{out}</div></div>{note}{smp}'


def m_percent_bars(m):
    out = ""
    for it in m.get("items") or [{}] * 4:
        v, ok = num(it.get("value"), 80)
        out += ('<div class="pbar">'
                f'{T("p", it.get("label"), "항목 입력")}'
                f'<div class="track"><i style="width:{v}%"></i></div>'
                f'<div class="fn">{esc(it.get("value") or "[실제 수치 입력]")}</div></div>')
    return f'<div class="stack">{out}</div>'


def m_reviews(m):
    out = ""
    for it in m.get("items") or [{}, {}, {}]:
        out += ('<div class="card">'
                '<div class="fn">★★★★★ · [작성자 입력]</div>'
                f'{T("quote", it.get("title"), "후기 제목")}{T("p", it.get("text"), "실제 후기 입력")}</div>')
    return f'<div class="stack">{out}</div>'


def m_qa(m):
    out = ""
    for it in m.get("items") or [{}, {}, {}]:
        out += (f'<div class="qa"><div class="q">Q. {esc(it.get("q") or "[질문 입력]")}</div>'
                f'{T("p", it.get("a"), "실제 답변 입력")}</div>')
    return f'<div class="stack">{out}</div>'


def m_spec_table(m):
    rows = m.get("rows") or [["항목", "[실제 입력]"]] * 5
    out = "".join(f'<div class="srow"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div></div>' for k, v in rows)
    return f'<div class="table">{out}</div>'


def m_notice_rows(m):
    out = ""
    for it in m.get("items") or [{}, {}, {}]:
        out += ('<div class="row-l nrow"><div class="ico"><span>ICON</span></div><div class="col-t">'
                f'<div class="lab k">{esc(it.get("title") or "안내")}</div>{T("p", it.get("text"), "실제 안내 입력")}</div></div>')
    return f'<div class="stack">{out}</div>'


def m_cert_grid(m):
    n = int(m.get("n", 6))
    w = (CW - 32) // 3
    return ('<div class="grid3">' + "".join(img(f"[IMG] 인증서·특허 {i + 1}", w, "3:4") for i in range(n)) + "</div>")


def m_callout(m):
    items = (m.get("items") or ["[특징 1]", "[특징 2]", "[특징 3]", "[특징 4]"])[:4]
    pos = ["left:16px;top:60px", "right:16px;top:60px", "left:16px;bottom:60px", "right:16px;bottom:60px"]
    pills = "".join(f'<div class="pill" style="{pos[i]}">{esc(t)}</div>' for i, t in enumerate(items))
    return (f'<div class="callout" style="height:{CW}px"><span>[IMG] {esc(m.get("label") or "제품 도해 컷")} · 1:1</span>{pills}</div>')


def m_tip(m):
    return f'<div class="tip"><span class="eyebrow sm">TIP!</span>{T("p", m.get("text"), "팁 입력")}</div>'


def m_claim(m):
    items = m.get("items")
    ic = ""
    if items:
        ic = '<div class="row-c">' + "".join(f'<div class="circle sm">{esc(i)}</div>' for i in items) + "</div>"
    return f'<div class="h xl claim">{rich(m.get("text") or "[강조 문구 입력]")}</div>{ic}'


def m_checklist(m):
    out = ""
    for t in m.get("items") or ["[선택 이유 입력]"] * 5:
        out += f'<div class="pillrow"><div class="chk">✓</div>{T("p", t, "이유 입력")}</div>'
    return f'<div class="stack">{out}</div>'


def m_lineup(m):
    items = m.get("items") or ["[제품 1]", "[제품 2]", "[제품 3]"]
    w = (CW - 32) // 3
    return ('<div class="grid3">' + "".join(
        f'<div class="col-c">{img("[IMG] " + i, w, "3:4")}<div class="cap">{esc(i)}</div></div>' for i in items) + "</div>")


def m_steps(m):
    out = ""
    for i, it in enumerate(m.get("items") or [{}, {}, {}], 1):
        out += ('<div class="row-l step">' + img(f"[IMG] STEP {i} 사용 컷 · 4:3", 380, "4:3") +
                f'<div class="col-t"><div class="eyebrow sm">STEP {i}</div>{T("sh", it.get("title"), "단계 제목")}'
                f'{T("p", it.get("text"), "설명 입력")}</div></div>')
    return f'<div class="stack">{out}</div>'


def m_vs(m):
    L, R = m.get("left", {}), m.get("right", {})
    return ('<div class="stack">'
            f'<div class="card"><div class="lab">{esc(L.get("tag", "흔한 생각"))}</div>{T("sh", L.get("text"), "흔한 생각 입력")}</div>'
            '<div class="arrow">↓</div>'
            f'<div class="card strong"><div class="lab">{esc(R.get("tag", "새로운 생각"))}</div>{T("sh", R.get("text"), "새로운 생각 입력")}</div>'
            '</div>')


def m_cta_band(m):
    return f'<div class="band">{esc(m.get("text") or "지금 구매하기 ▸")}</div>'


MODS = {k[2:]: v for k, v in globals().items() if k.startswith("m_")}

# ------------------------------------------------------------------ 섹션
TYPE_LABEL = {"hero": "Hero", "trust": "Trust", "pain": "Pain", "cause": "Cause", "point": "Point",
              "proof": "Proof", "howto": "How-to", "review": "Review", "why": "Why", "brand": "Brand",
              "info": "Info", "notice": "Notice", "maker": "Maker", "section": "Section"}
VISUAL_TYPES = {"hero", "brand"}


def needs_of(sec):
    def strings(v):
        if isinstance(v, str):
            yield v
        elif isinstance(v, dict):
            for x in v.values():
                yield from strings(x)
        elif isinstance(v, list):
            for x in v:
                yield from strings(x)
    raw = json.dumps(sec.get("blocks", []), ensure_ascii=False)
    found = []
    for t in strings(sec.get("blocks", [])):
        for m in re.findall(r"\[[^\[\]]*\]", t):
            if re.search(r"입력|실제|확인", m) and m not in found:
                found.append(m)
    # 값이 비어 있어 자동으로 자리표시가 된 모듈 수
    return found


def render_section(s, i):
    typ = s.get("type", "section")
    visual = bool(s.get("photo")) or (typ in VISUAL_TYPES and s.get("photo", True))
    bg = s.get("bg") or ("photo" if visual else ["bg0", "bg1"][i % 2])
    if visual:
        bg = "photo"
    inner = "".join(MODS[b["m"]](b) for b in s.get("blocks", []) if b.get("m") in MODS)
    tag = ""
    if bg == "photo":
        tag = f'<div class="bgtag">[BG IMG] 전체 배경 연출 이미지 · {esc(s.get("bg_label") or "연출 컷 설명 입력")}</div>'
    return f'<div class="sc {bg}">{tag}{inner}</div>', visual


def note_html(s, i, visual):
    typ = s.get("type", "section")
    parts = [f'<div class="n-h">P{i + 1} · {esc(TYPE_LABEL.get(typ, typ))} · {"비주얼" if visual else "정보"}</div>']
    for k, lab in (("theory", "기획 요소"), ("goal", "목적"), ("note", "메모")):
        if s.get(k):
            parts.append(f'<div class="n-r"><b>{lab}</b><span>{esc(s[k])}</span></div>')
    needs = needs_of(s)
    if needs:
        parts.append('<div class="n-r need"><b>입력 필요 %d</b><ul>%s</ul></div>' % (
            len(needs), "".join(f"<li>{esc(n)}</li>" for n in needs)))
    return '<aside class="note">' + "".join(parts) + "</aside>", len(needs)


CSS = r"""
:root{--bg:#ececea;--fg:#1b1b1b;--muted:#6a6a68;--line:#d4d4d0;--bar:#fff;--chip:#e8e8e5;--warnbg:#fff3d6;--warnfg:#7a5200;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#151515;--fg:#ececec;--muted:#9b9b98;--line:#333331;--bar:#1e1e1e;--chip:#2a2a28;--warnbg:#3a2f12;--warnfg:#f0c869}}
:root[data-theme="dark"]{--bg:#151515;--fg:#ececec;--muted:#9b9b98;--line:#333331;--bar:#1e1e1e;--chip:#2a2a28;--warnbg:#3a2f12;--warnfg:#f0c869}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Noto Sans KR","Pretendard",-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;line-height:1.5}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bar)}
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:11;background:var(--bar);border-bottom:1px solid var(--line);padding:12px 20px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.top h1{font-size:16px;margin:0}.top .meta{font-size:13px;color:var(--muted)}.top .sp{flex:1}
.tbtn{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--chip);color:var(--fg);border-radius:8px;padding:7px 12px;cursor:pointer}
.tbtn[aria-pressed="true"]{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.legend{max-width:1240px;margin:0 auto;padding:12px 20px 0;font-size:13px;color:var(--muted)}
.stage{padding:16px 20px 80px}
.sec{display:grid;grid-template-columns:860px 280px;gap:24px;justify-content:center;margin:0 auto;align-items:start}
.notes-off .sec{grid-template-columns:860px}.notes-off .note{display:none}
.canvas{width:860px;max-width:100%;font-family:"Noto Sans KR","Pretendard",sans-serif}
.note{font-size:13px;background:var(--bar);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin-top:12px;position:sticky;top:calc(env(safe-area-inset-top,0px) + 72px)}
.n-h{font-weight:700;margin-bottom:6px}.n-r{display:flex;flex-direction:column;gap:2px;margin-top:6px}
.n-r b{font-size:11px;color:var(--muted)}.n-r ul{margin:2px 0 0;padding-left:16px}.n-r.need li{color:var(--warnfg)}
@media (max-width:1240px){.sec,.notes-off .sec{grid-template-columns:minmax(0,860px)}.note{position:static}}

/* ===== 상세페이지 캔버스: 860 고정, 여백 40, 글자 22~82px, 섹션 이어 붙임 ===== */
.sc{position:relative;min-height:1200px;padding:80px 40px;display:flex;flex-direction:column;align-items:center;gap:32px;color:#111}
.bg0{background:#fff}.bg1{background:#f1f1f1}.bg2{background:#dcdcdc}
.dark{background:#222;color:#fff}.photo{background:#111;color:#fff;justify-content:center;padding-top:120px}
.bgtag{position:absolute;left:16px;top:16px;background:#fff;color:#111;font-size:22px;line-height:1.4;padding:4px 12px}
.h{margin:0;width:100%;text-align:center;font-weight:800;line-height:1.25;letter-spacing:-.01em;white-space:pre-line}
.h.xl{font-size:82px}.h.lg{font-size:64px}.h.md{font-size:48px}
.hl{font-weight:inherit;background:#cdcdcd;padding:0 8px}
.dark .hl,.photo .hl{background:rgba(255,255,255,.28)}
.sub{font-size:32px;line-height:1.5;color:#555;text-align:center;width:100%;white-space:pre-line}
.p{font-size:26px;line-height:1.6;color:#333;white-space:pre-line}.p.c{text-align:center}
.fn{font-size:22px;line-height:1.5;color:#666;width:100%;text-align:center}
.lab{font-size:22px;font-weight:700;color:#555;letter-spacing:.04em}.lab.c{text-align:center}.lab.k{color:#111}
.cap{font-size:22px;color:#555;text-align:center;line-height:1.4}
.sh{font-size:32px;font-weight:700;line-height:1.35;color:#111}.quote{font-size:32px;font-weight:700;line-height:1.35}
.dark .sub,.dark .p,.dark .fn,.dark .lab,.dark .cap,.photo .sub,.photo .p,.photo .fn,.photo .lab,.photo .cap{color:#e6e6e6}
.dark .sh,.dark .quote,.dark .lab.k,.photo .sh{color:#fff}
.eyebrow{font-size:22px;font-weight:700;letter-spacing:.06em;border:2px solid currentColor;border-radius:999px;padding:4px 22px}
.eyebrow.sm{padding:2px 14px;align-self:flex-start}
.phx{border:2px dashed #999;padding:10px 14px;color:#666;text-align:center;width:100%}
.dark .phx,.photo .phx{border-color:#aaa;color:#ddd}
.img{background:#111;color:#fff;display:grid;place-items:center;text-align:center;font-size:22px;line-height:1.45;padding:24px;flex-shrink:0}
.photo .img,.dark .img{outline:2px solid #fff;outline-offset:-2px}
.stack{width:100%;display:flex;flex-direction:column;gap:20px}
.card{width:100%;border:2px solid #bbb;background:#fff;color:#111;padding:28px;display:flex;flex-direction:column;gap:12px}
.card.strong{border-color:#111;background:#ececec}
.dark .card{background:#2e2e2e;border-color:#666;color:#fff}.dark .card .p{color:#e6e6e6}
.row-l{display:flex;gap:24px;align-items:center}.row-c{display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
.col-t{display:flex;flex-direction:column;gap:8px;min-width:0;flex:1}.col-c{display:flex;flex-direction:column;align-items:center;gap:12px}
.card.row-l{flex-direction:row}
.ico{width:96px;height:96px;background:#111;color:#fff;display:grid;place-items:center;font-size:22px;flex-shrink:0}.ico.lg{width:150px;height:150px}
.grid2{width:100%;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.grid3{width:100%;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.grid4{width:100%;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.circle{width:220px;height:220px;border-radius:50%;background:#fff;color:#111;border:3px solid #111;display:flex;align-items:center;justify-content:center;text-align:center;font-size:26px;font-weight:800;line-height:1.3;padding:16px;white-space:pre-line}
.circle.sm{width:170px;height:170px;font-size:24px}
.photo .circle,.dark .circle{border-color:#fff}
.bubble{max-width:82%;background:#dcdcdc;color:#111;border-radius:40px;padding:26px 36px;font-size:26px;line-height:1.5}
.bubble.l{align-self:flex-start;border-bottom-left-radius:8px}.bubble.r{align-self:flex-end;border-bottom-right-radius:8px;background:#c4c4c4}
.chart{position:relative;width:100%;padding:20px 0 0}.bars{display:flex;align-items:flex-end;justify-content:center;gap:40px;height:340px;border-bottom:3px solid #111}
.bar-c{display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:10px;width:200px}
.bar{width:100%;background:#bdbdbd}.bar.hot{background:#111}.chart .circle{position:absolute;right:0;top:0}
.pbar{width:100%;display:grid;grid-template-columns:1fr;gap:6px}.track{height:28px;background:#dcdcdc}.track i{display:block;height:100%;background:#111}
.dark .track{background:#444}.dark .track i{background:#fff}
.qa{border-bottom:2px solid #bbb;padding-bottom:20px;display:flex;flex-direction:column;gap:10px}.q{font-size:32px;font-weight:700;line-height:1.35}
.table{width:100%;border-top:3px solid #111}.srow{display:grid;grid-template-columns:220px 1fr;gap:16px;border-bottom:2px solid #ddd;padding:18px 0;font-size:26px;line-height:1.5}.srow .k{font-weight:700}.srow .v{color:#333}
.nrow{border-bottom:2px solid #ddd;padding-bottom:20px}
.callout{position:relative;width:100%;background:#111;color:#fff;display:grid;place-items:center;font-size:22px}
.pill{position:absolute;background:#fff;color:#111;border:3px solid #111;border-radius:999px;padding:10px 22px;font-size:24px;font-weight:700}
.tip{width:100%;border:3px dashed #666;padding:28px;display:flex;flex-direction:column;gap:12px}
.claim{padding:20px 0;white-space:pre-line}
.pillrow{display:flex;align-items:center;gap:20px;background:#fff;border:2px solid #bbb;border-radius:999px;padding:18px 32px;color:#111}.pillrow .p{color:#111}
.chk{width:56px;height:56px;border-radius:50%;background:#111;color:#fff;display:grid;place-items:center;font-size:28px;flex-shrink:0}
.step{align-items:flex-start;border-bottom:2px solid #ddd;padding-bottom:24px;width:100%}
.arrow{text-align:center;font-size:48px;line-height:1;color:#555}
.band{width:calc(100% + 80px);margin:0 -40px;background:#111;color:#fff;text-align:center;font-size:32px;font-weight:700;padding:36px 0}
"""

JS = """(function(){var b=document.getElementById('t-note');b.addEventListener('click',function(){var off=document.body.classList.toggle('notes-off');b.setAttribute('aria-pressed',String(!off));});})();"""


def build(spec):
    secs = spec.get("sections") or []
    if not secs:
        raise SystemExit("sections가 비어 있습니다.")
    blocks, total = [], 0
    for i, s in enumerate(secs):
        inner, visual = render_section(s, i)
        note, n = note_html(s, i, visual)
        total += n
        blocks.append(f'<section class="sec"><div class="canvas" contenteditable="true" spellcheck="false">{inner}</div>{note}</section>')
    title = spec.get("title") or "상세페이지 와이어프레임"
    brand = spec.get("brand")
    head = f"{brand} · {title}" if brand else title
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(head)}</title>
<style>{CSS}</style>
</head>
<body>
<header class="top"><h1>{esc(head)}</h1><span class="meta">{len(secs)}개 섹션 · 입력 필요 {total}</span><span class="sp"></span>
<button class="tbtn" id="t-note" aria-pressed="true" type="button">주석 보기</button></header>
<div class="legend">가로 860px 상세페이지: 섹션이 이어 붙어 한 장으로 보입니다. 검은 박스는 이미지 자리, 글자를 클릭하면 바로 수정됩니다. 점선 박스는 비어 있는 카피·사실 정보 자리입니다.</div>
<main class="stage">{"".join(blocks)}</main>
<script>{JS}</script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 3:
        print("사용법: python build_wireframe.py spec.json out.html")
        sys.exit(1)
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(spec), encoding="utf-8")
    print(f"완료: {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
