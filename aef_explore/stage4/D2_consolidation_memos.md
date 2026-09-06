# D2 — Consolidation memos (병합 설계)

## Design A: TB02 (observation-availability) + TE02 (climate-anomaly-transition)

### 1. Merged claim
**논문은 하나, single measurand.** 두 topic 모두 이미 동일 sample frame(0.1° block, stable-land stratum)과 동일 measurand(pixel 자체 median 대비 angular drift, arccos⟨e_y, ê_ref⟩)를 공유하고 있으므로, 병합 논문의 단일 measurand는 **"exogenous input-availability shock와 exogenous climate-anomaly transition이 stable-land embedding drift에 대해 갖는 partial-R² 기반 분해 가능 기여도(그리고 그 상호작용)"**다. 두 개의 서로 다른 자연실험(S1B outage, drought onset/break)을 하나의 pixel-FE panel에서 동시에 식별하는 **decomposition paper**로 프레이밍한다.

### 2. Shared strata
Cross factor: **S1 retention 5분위(TB02) × climate-anomaly state 3분위(onset/stable/break, TE02) × biome/aridity 4계층(humid tropical·temperate·semi-arid dryland·arid dryland) × cloud regime 2분위(low/high S2 cloud fraction)**. 완전교차 cell 수 = 5×3×4×2 = **120 cell**이며, 개별 논문의 power 계산(TB02: d≈0.65→ROI≈50/군, TE02: d≈0.68→ROI≈46/군)을 그대로 유지하려면 cell당 40-50 ROI가 필요해 완전 균형에는 4,800-6,000 ROI가 필요 — **비현실적**. 따라서 실제 표본은 marginal 2-way contrast(retention×anomaly, retention×biome, anomaly×biome)마다 최소 검정력을 확보하는 **부분 요인설계**로 총 350-400 ROI(TB02 200-300과 TE02 250-350의 union 상단)를 배분하고, **retention×anomaly interaction cell(특히 "retention 정상+강한 transition")을 우선 채운다**(이는 두 논문 모두 자기 verdict의 GO 조건으로 이미 요구한 cell이다). 솔직한 confound: **retention과 aridity/biome은 orbit·지리로 인해 상관될 수 있다** — pilot 6 ROI 기준 ZM_miombo(retention 0.01)는 semi-arid miombo이자 2021-22 가뭄과 collinear, CD_congo(retention 0.97)는 humid, 즉 "low retention × arid" 쪽 cell은 실제로 채워지기 쉽고 "low retention × humid" 또는 "high retention × extreme drought" cell은 비거나 sparse할 위험이 크다. 이 collinearity는 은폐하지 않고 T1에 cell 표본수와 empty-cell 목록을 그대로 보고한다.

### 3. One drift model
단일 panel (pixel FE, ROI-clustered SE):

```
drift_iy = α_i + β1·retention_iy + β2·onset_iy + β3·break_iy
           + β4·(retention_iy × onset_iy) + β5·(retention_iy × break_iy)
           + γ·z_level_iy + δ·cloud_iy + θ_year + ε_iy
```

