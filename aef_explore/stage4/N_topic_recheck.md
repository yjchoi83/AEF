# N — 토픽 novelty 재검증 (Stage 4, 2026-09-04)

대상: GO 1개(TB01) + CONDITIONAL-GO 8개(TA04, TB02, TD01, TH01, TE02, TC01, TA02, TE06). NO-GO인 TH03은 제외.
API: **Semantic Scholar + arXiv**(§2.3 규정대로 OpenAlex는 일일 한도 소진으로 사용 불가). 모든 인용은
in-session API 응답으로 확인된 것만 **[V]**, 확인 실패는 **[U]**, 429로 결과를 얻지 못한 쿼리는 **[U-429]**로
남기고 어느 방향으로도 증거로 쓰지 않았다.

## 결론 한 줄

**KILLED-BY-LITERATURE = 0건. NARROWED = 1건(TE06, RQ1 선점). 나머지 8개 토픽 SURVIVES.**
단 하나의 실질적 변화가 TE06에서 나왔고, 이는 D2의 병합 결정을 바꿀 만큼 중요하다.

## 토픽별 판정

| ID | 판정 | 근거 | 가장 위협적인 2025-2026 문헌 |
|---|---|---|---|
| TB01 | SURVIVES | mechanism 쿼리(within-year timing, annual embedding change detection, satellite embedding phenology, detection lag forest, annual composite timing disturbance) 전부 arXiv **genuine zero-hit**(요청 성공, n=0). annual embedding의 event-month 회복 가능성을 다룬 문헌 없음 | arXiv:2608.12663 [V] (AEF wildfire susceptibility) — ADJACENT, 월 단위 timing 주장 없음 |
| TB02 | SURVIVES | `all:"Sentinel-1" AND all:"outage"` n=0, `all:"missing observations" AND all:"land cover" AND all:"time series"` n=0, `all:"data gap" AND all:"SAR" AND all:"change detection"` n=0 — 모두 요청 성공한 zero-hit. sensor outage로 생기는 허위 change를 정량화한 문헌 없음 | arXiv:2606.29134 [V] (Beyond Backscatter: AEF land-cover priors for SAR flood segmentation) — ADJACENT, artefact 정량화 아님 |
| TC01 | SURVIVES | terrain/static-decodable subspace의 dimension-level attribution + ablation을 수행한 문헌 없음. 관련 쿼리 6건 중 OVERLAP 0건 | arXiv:2606.20034 [V] (AEF·TESSERA LCZ 비교, Switzerland) — ADJACENT이자 **신규 필수 인용**: TESSERA 대조가 이제 문헌에 존재 |
| TD01 | SURVIVES | ordinal degradation axis / sub-pixel clearing fraction / ALS·ICESat-2 calibration을 겨냥한 14개 쿼리에서 OVERLAP 0건 | arXiv:2603.06382 [V] (CHMv2 canopy-height FM) — ADJACENT, degradation measurand 아님 |
| TE02 | SURVIVES | dryland 허위 change를 climate-anomaly **transition vs level**로 귀속하고 ERA5 보정을 제시한 문헌 없음 | DOI:10.1371/journal.pone.0344835 [V] (Asian drylands GEE) — ADJACENT, embedding drift·FPR 귀속 없음 |
| **TE06** | **NARROWED** | **RQ1이 선점됐다.** arXiv:2609.03480 [V] (Denmark tree-species: S1+S2 spectral-temporal features + canopy height + XGBoost vs AlphaEarth/TESSERA, 전국 규모 검증, modality ablation)이 "AEF margin이 dimensionality·temporally matched classical baseline에서 살아남는가"에 이미 답했다 — **baseline이 전반적으로 우세하고 embedding은 low-label regime에서만 우세**. DOI:10.5194/isprs-annals-xi-3-2026-117-2026 [V] (S2 time-series features + AEF, forest type)이 약한 2차 확인. 두 논문 모두 **terrain-relief interaction은 검정하지 않음** | arXiv:2609.03480 [V] — RQ1 kill |
| TA02 | SURVIVES | stand-age saturation / regrowth age + embedding / canopy height + forest age 쿼리 arXiv zero-hit. embedding 기반 age ceiling을 nonlinear·ordinal head와 비-Landsat 독립 reference로 bound한 문헌 없음 | arXiv:2608.04792 [V] (GFM biomass regression) — ADJACENT, target이 age 아님 |
| TA04 | SURVIVES | mining/ASGM에 대해 label-parity ratio·transfer asymmetry·negative pooling을 측정한 문헌 없음 | arXiv:2605.10029 [V] (AEF slum detection, 12 cities) — 같은 representation-evaluation 기전, 도메인 불일치 |
| TH01 | SURVIVES (양 sub-RQ) | cross-border embedding-shift 진단(a), data-denied 국가의 GFM 기반 design-based 면적추정(b) 모두 해당 문헌 없음 | DOI:10.1109/JSTARS.2025.3608777 [V] (TerraDA, cross-city DA) — 정치적 국경·DPRK 사례 아님 |

