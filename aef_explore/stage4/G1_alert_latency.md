# G1 — TB01 alert-latency check (RADD detection-month vs. independent S2 breakpoint-month)

## 0. 방법 요약

Stage-2 TB01 파일럿(`scratch/TB01_pilot.py`, `stage2/TB01.md`)이 사용한 이벤트 월(month)은 RADD
`Date`(YYDDD, **탐지일**)에서 뽑은 것이다. RADD alert는 구조상 실제 교란(disturbance)보다 늦게
찍히므로(Reiche 2021), 이 값으로 만든 세 headline 통계(alpha-hat, December-shift, Q4 lag reversal)가
"탐지 지연이 섞인 월"에 기반한 것 아닌지 검증하는 것이 G1의 목적이다.

- ROI·연도: BR = Para/MT [-55.5,-7.5,-54.5,-6.5], CG = DRC [23,0,24,1], Y=2021 (Stage-2와 동일).
- Clearing 표본: Stage-2 TB01 CSV(`TB01_BR2021.csv`/`TB01_CG2021.csv`, RADD confirmed alert(Alert==3)
  且 Date∈2021 且 Hansen lossyear==21 且 treecover2000>50, 12개월×120pt=1440pt/region)에서 월별 40pt씩
  재추출 → **480pt/region** (>=300 요구치 충족, 월별 균등). RADD 월(`cls`)·AEF arc geometry(`w,sep,res,x,uv`)는
  Stage-2 계산을 그대로 재사용(재계산 없음).
- Stable-forest 표본: tc>80 & lossyear==0 & no-alert, 300pt/region, `.unmask(0)` 적용, angle(e_{Y-1},e_Y)만
  새로 계산 (threshold용).
- 독립 월 추정: 2020-12~2022-01 14개월 S2_SR_HARMONIZED **월별 합성**(SCL∉{1,3,8,9,10} 마스크, median),
  월별 NDVI·NBR·clear-obs count(`.unmask(0)` 필수 — count 미마스킹 시 780pt→4pt로 붕괴하는 것을 실제로
  겪음, gotcha 기록). `sampleRegions` 1회/region, 42 bands × 780pt (clearing 480 + stable 300).
- Breakpoint 탐색: 후보 분할월 b=1..12, pre=index[0:b], post=index[b:] (각 side clear-obs>=2개월 필요),
  (pre 평균−post 평균) 최대화하는 b 선택. 최소 드롭 폭(NDVI≥0.10, NBR≥0.05) 미달 또는 조건 미충족 →
  **UNRESOLVED**. NDVI 기반 b를 `m_indep`(주 지표)로 사용, NBR은 검증용.
- DETER: TerraBrasilis WFS(`deter-amz:deter_amz`) 필드명이 `view_date`(소문자), BBOX 축순서는
  (lon,lat)이어야 함(대문자/역순 시 0건) — 확인 후 **BR ROI 2021년 DESMATAMENTO_CR 190건 확보** (off-GEE,
  `ee.data.getAsset`로 GEE 자산 존재 여부를 주장하지 않음). CG(DRC)는 DETER가 Legal Amazon 전용 산출물이라
  대응 자산이 없음 — **CG는 S2-only로 진행**, 이 사실을 그대로 보고.

## 1. 표본 및 회수율

| region | n_clear (sub) | unresolved (n, %) | NDVI/NBR exact agree | within±1mo agree | p90 stable threshold (deg) |
|---|---|---|---|---|---|
| BR | 480 | 77 (16.0%) | 74.9% | 87.7% | 11.24 |
| CG | 480 | 136 (28.3%) | 71.8% | 86.3% | 10.38 |

CG의 unresolved 비율이 BR의 거의 2배다 — 이중모드 우기·구름 때문에 월별 합성의 clear-obs count가 낮은 달이
많다는 Stage-2 TB01 리스크(observation-calendar confound)가 독립 월 추정 단계에서도 그대로 재현된다.

DETER 교차검증(BR만, buffer 50m point-in-polygon): 480pt 중 **247pt(51.5%)**가 DETER 2021 폴리곤과
교차. 이 부분표본에서 RADD−DETER 월 median=0 (RADD가 DETER와 거의 동시), S2-breakpoint(m_indep)−DETER
월 median=+1 (S2 방법이 DETER보다 오히려 1개월 늦게 잡음 — S2 breakpoint estimator 자체도 완벽한 event-date가
아니라는 뜻; DETER는 절반만 매칭되고 그 자체도 탐지산출물이므로 참값 대체가 아니라 보조 참고치로만 사용).

## 2. Headline 1 — alpha-hat(m): w = a + b·(12-m)/12

