# 04_final_ranking.md — 최종 순위와 권고 (AEF 연구주제 탐색, 2026-09)

MODE=LIVE. 후보 48개 → Stage 1 통과 13 → Stage 2 PASS 10 → Stage 3: **GO 1, CONDITIONAL-GO 8, NO-GO 1**.
아래 순위는 각 subagent의 자기보고 총점이 아니라 **실측 효과크기 · 독립 검증 가능성 · 외부 데이터 의존도**로
main agent가 재교정한 것이다 (Stage 2에서 8개 토픽이 17/18로 몰려 자기보고 점수의 판별력이 없었다).

## 목표 대비 정직한 보고

TARGET은 "Stage 3 후 GO ≥5"였다. **무조건 GO는 1개(TB01)뿐이다.** 나머지 8개는 모두
CONDITIONAL-GO이며, 조건은 대부분 (a) GEE 밖 독립 reference 확보 또는 (b) stable/label stratum의
VHR 검증이라는 **실행 가능한 3-4주짜리 게이트**다. §8 규정에 따라 상위 5개를 조건 명시 하에 승격해
"추진 권고 5개"를 구성하되, 무조건 GO가 1개라는 사실을 축소하지 않는다. 조건을 통과하지 못하면
해당 토픽은 GRSL/JSTARS급 축소 논문 또는 negative-result 논문으로 강등되며, 각 제안서에 그 강등
경로가 이미 명시되어 있다.

## 최종 순위

