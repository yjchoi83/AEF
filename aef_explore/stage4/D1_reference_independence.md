###### D1 — Reference-independence audit (9 topics)

**AEF contamination set**(§4.1 기준): Sentinel-1 C-band SAR, Sentinel-2, Landsat 8/9, **GEDI canopy-height raster**, Copernicus GLO-30 DEM, ERA5-Land monthly, ALOS PALSAR-2 ScanSAR, GRACE monthly mass grid, geocoded text. 아래 표에서 "Shares input with AEF?"는 이 8개 센서/그리드 목록만 대상으로 한다(geocoded text는 land-cover/구조 reference와 무관하므로 표에서 생략).

## 1. Reference × Contamination 표

| Topic | Reference dataset | Role | Upstream sensors & products | Shares input with AEF? | Contamination type | Severity | Effect on claim |
|---|---|---|---|---|---|---|---|
| TB01 | RADD confirmed alert | training label (event date) | Sentinel-1 C-band 시계열 이상치 알고리즘 | S1 | Shared-sensor, independent pipeline | MED | RQ1 law/RQ2 lag의 날짜 축이 S1-derived date에 고정 — AEF도 S1을 섭취하므로 "AEF의 drift가 S1 신호를 재현했을 뿐"이라는 반론 가능. §4에 명시된 manual date + GLAD-S2 cross-date + S2 baseline confound control로 완화되나, 그 W-단계 실행 전까지는 잔여 위험. |
| TB01 | Hansen `lossyear` | stratification (clearing/stable 정의) | Landsat annual composite, 자동 classifier | Landsat | Shared-sensor, independent pipeline | LOW | clearing 여부만 정의(연도 단위), event month는 안 씀 → headline law/lag 수치에 직접 기여 안 함. |
| TB01 | GLAD-S2 alert | cross-date validation | Sentinel-2/Landsat 기반 자동 알고리즘 | S2, Landsat | Shared-sensor, independent pipeline | MED | RADD와 다른 센서·다른 알고리즘이라 label-algorithm 수준 독립은 확보되나, S2는 AEF 직접 입력이라 잔여 관측-캘린더 공유가 남음(§4에 이미 명시). |
| TB01 | 수동 판독 event date (S2/Planet-NICFI, n≈600) | primary validation (독립 날짜) | 인간 판독, S2 또는 Planet NICFI 영상 | Planet NICFI 사용 시 없음 / S2 사용 시 S2 | Human-interpreted | LOW(Planet 사용 시) / MED(S2 사용 시) | 날짜 오차가 알고리즘 편향과 무관해짐 — Planet NICFI를 쓸 경우 센서 수준까지 독립. |
| TB01 | DETER-B | cross-date validation | 인간 판독(INPE, Landsat/CBERS/S2 화면판독) | 판독은 인간, 기반 영상은 Landsat/S2 계열 | Human-interpreted | LOW | 인간 판독이라 알고리즘 순환은 없음; 영상 겹침은 잔존하나 판독 오차 구조가 다름. |
| TB02 | S1 retention (5계층) | **treatment 변수(참조 아님)** | Sentinel-1 IW/VV 가용성 | S1 | Not a reference at all | NONE(이미 올바르게 재분류됨) | §4에서 이미 "reference가 아니라 treatment"로 명문화 — mislabelling 없음. 감사에서 확인만 필요. |
| TB02 | Hansen `lossyear`/`gain` | stratification (stable pixel 정의) | Landsat | Landsat | Shared-sensor, independent pipeline | LOW | 안정 화소 모집단만 정의, FPR 자체는 AEF/S2 embedding에서 직접 계산 → 순환 아님. |
| TB02 | Dynamic World mode (2018 vs 2024) | stratification (stable pixel 정의) | Sentinel-2 기반 CNN | S2 | Shared-sensor, independent pipeline | MED | DW가 S2 CNN이므로 "AEF vs S2 baseline" 비교의 denominator를 S2-lineage 모델로 정의하는 셈 — stable class 오분류가 S2 쪽에 유리하게 편향될 위험. 결과 헤드라인(FPR 격차)이 아니라 모집단 정의에만 관여해 위험은 제한적. |
| TB02 | RADD alert | stable stratum 추가 검증 [U, GEE 접근성 미확인] | Sentinel-1 | S1 | Shared-sensor, independent pipeline | LOW | stratum 정의 보조, headline 수치(FPR 6-7배)는 여기 의존 안 함. |
| TB02 | VHR spot-check (Planet NICFI/Google VHR, n=500) | primary validation (stable stratum 확인) | 인간 판독 | 없음(광학 VHR이 AEF 입력 아님) | Fully independent measurement (판독 포함) | NONE | 가장 깨끗한 검증축. |
| TC01 | `ESA/WorldCover/v200/2021` | primary training/eval label | Sentinel-1 + Sentinel-2 + DEM 기반 RF classifier | **S1, S2, DEM** | Shared-sensor, independent pipeline | HIGH(라벨 자체) / MED(전이-격차 헤드라인) | 3개 AEF 직접 입력을 모두 흡수한 알고리즘의 산출물을 label로 씀 — label 오류가 static/climate subspace와 systematic하게 공변할 위험(§4 threat (a)에서 "최상위 위협"으로 이미 인지). AEF와 S2 baseline 둘 다 같은 label로 채점되므로 상대 비교(55% 회수)는 덜 취약하나 절대 balAcc는 label bias를 흡수. |
| TC01 | MapBiomas Collection 9 | 독립 대조 (Brazil arbitration) | Landsat 기반 자체 classifier | Landsat | Shared-sensor, independent pipeline | MED | WorldCover와 계보 분리 — arbitration으로 label-product bias 희석에 기여. |
| TC01 | LandCoverNet | 독립 대조 (arbitration) | Sentinel-2 기반 | S2 | Shared-sensor, independent pipeline | MED | 별도 해석자/legend, 그러나 S2 공유. |
| TC01 | Dynamic World | 독립 대조 (arbitration) | Sentinel-2 CNN | S2 | Shared-sensor, independent pipeline | MED | WorldCover와 다른 알고리즘이지만 여전히 S2 계열. |
| TC01 | GRACE mascon (≥1000 km predictor) | static covariate(참조 아님) | GRACE 중력장 | GRACE | Not a reference at all | NONE | 정확히 predictor로만 사용, mislabelling 없음. |
| TD01 | TMF `AnnualChanges/DegradationYear/DeforestationYear` | **stratification only(등급 산출 금지, §4 명시)** | Landsat 기반 자동 classifier | Landsat | Shared-sensor, independent pipeline | LOW | 저자가 이미 "등급 산출에는 절대 미사용"으로 못박음 — headline(순서형 강도)에 미기여. |
| TD01 | Hansen `lossyear` | stratification | Landsat | Landsat | Shared-sensor, independent pipeline | LOW | 상동. |
| TD01 | Sustainable Landscapes Brazil ALS 1 m CHM | grading reference(핵심 headline) | airborne LiDAR | 없음 | Fully independent measurement | NONE | 가장 강한 headline 근거. |
| TD01 | ICESat-2 ATL08 v006 | grading reference | ICESat-2 레이저 고도계(**GEDI 아님**) | 없음 | Fully independent measurement | NONE | GEDI와 다른 미션 — 명확히 구분됨(§4가 이미 "ATL08 ≠ GEDI" 취지로 사용). |
| TD01 | DETER-B polygon | driver(logging/burn/mining) 귀속 | 인간 판독(INPE, Landsat/CBERS/S2 화면) | 판독=인간, 영상=Landsat/S2 | Human-interpreted | LOW | 등급이 아니라 driver 귀속에만 사용. |
| TD01 | GEDI 파생 canopy height | **consistency check로만 보고, 등급 산출 금지** | GEDI(AEF 직접 입력) | **GEDI** | **Direct circularity** | HIGH(용도가 consistency check로 제한되어 실질 위험은 NONE) | §4가 이미 순환성을 명시하고 headline에서 배제 — 모범적 처리. 감사 결론: 위반 없음, 그대로 유지할 것. |
| TE02 | ERA5-Land monthly | **treatment 변수(참조 아님)** | ERA5-Land(AEF 직접 입력) | ERA5 | Not a reference at all | NONE(이미 올바르게 재분류됨) | §4가 "leakage가 아니라 climate-input dependence"로 명문화 — mislabelling 없음. |
| TE02 | Hansen/WorldCover/Dynamic World | stable/genuine-change 정의 | Landsat, S1+S2+DEM, S2 | Landsat/S1/S2/DEM | Shared-sensor, independent pipeline | MED | "genuine change" 라벨(DW mode 변화)이 SNR 헤드라인(0.23 vs 0.58) 계산에 직접 들어감 — DW는 S2 CNN이라 S2 baseline과 계보를 공유, S2의 SNR을 상대적으로 유리하게 만들 소지(§3-2 참조). |
| TE02 | Rangeland 현장자료(national monitoring/GLPS) [W3-4 확보 여부 미정] | primary validation(계획) | 현장 조사 | 없음 | Fully independent measurement | NONE(확보 시) | 확보되면 최상의 독립 축이나 현재 [U]. |
| TE02 | VHR spot-check(600점, Planet NICFI/Google VHR) | primary validation | 인간 판독 | 없음 | Fully independent measurement | NONE | genuine-change 이중조건의 한 축. |
| TE06 | `ESA/WorldCover/v200/2021` | primary target(land cover) | S1+S2+DEM RF classifier | S1, S2, DEM | Shared-sensor, independent pipeline | MED | TC01과 동일 논리. Δ(모델 간 차이)는 label noise가 공통이라 비편향이라는 저자 주장은 맞으나 절대 정확도는 상한 아님(§4 이미 인지). |
| TE06 | MapBiomas col.9 | 독립 대조 | Landsat | Landsat | Shared-sensor, independent pipeline | MED | 상동. |
| TE06 | ETH/Meta canopy height | **headline에서 배제됨** | GEDI 파생 모델 | **GEDI** | **Direct circularity** | HIGH(그러나 이미 배제 처리 → 잔여 위험 NONE) | §4가 명시적으로 제외 — 모범 처리. |
| TE06 | ICESat-2 ATL08 [U, GEE asset 미확인] | 구조 headline 대체 reference | ICESat-2 | 없음 | Fully independent measurement | NONE(확보 시) | GEDI 대체 축, 확보 실패 시 구조 cell을 supplementary로 강등하는 조건부 설계 이미 명시. |
| TE06 | Airborne lidar(NEON AOP, Brazil SL ALS) [U] | 구조 headline 대체 reference | airborne LiDAR | 없음 | Fully independent measurement | NONE(확보 시) | 상동. |
| TE06 | DEM/ERA5/GRACE | static/climate covariate(참조 아님) | 각각 AEF 직접 입력 | DEM/ERA5/GRACE | Not a reference at all | NONE | §4가 "input dependence, leakage 아님"으로 명문화 — mislabelling 없음. |
| TA02 | MapBiomas `secondary_vegetation_age` | training reference(headline R2 산출) | Landsat 기반 자체 classifier | Landsat | Shared-sensor, independent pipeline | HIGH(라벨) / MED(headline 비교, 이미 완화 설계) | age label 자체가 Landsat 파생이고 AEF도 Landsat을 직접 섭취 — "AEF가 나이를 잘 맞춘다"는 R2 0.29-0.34가 Landsat 공유로 일부 인플레이트될 수 있음. 저자가 이미 이를 "Label circularity" 최상위 threat로 명시하고 최종 주장을 ALS/ATL08 독립 검증(V 2→3 조건)으로만 확정하도록 설계 — 좋은 처리이나 그 W-단계가 완료되기 전엔 headline(saturation ceiling)이 여전히 부분적으로 label-circularity 위에 서 있음. |
| TA02 | Sustainable Landscapes Brazil ALS | 독립 validation(headline ceiling 확정용) | airborne LiDAR | 없음 | Fully independent measurement | NONE | 가장 강한 축. |
| TA02 | ICESat-2 ATL08 | 독립 validation | ICESat-2(**GEDI 아님**) | 없음 | Fully independent measurement | NONE | §4가 명시적으로 "GEDI는 구조 검증에 사용 금지"라 규정 — 모범 처리. |
| TA02 | Field chronosequence plot age [U] | 보조 validation | 현장 조사(문헌) | 없음 | Fully independent measurement | NONE(문헌 검증 시) | [U] — 세션 내 미검증이므로 실제 사용 전 문헌 [V] 확인 필요. |
| TA02 | PRODES clearance-year 재구성 age | 부분 독립 validation("graded independence") | Landsat 기반 자동 classifier | Landsat | Shared-sensor, independent pipeline | MED | 계보가 MapBiomas와 다르지만 여전히 Landsat — 저자가 이미 "graded"로 격하해 명시, 적절한 처리. |
| TA04 | `global_mining_polygons`(Maus et al.) | **sampling frame only(정확도 산출 금지, §4 명시)** | 다중 위성 기반 문헌 매핑(주로 Landsat/S2 계열) | Landsat/S2 계열 | Shared-sensor, independent pipeline | LOW | 저자가 이미 frame 전용으로 한정, 정확도(accuracy) 헤드라인은 (b) VHR/AMW에서만 산출 — 순환 차단 명시. |
| TA04 | Amazon Mining Watch(AMW) annual ASGM mask [U, 세션 내 미검증] | 필수 ASGM-only reference(headline label-efficiency 수치) | Sentinel-2 기반 CNN | **S2** | Shared-sensor, independent pipeline | MED(방향은 보수적) | AMW가 S2 CNN이라 AEF 입력(S2)뿐 아니라 비교 대상인 S2 baseline과도 계보 공유 — 그러나 저자 분석대로 이는 "AEF>S2" 주장에 불리한 방향(S2 baseline에 유리)이므로 결론을 왜곡하기보다 과소추정 방향의 보수적 편향. 여전히 [U] 미검증 상태라 W-단계에서 확인 필요. |
| TA04 | VHR 판독 galamsey sample(n≥500, Planet NICFI/Google VHR, 2 판독자) | 필수 ASGM-only reference(Ghana headline) | 인간 판독 | 없음 | Human-interpreted / Fully independent | NONE | 센서·판독자 모두 독립 — §4 자체 평가와 일치. |
| TA04 | Hansen `lossyear`(annulus negative frame) | hard-negative stratification | Landsat | Landsat | Shared-sensor, independent pipeline | LOW | 프레임 정의만, accuracy 헤드라인에 직접 기여 안 함. |
| TH01 | ROK MOE 토지피복도 + KFS 임상도 + MAFRA 팜맵 | training label | 행정 지도(현장조사+항측 기반, 남한 자체 갱신 체계) | 없음(남한 전용, DPRK 평가와 지리적으로 disjoint) | Fully independent measurement(행정 기록) | NONE | AEF 입력과 무관, 평가 대상 지역과도 분리 — 다만 현재 `data/rok/` 미확보로 `LABELS=FALLBACK` 상태(§4 명시, gating item). |
| TH01 | DPRK VHR stratified 판독(공개 basemap Maxar/Airbus, 필요 시 Planet NICFI) | **primary validation(headline)** | 인간 판독(2인+제3자 조정, κ 보고) | Planet NICFI 사용 시 없음(DPRK는 NICFI 비열대 지역이라 통상 Maxar/Airbus 공개 basemap 사용) | Fully independent measurement(판독) | NONE | 가장 강한 headline 근거 — embedding과 training map 모두로부터 독립임을 §4가 명시. |
| TH01 | ESA WorldCover / Dynamic World | **diagnostic/stratification only, 절대 accuracy 금지(§4 명시)** | S1+S2+DEM, S2 CNN | S1/S2/DEM, S2 | Shared-sensor, independent pipeline | LOW(용도 제한으로 이미 완화) | 상호일치도 0.674를 concordance ceiling으로만 병기 — headline accuracy에 사용 금지가 이미 명문화되어 모범 처리. |

