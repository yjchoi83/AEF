# 02_stage2_feasibility.md — Stage 2 실현가능성 및 smoke test (13개 토픽, MODE=LIVE)

모든 pilot은 실제 GEE 실행 결과다. 공통 규칙: spatial block GroupKFold(>=10 km, 0.1° block),
mandatory baseline = cloud-masked Sentinel-2 annual median composite(+NDVI/NBR), n·class balance·fold sd 보고.
개별 카드는 `stage2/<ID>.md`, pilot script와 CSV는 `scratch/`.

| ID | Bucket | Stage1 | Stage2 | 판정 | Pilot | 핵심 증거 (AEF vs S2 baseline) |
|---|---|---|---|---|---|---|
| TB01 | B | 17 | 17 | PASS | T1+T2 실행 | event-month 회귀 MAE 1.99개월 vs 2.71; 12-class bal-acc 0.229 vs 0.154 (chance 0.083); mixing 가설 기각 (α̂=0.33·(12−m)/12+0.568); Q4 detection-lag 역전 발견 |
| TB02 | B | 15 | 17 | PASS | T2 실행 | S1-gap ROI 2022 stable-land drift 초과 +2.3° vs 통제; S2 baseline 초과는 +0.56°; 5%-보정 임계에서 Zambia FPR 29.9%/32.9% (6-7배); 역방향: 흐린 Congo에서 S2 FPR 32.2% vs AEF 5.9% |
| TC01 | C | 17 | 17 | PASS | T1+T3 실행 | BR→CG transfer AEF 0.940→0.555 (drop 0.384) vs S2 0.907→0.705 (0.202); static-decodable 상위 16 dim과 mean-shift 상위 16 dim이 14/16 중첩; 제거 시 in-domain 손실 0, transfer +0.083 회복 |
| TD01 | D | 17 | 17 | PASS | T1+T2 실행 | intact/degraded/deforested bal-acc 0.775±0.026 vs 0.577±0.019 (+0.198, macro-F1 +0.218; fold 범위 비중첩); angular change 중위값 11.68°→15.89°→51.98° (GEDI subset) 단조; GEDI rh98 손실과 Spearman 0.755 (changed footprints, n=275); 단 AUC(clearing>degradation)는 Amazon 0.611, Congo 0.490(chance) |
| TH01 | H | 15 | 17 | PASS | T2+T3 실행 | ROK in-region OA 0.842±0.020 vs S2 0.715±0.018 (+12.7 pt), DPRK 측 WorldCover 일치 0.750 vs 0.677; T2는 연도 복원에서 AEF 3/4 sites vs S2 2/4 (z 절대값은 S2가 더 큰 경우 있음); 2024 Yalu 홍수 AEF z=1.8 vs S2 z=0.0; Hwasong은 [U] 좌표로 실패 (음성 결과로 보고) |
| TA02 | A | 17 | 17 | PASS | T4 실행 | age 회귀 R² 0.288/0.342 vs 0.157/0.137, MAE 6.35-6.89년 vs 7.73-7.85; saturation ~12-15년 (11-15y bin MAE 3.6년 → 26y+ 14-16년); trajectory feature 추가 이득 0.000-0.006 |
| TE02 | E | 16 | 17 | PASS | T2 실행 | 전제 역전: drought level이 아니라 anomaly transition이 drift 유발 (onset 16.42°, break 17.66° vs stable 14.68°); climate partial R² 0.147 vs S2 0.011; ET_somali FPR 76.7% vs 34.4%; climate regress-out으로 3/5 ROI 정상화 |
| TA04 | A | 16 | 17 | PASS | T1+T3+T5 실행 | label efficiency: Amazon에서 S2의 1000-label AUC를 AEF 40 labels로 (≥25배), Ghana는 25 labels로 (>40배); full AEF 0.855/0.977 vs S2 0.638/0.867; GHA→AMZ 역방향 0.557(비대칭) + negative transfer 관측 |
| TE06 | E | 17 | 14 | PASS | T1+T4 실행 | AEF 우위가 4개 cell 전부 생존 (20/20 paired folds); static covariate가 AEF−S2 격차를 Andes에서 62% 흡수, 평지에서 15% → "unfair baseline"은 고기복 국소 artefact; static-only는 어디서도 우세하지 않음 |
| TH03 | H | 15 | 14 | CONDITIONAL PASS | T2 실행 | UNOSAT Gaza 174,526 damage sites(12 epoch, 연도 귀속 가능) 확보; grid AUC AEF 0.605 vs S2 0.601 = 무승부 → "aggregation이 skill을 회복한다" 가설 기각; multi-year trajectory 0.879는 matched baseline 미실행 |
| TG01 | G | 16 | 11 | KILL | T1+area est. 실행 | conformal coverage가 spatial separation에서도 유지 (최대 6.2 pp, 대부분 fold sd 내); angular distance-coverage loss 상관 −0.007 (S2 Euclidean +0.121); embedding strata area-estimation SE 개선 1.0% → TG02도 함께 제외 |
| TC03 | C | 17 | 10 | KILL | T3 실행 | 전제 falsify: AEF unit-sphere/vMF 통계가 AEF 자신의 transfer loss를 예측하는 label-free 지표 중 최약 → hard kill (A=0, N=1) |
| TF02 | F | 16 | 10 | KILL | T1 ladder 실행 | differential inflation 가설 실패: AEF−S2 격차 부호가 landscape에 따라 반전(KE −0.038 vs MT −0.053), AEF가 더 부풀려지는 유일 사례도 "S2+300 m focal mean"(−0.043)이 재현 → A=1; 25/50 km rung은 GEE timeout으로 미측정 |