| 순위 | ID | Seed | Bucket | 지역 | 판정 | 1순위 저널 | 한 줄 기여 | 핵심 실측치 | 게이트 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | TB01 | S1 | B | Amazon + Congo | **GO** | IEEE TGRS | 연간 embedding의 geodesic mixing 법칙을 기각하고 3-state arc model과 lag-aware change rule로 대체 | 안정림 p90 임계에서 2021년 벌채의 99.2%(BR)/98.7%(CG)가 당해 연도에 이미 flag; 12월 사건도 27.0°/16.4° 이동; calibration MAE 0.418/0.396 vs S2 0.787/1.117 | 없음 (W8 stop rule만) |
| 2 | TA04 | S8 | A | Amazon + Ghana | C-GO | RSE | ASGM 탐지에서 label 예산 축 자체를 측정: ~40 labels로 S2의 1000-label 성능, 그리고 비대칭 transfer와 negative pooling | full-data AUC 0.855±0.027 vs S2 0.638±0.052 (Δ0.217 ≈ SE의 20배); Ghana 25 labels > S2 1000 labels; GHA→AMZ 0.557(chance 근접) | W3: ASGM-only reference (Amazon Mining Watch 또는 VHR galamsey 판독) |
| 3 | TB02 | S2 | B | Zambia·Bolivia·Para vs Congo·US·Bavaria | C-GO | RSE | Sentinel-1B 고장을 exogenous natural experiment로 써서 관측 가용성이 만드는 허위 change를 정량화하고 availability-aware 임계를 제시 | S1-gap ROI 2022 초과 drift +2.3°, sensor-free S2 baseline은 +0.56°(1/5); 5%-보정 FPR이 Zambia에서 29.9%/32.9% (통제 3.1-4.6%) | W3-4: ZM stable stratum RADD/VHR 500점 검증 + retention×drought 2×2 각 셀 ≥40 ROI |
| 4 | TD01 | S3 | D | Amazon + Congo | C-GO | RSE | degradation을 이진 alert이 아닌 **ordinal intensity 축**으로 측정하고 독립 구조손실에 calibrate | 3-class bal-acc 0.775±0.026 vs S2 0.577±0.019 (+0.198, fold 범위 비중첩); angular change 중위값 단조; GEDI rh98 손실과 Spearman 0.755 (n=275) | W1-2: Sustainable Landscapes Brazil ALS ≥4 사이트 + W7: clearing-fraction 통제 후 partial rho ≥0.15 |
| 5 | TH01 | D1 | H | DPRK + ROK 접경 | C-GO | RSE | 지상자료 0인 지역에서 DMZ가 representation 불연속이 아니라 **관리 불연속**임을 보여 "검증 불가"를 경계가 있는 transfer 문제로 전환 | cross-border cos-sim 0.504(0-100 m)→0.967(≥600 m), vMF kappa 5/6 class에서 DPRK ≥ ROK; ROK OA 0.842±0.020 vs S2 0.715±0.018; DPRK 측 두 독립 산출물 상호일치는 0.674뿐인데 AEF probe는 0.750 | W3: ROK MoE 토지피복 + KFS 임상도 확보, W9: 600점 2인 VHR design-based 검증 |
| 6 | TE02 | S6/S2 | E | Horn of Africa·Sahel·Caatinga | C-GO | RSE | 건조지 허위 change의 원인은 가뭄 **수준**이 아니라 이상치 **전이**이며, ERA5 이상치 보정으로 임계를 복원 | drought-break 17.66° vs stable 14.68°; ET FPR 76.7% vs S2 34.4%; climate partial R² 0.147 vs 0.011; 진짜 class-change 신호(+0.69°)/artefact(+2.98°) = SNR 0.23 | W3-4: 600점 VHR + rangeland 자료로 초과 drift의 과반이 artefact임을 입증 |
| 7 | TC01 | S4 | C | Brazil → Congo | C-GO | IEEE TGRS | terrain/climate-decodable 부분공간이 cross-region identity 부분공간과 일치(14/16)하며, 제거해도 in-domain 손실 없이 transfer 격차의 55%를 회복 | transfer 0.555→0.638 (+0.083), in-domain 0.940→0.942 (fold sd 0.016 내) | ≥8 region pair에서 random-dim null 초과 + static-dim-only z-score가 full z-score 이득의 과반 설명 |
| 8 | TA02 | S5 | A | Amazon + Atlantic Forest | C-GO | RSE | 단일연도 embedding이 재생림 연령을 담지만 12-15년에서 포화하여 29년 범위를 ~9년으로 압축한다는 **상한 논문** | R² 0.288/0.342 vs S2 0.157/0.137; 32년 임분 예측 평균 17.6년 (attenuation slope 0.30); trajectory 추가 이득 0.000-0.006 | W3-4: nonlinear/ordinal head가 상한을 뒤집지 않을 것 + W7: 비-Landsat 독립 reference(ALS/ATL08) |
| 9 | TE06 | S6 | E | Andes vs Mato Grosso | C-GO | IEEE JSTARS | AEF의 우위를 modality별로 귀속시키고, static covariate 흡수율이 **지형 기복에 조건적**임을 보이는 benchmarking 방법론 | 흡수율 Andes 62% vs 평지 15% (land cover), 35% vs 11% (height); AEF 우위는 4/4 cell, 20/20 paired fold 생존 | ≥12 region에서 relief interaction 유의 + W3: 독립 구조 reference (ETH/Meta는 GEDI 순환성으로 헤드라인 제외) |
| — | TH03 | D3 | H | Gaza (Mariupol 탈락) | **NO-GO** | (IEEE GRSL 축소안) | 300 m grid 집계는 building-level 대비 skill을 회복하지 못하며 재건도 탐지되지 않음 | grid AUC 0.605±0.205 vs S2 0.601±0.168 (무승부, 기존 building-level 0.59과 동급); 재건 신호 분리 없음 (20.56/20.15/21.35°) | 재진입 조건: matched S2/S1 trajectory baseline + negative range 있는 제2 도시 확보 (Gaza 단독은 MDD 0.067 > gate 0.03로 검정력 부족) |

## 다양성 점검 (상위 5개 기준)