식별 논거: **β1(관측결손 경로)의 외생성**은 S1B 태양전지판 고장(2021-12, 하드웨어 이벤트, 지표상태와 무관)이 제공하며 2021-12 기준 event-study pre-trend 검정으로 확인한다. **β2/β3(기후전이 경로)의 외생성**은 ERA5 강수/토양수분 anomaly가 pixel 자체 기후사(pixel FE로 제거)에 대한 편차이며 기상변동 자체는 land-management 결정에 선행하는 exogenous shock라는 논거(TE02 RQ1 재정의: level이 아니라 transition)로 성립한다. **두 경로의 분리**는 partial-R² 분해로 수행: clim|obs, obs|clim, joint, residual 네 성분을 ROI별로 보고 — pilot 수치 그대로 clim|obs 0.147(sd .027) vs obs|clim 0.087(TE02), ZM_miombo S1 R²=0.245 vs CD_congo 0.019(TB02) — 그리고 상호작용 β4/β5가 "retention 붕괴가 climate 효과를 증폭/차폐하는가"를 직접 검정해 TB02의 Top threat(#1, Zambia 가뭄-blackout collinearity)와 TE02의 Top threat(#3, retention 잔여교란)를 하나의 계수로 흡수한다. **사전등록 기각 기준**: (i) β1의 dose-response가 선형이면(blackout threshold 없이) H1 기각, sensor-free S2 baseline에서 동일 excess 재현 시도 기각, (ii) β2/β3의 95% CI가 0을 포함하거나 z_level 계수가 양의 유의이면 H1(TE02) 기각, (iii) β4/β5가 유의하지 않으면 "두 경로는 독립적으로 가산"으로 결론(병합의 정당성은 유지되나 상호작용 스토리는 폐기).

### 4. One baseline suite
| rung | 내용 | 차원 | temporal richness |
|---|---|---|---|
| R0 | sensor-free S2 annual median composite, 동일 angular metric | 6-8 feature unit vector | annual (AEF와 정합) |
| R1 | TESSERA(S1+S2 GFM) | ~64-128D | annual |
| R2 (fallback) | Clay v1 | ~64D | annual |
| R3 | NDVI/VCI anomaly ("순수 기후신호 상한", TE02 고유) | 1D | annual |
| R4 (reference, not baseline) | Hansen annual loss / Dynamic World class change | categorical | annual |

R0은 두 논문 모두의 mandatory baseline(이미 각각 pilot에서 사용), R1/R2는 TB02에는 "SAR dose-response 이상적 대조군", TE02에는 "ERA5/DEM을 input으로 안 쓰는 climate-input-dependence 대조군"으로 동시에 기능한다. 두 半이 서로 다른 baseline을 썼다는 비판을 사전에 봉쇄한다.

### 5. 병합이 각 원 topic을 강화/약화하는가
- **TB02**: 강화 쪽이 크다 — TE02가 이미 요구한 "retention×drought 2×2" 설계가 그대로 병합 panel의 상호작용항이 되어, TB02 자신의 Top threat(Zambia 가뭄-collinear)를 covariate가 아니라 **명시적으로 식별된 계수**로 처리할 수 있다. 다만 TB02의 강점은 "6-7배 FPR, blackout threshold"라는 **단일하고 날카로운 operational 서사**였는데, 두 번째 경로가 들어오면 그 서사가 흐려지고 RSE/TGRS 리뷰어에게 "산만한 two-pathway paper"로 읽힐 위험이 생긴다 — effect-size 자체는 안 줄지만 **narrative dilution**.
- **TE02**: 식별 강화는 확실 — clim|obs > obs|clim의 partial-R² 주장이 TB02의 retention 변수를 명시적 통제로 포함함으로써 더 방어 가능해진다. 그러나 TE02는 원래 FEWS NET/IGAD/UNCCD LDN이라는 **정책 stakeholder에 직결되는 단일 스토리**(dryland 조기경보 보정)로 설계됐고, ERL(Environmental Research Letters)라는 정책지향 저널을 secondary로 뒀다 — 병합되면 이 정책적 focus가 "GFM representation의 두 취약점 비교"라는 더 기술적인 논문에 희석되어 ERL 경로가 사실상 사라진다. 또한 TE02 자체가 이미 "BR_caat 보정 불가능(0건)", "ET는 3.5배 감소했지만 여전히 4배 초과"처럼 자기충족적이지 않은 caveat를 가지고 있어, TB02의 더 깔끔한 6-7배/blackout-threshold 결과에 가려질 위험(reviewer가 "TB02가 메인이고 TE02는 부록"으로 읽을 위험)이 있다.

### 6. Recommendation
**MERGE ASYMMETRICALLY** — TB02를 주축(primary spine)으로 삼고 TE02를 "climate-transition companion pathway" 섹션으로 편입한다. 결정적 이유: (i) TB02가 이미 stakeholder 범위(EUDR/GFW/국가 MRV)와 effect 선명도(6-7× FPR, 비선형 blackout threshold, 비대칭 modality robustness)에서 더 강한 단독 서사를 갖고 있고, (ii) TE02가 자신의 GO 조건 자체에서 "retention×drought 2×2를 못 채우면 SNR<unity 단일발견으로 축소, GRSL 전환"을 이미 예정해 두었으므로 독자 논문으로서의 최저선이 TB02보다 낮다, (iii) 두 논문을 따로 내면 동일 sample frame·동일 angular-drift metric을 쓰는 두 RSE 투고가 리뷰어 pool과 novelty 주장에서 충돌할 위험이 크다.
**Figure/table 분할**: F1(retention map)·F2(event-study, {AEF,S2,TESSERA})·F3(FPR inflation curve)·F4(ZM/BR map+면적추정) = TB02 소유 유지. TE02는 **F5(dryland transition drift reversal: level vs transition premise 반전 + SNR<1 그림)**와 **T2(dryland FPR restoration table: ET/SN/ZW/US, 보정 전/후)**로 편입되며, **T1(joint pixel-FE panel, interaction 포함)**은 공유 테이블로 신설한다. TE02의 정책 지향 ERL 경로는 폐기하지 않고, 병합 논문 투고 후 **독립적인 짧은 policy note**(SNR<1, dryland 조기경보 보정 권고만)로 별도 파생 가능성을 남긴다.

---

## Design B: TC01 (dimension-level static/climate-input attribution, transfer) + TE06 (fair-baseline modality attribution, relief-conditioned, in-domain)

### 결정적 제약 처리
2026년 Denmark tree-species mapping 논문(arXiv:2609.03480, [V])이 TE06의 RQ1("capability-matched·dimension-matched classical baseline에도 AEF-specific margin이 남는가")과 동일한 유형의 질문을 이미 답했다 — **matched spectral-temporal classical baseline이 전체적으로 이긴다, embedding은 label-scarce 구간에서만 이긴다.** 이는 TE06 pilot 자체의 "AEF margin 4/4 cell·20/20 fold 생존"이 (i) 도메인이 다르고(Andes/Mato Grosso LC·height vs Denmark tree species), (ii) baseline이 아직 최상위 rung(R3/R4, S1+Landsat+percentile/harmonic)까지 확장되지 않은 pilot 결과라는 점에서 **아직 반증되지는 않았지만**, RQ1급 질문 자체의 **일반적 결론(baseline이 대개 이긴다, embedding은 low-label에서만 이긴다)이 외부에서 이미 확립**되었으므로, TE06가 RQ1을 단독 headline으로 계속 주장하면 "이미 답변된 질문의 재확인"으로 읽혀 novelty가 크게 깎인다. → **TE06의 유일한 생존 novelty는 RQ2(relief-conditioned static-covariate absorption fraction)이며, 이는 TC01의 RQ3(TE06↔TC01 공유 예측: absorption fraction이 transfer recovery를 예측)과 정확히 맞물린다.** 이 사실이 병합 설계 전체의 축이 된다.

### 1. Merged claim
**논문은 하나, single measurand.** Measurand = **"static/climate-decodable subspace가 설명하는, (a) in-domain에서는 relief-conditioned margin-absorption fraction, (b) cross-region에서는 dimension-removal transfer-recovery fraction — 이 둘을 relief가 매개하는 하나의 인과 사슬"**. TE06는 RQ1(margin survives)을 headline에서 내리고 오직 absorption-fraction 산출 모듈로 축소, TC01은 transfer attribution의 spine을 유지한다.

### 2. Shared strata
Cross factor: **relief tier 3분위(low <2°, mid 2-15°, high >15°, TE06의 14-region 층화 채택) × region-pair 12개(TC01, 4대륙·climate 교차) × ROI extent scale 4단계(25/100/400/1000 km, TC01 scale ladder)**. 완전교차 = 3×12×4 = 144 cell로 과다 — 모든 region-pair가 모든 scale에서 유효하지 않다(예: 1000 km ROI는 관할 국가 경계·biome 경계를 넘어가 원래의 relief-homogeneous ROI 정의가 무너짐, low-relief↔low-relief pair는 static contrast가 작아 검정력이 낮음). 따라서 **48 primary cell(12 pair × 4 scale)을 1차 표본으로 확정**하고 relief는 categorical stratum이 아니라 **continuous moderator**(median slope, mixed-effects random intercept by region-pair)로 다뤄 요인설계의 조합 폭발을 피한다 — 이는 TE06가 이미 선택한 방식(H2를 mixed-effects로 검정)과 동일하다. Per-cell target: pixel-level classification sample은 TC01 기준 region당 3,000점 균형표본을 유지하고, scale-ladder 반복(같은 pair를 4 scale에서 재추출)에는 추가 GEE 비용만 든다(라벨/분류기 재사용).

### 3. One attribution model
```
T_p  = a + b1·S_scale(p) + b2·A_relief(p) + b3·(S_scale × relief) + u_p  (region-pair random effect)
A_r  = c + d1·relief_r + e_r                                              (TE06 RQ2)
S_s  = f + g1·scale_s  + h_s                                              (TC01 RQ2)
```
- **T_p** = TC01의 dimension-removal transfer-recovery fraction(pair p).
- **A_relief** = TE06의 in-domain static-absorption fraction(region r, relief 함수).
- **S_scale** = TC01의 static-decodability(ROI extent scale s의 함수, ridge R²).
Relief는 A와 T를 매개하는 조절변수(moderator)로서 양쪽 식에 동시 등장한다. 이것이 바로 TE06 §2 RQ3("H3: absorption fraction과 dim-removal transfer recovery가 relief를 매개로 Spearman ρ≥0.5")이며, 병합 논문의 headline test가 된다. Static-R2 ranking과 cross-region mean-shift ranking의 14/16 중복(TC01 pilot)은 이 모델에서 "A와 T가 같은 물리적 subspace를 가리키는가"의 검정으로 재사용한다.

### 4. One baseline suite
TE06의 baseline ladder **R0(S2 median 8-band) → R1(+static-6) → R2(+percentile/harmonic) → R3(+S1 VV/VH) → R4(+Landsat, ≈64-90D)**를 그대로 공유 ladder로 채택한다 — TC01이 이미 자기 데이터 절에서 "S2+static(TE06의 baseline ladder와 접속)"이라고 명시했으므로 접속점은 기존 설계에 존재한다. 각 rung을 linear probe와 GBT 양쪽으로 돌려 capacity confound를 분리하는 것도 공유. 차원/temporal richness 표는 TE06 §5 그대로: R0(8D, annual) / R1(14D, annual+static) / R2(~30D, intra-annual percentile+harmonic) / R3(~50D, +SAR) / R4(~64-90D, +Landsat, AEF-64와 차원 정합). 이 하나의 ladder를 TC01의 transfer-arm과 TE06의 in-domain-arm이 동시에 보고하므로 "두 半이 다른 baseline을 썼다"는 반론이 원천 차단된다.

### 5. 병합이 각 원 topic을 강화/약화하는가
- **TC01**: 강화가 명확하다. TC01의 최대 threat는 "단일 region pair pilot이라 일반화가 검증되지 않았다"인데, TE06의 relief-conditioned absorption fraction이 **"relief contrast가 큰 pair에서 dim-removal transfer recovery가 커야 한다"는 사전등록 가능한 예측**을 제공해 TC01의 55% 회수라는 단일 수치를 일반 법칙으로 승격시킨다. 또한 TE06의 R3/R4 rung(capability-matched GBT baseline)은 TC01이 원래 "TESSERA가 GEE에 없어 matched no-static-input control 부재"로 자인한 threat를 부분적으로 메운다. Identification 관점에서 TE06는 confound가 아니라 **TC01의 핵심 계수(relief moderator)를 강화하는 제2의 독립 측정**으로 작동한다.
- **TE06**: 결정적 제약 때문에 **약화가 불가피하며, 이것이 오히려 병합을 필요로 만든다.** RQ1이 외부에서 선점된 이상 TE06 단독 논문(JSTARS 목표)은 "이미 알려진 결론을 다른 지역에서 재확인"으로 읽혀 novelty score가 떨어지고, secondary 저널(ISPRS)로도 방어가 어려워진다. 반면 RQ2(relief-conditioned absorption)는 그 자체로는 여전히 참신하지만 **단독으로는 규모가 작아(14 region, 2 target) 독립 논문의 무게가 부족**하다. 즉 TE06는 홀로 서면 "선점된 RQ1 + 얇은 RQ2"로 격하되지만, TC01의 transfer 스토리에 RQ2만 이식하면 TC01의 일반화 문제를 푸는 핵심 조각으로 재탄생한다 — **병합이 TE06를 구제(salvage)한다.**

### 6. Recommendation
**MERGE, TC01을 primary spine으로.** 결정적 이유: (i) 외부에서 검증된 arXiv:2609.03480이 TE06의 RQ1을 선점해 TE06 단독 존속 근거를 약화시켰고, (ii) TE06 RQ3가 이미 TC01과의 연결을 사전등록된 가설로 설계해 두어 병합이 "억지 결합"이 아니라 **원래 설계 의도**이며, (iii) target journal도 수렴한다(TC01 primary=TGRS, TE06 stretch=TGRS) — 병합 논문은 TGRS를 주 타깃으로 유지할 수 있다. Abstract는 TE06식 "AEF margin survives unfair-baseline critique" 문장을 **삭제**하고, 대신 "동일한 static/climate-decodable subspace가 in-domain margin의 relief-조건부 일부와 cross-region transfer loss를 동시에 설명한다"는 단일 인과 서사로 시작하며, Denmark 논문을 "RQ1급 질문은 이미 다른 도메인에서 답변됨 — 본 논문의 기여는 그 다음 질문(왜/어디서 그런가)"이라는 각주로 인용해 선점 문제를 정면 처리한다.
**Figure/table 분할**: F1(region×region transfer matrix, TC01) · F2(static decodability vs scale, TC01) · F3(dim-removal recovery vs random-null, TC01) 유지. TE06는 **F4(relief-conditioned absorption fraction, "fair baseline" 프레이밍을 "moderator evidence" 프레이밍으로 재서술)**로 편입되고, 신설 **F5(headline)**로 absorption fraction × transfer-recovery 산점도(relief로 색칠, TE06 RQ3 검정)를 배치한다. **T1**은 12 pair × 4 scale × ladder rung의 공유 결과표, **T2**는 relief mixed-effects model 결과(TE06 RQ2)로 유지한다. TE06가 계획했던 canopy-height/circularity 관련 서브분석(ICESat-2/ALS)은 지면 압박 시 supplementary로 강등하되 폐기하지 않는다.
