# 와이어프레임 모듈 (상세페이지 부품)

Design 캔버스에서는 아래 인라인 스타일을 그대로 쓰고, 폴백 빌더에서는 `blocks`의 `m` 값(괄호 안 이름)으로 쓴다.
공통: 본문 폭 780px, 글자 22~82px, 이미지 자리는 검은 박스(#111, 흰 글씨 22px), 사실 정보는 `[실제 … 입력]`.
배경 톤(섹션 루트): `#fff` / `#f1f1f1` / `#dcdcdc` / 진한 `#222`(흰 글씨) / 전체 이미지 `#111`(흰 글씨).

## 텍스트 모듈
- **eyebrow** (`text`): `<div style="font-size:22px;font-weight:700;letter-spacing:.06em;border:2px solid #111;border-radius:999px;padding:4px 22px">POINT 01</div>`
- **headline** (`text`, `size`: xl 82 / lg 64 / md 48): `<h2 style="margin:0;width:100%;text-align:center;font-size:64px;line-height:1.25;font-weight:800;white-space:pre-line">작아도 알찬<br>…</h2>`, 강조 키워드는 `<span style="background:#cdcdcd;padding:0 8px">3가지</span>` (진한 배경에서는 `rgba(255,255,255,.28)`). 빌더에서는 `**키워드**`.
- **sub** (32px #555 가운데), **body** (26px #333), **footnote** (22px #666 가운데; 수치·출처·기준 시점)

## 이미지 모듈
- **image** (`label`, `ratio`, `gif`): 검은 박스, 라벨 `[IMG] 설명 · 16:9` 또는 `[GIF] …`. 폭 780 기준 높이 16:9=439, 3:2=520, 4:3=585, 1:1=780, 3:4=1040.
- **photo_grid** (`cols` 2/3, `items[{label,caption}]`): 검은 박스 + 아래 캡션(22px). 2열은 폭 382, 3열은 폭 249, 간격 16.
- **steps** (`items[{title,text}]`): 가로 줄 하나에 검은 이미지(380×285) 왼쪽 + 라벨 STEP n(알약) + 제목 32 + 설명 26.
- **callout** (`label`, `items` 4개): 검은 1:1 박스 위 모서리 4곳에 흰 알약 라벨(24px 굵게)을 올려 제품 도해를 표현.
- **cert_grid** (`n`): 3열 3:4 검은 박스(`[IMG] 인증서·특허`).
- **lineup** (`items`): 3열 3:4 검은 박스 + 제품명 캡션.

## 신뢰·아이콘 모듈
- **badges** (`items`): 지름 220px 원형 스티커(흰 바탕, 검은 테두리 3px, 26px 굵게). 히어로 제품 컷 옆·아래에 2~3개.
- **icon_row** (`items` 4): 4열, 검은 아이콘 박스 150×150 + 라벨 22px. 인증·특징 한 줄 요약.
- **icon_cards** (`items[{label,text}]`): 흰 카드 가로 배치, 왼쪽 검은 아이콘 96px, 오른쪽 영문 라벨 22px + 문구 26px. 3개 세로로.
- **check_grid** (`items` 4): 2×2 카드, 아이콘 + 문구.
- **checklist** (`items` 5): 알약 모양 행(둥근 테두리 999px) 왼쪽 검은 체크 원.
- **claim** (`text`, `items`): 82px 대형 문구(예: ZERO) + 아래 원형 아이콘 3개.

## 공감·설득 모듈
- **bubbles** (`items` 4): 둥근 말풍선(radius 40px, 회색), 왼쪽·오른쪽 번갈아, 문구 26px.
- **vs** (`left`, `right`): `흔한 생각` 카드 → 화살표(48px ↓) → `새로운 생각` 카드(굵은 테두리).
- **tip** (`text`): 점선 박스 + `TIP!` 알약 + 문구.

## 데이터 모듈 (수치는 작게)
- **chart** (`bars[{label,value,hot}]`, `badge`, `note`): 세로 막대 2~3개(우리 제품만 검정, 나머지 회색) + 오른쪽 위 원형 수치 배지 + 아래 기준·출처 22px. 수치가 없으면 샘플 높이이고 "샘플 비율" 표기.
- **percent_bars** (`items[{label,value}]`): 항목명 26px + 가로 막대 + 수치 **22px**.
- **spec_table** (`rows`): 위 검은 선 + 2열(항목 굵게 / 값), 26px.

## 후기·안내 모듈
- **reviews** (`items[{title,text}]`): 카드, 별점·작성자 22px + 인용형 제목 32px + 본문 26px. **실제 후기만**, 없으면 `[실제 후기 입력]`.
- **qa** (`items[{q,a}]`): `Q.` 32px 굵게 + 답변 26px.
- **notice_rows** (`items[{title,text}]`): 왼쪽 검은 아이콘 96px + 제목 22px + 안내 26px (보관·주의·배송·교환·환불).
- **cta_band** (`text`): 가로 전체(860) 검은 띠 + 흰 글씨 32px 굵게. 웹 버튼 대신 쓴다.

## 조립 예
히어로 = eyebrow → headline(xl) → badges → sub → image(3:2), 배경은 전체 이미지.
POINT = eyebrow(POINT 01) → headline → image 또는 chart 또는 photo_grid → body → icon_row/tip → footnote.