- Bucket: B(TB01, TB02), A(TA04), D(TD01), H(TH01) = **4 버킷** (요구 ≥3 충족). 상위 6개까지 보면 E(TE02) 추가로 5 버킷.
- 지역: Amazon, Congo, Zambia/Miombo, Ghana/서아프리카, 한반도(DPRK/DMZ) = **5 지역** (요구 ≥2 충족).
- 문제 유형: 표현 자체의 시간 충실도(TB01), 센서 가용성 artefact(TB02), 불법 채굴 집행(TA04), 산림 degradation MRV(TD01), 데이터 차단 지역 모니터링(TH01) — 방법론과 실세계 측정이 균형.

## 권고: 첫 프로젝트

**TB01** — 유일한 무조건 GO이고, 외부 데이터 취득 게이트가 없다(전량 GEE + Hansen/RADD). novelty가 가장
확실하다(연간 embedding의 temporal fidelity를 다룬 저널·프리프린트 0건, 8회 landscape 쿼리와 각 버킷의
반증 시도에서 모두 확인). 게다가 결과가 **다른 토픽의 전제**가 된다: lag-aware change rule은 TB02·TE02의
임계 보정, TD01의 연도 정렬, TH01의 사건 탐지 시점 해석에 그대로 들어간다. 12주 내 TGRS 투고 가능.

**병행 권고**: TA04를 2번째로 착수하되 W1에 ASGM-only reference 확보만 먼저 시도한다(성패가 3주 안에
드러나고, 실패해도 TB01 진행에 영향이 없다). 효과크기가 전 토픽 중 가장 크므로(Δ0.217 ≈ SE의 20배)
게이트를 통과하면 RSE급 결과가 가장 빠르게 나온다.

**TH01(D1)에 대한 별도 권고**: MUST_EVALUATE 지시로 평가했고 증거로 살아남았다. 다만 이 토픽만
유일하게 **두 개의 외부 취득 게이트**(ROK 라벨, 600점 VHR 판독 ~30 person-hours)를 갖는다. 라벨 취득이
가능하면 F·V가 각각 3으로 올라 최상위권으로 이동하므로, 착수 여부보다 **`data/rok/` 확보를 지금 시작하는
것**이 실질적 결정이다. Q1(산림 회복)은 현 상태로 주장 불가임을 다시 강조한다(ROK-2024 probe 직접 적용 시
10-20° 사면에서 +27 pt 허위 회복 vs Dynamic World +4.6 pt).

## 토픽별 pivot 2안

| ID | Pivot A | Pivot B |
|---|---|---|
| TB01 | 조건 붕괴 시 "AEF calibration이 S2보다 우수하다"는 단일 발견으로 IEEE GRSL 축소 | 사건 유형을 벌채에서 화재(MCD64A1 burn date)로 바꿔 within-year timing을 재검증 |
| TA04 | ASGM-only reference 실패 시 label 예산 축을 유지한 채 target을 mining→brick kiln/small dam으로 전환 | Maus 라벨을 그대로 쓰되 대규모/영세 광산 **구분 자체**를 측정 대상으로 재정의 |
| TB02 | stable stratum이 실제 degradation으로 판명되면 주제를 반전시켜 "AEF가 miombo degradation을 Hansen보다 먼저 본다"로 전환 | Sentinel-1C 복구(2024-12) 이후 회복 곡선을 측정하는 recovery-side 논문 |
| TD01 | ALS 확보 실패 시 ICESat-2 ATL08만으로 ordinality 검증 (해상도 손실 명시) | Congo 상단 붕괴가 확인되면 "ordinal 축은 biome-특이적"이라는 조건부 결과로 재프레이밍 |
| TH01 | ROK 라벨 미확보 시 measurand를 hillside cultivation에서 **국경 불연속 자체**로 좁혀 ISPRS JPRS 방법 논문화 | Q3(2024 Yalu 홍수)만 분리해 재난 피해·복구 단일 사례 논문 (여름 홍수가 annual composite에서 소멸하는 대비가 핵심) |
| TE02 | artefact 비율이 과반 미달이면 "AEF가 건조지 생태 전이를 포착한다"는 ecology 논문으로 전환(Global Change Biology 계열) | 보정 자체를 산출물로 만들어 anomaly-aware threshold 데이터셋 논문(ESSD) |
| TC01 | z-scoring이 우세하면 "generic moment-shift 레시피 + scale-dependent decodability" 논문으로 전환 | TESSERA 미러 확보 시 no-static-input 대조군으로 기전 주장을 강화 |
| TA02 | nonlinear head가 상한을 뒤집으면 그대로 age-mapping 논문으로 전환 | 상한이 유지되면 "언제 embedding 기반 regrowth 지도를 carbon crediting에 쓸 수 있는가"라는 정책 논문(ERL) |
| TE06 | rich classical baseline이 격차를 닫으면 그 자체를 결론으로 발표(benchmark 관행 교정) | relief interaction만 남기고 GRSL급 sharp finding으로 축소 |
| TH03 | 자산(UNOSAT 12-epoch onset 디코딩, Gaza 300 m harness)을 TH01의 검증 설계로 이전 | 제2 도시 확보 시 재진입, 단 matched trajectory baseline을 첫 실험으로 |