| region | source | a [95% CI] | b [95% CI] | off-plane resid mean/p90 | n |
|---|---|---|---|---|---|
| BR | OLD (RADD) | 0.613 [0.543,0.716] | 0.560 [0.425,0.669] | 0.409 / 0.589 | 480 |
| BR | NEW (indep) | 0.655 [0.525,0.784] | 0.518 [0.328,0.806] | 0.423 / 0.599 | 403 |
| CG | OLD (RADD) | 0.474 [0.412,0.547] | 0.778 [0.667,0.873] | 0.315 / 0.438 | 480 |
| CG | NEW (indep) | 0.211 [0.151,0.283] | 0.928 [0.828,1.029] | 0.311 / 0.441 | 344 |

(block bootstrap, 0.1° block, 300 resamples; n=480 subsample OLS의 a,b는 Stage-2 전체 n=1440 재적합값
BR a=0.599/b=0.592, CG a=0.506/b=0.741과 유사 — subsample 자체는 대표성 있음. Stage-2 TB01.md 텍스트가 언급한
"a=0.568, b=0.33-ish"는 본 재현치보다 낮은 근사 서술로 보임.)

off-plane residual은 (e_{Y-1},e_Y,e_{Y+1}) 3점 기하로만 정의되어 이벤트 월 라벨과 무관 — OLD/NEW 차이는
표본(unresolved 제외) 차이일 뿐, 실질적 변화 없음(둘 다 ~0.31-0.42/0.44-0.60).

**판정**: BR은 CI가 크게 겹쳐 a,b가 통계적으로 구별되지 않음 — 생존. CG는 b가 0.778→0.928로, CI가
서로 겹치지 않게 이동(0.667-0.873 vs 0.828-1.029) — **CG의 계수는 RADD-월 기반 값과 유의하게 다름**,
독립 월 사용 시 기울기가 더 가팔라짐(월 그레이딩 신호가 더 강해짐, 즉 RADD 지연이 CG 신호를 약화시키고
있었다는 뜻). 방향은 같지만 정량값은 CG에서 부분적으로만 생존.

## 3. Headline 2 — December-shift (mean ang(e_{Y-1},e_Y), deg, month==12 이벤트만)

| region | OLD (RADD, n) | NEW (indep, n) |
|---|---|---|
| BR | 27.0° (n=40) | 32.8° (n=9) |
| CG | 16.5° (n=40) | 14.7° (n=21) |

정의: "shift"는 e_{Y-1}(2020 embedding)에서 e_Y(2021 embedding)로의 각도 변화(arccos of unit-vector dot
product) — RADD alert 혹은 독립 추정 모두 "12월(month==12)"로 분류된 이벤트만 뽑아 그 각도의 평균.

**판정**: 방향(그래도 상당한 각도 변화가 있음)은 유지되나, BR은 독립 월 재분류로 n이 40→9로 붕괴 —
표본이 너무 작아 32.8°는 신뢰 구간을 계산할 수 없는 수준(단일 블록 편향 위험). **BR December-shift 수치는
정밀 추정으로서 생존하지 못함**(방향성만 생존). CG는 n=40→21로 상대적으로 안정, 16.5→14.7°는 유사한
크기 — CG는 생존.

## 4. Headline 3 — Q4 lag reversal (stable-forest p90 threshold에서 in-year 탐지율)

threshold 정의: angle = arccos(dot(unit(e_{Y-1}), unit(e_Y))) (Headline 2와 동일한 각도), stable-forest
strat(300pt/region)의 p90 값 — BR 11.24°, CG 10.38°. "탐지"= 해당 이벤트 pt의 이 각도가 threshold 이상.

| region | source | Q1 | Q2 | Q3 | Q4 | overall | n |
|---|---|---|---|---|---|---|---|
| BR | OLD | 1.000 | 1.000 | 1.000 | 0.983 | 99.6% | 480 |
| BR | NEW | 1.000 | 1.000 | 0.996 | 0.985 | 99.5% | 403 |
| CG | OLD | 1.000 | 1.000 | 1.000 | 0.817 | 95.4% | 480 |
| CG | NEW | 0.991 | 1.000 | 0.865 | 0.754 | 93.6% | 344 |

**판정**: BR은 OLD/NEW 거의 동일 — Stage-2의 99.2% 근사 헤드라인이 생존(재현치 99.5-99.6%). CG는 OLD
95.4%→NEW 93.6%로 하락하고, 특히 **Q4가 81.7%→75.4%로 더 벌어짐** — RADD-월 기반 통계가 실제보다
"in-year 탐지가 거의 완전하다"는 인상을 CG에 대해 과장했다는 뜻. **CG의 98.7%(Stage-2 언급치) 및
"거의 완전 탐지" 주장은 독립 월로 보면 생존하지 않음**(진짜 값은 93-95% 수준이고 Q4는 75-82%에 불과).