## 2. Topic별 "One independent reference and how to obtain it"

**TB01** — **Planet NICFI human-interpreted event date**(§4에 이미 명시된 수동 판독 축을, RADD/S2가 아닌 **Planet NICFI monthly basemap 기반**으로 한정해 사용).
(a) 독립성: Planet NICFI는 AEF 입력 목록(S1/S2/Landsat 등)에 없는 별도 상업위성 원본이며, 판독은 자동 알고리즘이 아니라 인간이 시계열을 눈으로 훑어 clearing이 처음 나타난 월을 정하므로, RADD/GLAD-S2의 알고리즘 편향과 무관 — w(m) 법칙의 반증 검정을 알고리즘-순환에서 완전히 떼어낼 수 있는 유일한 축이다.
(b) 취득: `planet.com/nicfi` 무료 non-commercial 라이선스 신청(연구용, 승인까지 통상 수일) → API 또는 GEE 자산(`projects/planet-nicfi/...` 접근 가능 시)로 5 m 월간 basemap 취득, n≈600 지점 × 소형 chip(약 1×1 km) 시계열 ≈ 수 GB. 인원: 2 판독자 × 600점 × 약 2-3분/점(월별 스크롤 포함) ≈ 40-60 person-hours + 불일치 조정 10-15 h.
(c) 반증 시 모습: H1'(replacement, a≈0.55-0.60)이 Planet 기반 독립 날짜로도 재현되지 않고 대신 a가 0에 가깝게(즉 원래 seed H1 `w=(12-m)/12`) 나오면, 지금까지의 "57% 즉시 이동" 결과는 RADD date-lag 자체의 인공물이었다는 뜻 — 반대로 사건월 의존적 residual off-plane 분율이 사라지면 3-state arc 자체가 반증된다.