## Kill log 요약 (전체 15건)

**Stage 1 (11건)** — TA06(단일 epoch 라벨로 성장 검증 불가), TB06·TE05·TF01·TG06(hard kill A≤1 & N≤1),
TC05(TC01+TC04의 단일 사례), TD04(crop type 포화 + yield 라벨 없음), TD05(AGB 4편 이상이 동일 RQ 답변),
TE04(stakeholder 없는 engineering note), TF06(재현 데이터 확보 불가), TH06(cross-view geo-localisation
포화 + dual-use 경계 위험). 상세: `01_stage1_screen.md`.

**Stage 2 (3건 + 1건 흡수 거부)** — 모두 pilot이 전제를 반증했다:
- TC03 (17→10): AEF unit-sphere/vMF 통계가 AEF 자신의 transfer loss를 예측하는 label-free 지표 중 **최약**.
- TF02 (16→10): differential inflation 가설 실패. AEF−S2 격차 부호가 landscape에 따라 반전되고, AEF가
  더 부풀려지는 유일 사례도 "S2 + 300 m focal mean"이 재현 → AEF 특이성 없음. 25/50 km rung은 GEE timeout.
- TG01 (16→11): conformal coverage가 spatial separation에서도 유지(최대 6.2 pp, 대부분 fold sd 내);
  angular distance와 coverage loss 상관 −0.007 (S2 Euclidean은 +0.121). embedding strata의 area-estimation
  SE 개선 1.0% → **TG02도 별도 토픽에서 제외**.

**Stage 3 (1건)** — TH03: 핵심 가설(집계가 skill을 회복)이 기각되고, 살아남은 trajectory 우위는 matched
baseline 없이 주장 불가. 결정적으로 Gaza 단독 설계는 gate(0.03 AUC)를 판정할 검정력이 없다(MDD 0.067,
필요 block 56 vs 보유 11, 무피해 cell 7.0%).

**하지 않은 것**: 쿼터를 채우기 위해 kill을 완화하지 않았다. Stage 2 PASS가 10개로 목표(5-8)를 넘었기
때문에 Stage 1.5(추가 후보 생성)는 불필요했다.

## 파일

`00_landscape.md` · `01_stage1_screen.md` · `stage1/bucket_A..H.md` · `02_stage2_feasibility.md` ·
`stage2/<ID>.md` (13) · `03_stage3_proposals.md` · `stage3/<ID>.md` (10) · `04_final_ranking.md` ·
pilot script와 표본 CSV는 `scratch/` (검증된 asset ID와 두 개의 sampling 함정은 `scratch/STAGE2_KIT.md`).
