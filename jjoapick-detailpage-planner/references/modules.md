# 와이어프레임 모듈 (상세페이지 부품)

Design 캔버스에서는 아래 인라인 스타일을 그대로 쓰고, 폴백 빌더에서는 `blocks`의 `m` 값(괄호 안 이름)으로 쓴다.
공통: 본문 폭 780px, 글자 22~82px, 이미지 자리는 **글자 없는 검은 박스(#111)**(설명·비율·[IMG] 표기 없음), **모든 글자는 문장으로 채운다(대괄호 자리표시 금지).**
배경 톤(섹션 루트): `#fff` / `#f1f1f1` / `#dcdcdc` / 진한 `#222`(흰 글씨) / 전체 이미지 `#111`(흰 글씨).

## 텍스트 모듈
- **eyebrow** (`text`): `<div style="font-size:22px;font-weight:700;letter-spacing:.06em;border:2px solid #111;border-radius:999px;padding:4px 22px">POINT 01</div>`
- **headline** (`text`, `size`: xl 82 / lg 64 / md 48): `<h2 style="margin:0;width:100%;text-align:center;font-size:64px;line-height:1.25;font-weight:800;white-space:pre-line">작아도 알찬<br>…</h2>`, 강조 키워드는 `<span style="background:#cdcdcd;padding:0 8px">3가지</span>` (진한 배경에서는 `rgba(255,255,255,.28)`). 빌더에서는 `**키워드**`.
- **sub** (32px #555 가운데), **body** (26px #333), **footnote** (22px #666 가운데; 수치·출처·기준 시점)

## 이미지 모듈
- **image** (`label`, `ratio`, `gif`, `bleed`): **글자 없는 검은 박스.** `label`은 구성표·기획용 메모일 뿐 캔버스에는 표시되지 않는다. 폭 780 기준 높이 16:9=439, 3:2=520, 4:3=585, 1:1=780, 3:4=1040.
- **photo_grid** (`cols` 2/3, `items[{label,caption}]`): 검은 박스 + 아래 캡션(22px). 2열은 폭 382, 3열은 폭 249, 간격 16.
- **steps** (`items[{title,text}]`): 가로 줄 하나에 검은 이미지(380×285) 왼쪽 + 라벨 STEP n(알약) + 제목 32 + 설명 26.
- **callout** (`label`, `items` 4개): 검은 1:1 박스 위 모서리 4곳에 흰 알약 라벨(24px 굵게)을 올려 제품 도해를 표현.
- **cert_grid** (`n`): 3열 3:4 검은 박스(글자 없음) + 아래 22px 확인 문구.
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
- **reviews** (`items[{title,text}]`): 카드, 별점·작성자 22px + 인용형 제목 32px + 본문 26px. 입력된 후기가 있으면 그대로, 없으면 샘플 후기(실명·실존 인물 없이 "구매자" 호칭)로 채우고 `sample`에 적는다.
- **qa** (`items[{q,a}]`): `Q.` 32px 굵게 + 답변 26px.
- **notice_rows** (`items[{title,text}]`): 왼쪽 검은 아이콘 96px + 제목 22px + 안내 26px (보관·주의·배송·교환·환불).
- **cta_band** (`text`): 가로 전체(860) 검은 띠 + 흰 글씨 32px 굵게. 웹 버튼 대신 쓴다.

## 조립 예
히어로 = eyebrow → headline(xl) → badges → sub → image(3:2), 배경은 전체 이미지.
POINT = eyebrow(POINT 01) → headline → image 또는 chart 또는 photo_grid → body → icon_row/tip → footnote.


## 레이아웃 모듈 (가로 분할·교차·이미지 위 글자 등)

모든 섹션이 "가운데 제목 → 세로로 쌓기"가 되지 않도록 쓰는 구조 모듈이다. 섹션 제목(headline)은 가운데 정렬을 유지하고, 모듈 안의 소제목·본문은 왼쪽 정렬이다.

| 모듈 | 구조 | 필드 | 어울리는 내용 |
|---|---|---|---|
| **split** | 사진(폭 380) + 설명 가로 배치. 소제목 40px, 본문 26px, 불릿 | `label`, `ratio`(3:4 등), `side`(left/right), `eyebrow`, `title`, `text`, `items` | 사진 한 장에 설명 2~4줄 |
| **zigzag** | split을 좌우 번갈아 반복 | `items[{label, ratio, title, text, items}]` | 항목 2~4개, 각각 사진이 있는 설명 |
| **overlay** | 검은 이미지 박스 위에 글자(제목·서브)를 얹음 | `label`, `ratio`, `title`, `sub`, `align`, `valign`, `size` | 사진 한 장으로 분위기·대표 메시지를 강하게 |
| **circle_row** | 원형 이미지 3개(지름 240) + 제목 + 22px 캡션 | `items[{label, title, text}]` | 원료·구성·환경처럼 대표 3가지 |
| **stat_rows** | 가로 줄마다 왼쪽 큰 문구(48px), 오른쪽 작은 설명(22px), 위아래 굵은 선 | `items[{claim, data}]` | 가격표, 수치·순위처럼 "큰 값 + 작은 설명" |
| **timeline** | 세로선과 번호 원, 제목 32px + 설명 | `items[{title, text}]` | 이미지 없는 절차·과정 |
| **numbered_list** | 큰 번호(64px) + 제목 + 설명, 줄 구분선 | `items[{title, text}]` | 순서가 있는 안내, 편집 느낌 |
| **ticker** | 가로 전체 띠에 키워드를 · 로 나열 | `items`, `invert` | 구분선 역할, 핵심 키워드 요약 |
| **quote** | 큰 따옴표 + 48px 문장 | `text`, `who` | 한 줄 선언, 인용 |
| **two_col** | 2열 소제목 + 본문(위에 굵은 선) | `items[{title, text}]` | 두 가지 유형 비교 설명 |
| **index** | 큰 번호(82px) + 굵은 선 | `text` | 섹션 번호 강조 |

- **image에 `bleed: true`**를 주면 좌우 여백 없이 가로 860px 전체 폭 이미지가 된다.
- 생성기는 이 모듈들의 높이를 계산해 보드 높이를 정한다. 내용이 짧아 하단이 비면 경고를 낸다.
- 폴백 HTML 빌더(`build_wireframe.py`)는 같은 모듈을 단순한 형태로 보여 준다.


## 항목 개수에 따라 레이아웃이 바뀌는 모듈

특징·구성·장점처럼 **같은 비중의 항목을 나열할 때는 개수에 맞춰 `feature_set`을 쓴다.** `icon_row`(4칸 고정 느낌)나 `icon_cards`(세로 쌓기)에 개수를 억지로 맞추지 않는다. 입력된 특징 개수가 2개든 7개든 그 개수 그대로 쓰고, 4개로 맞추지 않는다.

`{"m":"feature_set","items":[{"title","text","label(사진을 넣을 때 표시, 선택. 캔버스에는 글자가 없는 사진 박스로만 나온다)"}], "style":"icon|image|number(선택)", "layout":"자동 선택을 덮어쓸 때만"}`

| 항목 수 | 자동 레이아웃 |
|---|---|
| 1개 | 가로로 넓은 대표 카드 |
| 2개 | 큰 사진 카드 2열 (3:4) |
| 3개 | 3열 사진 카드(글이 짧을 때), 글이 길면 번호 리스트 |
| 4개 | 2×2 카드 |
| 5개 | 대표 1개(전체 폭) + 2×2 |
| 6개 | 3×2 소형 카드(글이 짧을 때), 길면 2열 3줄 |
| 7개 | 대표 1개 + 3×2 소형 카드 |
| 8개 | 2×4 카드 |
| 9개 이상 | 큰 번호 리스트 |

- 항목이 3개 이하이면 사진 카드(큰 이미지 자리)로 채워 섹션이 비어 보이지 않게 한다. 4개 이상은 아이콘 카드이고, 사진이 필요하면 항목에 `label`을 준다.
- `photo_grid`도 `cols`를 생략하면 개수에 맞춰 열 수를 정한다. (2·4·5·7·8개는 2열, 3·6·9개는 3열)
- `icon_row`는 개수에 따라 열 수를 맞춘다. (4개 이하는 개수만큼, 5·6개는 3열, 7개 이상은 4열)


## 비주얼 섹션 구성 요소 (상단 카피 + 로고 + 하단 픽토그램 바)

| 모듈 | 구조 | 필드 |
|---|---|---|
| **logo** | 흰 윤곽선의 작은 정사각형 자리(96px, 안에 `LOGO`). 서브 문구 위에 중앙 배치 | `text`(선택) |
| **pictogram_bar** | 화면 맨 아래 흰 바(폭 860). 칸마다 검은 아이콘 자리(64px) + 작은 문구(22px) + 굵은 값(22px), 칸 사이 세로선. 칸 수 = 주요 특징 개수(6칸까지 한 줄, 7~8칸은 4칸씩 두 줄) | `items[{label, value}]` |

비주얼 섹션 블록 순서: `logo` → `sub`(작은 서브) → `headline`(size xl) → `sub`(한 줄) → `pictogram_bar`(선택).
- `pictogram_bar`는 어디에 적어도 섹션 맨 아래에 붙는다. 칸 문구는 짧게(칸당 6자 안팎: 용량·가격·인증·사용법 같은 핵심 키워드).
- 비주얼 섹션의 `valign`을 `"middle"`로 주면 상단 정렬 대신 가운데 정렬이 된다(특별한 경우에만).


## entries 모듈 (레이아웃을 무작위로 정하는 목록)

`{"m":"entries","kind":"features|steps|prices|options|reasons","items":[{"title","text","label(선택)","points(선택: 좌우 교차에서 불릿)"}],"lead_image":"(선택) 전체 폭 이미지 자리","lead_title":"(선택) 이미지 위 글자용 제목","lead_text":"(선택)","image_label":"(선택) 분할·오버레이 사진 자리","allow":["후보를 줄일 때만"],"pattern":"고정할 때만"}`

| 패턴 | 이름 | 조건 |
|---|---|---|
| cards | 카드 격자(개수에 맞춰 자동) | 2~8개 |
| zigzag | 좌우 교차 | 2~4개 |
| timeline | 세로 타임라인 | 2~5개, 단계·특징·이유 |
| numbered | 큰 번호 리스트 | 2~6개 |
| circles | 원형 사진 | 3개 |
| datarows | 데이터 행 | 2~5개, 특징·가격·옵션·이유 |
| photogrid | 사진 그리드 | 2~6개 |
| splitlist | 가로 분할 + 목록 | 2~5개 |
| duo | 2열 대비 | 2개 |
| checklist | 체크 목록 | 3~6개, 글이 짧을 때 |
| overlaycards | 이미지 위 글자 + 카드 | 2~4개, `lead_title` 있을 때 |

- 생성기가 시드와 섹션별 선택 결과(`레이아웃 - P4 Point: 타임라인`)를 출력한다. 사용자에게 알린다.
- 항목 문구는 어떤 패턴에서도 어색하지 않게 한 문장 안팎으로 쓴다.