**TB02** — **VHR spot-check(Planet NICFI/Google VHR, n=500, 2 판독자)**, 이미 §4에 명시.
(a) stable-land 정의가 맞는지 확인하는 데 있어 S1/S2 어느 쪽도 원본으로 쓰지 않으므로, "관측 결측이 진짜 stable에서 발생했는지"라는 headline 전제 자체를 센서 독립적으로 검증할 수 있다.
(b) 취득: Google Earth Pro(무료) 또는 Planet NICFI(무료 연구 라이선스)로 500점 chip 확인, 볼륨 <1 GB, 인원 2 판독자 × 500점 × 1-2분 ≈ 20-30 person-hours.
(c) 반증 시 모습: VHR이 실제로는 stable이 아닌(예: 선택적 벌채·산불) 화소가 표본에 다수 섞여 있다고 드러나면, "+2.3° 회전이 순수 관측-공백 인공물"이라는 headline이 무너지고 일부는 진짜 지표 변화로 재분류돼야 한다.

**TC01** — 기존 §4 참조(WorldCover/MapBiomas/LandCoverNet/DW)는 전부 S1/S2/Landsat을 공유해 NONE/LOW 기준을 만족하지 못한다. **신규 제안: 독립 VHR 판독 포인트 샘플**(Google Earth Pro/Bing VHR 고해상 이미지, region-pair당 ~150점, 총 ~1800점, arbitration set과 별도로 순수 인간 판독).
(a) 독립성: 판독자가 실제 지표를 눈으로 보고 판정하므로 S1/S2/DEM 기반 알고리즘의 systematic error와 무관 — label-product bias(§4 최상위 threat)를 직접 반증할 수 있는 유일한 축.
(b) 취득: 무료(Google Earth Pro 데스크톱), 라이선스는 시청/연구용 스크린캡처 허용 범위 내(재배포 금지). 볼륨: 스크린샷 수백 MB. 인원: 2 판독자 × 1800점 × 약 2분/점 ≈ 120 person-hours + 조정 20 h(~1인 3-4주 상당 파트타임).
(c) 반증 시 모습: static-R2 top-16 제거 후 transfer 회수량(+0.083)이 VHR 독립 표본에서는 재현되지 않고(즉 WorldCover 기준 회수가 label-product bias의 인공물이었을 때) 사라지면, RQ1의 핵심 주장이 무너진다.

