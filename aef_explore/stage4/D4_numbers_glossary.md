# D4 — Numbers Glossary: `04_final_ranking.md`에 등장하는 모든 metric의 정의

목적: `04_final_ranking.md`에 나오는 모든 실측치가 정확히 무엇의 estimator인지, denominator가 무엇인지, 어떤
population/fold/block에 대해 평균낸 것인지를 `stage2/<ID>.md` · `stage3/<ID>.md` · `scratch/*.py` 코드까지
추적해 확정한다. GEE 재실행 없이 기존 코드와 로그만으로 재구성했다.

---

## 0. 공통 primitive (모든 topic이 공유)

| 이름 | 정의 |
|---|---|
| **AEF embedding vector** | `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`의 64-D 픽셀 벡터(A00-A63). 카탈로그 스펙상 unit-norm이라고 가정되지만, 어떤 pilot 코드도 `‖e‖=1`을 직접 검증하지 않는다(→ §12 ambiguity 참고). |
| **Angular distance (angular drift)** | `ang(A,B) = arccos(clip(A·B, -1, 1)) × 180/π` [degree]. `A,B`는 같은 픽셀의 서로 다른 연도 AEF 벡터. `aefkit.py:21-23`의 `angle()`이 표준 구현이며, 정규화를 다시 하지 않고 raw dot product를 그대로 arccos에 넣는다 — 즉 "AEF 벡터가 이미 unit-norm"이라는 가정에 전적으로 의존한다. |
| **S2 baseline의 등가 벡터** | Sentinel-2 median composite 밴드(B2,B3,B4,B8,B11,B12)+NDVI(+NBR)를 표준화 후 L2-normalize하거나(TB01), 표준화 없이 raw reflectance를 L2-normalize(TB02/TE02)해서 만든 unit vector. **주의: topic마다 S2 벡터 구성이 다르다** — 모든 topic이 "동일한 S2 baseline"을 쓴다고 착각하면 안 된다(§12). |
| **Spatial block CV** | `blocks(df,size=0.1)` = `floor(lon/0.1)_floor(lat/0.1)` 문자열 키 (≈11 km grid cell). `GroupKFold(n_splits=5)`의 group으로 사용. `probe()`는 분류면 `LogisticRegression(class_weight='balanced')` 후 이진이면 AUC, 다항이면 balanced accuracy; 회귀면 `Ridge(alpha=1)` 후 R². |
| **"±sd" 표기의 실체** | `04_final_ranking.md`의 거의 모든 "mean±sd"는 **5-fold GroupKFold의 fold 간 표준편차**(fold sd)이다. Block-bootstrap CI가 아니다. Block-bootstrap CI는 Stage-3 제안서에서 "하겠다"고 적힌 계획이며, 읽은 모든 pilot 스크립트에서 실제로 계산된 사례는 없다(TA04/TC01/TE06/TB01/TB02/TE02/TD01/TH01/TH03 전부 확인). |
| **stable-forest / stable stratum percentile threshold** | "p90 threshold", "5%-calibrated threshold"는 모두 **"reference(안정) population의 특정 연도군에서 계산한 각도의 백분위수를 change-detection 임계값으로 쓴다"**는 같은 아이디어의 변형이다. 그러나 topic마다 (i) 백분위(90 vs 95), (ii) reference population의 정의, (iii) 각도 정의(1-yr drift vs 2-yr endpoint separation vs ROI-specific)가 다르다 — 절대 숫자를 topic 간에 바로 비교하면 안 된다(§12에서 상세 비교표 제공). |

---

## 1. TB01 (GO) — within-year event timing / detection lag