## PASS 토픽별 요약 (Stage 3 진입 10개)

**TB01 (B, S1)** — 연간 embedding의 within-year 시점 정보. 핵심은 seed가 제시한 geodesic mixing 법칙이 정량적으로 **기각**되고, 그 자리에 측정된 대체 모델(α̂ 절편 0.568)과 Q4 detection-lag 역전이 들어온 것이다. 즉 12월 벌채도 year-Y embedding을 post-state의 약 57%까지 이동시키며, 이는 annual 산출물의 change rule을 다시 써야 함을 뜻한다. 위험은 1-2월 alert 이상치가 dry-season 현상학의 부산물일 가능성으로, Congo Basin(bimodal season) 복제가 결정적 시험이다.

**TB02 (B, S2)** — Sentinel-1B 고장(2021-12)이 만든 exogenous natural experiment. S1 VV scene 잔존율이 대륙과 정렬되지 않아(Zambia 0.01, Congo 0.97) 지역 교란 없이 식별이 가능하다. sensor-free S2 baseline이 같은 조건에서 1/5 크기 효과만 보이므로 초과 drift는 AEF 특이적이다. GRACE V04는 2024-09 종료 + 2017-18 gap으로 사용 불가 판정.

**TC01 (C, S4)** — static/climate 입력 의존이 transfer 손실의 기전이라는 주장을 in-domain 무손실·transfer 회복이라는 이중 조건으로 확인했다. 다만 ROI 내 static decodability는 R²≤0.47로 문헌의 0.97과 다르며(100 km ROI의 지형 범위 한계), per-region z-scoring이 ablation보다 더 잘 작동해 moment shift가 경쟁 설명으로 남는다. TESSERA가 GEE에 없어 matched no-static-input 통제는 desk-only.

**TD01 (D, S3)** — degradation intensity를 ordinal 축으로 다루는 새 measurand. separability와 ordinality 두 축 모두에서 S2 baseline을 이기고(+0.198 bal-acc) GEDI 구조손실과 연결된다. 다만 축의 상단(clearing vs degradation)은 Congo에서 chance 수준이다. F는 3→2로 하향(DETER off-GEE, TMF degradation 미귀속, ALS/ATL08 필요). 최대 위협은 30 m TMF cell 내 clearing fraction proxy 가능성.

**TH01 (H, D1, MUST_EVALUATE)** — 증거로 확인된 flagship. 핵심 근거는 label-free 지표다: ROK class centroid에 대한 mean max-cosine이 ROK 0.874 → DPRK 0.837로 0.037만 떨어지고, vMF kappa는 water를 제외한 5/6 class에서 DPRK가 같거나 더 집중되어 있다. 즉 국경은 representation-space 붕괴가 아니라 management 불연속이며, 이는 D1 Q4 가설을 지지한다. 또한 DPRK 측에서 WorldCover와 Dynamic World의 상호 일치가 0.674뿐이어서, ROK-훈련 AEF probe의 0.750은 두 독립 산출물 간 일치보다 높다 — 잔차는 domain shift보다 label noise가 지배한다. `LABELS=FALLBACK`(Dynamic World는 paddy/dry cropland 분리 불가)이 V를 2로 묶고 있으며, `data/rok/` 제공 시 F·V 상향. Q1(산림 회복)은 ROK-2024 probe 직접 적용 시 +27 pt의 허위 회복이 나와 per-year training과 domain adaptation 없이는 주장 불가.