**TD01** — **Sustainable Landscapes Brazil ALS 1 m CHM**(§4에 이미 명시, headline grading reference).
(a) airborne LiDAR는 AEF 입력에 전혀 없고 TMF/Hansen의 Landsat classifier와도 독립 — 순서형 강도 축이 실제 구조손실을 반영하는지에 대해 가장 직접적인 반증 수단.
(b) 취득: ORNL DAAC HTTP 다운로드(무료, NASA Earthdata 로그인 필요), 규모 ~60 GB, 라이선스는 NASA 공개데이터 정책(재배포 자유, 인용 요구). 인원: pre/post 사이트 매칭·클리핑 스크립트 작성/실행 ~1 person-week(30-40 h).
(c) 반증 시 모습: f-quintile로 sub-pixel clearing fraction을 통제한 뒤에도 partial Spearman ρ(latent intensity, ALS ΔRH98)가 0.15 이하로 떨어지면, "순서형 강도 축은 clearing fraction의 재현일 뿐"이라는 반증 결론(negative-result pivot)이 확정된다.

**TE02** — **VHR spot-check(600점, Planet NICFI/Google VHR, 2 판독자, §4에 이미 명시)**.
(a) genuine-change 판정에 DW(S2 CNN) 단독이 아니라 인간 판독을 이중조건으로 요구하므로, SNR 헤드라인(0.23 vs 0.58)의 분자(genuine drift)가 S2-lineage 라벨에만 의존하지 않게 된다.
(b) 취득: 상동(TB02) 방식, 5개 ROI × 120점, 무료/저비용, 인원 40-60 person-hours.
(c) 반증 시 모습: VHR 확인 결과 DW mode 변화 지점 다수가 실제로는 무변화(오분류)로 나타나면 genuine-change 분자가 줄어 SNR이 재계산되고, drought-break artefact가 실제로는 genuine 신호의 상당 부분을 흡수하고 있었다는 재해석이 필요해진다.