| Metric (04 표기) | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference/chance | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **mixing weight w(m)** | `w = arccos(clip(dot(e_{Y-1},e_Y),-1,1)) / arccos(clip(dot(e_{Y-1},e_{Y+1}),-1,1))` — pre→event 각도를 pre→post 총 각도로 나눈 비율(0~1을 초과할 수도 있음). `TB01_pilot.py:41-45`(`wres`). | 무차원 | pixel별 계산, n=1440/region(120px×12개월) | 픽셀 단위 산식, fold 없음. `w(m)=a+b·(12-m)/12` OLS 적합의 a,b는 회귀식으로 명시되어 있으나 **pilot 코드 어디에도 이 OLS 적합을 직접 실행한 스크립트가 없다** — stage3 문서의 사후 서술로 보임. | seed H1: `a=0,b=1` | `stage3/TB01.md` RQ1; `TB01_pilot.py` | `tb01_p1.py`는 다른 barycentric 통계(`alpha`)를 계산 — `w`와 혼동 금지 |
| **intercept a≈0.568** | 12월(m=12)에서의 평균 w 값(≈Dec mean w=0.57)로 보이며, 정식 OLS 적합 산출물이라는 근거 스크립트는 못 찾음 | 무차원 | month=12 stratum, n≈120/region | group mean, sd는 pixel 분산(fold sd 아님) | seed 예측 a=0 | `stage2/TB01.md` L20 | a,b를 만든 정식 회귀가 코드에 없음(§12) |
| **off-plane fraction (0.31–0.41)** | `res=sqrt(max(0,1-inpl))`, `inpl=(x²-2xy·uv+y²)/(1-uv²)`, x=cos(e_{Y-1},e_Y), y=cos(e_Y,e_{Y+1}), uv=cos(e_{Y-1},e_{Y+1})` — year-Y 벡터가 pre/post 두 점을 지나는 great-circle geodesic 평면에서 벗어난 정도(0=평면 위, 1=완전히 벗어남) | 무차원[0,1] | clearing pixel만, n=1440/region | mean/p90, fold 없음 | H1 반증 기준: CI가 0.15 초과 | `TB01_pilot.py:41-44` | "0.31–0.41이 벡터의 31–41%"라는 식으로 읽으면 오류 — norm 비율이 아니라 구면기하학적 이탈도 |
| **endpoint separation (clearing 48.7°/39.2° vs stable 9.2°/6.5°)** | `sep=arccos(dot(e_{Y-1},e_{Y+1}))` = 2년 전체 geodesic span | degree | clearing 전체 vs stable(`tc>80&no loss&no alert`) | mean + p10/p90, fold 없음(descriptive) | — | `TB01_meta2.py` | — |
| **stable-forest p90 threshold(TB01, 11.4°/8.9°)** | 안정림(`tc>80&lossyear=0&Alert=0`) 픽셀의 `sep=arccos(dot(e_{Y-1},e_{Y+1}))`(2년 span) 분포에서의 90th percentile, Y=2021만 | degree | stable 전체 population(BR≈1.95M, CG≈2.82M @60m) | percentile, fold 없음 | — | `TB01_meta2.py:25-26` | **정합성 문제**: threshold는 2-yr span(sep) 위에서 계산됐는데 99.2%/98.7% detection rate는 1-yr span(`aY=arccos(dot(e_{Y-1},e_Y))`)을 그 threshold와 비교한다고 서술됨 — 서로 다른 각도 정의를 교차비교(§12) |
| **당해연도 detection rate (99.2%/98.7%)** | 2021년 clearing pixel 중 `aY`가 stable p90 threshold를 넘는 비율 | % | num=threshold 초과 clearing px, denom=전체 clearing px(n=1440/region) | pooled fraction | threshold=stable p90 | `stage2/TB01.md` L24 | 월별 detection-rate curve(진짜 "Q4 reversal"의 직접 증거)는 어느 로그에도 없음 — 12월 평균 각도(27.0/16.4°)가 threshold를 넘는다는 것으로부터의 간접 추론 |
| **December-shift (27.0°/16.4°)** | month=12로 라벨된 clearing pixel들의 평균 `aY=arccos(dot(e_{Y-1},e_Y))`(BR/CG 각각) | degree | month=12 stratum, n≈120/region | group mean, CI 없음 | 비교 대상은 같은 region의 stable p90 threshold(11.4°/8.9°) | `stage2/TB01.md` L24 | "BR vs CG 이동"이 아니라 **각 region 내부에서 12월 사건 vs 그 region의 threshold**를 비교하는 두 개의 별개 숫자 |
| **Q4 detection-lag reversal** | 정성적 결론: Dec 사건도 threshold를 훨씬 초과 → lag가 사건월에 거의 의존하지 않음 | — | 위와 동일 | 위와 동일 | H2(단조 지연) vs H2'(reversal) | `stage3/TB01.md` RQ2 | 월별 정량 curve 부재, 현재는 간접 증거 |
| **calibration MAE (0.418/0.396 vs S2 0.787/1.117)** | `mean(|w - (12-m)/12|)` — seed geodesic law에 대한 goodness-of-fit(예측 모델의 held-out 성능이 아님) | w-unit(무차원) | n=1440/region, clearing pixel만 | pooled 점추정, CV/fold 없음 | — | `TB01_pilot.py:59` | 학습/평가 분리가 없는 in-sample fit — "예측 정확도"로 오독 금지 |
| **Spearman ρ(month,w) = -0.634/-0.574** | month과 w의 순위상관 | 무차원[-1,1] | n=1440/region | pooled, CV 없음 | S2: -0.573/-0.382 | `TB01_pilot.py:57-59` | — |
| **block-level ρ (mean -0.34 sd0.27, n=17 / mean -0.47 sd0.25, n=27)** | 0.1° block별로 따로 계산한 ρ(month,w)의 block간 평균/표준편차(block ≥25px, ≥5개월) | 무차원 | BR 17 block, CG 27 block | block-level mean/sd(사실상 block-bootstrap과 유사하지만 resampling이 아니라 실제 disjoint block 집계) | — | `stage2/TB01.md` L23 | block별 부호가 [-0.91,+0.06]까지 뒤집힘 → 저자들도 pixel-level 예측력은 주장하지 않고 population-level(0.1°/분기) estimator로 scope를 한정 |
| **partial Spearman(관측밀도·burn date 통제)** | Stage-3 계획: burn date(MCD64A1)와 관측밀도를 통제한 partial correlation. **Stage-2 pilot에는 이 수치가 없음** — 계획된 검정 | — | — | — | H3: \|rho\|≥0.35 유지해야 통과 | `stage3/TB01.md` RQ3 | 아직 값 없음, 인용 시 "계획"임을 명시해야 함 |

---

## 2. TA04 (C-GO) — ASGM label efficiency & transfer

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **AUC (ROC-AUC)** | `roc_auc_score(y_test, P(pos))`. **Positive class = Maus et al. global-mining polygon 내부 픽셀(30 m erosion)**. 부정 클래스: hard-negative(주변 1.5-12 km annulus 내 2015-19 forest loss) + stable forest | 무차원[0,1] | n=2700/region(900 pos/900 hard-neg/900 stable), pos_frac=0.333 | 5-fold GroupKFold(0.1° block, AMZ 82block/GHA 158block), 5 seed 평균, sd=fold sd | chance=0.5 | stage2/TA04.md §3; `TA04_p2.py` | Ghana box는 산업형(LSM)과 ASGM을 같은 "mining" 양성 클래스로 묶음 → GHA AUC(0.977)가 인위적으로 쉬움(confound로 명시됨) |
| **label-efficiency curve** | 각 label 예산 n∈{25,50,100,250,500,1000,full}에서의 평균 AUC(train fold만 subsample, test fold는 항상 전체) | AUC vs n | train partition에서 class-ratio 보존 stratified subsample, 5 seed | 동일 GroupKFold-5 + 5-seed | S2-8, n=1000 AUC가 비교 기준 | `TA04_p2.py` | n=25는 seed 분산이 큼; "~40 labels" 교차점은 **두 측정점 사이의 선형 보간값**, 직접 측정되지 않음 |
| **label-parity ratio ("40 vs 1000", "≥25x")** | Stage-2식(informal): ratio=1000/40(AMZ 교차점 label 수). Stage-3식(formal, H1): S2가 자기 full-label AUC에 도달하는 label 수 ÷ AEF가 **동일 AUC 값**에 도달하는 label 수, 8점 power-law curve 적합 + bootstrap 95%CI | 배수(무차원) | 두 곡선에서 각각 도출된 "도달 label 수" | Stage-2: 단일 보간점(CI 없음); Stage-3: 20회 block-stratified resample, 고정 held-out test block, bootstrap CI | H1 기각기준: ratio<3x in ≥4/6 region | stage2/TA04.md §3; stage3/TA04.md §5 H1 | Fragile한 이유: (a) 교차점이 단 2개 측정점 사이 보간, 각 점의 seed sd가 AUC gap과 비슷한 크기; (b) "S2가 AEF-40을 따라잡는 데 필요한 label 수"가 아니라 "S2가 자기 최대 예산(1000)에서 낸 값을 AEF가 어디서 넘는가"를 거꾸로 읽은 것 — 비대칭적 정의 |
| **"SE의 20배" (Δ≈0.217 vs SE≈0.011)** | Δ=full-data AUC(AEF)-AUC(S2)=0.855-0.638=0.217. SE는 fold sd(0.027/0.052)가 **아니라** Hanley–McNeil류 large-sample AUC 근사식으로 n=2700,pos_frac=0.333에서 계산한 **이론적 SE≈0.011**. 20≈0.217/0.011 | 무차원(비율) | — | fold sd와 다른 산식(주의) | — | stage3/TA04.md §7 | 이 topic에는 두 개의 "SE"가 공존: 실측 fold sd(Cohen's d≈4-5용)와 이론적 대표본 SE(20x용) — 혼용하면 효과크기가 실제보다 과장돼 보임 |
| **Cohen's d≈4-5** | Δ(0.217)÷fold sd(0.027-0.052) | 무차원 | — | fold sd 기반 | — | stage3/TA04.md §7 | — |
| **Transfer drop** | Δ=AUC(in-region) − AUC(cross-region: source의 5-fold train으로 학습한 모델을 target 전체에 적용, 평균)|AUC점|source 5-fold 각각 → target 전체(target은 hold-out 분할 없음)|`TA04_p2.py`|drop→0(AUC→0.5)=chance 수준|stage2/TA04.md §3; `TA04_p2.py`|양방향이 동일 샘플/난이도가 아님(대칭 아님) — 이것 자체가 RQ2(비대칭)의 측정 대상|
| **Asymmetry index (0.131 vs 0.113)** | `|drop(A→B)-drop(B→A)|`, 단일 pair(AMZ-GHA)에서만 계산됨(AEF: \|-0.167-(-0.298)\|=0.131; S2: \|-0.165-(-0.052)\|=0.113) | AUC점 | 1개 pair(검정 불가) | — | — | stage2/TA04.md §3; stage3/TA04.md §2 H2 | 단일 pair라 유의성 검정 불가 — Stage-3는 30 ordered pair(6region)로 확장 계획 |
| **GHA→AMZ 0.557 (chance 근접)** | transfer drop 정의의 특수 케이스, AUC=0.557 (chance=0.5) | AUC | — | 위와 동일 | 0.5 | stage2/TA04.md §3 | — |
| **negative pooling Δ (0.020/0.045)** | AUC(local-k-only) − AUC(AMZ pool+k local labels), k∈{25,100} | AUC점 | GHA 5-fold GroupKFold, 5 seed | — | k당 20 draws로 확대 예정(Stage-3) | `TA04_p3.py` | 5 seed로는 marginal — Stage-3에서 20 draws 요구 |
| **T5 retrieval P@100** | unit-norm dot-product(=cosine) top-100 검색의 precision, 10 seed query×10 draw 평균 | 비율 | top100/pool, base rate=pos_frac(0.333) | 10-seed 평균 | base rate 0.333 | `TA04_p2.py` | AEF AMZ 0.376(거의 lift 없음), GHA 0.001(base rate 밑) → label-free 검색 실패 |

---

## 3. TB02 (C-GO) — Sentinel-1 blackout natural experiment

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **year-over-year drift `ang_y`** | `arccos(dot(e_{y-1},e_y))×180/π`, stable pixel(Hansen loss=0&gain=0&datamask=1 & DW mode 2018==2024 & mode∉{water,built,snow}) | degree | 픽셀별 | descriptive, 연도별 | — | `tb02_p1.py:44` | "stable" 정의가 8년 동일 mode에 기반한 static 정의 → 그 구간 내 실제 degradation은 정의상 "change"에서 배제되고 "drift"로 흡수됨 |
| **dev(연도 효과)** | `dev_y = ang_y - median(ang_{2019,2020,2021})`(픽셀별 baseline) | degree | 픽셀별 | median baseline, 2019-21만 사용(2017-18은 S2 sparse로 제외) | — | `tb02_p3.py:14` | baseline window가 비대칭(3년만, 시작연도 제외) |
| **S1 retention ratio** | `mean(median(S1_VV count,2022-24)) / mean(median(S1_VV count,2017-21))`, ROI 단위 | 무차원 비율 | ROI당 1개 값(6개 ROI) | ROI-level, pixel-level 아님 | — | `tb02_p3.py:7-9` | pixel-level retention은 Stage-3 계획일 뿐, Stage-2는 ROI당 1값 |
| **excess drift +2.3°** | (S1GAP ROI군 2022 평균 dev) − (S1OK ROI군 2022 평균 dev). S1GAP=retention<0.6(ZM 0.01, BO 0.35, DE 0.48), S1OK=retention≥0.6(BR 0.72,US 0.84,CD 0.97) | degree | trees-only stratum, 2022, pixel-year pooled per 그룹 | 그룹평균, CV/CI 없음 | S1OK군(+0.87°) | `tb02_p3.py:10-16` | **동일 quantity가 문서 내에서 +2.3°와 +2.67°로 두 번 다르게 인용됨**(§12); 3-ROI-per-arm으로 그룹 나눈 것이라 통계적으로 얇음; 0.6 cutoff는 임의적이고 DE(0.48)는 dose-response에 반례 |
| **sensor-free S2 excess +0.56° ("1/5")** | 동일 excess-drift 정의를 S2 각도에 적용 | degree | 동일 정의 | 동일 | AEF excess(≈2.3-2.67°)의 약 1/5 | `tb02_p2.py` | 비율(1/5)이 어느 AEF 수치(2.3 vs 2.67) 기준인지 불명확 |
| **5%-calibrated threshold / FPR (29.9%/32.9% vs control 3.1-4.6%)** | threshold=해당 ROI 자체의 stable pixel-year(2019-2021만) 각도 분포의 95th percentile; FPR(y)=그 ROI의 stable pixel-year 중 threshold 초과 비율(연도별) | % | ROI별·연도별, denom=그 ROI의 stable pixel수 | pooled fraction, CV 없음 | control=US_mo(3.1-4.3%), DE_bav(2.8-4.6%) — 서로 다른 두 control ROI·두 연도의 범위 | `tb02_p3.py:27-30` | threshold가 **ROI-specific**(global 아님); "control 3.1-4.6%"는 실제로는 2개 ROI×2개 연도에 걸친 범위이지 단일 수치 아님 |
| **S2 FPR collapse 32.2% (Congo)** | 위와 동일 FPR 정의를, S2 각도로 CD_congo(2022)에 적용 | % | 동일 | 동일 | 같은 ROI/연도의 AEF FPR=5.9% | stage2/TB02.md L16 | — |
| **partial R² 분해(관측 vs 기후)** | Ridge 회귀 R², feature={S1 count, S2 count} vs {precip anomaly, temp anomaly}, raw `ang`(dev 아님) 예측, 5-fold spatial-block GroupKFold | R² | pooled(6 ROI) vs ROI별 | mean over 5 fold, sd=fold sd | null=연도중심 intercept만 | `tb02_p3.py:34-57` | pooled R²(0.038-0.059)는 매우 작아 보이지만 효과가 ROI에 국지적(ZM S1 R²=0.245 vs CD 0.019)이라 pooling이 신호를 희석시킴; 기후 R²는 ERA5(~11km 해상도)가 ROI(0.5-1°) 내부에서 ROI×연도와 confound |
| **Cohen's d≈0.65 (TB02 power calc)** | excess 2.3° ÷ stable-drift IQR(≈3.5°) | 무차원 | ROI cluster가 유효 표본 단위(픽셀 아님) | — | — | stage3/TB02.md §7 | TB01/TE02와 분모 정의(IQR vs sd, 단위)가 다름 — topic간 d를 직접 비교 금지 |

---

## 4. TD01 (C-GO) — ordinal degradation intensity

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **"3-class" balanced accuracy (04의 표기, 실제로는 4-class)** | `balanced_accuracy_score`(macro recall). 실제 클래스는 **4개**: intact forest / stable non-forest / degradation(TMF DegradationYear=Y) / clearing(TMF DeforestationYear=Y or Hansen lossyear=Y). n=3600(900/class), Pará Y=2022 | 비율[0,1] | 4-class 균등(900/class) | 5-fold GroupKFold(0.1° block, 64 block), fold sd | chance=0.25(4-class) | `td01_p1b.py`; `TD01_p2.log` | **04_final_ranking.md의 "3-class"는 오기**: 분류기는 4-class, 진짜 3-class인 것은 ordinal 통계(ρ,τ,AUC — non-forest 제외)뿐. 두 다른 클래스 수를 "3-class"라는 이름 하나로 섞어 부른 것이 이 topic의 가장 명확한 표기 오류(§12) |
| **macro-F1 (+0.218)** | `f1_score(average='macro')`, 동일 4-class 프로브. AEF 0.765±0.031 vs S2 0.547±0.033 | 비율 | 동일 | 동일 | — | `TD01_p2.log` | — |
| **"fold 범위 비중첩"** | min(AEF 5-fold) > max(S2 5-fold) | — | — | descriptive, **유의성 검정 아님** | — | stage2/TD01.md | Stage-3 스스로 "n=5는 저검정력이므로 paired Wilcoxon + block bootstrap 1000회 CI를 병기해야 한다"고 명시 — 04에서 이걸 근거처럼 쓴 것은 성급함 |
| **inter-annual angular change(중위값)** | `arccos(dot(â_{Y-1},â_Y))×180/π`, 픽셀별, 클래스별 mean/median | degree | class별(900/class, Congo 500/class) | descriptive(모델 아님) | — | `td01_p1b.py:ang()` | 절대값이 지역마다 다름(degradation Amazon 15.7° vs Congo 29.0°) — **순위만** 전이되고 스케일은 전이되지 않음 |
| **Spearman ρ / Kendall τ (ordinal)** | ordinal rank r∈{0=intact,1=degradation,2=clearing}(non-forest 제외)와 각도의 순위상관 | 무차원 | Amazon ρ=0.684(AEF)/0.526(S2); Congo ρ=0.675/0.556 | pooled, CV 없음(스칼라 각도 자체이므로) | — | `td01_p1b.py`, `td01_p1.py` | partial Spearman(clearing fraction 통제)은 아직 미실행(Stage-3 계획) |
| **AUC(deg>intact), AUC(clr>deg)** | Mann-Whitney U 정규화(rank-biserial AUC) — 무작위로 뽑은 "상위" class 각도가 "하위" class 각도보다 클 확률 | 무차원[0,1] | Amazon 0.933/0.611; Congo 0.963/0.490 | — | 0.5=chance | `td01_p1b.py` | Congo의 clearing-vs-degradation AUC=0.490은 chance 수준 — 스칼라 각도로는 두 클래스 구별 불가(Reviewer-2 포인트) |
| **GEDI rh98 손실 Spearman ρ=0.755 (n=275)** | AEF 각도 vs `hloss`(=intact class median rh98 − 해당 footprint rh98), degradation+clearing footprint만(n=117+158=275), intact 제외 | 무차원 | n=275(변화 footprint만; 전체 GEDI-matched n=3275) | pooled | 전체(intact 포함, n=3275) ρ=0.161과 대비 | `td01_p2.py`; `td01_p2.out` | **GEDI 순환성**: AEF는 GEDI 높이 래스터를 학습 입력으로 흡수하므로 GEDI는 독립 reference가 아님 — 이 ρ는 내적 일관성 체크일 뿐 검증으로 쓸 수 없음(문서에도 명시). 또한 04와 이전 내부 요약본 사이에 "0.826 vs 0.719"/"11.9/21.3/54.2" 같은 **단일 fold값을 평균처럼 잘못 인용한 전례**가 stage3 문서에 자체 언급됨 — 반드시 `td01_p2.out` 원본과 대조 필요 |

---

## 5. TH01 (C-GO, MUST_EVALUATE) — DPRK cross-border transfer

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **cross-border mean-embedding cosine (0.504→0.967)** | elevation bin(0-100/100-300/300-600/600+m, Copernicus DEM)별로 ROK 평균벡터 `ma`, DPRK 평균벡터 `mb`(raw, 정규화 안 된 64-D 평균)를 구하고 `cos=(ma·mb)/(‖ma‖‖mb‖)` — **두 population의 평균벡터 간 코사인**(pairwise cosine의 평균이 아님) | 무차원[-1,1] | elevation bin별 population | 기술통계(점추정), Stage-3에서 13km block-bootstrap CI 예정 | — | `p_th01_t3.py` | (a) "0-100m"/"≥600m"는 **국경으로부터의 거리가 아니라 해발고도** bin — 04의 서술이 거리처럼 읽히면 오독; (b) 정확한 0.504/0.967 숫자가 저장된 로그에서 재확인되지 않음(스크립트는 확인, 출력 캡처는 못 찾음) |
| **vMF concentration κ (class별, DPRK vs ROK)** | Banerjee 근사 MLE: `Rbar=‖mean(unit vectors)‖; κ=Rbar(d-Rbar²)/(1-Rbar²)`, d=64. 6-class(water/forest/grass-bare/wetland/cropland/built, WorldCover 재매핑) | 무차원(>0) | class×country | — | — | `TH01_t3_transfer.py:66` | κ는 클래스를 정의한 라벨(WorldCover) 자체의 품질에 의존 — "DPRK κ≥ROK"가 "DPRK 라벨이 맞다"는 뜻은 아님, embedding 구형 분산 통계일 뿐 |
| **ROK OA / DPRK agreement(0.842/0.750 vs S2 0.715/0.677)** | OA=단순 accuracy(class 사전 균형 표집이라 balanced에 근접), 5-fold GroupKFold(0.12°,77 block). DPRK "agreement" = ROK 학습 모델의 DPRK 예측 vs **WorldCover 라벨**(=학습에 쓴 라벨과 동일 산출물) 일치율 | 비율 | ROK n=4540/6class, DPRK n=3348 | fold sd(ROK); pooled fraction(DPRK) | — | `TH01_t3_transfer.py`; `TH01_t3_out.json` | DPRK 쪽은 **ground truth가 전혀 없고 WorldCover(학습 라벨과 동일 산출물)와의 일치**일 뿐 — "accuracy"라 부르면 과장 |
| **두 독립 산출물 상호일치 0.674 vs AEF probe 0.750 (apples-to-oranges)** | 0.674=WorldCover와 Dynamic World(둘 다 모델 없는 외부 산출물)가 DPRK에서 서로 일치하는 비율. 0.750=ROK 학습 AEF probe의 예측이 WorldCover와 일치하는 비율 | 비율 | 둘 다 DPRK 픽셀 전체 | — | — | `TH01_t3_transfer.py:55` | **명백한 지표 혼동 위험**: 0.674는 모델이 전혀 없는 산출물간 일치도, 0.750은 모델-vs-라벨 일치도 — "AEF probe가 두 독립 산출물의 상호일치보다 낫다"는 서술은 **"probe가 ground truth보다 정확하다"는 뜻이 아니다** — 이 자체가 04에서 가장 위험한 오독 포인트 |
| **"+27pt 허위 forest-recovery" vs Dynamic World "+4.6pt"** | ROK-2024 학습(연도별 재학습·DA 없음) probe를 DPRK 2018/2024에 그대로 적용, 10-20° 사면 stratum에서 `Δ%forest=100×[mean(pred2024==forest)-mean(pred2018==forest)]`; 동일 stratum에서 Dynamic World 자체 라벨(2018 vs 2024)의 변화율과 비교 | 퍼센트 포인트(pp) | 10-20° slope stratum 픽셀 | — | Dynamic World(독립 산출물)의 변화율 | `p_th01_q1.py` 설계; stage3/TH01.md §7 | 이 실험은 stage3 자체 문서에 "Q1은 pilot되지 않았음"이라 명시 — 정확히 이번 세션에서 재실행되지 않은 값이므로 인용 시 "설계 존재, 수치 재확인 필요"라고 flag |
| **z (detection-timing, 사건 탐지)** | `z=(사건연도 각도 - control 각도 평균)/control 각도 표준편차`. control=사건지 인근 20-30km, 8방향×2반경, DEM/DW-class 매칭 박스 5-6개 | 무차원 | 사건별 | — | — | `TH01_t2_change.py`; `TH01_t2_log2.txt` | **stage2(코드로 확인됨, Jungpyong z=6.0/0.7)와 stage3(z=9.8/3.0)의 숫자가 서로 다름** — 두 문서가 내부적으로 불일치, stage2/로그가 코드로 추적 가능한 유일한 숫자 |
| **design-based area estimate + 95% CI (Olofsson n=566→600)** | Olofsson et al. 2014 stratified estimator: `n=(ΣWᵢSᵢ/SE)²`, 목표 SE(OA)=0.015, UA≈0.85(Sᵢ≈0.357) 가정 → n=566, 실무 600점(rare/change 4 strata 각 100 + stable 4 strata 비례배분) | 픽셀(표본크기) / 면적비율+95%CI(최종 산출물) | — | **아직 미실행** — Stage-3 power 설계 단계 | — | stage3/TH01.md §7 | 04에 등장하는 것은 "필요한 설계"이지 실제 area 추정치/CI가 아님 — 값이 존재하지 않는데 마치 결과처럼 인용되면 오류 |
| **McNemar power (4.0σ, MDD 5.1pt)** | 600 동일 위치점, discordance rate≈0.20 가정하 paired McNemar test의 power 계산 — 관측된 +7.3pt AEF-S2 격차를 4.0σ로 검출(power>0.98), 80% power 기준 최소검출차 5.1pt | pp(AUC/accuracy 차이 단위) | — | 사전 power 계산(설계용), 실측 아님 | — | stage3/TH01.md §7 | 마찬가지로 "계획된 검정력"이며 이미 수행된 McNemar 검정 결과가 아님 |

---

## 6. TE02 (C-GO) — drought anomaly transition vs stable drift

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **drought-break 17.66° vs stable 14.68°** | `dpz_y=pz_y-pz_{y-1}`(연간 precip z-score의 1년 변화)로 분류한 **transition class**: break(dpz>1)의 median angular drift vs "stable"(\|dpz\|<0.5) class median | degree | 46,314 pixel-year, 6 dryland ROI | median/IQR, CV 없음 | — | `te02_an2.py` | 여기서의 "stable"은 **transition-class 라벨**이며, TE02 안에서만도 (i) 이 transition-stable, (ii) 별도의 land-cover "stable stratum" 표집, (iii) drought-**level**의 "normal" class(§1의 다른 통계) — 최소 3개의 "stable/normal"이 다른 의미로 쓰인다(§12) |
| **ET FPR 76.7% vs S2 34.4%** | threshold=ROI별 transition-stable(\|dpz\|<0.5) 각도의 95th percentile; FPR=onset(dpz≤-1)+break(dpz>1)를 **합친** 픽셀-연도 중 threshold 초과 비율 | % | denom=해당 ROI의 \|dpz\|≥1 pixel-year(onset+break 합) | pooled fraction | nominal 5%(threshold 구성상) | `te02_an2.py` | onset과 break를 합친 값이므로 "drought-break가 만드는 FPR"이라는 서술은 부정확 — onset도 포함됨; BR_caat는 \|dpz\|<0.5 표본이 0이라 계산에서 통째로 빠짐(분모=0으로 조용히 스킵) |
| **climate partial R² 0.147 vs 0.011** | Ridge 회귀, within-pixel demeaned drift에 대해 `partial_R²=(R²_{base+add}-R²_base)/(1-R²_base)`, base={log1p(S1obs),log1p(S2obs)}, add={precip anomaly pz, temp anomaly tz} — **level-panel**(연도별 절대 anomaly, `te02_an.py`) 산출, transition-panel(dpz 기반)과는 다른 스크립트/패널 | R² | pooled 46,314 pixel-year | 5-fold spatial-block GroupKFold, fold sd | — | `te02_an.py` | 0.147/0.011은 level-panel 값이며, FPR 76.7%(transition-panel, `te02_an2.py`)와 **다른 패널/다른 정의**에서 나옴 — 같은 문단에 나열되어 있어도 섞어 해석하면 안 됨 |
| **SNR 0.23 (진짜 신호/artefact)** | 서로 다른 두 실험의 비율: 분자=genuine class-change Δ(+0.69°, DW mode 변화 stratified sample n=3600, normal year만); 분모=drought break-minus-stable Δ(+2.98°, transition panel n=46,314). `SNR=0.69/2.98=0.232` | 무차원(비율) | 분자·분모가 **서로 다른 표본/연도조건/ROI 구성** | 두 점추정의 비율, 결합 CI 없음 | 1(=신호와 artefact 동급)이 기준선; <1이면 artefact가 신호를 압도 | stage2/TE02.md; stage3/TE02.md | 이건 **같은 실험 내부의 variance ratio가 아니라 cross-experiment ratio**이다 — 전파된 불확실성이 없고, 두 원천 표본의 이질성 때문에 신뢰구간을 만들 수 없음(§12) |
| **corrected FPR (21.9% 등)** | `drift ~ [dpz,dtz,\|dpz\|,\|dtz\|]` 선형회귀를 **그 ROI 전체 데이터로 학습·평가**(held-out 없음), 잔차의 95th percentile을 새 threshold로 재설정 후 FPR 재계산 | % | 위와 동일 population | in-sample(훈련=평가 데이터 중첩) | 보정 전 FPR | `te02_an2.py` | in-sample 보정이라 일반화 성능 검증 안 됨 — "실용적 보정"이라 부르지만 held-out 평가가 없음 |
| **Cohen's d≈0.68 (TE02 power calc)** | break-stable +2.98° ÷ stable-drift IQR≈6.0°(sd≈4.4) | 무차원 | ROI cluster 단위 | — | — | stage3/TE02.md §7 | 유효 표본 단위=ROI cluster(픽셀 아님)라는 점이 power 계산(46/군, 250-350 ROI 설계)의 핵심 전제 |

---

## 7. TC01 (C-GO) — static/climate-decodable subspace로서의 transfer 실패 기전

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **3-class balanced accuracy(in-domain 0.940, transfer 0.555)** | WorldCover {tree,shrub,grass} 3-class, `balanced_accuracy_score`, LogReg | 비율 | n=1800/region, 600/class | 5-fold GroupKFold(0.1°); in-domain=BR 내 fold 평균; transfer=BR 각 fold train→CG 전체(1800) 예측 | chance=1/3 | `TC01_p2.py` | transfer는 BR→CG 단방향만 pilot됨(대칭 미검증) |
| **"drop" (in-domain − transfer)** | 두 값의 단순 차 | 정확도점 | — | — | — | stage2/TC01.md §3 표 | 부호규약: drop=in−transfer(transfer가 낮을수록 drop 큼) — "transfer−in"으로 헷갈리기 쉬움 |
| **within-ROI static ridge R² (max 0.47)** | AEF 64개 dim 각각을 4개 static covariate(고도,경사,연평균 T,연강수 P)로 Ridge 예측, 5-fold GroupKFold(BR 내부) | R² | dim별 | fold 평균 R² | CONUS급 문헌치 0.97은 별도 extent 참조(직접 측정 아님) | `TC01_p2.py: dimR2()` | 0.47(ROI 내부) vs 0.97(대륙 규모)은 모순이 아니라 **spatial extent 차이**(scale-dependent decodability, RQ2) |
| **pooled static-R² (top-16 랭킹용)** | BR+CG **pooled**(n=3600) Ridge, in-sample(CV 없음) R² | R² | pooled | **in-sample**(fit=score 데이터 동일) | — | `TC01_p3.py` | within-ROI R²(GroupKFold 사용)와 달리 이 랭킹용 R²는 **CV 없이** 계산됨 — 재현 시 반드시 구분 |
| **standardized mean-shift (Cohen's d형)** | dim별 `|mean(BR)-mean(CG)|/sqrt(0.5(var(BR)+var(CG)))` | 표준화 단위 | 전체 BR(1800)/CG(1800) | 단일 계산, CV 없음 | — | `TC01_p3.py` | — |
| **14/16 overlap** | pooled-static-R² top-16과 mean-shift top-16의 교집합 크기 | 정수(≤16) | 단일 pilot pair | **permutation null 미실행**(Stage-3 계획, 500 draws) | — | stage2/TC01.md; stage3/TC01.md | 현재는 관측된 겹침 수치뿐, p-value 없음 |
| **transfer 회복률 55%** | `(transfer_top16제거후 - transfer_AEF64) / (transfer_S2 - transfer_AEF64)` = (0.638-0.555)/(0.705-0.555)=0.553 | AEF-S2 gap의 비율 | 분자=제거 후 transfer 개선분, 분모=AEF-S2 전체 gap | 동일 5-fold BR→CG 프로토콜 | S2-8 baseline이 "회복 목표선" | `TC01_p3.py` | 55% 회복 후에도 AEF(0.638)는 여전히 S2(0.705)보다 낮음 — "회복"이라는 표현이 "S2를 넘어섰다"로 오독될 위험; 분모(0.150)가 어떤 S2 변형을 쓰느냐에 의존 |
| **per-region z-score 전이(0.680)** | BR/CG 각각 자기 평균·표준편차로 표준화(공유 target 분포에 맞춘 것 아님) 후 재학습 | 정확도 | — | 동일 5-fold | top-16 제거(0.638)보다 **더 높음** | `TC01_p3.py` | 순수 static-input 제거보다 단순 moment-matching이 더 잘 통한다는 점이 "static subspace가 기전"이라는 주장을 흔드는 반대증거로 문서 자체에 명시 |
| **static-dim-only z-score (RQ3)** | 전체 64 dim 중 static-decodable dim에만 z-score 적용 vs 나머지에만 적용 — **Stage-3 계획, Stage-2에 수치 없음** | — | — | 미실행 | H3: static-dim-only가 전체 z-score 이득의 ≥60% 설명해야 통과 | stage3/TC01.md §2,§5 | 값 인용 금지 — 아직 실행되지 않음 |
| **random-dim null (500 draws)** | top-16과 같은 크기 k를 무작위로 뽑아 500회 반복, transfer 회복률의 empirical null 분포 구축 — **Stage-3 계획, 미실행** | — | — | — | H1 기각: 관측치가 null 95th percentile 이내면 기각 | stage3/TC01.md §2,§7 | 값 없음 |

---

## 8. TA02 (C-GO) — secondary-forest age ceiling

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **R² (0.288/0.342 vs S2 0.157/0.137)** | `r2_score`를 **각 fold 내부**에서 계산 후 5-fold의 mean±sd. **Fold-averaged, pooled 아님** — fold별 예측을 이어붙여 한 번에 채점하지 않음 | R² | 각 fold의 test set(SS_tot도 그 fold 자체 평균 기준) | Ridge(α=10)+StandardScaler, 5-fold GroupKFold(0.1°) | chance R²≈0 | `ta02_pilot.py`/`ta02_pilot2.py` | fold R²가 매우 음수로 나올 수 있음(cross-region 예: R²=-2.27) — 각 fold의 SS_tot이 그 fold 고유 평균이라 global 척도로 비교 불가 |
| **MAE (년)** | `mean_absolute_error(age_true,age_pred)`, fold 평균 | **년(stand age)** | 6개 age bin(1-3,4-6,7-10,11-15,16-25,26+) 전체 및 bin별 | 동일 GroupKFold-5 | — | `ta02_pilot.py` | bin7("mature", age label 없음)은 MAE 계산에서 제외, 별도 진단(아래) |
| **attenuation slope ≈0.30** | 6개 age-bin의 (평균 실제연령, 평균 예측연령) 점들을 잇는 기울기 — Δ(평균예측)/Δ(평균실제), "29년 실제범위 → 9년 예측범위 압축"을 나타내는 back-of-envelope 비율(6점으로 만든 것, 정식 최소자승 CI 없음) | 무차원(Δpredicted/Δtrue) | — | Stage-2: 6개 bin-mean 점 기반 약식 계산; Stage-3 계획: block-bootstrap 1000회 + regression-to-mean 시뮬레이션 대조군으로 정식화 | slope=1이면 압축 없음 | stage2/TA02.md §3; stage3/TA02.md §5 | 0.30은 **정식 회귀로 적합된 기울기가 아니라 6개 점으로 만든 약식 비율** — regression-to-mean(리지 정칙화의 인공물)과 진짜 표현 한계를 구분하는 synthetic-control 비교가 아직 없음 |
| **trajectory 추가 이득 0.000-0.006** | Δ=R²(AEF-64+연간각도변화 6밴드) − R²(AEF-64 단독), 둘 다 fold-averaged R² | R² 증분 | — | GroupKFold-5 | AEF-64 단독의 fold sd(≈0.035) | stage2/TA02.md; `ta02_pilot.py` | 증분이 fold sd보다 작음(실질적으로 0) — trajectory feature 자체의 단독 R²(0.05-0.14, AEF-64보다 훨씬 낮음)와 혼동하지 말 것 |
| **range-restricted R² (young/old)** | 동일 R² 정의를 age∈[1,15](young) 또는 [16,60](old) 부분집합에 한정 | R² | 부분집합별 | GroupKFold-5 | 전체범위 R²(0.29-0.34)가 참조선 | `ta02_pilot2.py` | old 구간 R²가 0.011-0.037로 붕괴 — 전체 R²가 대부분 young-vs-old 분리에서 나온다는 증거이자 "18y 근처 상한"의 근거 |
| **mature-stratum 평균 예측연령(19.9-22.7y AEF vs 13.9-14.6y S2)** | age label이 전혀 없는 mature-forest 픽셀에 대해, age로 학습된 5개 fold-model의 예측을 평균 | 년 | mature px 전체 | 5-fold model 예측의 평균 | — | stage2/TA02.md | age-label을 전혀 안 쓴 독립적 ceiling 확인 — regression-to-mean 아닌 별도 anchor |

---

## 9. TE06 (C-GO) — static covariate absorption 기전

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **balanced accuracy (LC, 9-class Andes / 8-class flat)** | `balanced_accuracy_score`, WorldCover class(450/class 균등) | 비율 | Andes n=4050, flat n=3600 | 5-fold GroupKFold(0.1°), fold sd | **chance가 지역마다 다름**: Andes 1/9=0.111, flat 1/8=0.125 | `TE06_meta.py`; `aefkit.probe()` | 두 지역의 chance가 다른데 raw balanced accuracy를 직접 비교 — chance 정규화 없이 비교하면 왜곡 가능 |
| **ridge R² (canopy height, ETH GlobalCanopyHeight)** | Ridge+StandardScaler, `r2_score` | R² | Andes n=2423, flat n=2482 | 동일 GroupKFold-5 | — | `aefkit.probe()` | **순환성**: ETH 높이는 GEDI 기반이고 GEDI는 AEF의 학습 입력 — height R² 우위는 input leakage로 인플레이션되었을 수 있음(TD01의 GEDI 문제와 같은 성격) |
| **absorption fraction (62%/15%, 35%/11%)** | `(Δ_{AEF-S2} - Δ_{AEF-(S2+static)}) / Δ_{AEF-S2}` — AEF 대 S2-only의 격차 중, static covariate를 S2에 더했을 때 좁혀지는 비율. LC-Andes: (0.170-0.065)/0.170=0.618; LC-flat: (0.119-0.101)/0.119=0.151; height-Andes 0.35; height-flat 0.11 | AEF-S2 gap의 비율 | 단일 ROI, 단일 fold-CV 점추정(부트스트랩 CI 없음) | 4-arm ladder(AEF/S2/S2+static/static-only)의 GroupKFold-5 cell 값으로부터 산술 | — | `TE06_meta.py`; stage2/TE06.md §3 | **분산분해나 partial R²가 아니라 두 델타의 단순 비율**이다("partial R²(clim\|obs, obs\|clim)"라는 통계는 TE06에 존재하지 않음 — 요청받았지만 파일에 없음, §12); 단일 ROI 점추정이라 Andes 62%/flat 15%는 그 ROI의 클래스 구성(예: 눈/나지 고도 zonation)에 취약 — Stage-3는 14개 region의 mixed-effects model로 재설계 |
| **AEF margin 생존 (4/4 cell, 20/20 paired fold)** | AEF>S2+static인 (target×region) cell 수 / fold 수(4 cell×5 fold=20) — **승패 카운트, p-value 아님** | 카운트 | 4 cell, 20 fold | fold별 승패 비교, 정식 검정 없음 | — | stage2/TE06.md §3 | Stage-3에서 paired Wilcoxon+BH 보정+bootstrap CI를 필수로 추가 예정 — 04의 "20/20"은 아직 검정통계량이 아님 |
| **Cohen's kappa (별도 pilot arm, 헤드라인 아님)** | `cohen_kappa_score`, MapBiomas Brazil→Congo RF transfer(RF+accuracy+κ) — **62%/15% 흡수율과는 다른, 병행/이전 pilot arm** | κ[-1,1] | — | RF(300 trees), GroupKFold-5 | — | `TE06_pilot1/2/3.py`, `te06_check2.py` | 04에 인용된 흡수율 숫자와 절대 혼동 금지 — 다른 라벨(MapBiomas vs WorldCover), 다른 분류기(RF vs LogReg/Ridge)에서 나온 값 |

---

## 10. TH03 (NO-GO) — Gaza 300m grid

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **grid AUC 0.605±0.205 vs S2 0.601±0.168** | 단일 bi-temporal(2022→2024) 각도 feature의 LogReg AUC. 양성="heavy damage"(built cell당 damage-site 밀도가 상위 1/3), 음성="무피해"(density=0, n=167) | AUC | n_pos=735,n_neg=167 | **5-fold GroupKFold, 단 block이 11개뿐** — sd=fold sd | 0.5 | `th03_an.py` | **fold-sd(0.17-0.21)가 AEF-S2 차이(0.004)의 40-70배** — 문서 자체가 "fold 분산이 지표차이를 완전히 압도한다"고 인정. 이 비교 자체가 통계적으로 무승부 이상의 의미가 없음 |
| **partial Spearman(built-surface 통제, 0.387/0.331)** | rank 변환 후 rank-잔차 partial correlation(고전적 partial-Spearman 공식이 아니라 rank-residual Pearson으로 근사) | 무차원 | — | — | raw Spearman(0.286/0.298, -0.018/0.133)과 대비 | `th03_an.py` | AEF raw Spearman(-0.018, damage density 붕괴)이 built-surface 통제 후 +0.387로 반전 — "urbanness confound"일 가능성이 문서에도 명시됨 |
| **다년 trajectory AUC(0.834/0.879) "생존"** | 2/4개 연도쌍 각도 feature를 쓴 동일 LogReg/AUC 설계 | AUC | — | 동일 GroupKFold-5, 11 block | S2+bs(단일 각도+built surface, **매칭된 다년 S2/S1 궤적 아님**) 0.774 | `th03_an.py` | 문서 스스로 "S2 다년 궤적 baseline을 실행하지 못했으므로 0.879 vs 0.601 비교는 like-for-like가 아니다"라고 명시 — 재진입 조건의 핵심 |
| **재건 신호 20.56°/20.15°/21.35°** | 2024→2025 단일 연도쌍 각도의, **2024년 피해강도로 나눈 3개 severity strata**(무피해/저피해/고피해) 각각의 평균±sd — pre/post/재건 3단계 아님, 같은 연도쌍을 피해강도로 층화한 것 | degree | strata별 built cell | mean±sd(pixel population), CV 아님 | — | `th03_an.py` | 단조적 분리 없음(20.15-21.35° 범위) → "재건이 측정 가능하다"는 가설의 pre-registered 반증으로 해석됨 |
| **MDD 0.067 vs gate 0.03** | Hanley-McNeil SE(0.018)는 무시하고, traj4의 fold-sd(0.097)로부터 `SE(mean AUC)≈0.097/√5≈0.043`, paired block-차이 sd≈0.08(낙관적 가정)로 80% power 최소검출차 계산 | AUC점 | — | **사후(post-hoc) power 추정** — 사전 설계 검정력이 아니라 pilot의 실측 fold-sd로 거슬러 계산 | pre-registered kill-gate=0.03 | stage3/TH03.md §7 | 0.067이라는 정확한 숫자는 "optimistic" 가정에 기반한 근사치로 문서에 명시 — 정성적 결론(11개 block으로는 56개 필요한 0.03 gate를 판정할 수 없다)만 안정적, 소수점까지 믿지 말 것 |
| **무피해 cell 비율 7.0%** | built cell(GHS built-surface≥500㎡, 300m cell 기준) 중 2024 매칭 damage site가 0인 cell의 비율 | % | 167/2370 | — | — | `th03_p6.py` | 이 낮은 비율 자체가 음성 클래스 표본 부족(=검정력 부족)의 직접 원인 |

---

## 11. Kill된 topic (TC03·TF02·TG01) — 04 kill-log 요약에 등장하는 수치

| Metric | 정식 정의 | 단위 | Num/Denom | Estimator & CV | Reference | 출처 | Pitfall |
|---|---|---|---|---|---|---|---|
| **TC03: vMF kappa ratio(가장 약함)** | `\|ln(κ_source/κ_target)\|`, unit-normalize한 feature의 vMF concentration 비율(로그 절대비) | 무차원 | region pair(30개, 6region) | Spearman ρ(kappa_ratio, 실측 transfer drop) | AEF: ρ=+0.223(p=0.236, 비유의) vs S2: ρ=+0.631(p=0.0002) | `TC03_analyze.py` | "AEF 자신의 transfer loss를 예측하는 label-free 지표 중 최약"이라는 서술은 **AEF 공간에서 시도한 5개 후보(centroid cosine distance, kappa ratio, linear MMD, energy distance, domain-classifier AUC) 중 최약**이라는 뜻이며, 동시에 AEF의 최선(energy distance ρ=0.550)조차 S2 공간의 동등 통계(ρ=0.83)에 진다는 이중 패배임 |
| **TC03: energy distance / linear MMD (최선의 대안, 참고)** | energy distance=`2·mean‖Xi-Yj‖-mean‖Xi-Xi'‖-mean‖Yj-Yj'‖`(subsample m=400); linear MMD=`‖mean(X)-mean(Y)‖₂` | feature 단위 | region pair | Spearman vs drop | — | `TC03_analyze.py` | 04에는 등장하지 않지만 kill 이유의 정량적 배경 — "vMF/unit-sphere가 최약"이라는 문장 뒤에 숨은 비교 기준 |
| **TF02: differential inflation Δ(rand→rung)** | `balanced_accuracy(무작위 fold split) - balanced_accuracy(공간적으로 분리된 block split)`, block 크기(rung)를 50m~2km(근접)/최대10km(넓음)로 변화 | 정확도점 | rung/landscape/featureset별 | GroupKFold(group=rung별 block 또는 무작위 그룹) | — | `tf02_near.py`/`tf02_pilot.py` | 04의 "부호 반전"은 이 Δ가 지역(KE_a vs MT_b)에 따라 AEF>S2 또는 AEF<S2로 뒤집힌다는 뜻; "S2+300m focal mean이 재현"은 AEF의 patch-context 자체가 아니라 **공간적 맥락 정보 일반**이 원인일 수 있음을 보여준 대조실험. 25/50km rung은 GEE timeout으로 **측정 실패**(null 결과 아님) |
| **TG01: conformal coverage(최대 6.2pp)** | split-conformal LAC score(1-softmax) 기반 prediction set의 marginal/Mondrian coverage, nominal 90%/80%; 공간분리(Regime B, ≥11km gap) vs 무작위분리(Regime A)의 coverage 차이(pp) | pp(백분율포인트) | test set 전체 또는 class-conditional | Regime A/B 각 4개 spatial split을 "fold"처럼 취급, fold sd | nominal 90%/80% | `tg01_conf.py` | 최대편차 6.2pp는 Mondrian α=0.20 조건에서 발생 — "대부분 fold sd 내"라는 서술은 8개 행 중 대부분(all은 아님)에 해당 |
| **TG01: angular distance-coverage correlation (-0.007 vs S2 +0.121)** | **Pearson** correlation(코드에서 `np.corrcoef` 명시, Spearman 아님) between (AEF: 최근접 calibration point까지의 max-cosine을 각도로 변환한 값) 또는 (S2: 표준화 Euclidean 최근접거리) and 이진 coverage 지표 | 무차원[-1,1] | test point 전체 | — | 단조감소(가설) 기대: r<0 | `tg01_dist.py` | AEF와 S2의 "distance"가 **다른 기하학적 정의**(각도 vs Euclidean)이므로 두 상관계수의 직접 비교는 angular-vs-Euclidean을 통제한 ablation이 아님; 통계량은 Pearson r이지 Spearman이 아님(요청 사항과 달리 코드 확인됨) |
| **TG01: area-estimation SE 개선 1.0%** | `SE=sqrt(Σ_h W_h² p_h(1-p_h)/n_h)`(계층별 stratified 비율추정 SE), map-class 단독 대비 map-class×conformal-set-size 결합 계층화의 **상대적** SE 감소율 | SE의 상대적 %(포인트 아님) | pool(n≈5291)을 pseudo-population으로, n=500/1000/2000 표본크기 | — | map-class 단독 SE가 기준(=100%) | `tg01_area.py` | **"1.0%"는 percentage-point가 아니라 상대적(relative) 감소율**이다 — 절대 SE는 0.01040→0.01029로 겨우 0.00011 감소; conformal-set-size **단독**은 SRS보다도 나쁨(개선은 map-class와의 **결합**에서만 나옴) — TG02가 별도로 제외된 이유이기도 함 |

---

## 12. Numbers in 04 that are stated ambiguously or inconsistently

이 섹션이 이 문서의 핵심 가치다. 아래는 `04_final_ranking.md`가 (a) denominator를 명시하지 않거나, (b) 단위를 섞거나,
(c) fold sd와 bootstrap CI를 혼용하거나, (d) 같은 이름이 topic마다 다른 것을 가리키는 경우다.

1. **"5%-calibrated threshold" / "p90 threshold"가 topic마다 완전히 다른 대상이다.**
   - TB01: 2-yr endpoint separation(`sep=arccos(dot(e_{Y-1},e_{Y+1}))`)의 90th percentile, 안정림 population, 단일 연도(2021)만.
   - TB02: **1-yr drift**(`ang_y`)의 95th percentile, **그 ROI 자체**의 stable pixel-year, 2019-2021 pooled.
   - TE02: 1-yr drift의 95th percentile이지만 reference population이 "transition-stable"(연간 precip anomaly 변화 \|Δz\|<0.5) class — 계절/기후 조건에 의존하는 population이며 calendar year로 고정되지 않음.
   - 즉 "5% FPR" 또는 "p90"이라는 말은 세 topic에서 서로 다른 각도 정의·다른 reference population·다른 시간창을 가리킨다. 절대 숫자(TB02의 29.9%/32.9% vs TE02의 76.7%)를 나란히 놓고 "TE02가 더 나쁘다"고 말하는 것은 같은 척도가 아니다.

2. **TB01 내부에서 threshold와 detection-rate가 서로 다른 각도 정의를 쓴다.** threshold(11.4°/8.9°)는 2-yr span(`sep`) 위에서 계산됐는데, 99.2%/98.7% detection rate는 1-yr span(`aY`)을 그 threshold와 비교한다고 서술된다. 두 각도가 같은 스케일이 아니므로 이 비교 자체가 재확인 없이는 성립하지 않는다.

3. **"December-shift 27.0°/16.4°"는 BR-vs-CG 비교가 아니라, 각 region 내부에서 12월 사건 각도 vs 그 region의 threshold 비교다.** 04의 서술("12월 사건도 27.0°/16.4° 이동")은 두 나라를 나열한 것처럼 보이지만 실제로는 "BR에서 12월 사건 각도=27.0°(BR threshold=11.4° 초과)", "CG에서 12월 사건 각도=16.4°(CG threshold=8.9° 초과)"라는 독립된 두 문장이다.

4. **TB02의 excess drift가 문서 내에서 두 가지 숫자(+2.3° vs +2.67°)로 인용된다.** 04는 "+2.3°"를 쓰지만 stage2 문서의 다른 문장은 같은 quantity를 "+2.67°"로 부르며 이를 기준으로 "sensor-free S2 baseline은 1/5"라는 비율을 낸다. 어느 숫자가 그 "1/5"의 분모인지 재확인 없이는 이 비율을 인용할 수 없다.

5. **TD01의 "3-class balanced accuracy"는 실제로 4-class 분류기의 결과다.** intact/non-forest/degradation/clearing 4개 클래스로 학습·평가된 balanced accuracy(0.775/0.577)를 "3-class"라고 부른 것은 04의 명백한 오기다. 진짜 3-class인 것은 non-forest를 제외한 ordinal 통계(Spearman ρ, AUC(deg>intact) 등)뿐이며, 이 둘을 같은 문장에서 "3-class"라는 단어로 섞으면 독자는 두 다른 실험을 하나로 착각한다.

6. **TD01의 GEDI rh98 Spearman(0.755)은 독립 검증이 아니다.** GEDI는 AEF의 학습 입력 데이터이므로, "degradation intensity가 GEDI 높이손실과 상관된다"는 결과는 순환적이다. 04는 이 수치를 다른 실측치들과 나란히 "핵심 실측치" 목록에 놓아, 마치 외부 검증인 것처럼 읽히게 한다. 같은 문제가 TE06의 canopy-height R²(ETH 데이터가 GEDI 기반)에도 있다.

7. **TH01의 "두 독립 산출물 상호일치 0.674 vs AEF probe 0.750"은 서로 다른 종류의 지표를 나란히 놓은 것이다.** 0.674는 모델이 전혀 없는 두 외부 산출물(WorldCover, Dynamic World) 사이의 일치율이고, 0.750은 ROK에서 학습한 AEF probe의 예측이 WorldCover(그 자체가 학습 라벨)와 일치하는 비율이다. "AEF probe가 두 독립 산출물의 상호일치보다 낫다"는 문장은 "AEF probe가 ground truth보다 정확하다"로 오독되기 쉬우나, 실제로는 AEF probe가 자신의 학습 라벨과 더 가깝다는 것 이상을 말하지 않는다.

8. **TH01의 detection-timing z 통계가 stage2와 stage3 문서에서 서로 다른 숫자로 나온다.** stage2(및 코드로 재확인 가능한 로그)는 Jungpyong z=6.0(AEF)/0.7(S2)를 보여주지만, stage3 제안서 본문은 같은 사이트에 대해 z=9.8/3.0을 언급하며 "Songhwa z=1.5"라는, 로그에서 확인되지 않는 사이트명까지 등장시킨다. 04를 쓴 main agent가 어느 문서에서 인용했는지 불명확하다 — 재현 가능한 쪽(stage2/로그)이 우선해야 한다.

9. **TE02의 "stable/normal"이라는 단어가 최소 세 가지 다른 것을 가리킨다.** (i) drought-**level** framing의 "normal"(precip z-score −0.5~0.5), (ii) drought-**transition** framing의 "stable"(연간 z-score 변화 \|Δz\|<0.5, 완전히 다른 변수), (iii) 원래의 land-cover 표집 "stable stratum"(연도 간 DW class 불변). 04가 인용하는 14.68°(stable)는 (ii)이지만, 문서를 처음 읽는 사람은 (iii)으로 착각하기 쉽다.

10. **TE02의 SNR 0.23은 같은 실험의 신호대잡음비가 아니라, 서로 다른 두 실험의 점추정치 비율이다.** 분자(+0.69°, DW-class-change stratified sample, "정상년"만, n=3600)와 분모(+2.98°, drought-break transition panel, n=46,314)는 표본·연도조건·ROI 구성이 다르다. 진짜 SNR(같은 표본에서 신호 분산 대 잡음 분산의 비)이 아니라 cross-experiment ratio이며, 결합된 신뢰구간이 없어 "0.23"이라는 숫자에 오차범위를 붙일 수 없다.

11. **TA04의 "SE의 20배"와 TC01/TE06에서도 반복되는 "Nx SE" 서술은 fold sd와 전혀 다른 SE를 쓴다.** fold sd(TA04에서 0.027-0.052)로 정규화하면 Cohen's d≈4-5인데, "20배" 주장은 이것과 별개로 Hanley–McNeil류 대표본 근사 SE(≈0.011, n과 pos_frac만으로 계산한 이론값)를 쓴다. 04에 "SE의 20배"라고만 적으면 독자는 이것이 fold sd 기반인지 이론적 SE 기반인지 알 수 없고, 실제로는 더 작은 분모를 골라 효과크기를 더 크게 보이게 만든 쪽이다. TC01(≈7x)과 TE06(≈8x)에도 동일한 이중 SE 문제가 있다.

12. **label-parity ratio("40 labels vs 1000 labels", "≥25x")는 04에 실린 수치 중 가장 취약한 축에 속한다.** Stage-2의 ratio는 6~8개의 측정점 중 단 2개 사이의 **선형 보간**으로 만든 교차점이며, 그 교차점 자체의 신뢰구간이 없다. 게다가 정의가 "AEF가 몇 label로 S2의 최대예산(1000) 성능에 도달하는가"이지 "S2가 AEF-40에 도달하려면 몇 label이 필요한가"가 아니다 — 두 정의는 대칭이 아니고, 04의 서술은 이 비대칭을 명시하지 않는다.

13. **absorption fraction(TE06 62%/15%, 35%/11%)과 label-parity ratio, 그리고 TC01의 55% "회복률"은 모두 "partial R²"나 분산분해가 아니라 단순 델타의 비율이다.** 요청받은 "partial R²(clim\|obs, obs\|clim)"라는 명명된 통계량은 TE02의 climate partial R²(0.147/0.011, Ridge 기반 `(ΔR²)/(1-R²_base)`)에서만 실제로 존재하며, TE06/TC01/TA04의 유사한 비율들은 이름은 비슷해도 계산식이 다르다(단순 델타의 비, in-sample 랭킹, 보간 등). "partial R²"라는 통계학적으로 무거운 용어를 04가 함부로 재사용하지 않도록 주의가 필요하다.

14. **TH03의 grid AUC(0.605±0.205 vs 0.601±0.168)는 fold sd가 효과크기를 40-70배 압도하는데도 04의 순위표에 "핵심 실측치"로 나란히 적혀 있다.** 이 topic만 유일하게 fold sd가 명목상의 차이(0.004)보다 훨씬 크다는 것이 이미 stage2/3 문서에 자인되어 있음에도, 04의 표 형식은 다른 GO/C-GO topic들의 "견고한" 효과크기와 시각적으로 동일한 취급을 받는다 — 독자가 스캐닝만 하면 TH03의 무승부를 다른 topic의 큰 효과크기와 같은 신뢰도로 오인하기 쉽다.

15. **TG01의 "SE 개선 1.0%"는 percentage-point가 아니라 relative reduction이다.** 절대 SE 변화는 0.01040→0.01029(약 0.11 percentage point)에 불과하며, "1.0%"는 이 절대변화를 map-class 단독 SE로 나눈 상대적 비율이다. 04 kill-log의 "SE 개선 1.0%"라는 표현은 이 상대/절대 구분을 명시하지 않아, 절대적으로 큰 개선처럼 오독될 수 있다.

16. **fold sd vs block-bootstrap CI가 topic마다 다르게, 그리고 종종 같은 topic 안에서도 혼용된다.** 모든 Stage-2 pilot 수치의 "±"는 5-fold GroupKFold의 fold sd다(예외 없음, 이 문서 §0-§11에서 확인). 반면 04와 stage3 제안서들이 "block-bootstrap CI", "13km block bootstrap", "1000회 resample" 등을 언급하는 곳은 전부 **아직 실행되지 않은 Stage-3 계획**이다. 04를 읽는 사람이 "±sd"를 신뢰구간처럼 취급하면, 실제보다 훨씬 좁은 불확실성을 상상하게 된다 — 특히 n=5인 fold 수 자체가 sd 추정치의 신뢰도를 낮춘다는 점(TD01 stage3가 스스로 인정)까지 고려하면 더욱 그렇다.

17. **TB01의 intercept a≈0.568, 기울기 b≈0.5를 만들어낸 정식 회귀가 어떤 pilot 스크립트에도 없다.** 이 값들은 stage3 제안서 본문에서 서술되지만, `w(m)=a+b·(12-m)/12`를 실제로 fit한 코드(가중최소자승/isotonic regression)는 이 세션에서 확인되지 않았다 — 아마 monthly mean w 값(Dec≈0.57)으로부터 사후에 근사한 것으로 보이나, 04가 이를 "측정된 계수"처럼 소수점 세 자리(0.568)까지 제시하는 것은 정밀도 착시를 유발한다.

18. **AEF 벡터의 unit-norm 가정이 코드에서 검증되지 않는다.** 모든 angular-distance 계산은 `arccos(clip(dot,-1,1))`을 쓰며 clip이 있어 dot이 [-1,1]을 벗어나도 조용히 잘린다. 이는 "AEF가 unit-norm이 아니어도 각도 계산이 깨지지 않게" 만들어주지만, 동시에 **AEF가 실제로 unit-norm인지 검증하지 않고 넘어가게 만드는 안전장치**이기도 하다. 04에 나오는 모든 "각도" 수치는 이 가정 위에 서 있다.