**TA02 (A, S5)** — 단일연도 embedding이 stand age를 담지만 12-15년에서 포화한다. trajectory feature는 이득이 없어(0.000-0.006) AEF 9년 window의 한계가 아니라 표현 자체의 한계임을 시사한다. 프레이밍은 age mapping이 아니라 carbon accounting 용도의 **ceiling 논문**. MapBiomas age가 Landsat 파생이라 순환성 위험이 있어 V=2.

**TE02 (E, S6/S2 분기)** — TB02와 분업이 성립한다. TB02는 관측 가용성 경로, TE02는 기후 경로이며 partial R²(clim|obs 0.147 > obs|clim 0.087)와 S1 커버리지가 오히려 증가한 ET_somali에서도 FPR 76.7%가 나오는 점이 분리를 증명한다. 정책적 의미: 진짜 DW class-change 신호(+0.69°)가 drought-break artifact(+2.98°)보다 작아 SNR이 0.23에 불과하다.

**TA04 (A, S8)** — Maus et al. mining polygon이 실제 reference로 확보되어 proxy 논쟁을 회피했다. label efficiency 우위(25-40배)는 convenience가 아니라 sparse-label 영역의 과학적 이점이며, GHA→AMZ 비대칭과 negative transfer는 별도의 발견이다. 위험은 Ghana box에 Tarkwa/Obuasi 대규모 광산이 섞여 ASGM-only 검증이 필요하다는 점(V=2).

**TE06 (E, S6)** — 비판이 아니라 조건부 확인으로 귀결. 정직하게 총점을 17→14로 내렸다. 남는 기여는 "static covariate 흡수율이 지형 기복에 따라 62% vs 15%로 갈린다"는 interaction이며, capacity/capability 혼입(차원·시간해상도 맞춘 고전 baseline)이 최대 위협이다. canopy height cell은 ETH height가 GEDI 파생이고 GEDI가 AEF 입력이라 label-source 중첩 위험.

**TH03 (H, D3) — CONDITIONAL** — 독립 damage reference(UNOSAT 174,526 sites, 연도 귀속 가능)를 실제로 확보한 것이 최대 성과지만, 핵심 가설("neighbourhood 집계가 building-level의 낮은 skill을 회복")은 기각됐다(0.605 vs 0.601, 무승부). 조건: Stage 3의 첫 실험은 S2/S1 multi-year trajectory baseline이며, 이것이 AEF의 0.879를 0.03 AUC 이내로 따라오면 NO-GO. Gaza는 무피해 cell이 7.0%뿐이어서 negative-side range 부족 → 제2 도시(Khartoum) 필수. 윤리: 공개데이터·근린 단위·재건 프레이밍만.

## Budget 및 규정 준수 기록

- Stage 2 lookups: 토픽당 <=6 준수. OpenAlex는 세션 중 일일 비용 한도 소진 → 이후 arXiv(https) 전용, 미검증 항목은 [U] 태그.
- Pilot run cap(3) 초과 2건 declared: TH01 5회, TH03 6회 — 모두 harness/GEE 실패(memory limit, computation timeout, band-key 버그) 재시도이며 결과를 본 뒤 실험을 재설계한 사례는 없음.
- API 529 다발로 4개 agent가 중단 후 재개됨. 재개 시 완료 단계를 재실행하지 않도록 부분 저장(`scratch/*_progress.txt`) 적용.
- 검증 오류 정정: `projects/sat-io/*`는 읽기 가능(내가 추측한 ID가 틀렸음) — `global_mining_polygons` 사용 확인. `COPERNICUS/DEM/GLO30`은 deprecated → `GLO30_2024_1`. MapBiomas Collection 10은 GEE에 없음(9 사용).
- TH01 수치 계보 정정: 본 표와 문단은 최종본 `stage2/TH01.md`(WorldCover 2021 라벨, AEF year 2021 정렬)을 기준으로 한다. 세션 중간 보고에 등장한 `z=9.8`·`+7.3 pt` 등은 폐기된 초기 run(Dynamic World 2024 라벨) 수치이며 인용하지 않는다. 최종 run에서 z 절대값은 일부 site에서 S2가 더 크고, AEF의 우위는 **보고 연도 복원 정확도**(3/4 vs 2/4)와 여름 홍수 같은 sub-annual 사건 보존(z 1.8 vs 0.0)에 있다.