**TE06** — **ICESat-2 ATL08 v006**(§4에 이미 명시, ETH/Meta의 GEDI 순환성 대체).
(a) ICESat-2는 GEDI와 다른 레이저 고도계 미션이며 AEF 입력 목록에 없음 — canopy-height headline을 순환성 없이 검증하는 필수 축.
(b) 취득: NSIDC(Earthdata 로그인 무료) `icepyx` 쿼리, 연구 영역 규모 ~15 GB, 라이선스 공개(CC0급 공개데이터). 인원: 세그먼트-화소 매칭 스크립트 ~1 person-week.
(c) 반증 시 모습: ATL08 기반 재구성 시 AEF의 canopy-height margin이 사라지거나(예: R2가 static-only baseline과 동등) relief-conditioning 상호작용(15%→62%)이 재현되지 않으면, "구조 target의 margin"이라는 headline 요소는 GEDI 순환성의 인공물이었다는 뜻이 된다.

**TA02** — **Sustainable Landscapes Brazil ALS**(§4에 이미 명시, headline ceiling 확정용 필수 조건).
(a) MapBiomas 학습 라벨(Landsat 파생)과 완전히 분리된 airborne LiDAR 기반 canopy height/AGB — age-ceiling(12-15y saturation)이 label circularity의 인공물인지 가르는 핵심 축.
(b) 취득: ORNL DAAC, ~60 GB(Para·Mato Grosso 겹침 확인됨), 무료, 인원 ~1 person-week.
(c) 반증 시 모습: ALS 구조지표(canopy height/AGB)가 예측 age와 함께 12-15y를 넘어서도 계속 증가하는데 AEF 예측 age만 saturate한다면 ceiling은 확정(현재 주장 유지); 반대로 ALS 구조지표 자체도 비슷한 연차에서 saturate하면 "AEF의 한계가 아니라 생태학적으로 실제 성숙 신호가 약해지는 구간"이라는 재해석이 필요해 headline이 바뀐다.