## TE06 조치 (유일한 실질 변경)

RQ1은 **replication으로 강등**해야 하고 논문의 novelty는 전부 RQ2(relief-conditioned static-covariate
absorption, pilot 62% vs 15%)에 실린다. Denmark 논문의 "embedding은 low-label regime에서만 우세"라는
결론은 TE06뿐 아니라 **TA04의 label-efficiency 주장과 같은 방향**이므로(그쪽은 오히려 보강) 두 토픽의
서사를 함께 조정해야 한다. D2는 이 가정 위에서 TC01+TE06 병합을 권고했다.

## 신규 필수 인용 / baseline (모두 [V])

| ID | 왜 필요한가 | 해당 토픽 |
|---|---|---|
| arXiv:2507.22291 | AEF 원 논문 (base embedding source) | 전 토픽 |
| arXiv:2609.03480 | matched spectral-temporal baseline vs AEF/TESSERA, low-label regime 한정 우위 | TE06(RQ1 kill), TA04, TC01 |
| DOI:10.5194/isprs-annals-xi-3-2026-117-2026 | S2 time-series features + AEF 결합, forest type | TE06, TC01 |
| arXiv:2606.20034 | AEF vs **TESSERA** 실제 비교 사례 (LCZ, Switzerland) | TC01, TE06 |
| arXiv:2603.02080 | From Pixels to Patches: Earth embedding pooling 전략 | TC01 |
| arXiv:2601.11183 | ultra-lightweight Earth embedding database (ESSD) | TB01, TC01 |
| arXiv:2606.29134 | AEF land-cover prior + SAR flood segmentation | TB02 |
| arXiv:2608.01751 | SPECTRA: cross-sensor fine-tuning of GFMs | TC01 |
| arXiv:2608.04792 / arXiv:2606.05368 | GFM biomass regression / Biomazon 3D 구조 데이터셋 | TA02, TD01 |
| arXiv:2605.10029 | AEF slum detection 12 cities (representation-evaluation 선례) | TA04 |
| DOI:10.1109/JSTARS.2025.3608777 | TerraDA cross-city domain adaptation | TH01 |
| DOI:10.7780/kjrs.2025.41.5.10 | KJRS AEF-in-Korea (수질) — 한국 맥락 인용 | TH01 |

## Coverage 한계 (정직 보고)

- **Semantic Scholar가 세션 대부분 429로 차단됐다**(공유 IP + 동시 세션). TB01/TB02/TC01의 S2 쿼리 13건 중
  11건이 [U-429]다. 이 세 토픽의 SURVIVES 판정은 **arXiv의 성공한 zero-hit 쿼리**(요청이 200으로 성공하고
  결과가 0건)에 근거하며, 429 쿼리를 "없음의 증거"로 쓰지 않았다. OpenAlex는 한도 소진으로 전 세션 불가.
- 따라서 TB01/TB02/TC01은 **arXiv 단독 커버리지**다. 저널 전용 문헌(TGRS/RSE/JSTARS 2026 최신호)에 대한
  커버리지는 g2/g3 토픽보다 얕다. 투고 전 한 번 더 S2/OpenAlex로 재조회할 것을 권고한다.
- 판정을 쿼터에 맞추지 않았다: kill 0건은 완화의 결과가 아니라 mechanism 쿼리가 실제로 비어 있었기 때문이며,
  유일하게 실제 충돌이 발견된 TE06은 그대로 NARROWED로 내렸다.

세부 로그: `parts/N_g1.md`(초기 시도, 429 기록), `parts/N_g1_raw.txt`(재조회 원시 로그), `parts/N_g2.md`, `parts/N_g3.md`.
