# 섹션 유형과 장수별 구성안

STEP 3에서 구성표를 만들 때 사용한다. 각 섹션은 `detailpage-anatomy.md`의 해부 틀(라벨 → 제목 → 문구 → 비주얼 모듈 → 각주)을 따르고, 모듈은 `modules.md`에서 고른다. 구분이 레이아웃을 정한다.
- 비주얼: 섹션 전체 배경이 연출 이미지(검은 박스), 글자는 흰색
- 정보: 회색 톤 배경(흰/연회색/중간/진한 교대), 검은 이미지 박스 포함

## 장수별 기본 뼈대 (중립 기본값, 그대로 쓰지 않는다)

**이 표는 어떤 섹션이 들어가는지의 기본값일 뿐이다. 순서와 강조는 `planning-logic.md`의 "제품에 맞게 순서·강조·레이아웃 정하기"로 반드시 재배치한다.**

| 장수 | 구성 (V = 비주얼) |
|---|---|
| 8장 | Hero(V) → Trust → Pain(끝에 새로운 생각 한 줄) → Point 1 → Point 2 → Proof → How-to → Info |
| 10장 | Hero(V) → Trust → Pain → Cause → Point 1 → Point 2 → Point 3 → Proof → How-to → Info |
| 12장 | Hero(V) → Trust → Pain → Cause → Point 1 → Point 2 → Point 3 → Proof → How-to → Review → Brand(V) → Info |
| 15장 | Hero(V) → Trust → Pain → Cause → Point 1 → Point 2 → Point 3 → Point 4(V, 대형 문구) → Proof → How-to → Review → Why → Brand(V) → Info → Notice |

- 와디즈를 언급했다면 Maker(메이커 소개)를 Proof 뒤에 넣고 한 장 늘어난다고 알린다. Notice도 권한다.
- 서비스·강의: How-to는 진행 과정, Proof는 수강생 결과로 바꾼다.
- 8~10장은 마지막 Info 섹션 끝에 구매 띠 배너를 넣는다. 12장 이상은 Brand 끝에 넣는다.

## 섹션별 구성 (위 → 아래 모듈)

| 유형 | 구분 | 모듈 순서 | 배경 | 쓰는 사실(입력된 것만) |
|---|---|---|---|---|
| Hero | 비주얼 | logo → sub(작은 서브) → headline(xl) → sub(한 줄) → pictogram_bar(주요 특징 개수만큼, 선택) | 전체 이미지 | 로고, 칸 문구 사실 |
| Trust | 정보 | eyebrow → headline → icon_row 4 → icon_cards 3 | 연회색 | 특징 |
| Pain | 정보 | headline → bubbles 4 → photo_grid 3열(상황 컷+캡션) → sub(원인 한 줄) | 흰색 | - |
| Cause | 정보 | headline → vs(흔한 생각 → 새로운 생각) → image | 중간 회색 | - |
| Point n | 정보 | eyebrow(POINT 0n) → headline → 비주얼 모듈 하나(image / chart / photo_grid / callout) → body → icon_row 또는 tip → footnote | 흰/연회색 교대 | 사실·수치 |
| Point 4 | 비주얼 | sub → headline(대형 문구) → sub → pictogram_bar(선택) | 전체 이미지 | 근거 |
| Proof | 정보 | headline(md, 순위·인증 메시지 크게) → footnote(수치·출처 22px) → percent_bars → cert_grid 또는 reviews | 진한 회색 | 실제 수치·출처 |
| How-to | 정보 | eyebrow(HOW TO USE) → headline → steps 3 → image(GIF) | 연회색 | 사용 방법 |
| Review | 정보 | headline → reviews 3~4 | 흰색 | 실제 후기 |
| Why | 정보 | headline → checklist 5 | 연회색 | - |
| Brand | 비주얼 | logo(선택) → sub → headline → sub → pictogram_bar(선택). 이전 → 이후를 말하려면 vs를 상단 카피 아래에 | 전체 이미지 | - |
| Info | 정보 | headline → spec_table → notice_rows(보관·주의) → qa → footnote(법적 안내) → (cta_band) | 흰색 | 실제 스펙·안내 |
| Notice | 정보 | headline → notice_rows(배송·교환·환불·AS·문의처) → footnote | 연회색 | 실제 안내 |
| Maker | 정보 | headline → image(실물 사진 1:1) → body → icon_cards | 흰색 | 메이커 소개·이력 |

각 섹션은 세로 1200px 이상이 되도록 모듈을 채운다(내용이 모자라면 비주얼 모듈을 늘린다).


## 추가 유형 (제품 분석 결과에 따라 쓴다)

| 유형 | 구분 | 모듈 순서 | 쓰는 경우 |
|---|---|---|---|
| Offer | 정보 | headline → checklist(구성·혜택) → photo_grid(구성품 컷) → spec_table(가격·구성) → cta_band | 가격·혜택형, 세트·보조금 안내가 핵심일 때 |
| Option | 정보 | headline → photo_grid 2열(컬러·사이즈·맛 컷 + 캡션) → tip(고르는 팁) → spec_table | 감성·디자인형, 옵션이 구매 결정을 좌우할 때 |
| Compare | 정보 | headline → vs 또는 chart(타사·이전 대비) → footnote(기준·출처) | 경쟁 대비가 강점일 때 (근거 자료 필수) |
| Story | 정보 | headline → 단계 나열(steps 또는 bubbles) → image | 서비스·전문가형, 브랜드 배경이 중요할 때 |

Point는 한 섹션에 강점 하나를 담고, 담는 내용에 따라 모듈을 다르게 고른다(`planning-logic.md` 5번 표).


## 비주얼 섹션의 공통 구성
비주얼 섹션(Hero, Brand, 대형 문구 Point)은 모두 **연출 이미지 전체 배경 + 상단 카피(로고·서브·메인 카피·서브) + 하단 픽토그램 바(선택)** 구성이다. 하단 바의 칸 수는 주요 특징 개수와 같다. 자세한 규칙은 `wireframe-canvas.md` 7번, 모듈은 `modules.md`.