**TA04** — **VHR 판독 galamsey sample(n≥500, Planet/Google VHR, 2 독립 판독자, §4에 이미 명시)**.
(a) 센서·판독자 모두 AEF/S2 baseline과 완전히 분리 — label-efficiency 헤드라인(≈40 labels, ≥25배)의 분모가 되는 정확도 산출을 순환 없이 지지.
(b) 취득: 무료(Planet NICFI Ghana/Amazon 커버, 또는 Google Earth Pro VHR), 인원 2 판독자 × 500점 × ~4-5분(광산은 판독 난이도 높음) ≈ 70-80 person-hours + 3자 조정 15 h.
(c) 반증 시 모습: VHR 정확도로 재채점 시 AEF의 40-label 성능이 1,000-label S2 baseline과 통계적으로 구분되지 않으면(현재 ≥25배 주장이 AMW의 S2-lineage 편향에 의한 인공물이었다면), label-efficiency 헤드라인이 무너진다.

**TH01** — **DPRK VHR stratified 판독(공개 Maxar/Airbus basemap, 2 판독자 + 제3자 조정, κ 보고, §4에 이미 명시)**.
(a) embedding과 ROK training map 모두로부터 독립적인 유일한 DPRK 측 축 — "국경이 representation 불연속이 아니라 management 불연속"이라는 headline을 직접 검정 가능.
(b) 취득: 무료 공개 basemap(Google Earth Pro/Bing 내 Maxar/Airbus 타일), 필요 시 유상 VHR(Maxar/Airbus 상업 라이선스, 소규모 tasking 비용 발생 가능). 8 strata × 표본, 총 수백~1000점, 인원 2 판독자 × 표본 × ~5분 + 조정 ≈ 100-150 person-hours.
(c) 반증 시 모습: VHR 판독 결과 0-100 m stratum과 600 m+ stratum의 실제 토지이용 차이가 미미하다고 나오면(즉 cosine similarity 0.504→0.967 상승이 embedding 자체의 인공물), "국경=management discontinuity" headline이 무너지고 순수 representation-shift 해석으로 되돌아가야 한다.