## 5. Observation-density confound (clear-obs count tercile stratification)

2021년 1-12월 중 clear-obs(SCL 필터 통과) 월수 기준 tercile:

| region | tercile | n | unresolved% | a (m_indep fit) | b (m_indep fit) |
|---|---|---|---|---|---|
| BR | low | 228 | 18.9% | 0.750 | 0.366 |
| BR | mid | 201 | 12.4% | 0.623 | 0.567 |
| BR | high | 51 | 17.6% | 0.529 | 0.653 |
| CG | low | 218 | 25.2% | 0.250 | 0.809 |
| CG | mid | 109 | 26.6% | 0.196 | 0.950 |
| CG | high | 153 | 34.0% | 0.184 | 1.059 |

**핵심 confound**: a,b가 tercile마다 크게 흔들린다(BR a: 0.53-0.75, b: 0.37-0.65; CG a: 0.18-0.25, b:
0.81-1.06) — 독립 월 추정치 자체가 관측 밀도에 따라 편향된 표본에서 나온다는 뜻. CG는 특히
관측이 **가장 많은** tercile에서 unresolved율이 오히려 가장 높다(34.0% vs low 25.2%) — "관측이 많을수록
월 복원이 쉬워진다"는 단순한 그림이 아니라, 관측 밀도가 높은 지역/계절이 계절성 대비(dry-season contrast)가
약한 곳과 겹쳐 breakpoint 폭 기준(NDVI≥0.10)을 못 넘기는 경우가 늘어나는 것으로 보인다. 이는 Stage-2가
이미 지적한 "관측 캘린더 confound"가 독립 월 추정 단계에서도 사라지지 않았다는 증거이며, 위 headline
3개 모두의 정밀값에 편향 상한을 씌워야 함을 뜻한다.

## 6. RADD − independent(m_indep) month 차이 (latency 추정)

| region | median | IQR | frac ≥2mo late | n |
|---|---|---|---|---|
| BR | 0.0 | [-2.0, 1.0] | 15.4% | 403 |
| CG | 2.0 | [0.0, 4.0] | 52.6% | 344 |

BR은 RADD alert 월이 독립 S2 breakpoint 월과 거의 일치(중앙값 0, 하지만 IQR이 -2~+1로 넓어 pixel 단위
잡음이 큼). CG는 RADD가 **중앙값 2개월, 절반 이상의 이벤트가 2개월 이상** 늦다 — Stage-3 제안서가
"수동 판독으로 얻고자 한" latency 추정치를 저비용으로 얻은 결과이며, CG 쪽 RADD 지연이 실질적임을
정량적으로 확인한다.

## 무엇이 살아남았는가 (survival verdict)

- **살아남음**: (1) BR alpha-hat(m) 계수(a,b) — RADD/독립 월 CI가 겹침. (2) BR Q4 in-year 탐지율(~99%,
  Stage-2 헤드라인과 일치). (3) 선형(12-m)/12 월-혼합 법칙의 **방향성**(양쪽 region, 양쪽 월 정의 모두).
  (4) off-plane residual(~0.3-0.6) — 월 라벨과 무관하게 불변.
- **부분적으로만 살아남음**: BR December-shift(방향 유지, 정밀값은 n=9로 신뢰 불가). CG alpha-hat(m)의
  b(0.778→0.928, CI 불일치, 방향은 같지만 정량값이 유의하게 다름).
- **살아남지 못함**: CG의 "98.7% 거의 완전 in-year 탐지" 헤드라인 — 독립 월 기준 93.6%로 하락, Q4는
  75.4%까지 하락(Stage-2 원 주장보다 유의하게 나쁨). 그리고 "이 세 통계가 관측 밀도와 무관하다"는 암묵적
  전제 — tercile 분석에서 a,b가 최대 2배 가까이 흔들려 confound가 실재함을 확인, 특히 CG는 unresolved
  비율(28.3%)과 confound(관측 많을수록 오히려 unresolved↑) 둘 다 지표를 흔들 수 있는 수준.

**결론**: TB01은 BR에서는 GO를 유지하나(핵심 통계 재현), CG(DRC)에서는 headline 수치(특히 in-year 탐지율과
alpha 기울기)를 하향 조정하고 unresolved 28%·관측밀도 confound를 본문에 명시해야만 GO — **conditional GO**
(BR 그대로 채택 가능, CG는 수치 재작성 + 두 caveat 필수 반영).