## 3. Stage-3가 현재 headline claim에 contaminated reference를 쓰는 지점(actionable)

1. **TC01** — headline(transfer-gap 55% 회수)이 `ESA/WorldCover/v200/2021`(S1+S2+DEM 기반) 단일 primary label에 의존. MapBiomas/LandCoverNet arbitration으로 완화되어 있으나, 셋 다 Landsat/S2 계열이라 완전한 독립축이 없음 → §2의 신규 VHR 포인트 샘플 도입을 W-단계에 추가 권고.
2. **TA02** — headline R2(AEF 0.29-0.34)의 1차 training reference인 MapBiomas `secondary_vegetation_age`가 Landsat 파생이고 AEF도 Landsat을 직접 섭취 — label circularity. 저자가 이미 "최종 주장은 ALS/ATL08 독립 검증으로만" 확정하도록 조건화해 두었으므로, **이 조건(V 2→3 gate)이 실제로 충족되기 전에는 saturation ceiling을 headline으로 발표하지 말 것**을 명시적 게이트로 유지 권고.
3. **TE02** — SNR headline(0.23 vs 0.58)의 genuine-change 분자에 Dynamic World(S2 CNN) mode 변화가 들어감. S2 baseline과 DW가 계보를 공유하므로 AEF의 SNR을 상대적으로 더 낮게 보이게 할 잠재적 편향 — VHR 600점 이중조건이 이미 설계돼 있으니 **DW-only로 산출한 예비 수치를 headline으로 확정하지 말고 VHR 확인 후 수치만 채택**할 것.
4. **TB01** — w(m) 법칙의 1차 event-date 소스가 RADD(S1 파생)로, headline 절편 a≈0.568이 S1-AEF 공유 신호의 인공물일 위험. §4가 이미 manual/GLAD-S2 cross-check를 계획해 두었으나 **아직 실행 전(W-단계) 상태이므로 그 결과 없이 a값을 최종 수치로 인용하지 말 것**.
5. **TA04** — AMW(S2 CNN 계열, [U] 세션 내 미검증)가 Amazon 쪽 필수 accuracy reference. 방향은 보수적(AEF에 불리)이라 결론을 왜곡할 위험은 낮으나, [U] 상태 확인 없이 수치를 인용하면 안 됨.

나머지 4개 토픽(TB02, TD01, TE06, TH01)은 headline claim에 direct-circularity(GEDI) 또는 미검증 shared-sensor reference를 이미 명시적으로 배제·강등하는 설계를 갖추고 있어 별도 시정 조치 불필요 — 감사 결과 "모범 처리"로 분류.
