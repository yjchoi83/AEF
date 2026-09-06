# D3 — TH01 redesign: DMZ/CCZ exclusion, distance-band redesign, VHR sampling, Gangwon analog domain

**대상.** Stage-3 TH01(flagship) 재설계. Stage-2/3의 핵심 수치 — cross-border mean-embedding cosine 0.504(0-100 m) → 0.967(600 m+) — 는 아래 이유로 폐기하고, 5-30 km distance-band 설계로 교체한다. RQ1/RQ2/RQ3 구조와 journal target은 유지하되, 주력 수치(headline number)와 그 해석은 근본적으로 바뀐다.

## 1. DMZ/CCZ exclusion — 왜 필요한가, 그리고 무엇이 기존 수치를 대체하는가

**문제의 본질.** Stage-2/3 T3의 elevation/distance stratum(0-100 m, ..., 600 m+)은 물리적 고도가 아니라 **MDL(Military Demarcation Line)로부터의 지표상 거리**를 대리(proxy)한 것이었다. 그런데 국경에서 가장 가까운 stratum은 지리적으로 정확히 다음 두 특수지대와 겹친다.

- **DMZ**: MDL 기준 남북 각 2 km, 총 폭 약 4 km. 1953년 정전협정 이후 **70년간 사람의 출입과 경작이 전면 통제**된 지역으로, 이 기간 동안 산림·습지가 자연 재생(rewilding)되어 한반도에서 식생 밀도·구조가 가장 이질적인 띠 중 하나다.
- **CCZ(민간인출입통제구역)**: DMZ 남측 경계(SLL, 남방한계선)에서 다시 남쪽으로 설정된 ROK 측 통제 벨트(현재는 대부분 SLL 이남 5-20 km 내에서 지자체별로 상이하게 재조정되어 있으나, 이 구역 안에서는 영농 허가가 군 통제 하에 제한적으로만 이루어진다). 즉 **경작이 정책적으로 억제된 지대**다.

따라서 0-100 m stratum에서 관측된 cosine 0.504는 "ROK의 집약 영농 관리 대 DPRK의 관리 방식"을 비교한 것이 아니라, **"양측 모두에서 access-restriction으로 경작이 억제된 좁은 띠" 대 "정상적으로 경작되는 배후지"**를 비교한 것이다. DPRK 측도 MDL 인접부는 군사통제로 인해 정상 영농이 이루어지지 않으므로, 남북 모두에서 같은 방향(관리 배제 → 자연화/방치)으로 편향되어 있다. 즉 이 stratum의 저(低) 유사도는 **access restriction의 대칭적 효과**이며, 논문이 주장하는 "ROK/DPRK 토지관리 체제(management regime) 차이"를 측정한 것이 아니다. 이것은 confound이지 노이즈가 아니다 — 방향성이 있고 체계적이며, 600 m+ stratum으로 갈수록 사라지는 것도 바로 access restriction이 옅어지기 때문이다. 다시 말해 0.504→0.967 monotonic 상승 자체가 "국경이 관리 불연속"이라는 근거가 아니라 "국경 인접부는 access-restriction 불연속"이라는 근거일 수 있고, 두 해석은 현재 설계로 구분되지 않는다.

**무엇이 사라지는가.** 현재 flagship 수치(0.504 → 0.967, F1의 핵심 그림)는 **그대로는 폐기**한다. DMZ(±2 km)와 CCZ 폭 전체를 cross-border 비교 표본에서 제외하면, 이 특정 pair 수치는 재현되지 않는다 — 애초에 이 수치를 만들던 stratum 자체가 제거 대상이기 때문이다.

**무엇이 대체하는가.** RQ1의 measurand는 유지된다("ROK-DPRK 국경은 representation-space 불연속이 아니라 관리 체제 불연속인가"), 다만 근거는 §2의 5-30 km distance-band ROK-vs-DPRK contrast와 그 band-trend로 바뀐다. 새 flagship 후보 수치는 "DMZ/CCZ를 제외한 5-30 km 대역에서 ROK-DPRK cosine이 band별로 평평한가 혹은 하락하는가"이며, 평평하면 covariate shift(H1 반증), 하락 추세가 유의하면 management-regime 해석이 (근거는 더 약해졌지만) 살아남는다. 즉 이 redesign은 **더 방어 가능하지만 더 작은 효과 크기**를 목표로 한다.

**Geometry 구성.**
- **MDL 근사**: 공개 자료로 MDL 정확 좌표는 존재하지 않으나(정전협정 지도는 비공개), 실무적으로 다음 세 가지 public proxy를 조합한다: (i) OSM/OpenStreetMap의 "Korean Demilitarized Zone" 경계 polygon(DMZ 남·북 경계선으로 태깅된 way), (ii) Wikimedia/38 North가 공개한 DMZ 개형도의 georeference(참고용, [U]로 표기), (iii) 위 두 소스로부터 역산한 MDL 중심선 = DMZ 남측경계와 북측경계의 중간선. 이 중심선을 MDL 근사선으로 채택하고, 이 근사 자체가 ±수백 m 오차를 가질 수 있음을 명시한다(이는 5-30 km band 설계에서는 무시 가능한 오차이지만 기존 0-100 m 같은 fine stratum에서는 치명적이었다는 점도 근거 중 하나다).
- **DMZ 제거**: MDL 근사선 기준 ±2 km buffer(geodesic buffer, EPSG:5179 또는 UTM 52N에 투영 후 buffer 연산, 결과를 EPSG:4326으로 역투영).
- **CCZ 제거**: ROK 측만 존재. SLL(남방한계선)의 public 근사는 OSM의 "civilian control line" 관련 tag 또는 각 시군 공고문 기반 GIS 자료(공개된 것에 한함)로 얻는다. 정확한 공식 CCZ 경계가 지자체별로 상이하므로, 본 설계에서는 **DMZ 남측 경계(SLL)로부터 남쪽 5 km를 CCZ 근사 폭의 상한**으로 채택한다(공고된 CCZ 폭이 지역별로 5-20 km 범위이므로 5 km는 보수적 최소 제외폭). 즉 실제로는 5-30 km band의 첫 구간(5-10 km)이 일부 CCZ 잔여 통제 지역을 포함할 수 있다는 caveat을 3.9절 Threats에 명시한다.
- **DPRK 측**: 공식 CCZ 대응 개념(북측 민간인 출입 제한 벨트)의 공개 경계 자료는 없다. 따라서 DPRK 측은 DMZ 북측 경계(NLL 아님, DMZ 북방한계선)로부터 buffer만 적용하고 CCZ급 추가 제외는 하지 않는다 — 이는 **비대칭 처리**이며, band 해석 시 "5-10 km band는 ROK 쪽만 통제 잔여 영향이 있을 수 있다"는 방향성 있는 caveat으로 명시한다.
- **손실 면적**: paired frame은 ROK 37.35-38.05N / DPRK 38.45-39.35N, 127.0-128.4E, 총 위도 폭 남측 0.70도(약 78 km) + 북측 0.90도(약 100 km), 경도 폭 1.4도(약 127 km, 위도 38도 부근에서 1도 ≈ 88 km이므로 약 123 km) 규모다. DMZ(±2 km, 총 4 km 폭) + CCZ 근사(ROK측 남쪽 5 km 추가)를 제거하면, ROK 측은 MDL로부터 남쪽 0-7 km(DMZ 2 km + CCZ 5 km)가 제외되고, DPRK 측은 0-2 km만 제외된다. ROK 프레임의 남북 폭 78 km 중 7 km ≈ **9%**, DPRK 프레임 100 km 중 2 km ≈ **2%**가 제외된다. 다만 이 좁은 띠는 기존 flagship 수치를 전부 생산한 stratum이므로, **표본 개수 손실률(9%/2%)보다 "핵심 결과가 이 좁은 띠에서만 나왔다"는 사실 자체가 더 중요한 손실**이다.

## 2. 5-30 km distance band 재설계

**Band 정의.** MDL 근사선으로부터 편측 거리 5-10, 10-15, 15-20, 20-25, 25-30 km, 양측(ROK/DPRK) 대칭 적용, 총 5개 band × 2 side = 10 stratum. DMZ(0-2 km)와 CCZ 근사(ROK 2-7 km, 즉 5 km 폭)는 모든 band에서 완전 배제되므로 5 km 이하는 애초에 band 정의에 포함하지 않는다(제목의 "5-30 km"와 정합).

**Estimand.** 두 개의 층위:
1. **Band 내 ROK-vs-DPRK contrast**: 각 band b에서 mean-embedding cosine similarity(ROK band-b 표본 대 DPRK band-b 표본), block bootstrap 95% CI 동반. 이것이 H1 검정의 1차 단위다.
2. **Band trend**: 5개 band에 대한 contrast의 monotonic 여부(Mann-Kendall 또는 단순 선형회귀 slope, block-bootstrap CI). "band trend가 유의하게 상승(거리가 멀수록 유사도 상승)"이면 management-regime 해석 유지, "평평(모든 band CI가 겹침)"이면 H1 기각으로 이어지는 covariate-shift 해석.

**Matching (comparability 확보).** 각 band 내에서 ROK/DPRK 표본을 다음 covariate로 stratified matching(또는 최소한 covariate balance 보고)한다: (i) **elevation**(GLO-30, ±50 m bin), (ii) **slope**(GLO-30 derived, ±5도 bin), (iii) **aspect**(8-direction categorical, N/NE/E/SE/S/SW/W/NW), (iv) **prior land cover**(DMZ/CCZ 설정 이전 시기, 가능하면 1970s 미군 지도 또는 가장 이른 available Landsat 기반 land cover로 "인위적 관리 개입 이전 배경" 근사; 미가용 시 가장 이른 AEF 연도인 2017년의 DPRK 측 label-free cluster로 대체), (v) **climate**(WorldClim 또는 CHELSA 연 강수량/기온 bin, 위도 차이로 인한 남북 기후 gradient 통제). Matching은 exact match가 불가능하므로 **coarsened exact matching(CEM)** 또는 propensity-score 기반 nearest-neighbor 방식으로 수행하고, 매칭 후 covariate balance(표준화 평균차 SMD < 0.1)를 표로 보고한다.

**Per-band 표본 규모.** paired frame의 폭(경도 127.0-128.4E, 약 123 km)과 band 폭(5 km) 및 10 m 해상도를 고려하면 band당 이론적 화소 수는 매우 크므로(수백만), 실질적 제약은 spatial autocorrelation이다. Stage-2 T3과 동일 원칙(13 km GroupKFold block)을 적용해 **band당 목표 유효 표본 = 30개 이상의 13 km block**(각 block에서 subsample, 예: block당 30-50 pixel)을 목표로 하며, 이는 band당 약 900-1500 pixel 규모다(band 폭 5 km이므로 block 상당수가 걸치는 문제는 block을 band 축이 아니라 경도 축으로 격자화하여 회피). ROK 측 5개 band 순서로 폭이 넓어질수록(위도 범위 78 km 남북) block 수가 줄어드는 5-band 구조상, 가장 좁은 band(5-10 km)에서 최소 표본이 나오므로 이 band의 CI가 가장 넓을 것으로 예상하고 사전에 보고한다.

**Block-bootstrap 단위.** 13 km × 13 km grid cell(Stage-2/3과 동일 정의)을 resampling 단위로 삼아 band별, side별로 독립적으로 block bootstrap(예: B=2000회)하여 band contrast와 band trend의 95% CI를 산출한다. Block은 ROK/DPRK 각각 별도로 뽑고(두 모집단이 다르므로), contrast의 CI는 두 bootstrap 분포의 차이 분포로 구성한다.

**Null 결과의 형태와 위험.** 근접(0-100 m) 극단 stratum이 제거되었으므로, band 간 cosine 차이의 절대 크기는 Stage-2의 0.504-0.967 스팬보다 **훨씬 작을 것으로 예상**된다(band trend가 존재해도 아마 0.85-0.95 범위 내 완만한 상승 정도). 이 경우 다음이 "null 결과"의 정직한 모습이다: 5개 band의 contrast CI가 서로 겹치고 trend의 CI가 0을 포함 — 즉 **"MDL로부터 5 km 이상 떨어지면 ROK-DPRK 표현 차이는 이미 거리와 독립"**이라는 결과. 이것은 RQ1을 기각시키는 결과이며, 이 경우 논문의 주장은 "국경 관리 불연속은 오직 DMZ/CCZ의 access-restriction 효과이며, 5 km를 넘어서면 순수 covariate shift(기후·고도·토지이용 배분)로 완전히 설명된다"로 재구성해야 한다 — 이는 **여전히 출판 가능한 결과이지만 flagship이 아니라 negative/bounding 결과**로 격하된다. 이 위험은 실재하며 본 redesign이 진행되기 전에는 해소되지 않는다. 이것이 TH01의 CONDITIONAL-GO 판정에 새로운 조건(C3)으로 추가되어야 한다.

## 3. VHR labelling용 hillside-field 표본설계(slope-stratified)

**목적.** RQ3의 measurand인 다락밭(hillside/sloping terraced field)은 Dynamic World/WorldCover로 분리 불가능하며, VHR 판독으로만 확인 가능하다. 아래는 5-30 km band 설계와 결합된 slope-stratified VHR 표본 계획이다.

**Slope strata(GLO-30 기반).** <5°, 5-10°, 10-20°, 20-30°, >30° 5개 strata. 다락밭은 통상 5-30° 범위에 집중되고 <5°는 평지 논/밭 대조군, >30°는 경작 불가능에 가까운 산지(주로 forest/degraded forest) 대조군 역할을 한다.

**배분(allocation) — slope × side × distance band.** 목표 총 VHR point는 Stage-3에서 이미 채택된 Olofsson n=600(전체 8-class 표본)에 **추가로** hillside-field 전용 층을 얹는 것이 아니라, 600점 중 "hillside cropland" rare/change stratum(기존 100점 배정)을 slope×side×band로 세분한다. 구체적으로:
- slope 5-10°, 10-20°, 20-30° 3개 stratum(다락밭 발생 가능 구간)에 각 20점, side(ROK/DPRK) 균등(각 10점) → 60점.
- 이 60점을 5개 distance band(5-10...25-30 km)에 걸쳐 side별 각 2점씩 배치(band당 slope-stratum당 2점 × 3 slope stratum × 2 side = 12점/band × 5 band = 60점, 위와 합치).
- <5°(평지 대조), >30°(비경작 대조) stratum에 각 20점(양측 균등 10/10) → 40점 추가.
- 총 hillside 전용 층 = 100점(Stage-3 기존 배정과 동일 총점 유지, 세부 배분만 slope×side×band로 재구성). 나머지 500점은 기존 8-class stable/rare 배분(forest→cropland, cropland→forest, built expansion 등) 유지.

**Target SE와 Olofsson n 산식 연계.** 기존 산식 n = (Σ W_i S_i / SE)²을 hillside stratum에 재적용한다. hillside cropland의 예상 면적비중 W_hillside ≈ 0.05-0.08(paired frame 내 추정), 예상 표준편차 S_hillside ≈ 0.40(binary correct/incorrect 분류에서 rare/heterogeneous class는 p(1-p) 최대치에 근접, p≈0.6-0.7 가정 시 S≈sqrt(0.6*0.4)≈0.49로 다소 상향 조정). 목표 SE(class-level UA)=0.05(±10 pt 95% CI)를 잡으면 n_hillside = (W_hillside*S_hillside/SE)^2 규모 산정 시 100점 배정은 W*S/SE ≈ 0.06*0.45/0.05 ≈ 0.54 → 제곱 시 약 0.3, 즉 100점이면 이미 여유가 있다(단일 stratum 100점 배정 시 실질 SE는 S/sqrt(n)=0.45/10≈0.045, 목표 0.05를 상회 충족). slope×side×band로 12개 세부 조합에 분산하면 세부조합당 평균 8점 남짓이 되어 **band-level·slope-level 개별 정밀도는 낮아진다** — 이는 band-level hillside 비율 추정이 아니라 "hillside class가 전체적으로 존재하는가/거리에 따라 증가하는가"라는 **집계된 pattern 검정**에만 이 100점이 쓰일 수 있음을 의미하며, 개별 band×slope 셀의 CI는 넓을 것으로 사전에 명시한다.

**Interpreter 프로토콜.** 2명의 독립 interpreter가 전체 100점(및 나머지 500점)을 모두 판독, 제3자가 불일치 건을 조정(Stage-3 기존 protocol과 동일). Hillside cropland 여부에 대해 Cohen's kappa를 별도로 보고(전체 8-class kappa와 별개로, hillside-vs-not-hillside binary agreement).

**VHR에서 다락밭 판별 시각 지표.** (i) 등고선을 따라가는 곡선형 필지 경계(자연 지형에 순응, 직선 도로/경작 격자와 구분), (ii) 필지 간 단(段)차 — 계단식 경작(terracing)에서 발생하는 미세한 명암 대비 줄무늬(shadow banding), 특히 태양 방위각이 낮은 계절 영상에서 뚜렷, (iii) 재배기 내 색상 변화(작기(作期) 신호) — 초록/갈색 patch가 계절에 따라 규칙적으로 변하며 forest canopy의 안정적 질감과 대비, (iv) 필지 크기와 형태의 불규칙성 — 평지 논과 달리 소규모(0.1-0.5 ha)·불규칙 다각형, (v) 접근 경로(소로/농로)의 존재 — 완전 방치된 degraded forest에는 이런 network가 없음. Grassland와의 구분은 특히 어려운데, 다락밭이 방치(fallow) 상태일 때 초지처럼 보이기 때문 — 이 경우 (a) 과거 시점 영상(availability 시)의 필지 경계 잔존 여부, (b) 인접 필지와의 형태 유사성(연속 경작단지의 일부인지)으로 판별한다.

**예상 난이도(stratum별).** <5° 평지: 논/밭 구분은 쉬우나 paddy-dry 구분은 물 반사(flooding season) 유무로만 가능 → 중간 난이도. 5-10°: 다락밭과 완만한 밭의 구분 쉬움(경계 뚜렷), 낮은 난이도. 10-20°: 전형적 다락밭 구간, terracing 흔적이 뚜렷 → 낮은-중간 난이도. 20-30°: 방치된 다락밭과 degraded forest/shrub 구분이 **가장 어려움** — 방치 후 수년 내 이차 초지·관목으로 천이되어 필지 경계만 남는 경우가 많음 → 높은 난이도, adjudication 빈도가 가장 높을 stratum으로 사전 명시. >30°: 대부분 forest/bare, 오분류 위험 낮음 → 낮은 난이도.

**Person-hours.** Stage-3 기존 추정(2 interpreter × 600점 ≈ 30 person-hour)을 유지하되, 20-30° stratum의 판독 난이도 상승을 반영해 해당 stratum(및 adjudication)에 시간 가중을 둔다: 600점 중 표준 판독 540점 × 평균 2.5분/점 ≈ 22.5 person-hour(2인 기준 45점/hour 가정 시 재계산하면 2인 합산 약 45 person-hour 수준), 고난도 20-30° hillside 60점(양 side 합산)은 점당 평균 5분(2배) 배정 → 추가 5 person-hour, 3자 adjudication은 불일치율 약 15% 가정 시 90점 × 점당 3분 ≈ 4.5 person-hour. **총 person-hour ≈ 50-55시간**(Stage-3 원안 30시간에서 상향 — slope-stratified 세분화와 고난도 stratum 반영).

## 4. Gangwon 고랭지(upland-field) analog domain — DPRK hillside class를 위한 ROK 훈련 라벨

**문제.** `data/rok/`가 비어 있고 Dynamic World/WorldCover는 paddy와 dry/hillside cropland를 분리하지 못한다(RQ3의 measurand 자체). Stage-3는 이를 KFS/MoE 공식 map 확보(gating item, C2)로 해결하려 했으나, 공식 map조차 **DPRK 유사 환경의 다락밭 학습 예시를 직접 제공하지는 않는다** — ROK 내에서도 평지 위주 팜맵 지역은 지형이 DPRK 국경 인접 산악 지대와 다르다.

**Analog 지역 지정.** 강원도 고랭지 농업지대 — **태백(Taebaek), 정선(Jeongseon), 평창(Pyeongchang), 홍천(Hongcheon) 상부 지역**의 고랭지 밭(주로 배추·감자 등 고랭지 채소, 해발 400-1000 m대 경사지 경작)을 DPRK hillside-field class의 **labelled analog domain**으로 지정한다.

**매칭 근거(기후·지형).** (i) **고도**: 태백·정선·평창 고랭지는 해발 500-1300 m 범위로, DPRK 국경 인접 함경/강원 북부 산악 경작지(대부분 400-1000 m대)와 고도 분포가 근접. (ii) **경사**: 강원 고랭지는 5-25° 경사 경작이 전형적이며 이는 §3에서 정의한 다락밭 slope stratum(5-30°)과 직접 대응. (iii) **기후**: 강원 산간은 한반도에서 가장 한랭한 ROK 지역으로, 연평균 기온·강수 패턴이 DPRK 중북부 산악지대와 남한 다른 지역보다 훨씬 유사(둘 다 대륙성 기후 영향이 상대적으로 강함). (iv) **작물/경작 양식**: 고랭지 밭은 다락밭과 마찬가지로 등고선형 필지, 계단식 또는 준계단식 경작을 보여 VHR 시각 특징(§3)이 공유된다.

**훈련 라벨 공급 방식.** 강원 고랭지 지역에서 (a) 기존 공개 팜맵/농경지 필지 경계(농식품부 팜맵, 확보 시) 또는 (b) 없을 경우 VHR + AEF embedding을 이용한 **자체 판독 라벨링**(§3과 동일 2-interpreter 프로토콜을 소규모로 적용, 예: 200-300점)으로 "hillside dry-field" positive 예시를 확보하고, 이를 기존 8-class harmonisation의 dry/hillside cropland class 학습 표본에 **ROK 평지 밭 표본과 별도의 sub-label**로 추가한다. 즉 dry/hillside cropland class를 "lowland dry field"와 "hillside/terraced field(고랭지형)"로 세분한 뒤, 후자의 학습 표본을 강원 analog 지역에서만 추출한다. 이는 probe 학습 시 class-conditional feature 분포에 경사지 특유의 embedding 신호(§3 시각 지표에 대응하는 spectral/textural signal)를 포함시켜, DPRK hillside 필지에 대한 probe의 민감도를 높인다.

**해결하지 못하는 residual domain gap.** 강원 고랭지는 여전히 ROK 내 지역이므로 다음이 남는다: (i) **관리 강도(management intensity)의 근본적 차이** — 강원 고랭지는 상업적 채소 재배(고소득 작물, 기계화 일부 도입)인 반면 DPRK 다락밭은 대개 식량작물(옥수수·감자) 위주의 저투입 자급 경작으로, 계절 생장곡선·시비(施肥) 패턴이 다를 수 있다. (ii) **필지 규모·형상 분포 차이** — DPRK 다락밭은 강원 고랭지보다 평균 필지가 작고 불규칙할 가능성. (iii) **atmospheric/sensor 조건 차이는 없음**(같은 AEF/Sentinel-2 embedding이므로), 그러나 **DPRK 측 valid-observation 밀도 차이**(Stage-3에서 이미 지목된 confounder)는 analog 라벨로 해결되지 않는다. (iv) 강원 지역은 위도상 DPRK 국경 인접 지역보다 남쪽에 위치하므로 생장 계절(phenology) timing이 다르다 — per-year probe에 calendar-year 정합은 되지만 phenological offset은 남는다.

**Transfer 검증 방법.** 강원 analog에서 학습한 hillside sub-class probe를 (a) 먼저 **강원 내 held-out block**(GroupKFold, 13 km block)에서 in-region 성능 확인, (b) 그 다음 **ROK-DPRK cross-border transfer와 동일한 설계**로 5-30 km band의 DPRK 측 VHR-판독 hillside 표본(§3의 100점 중 DPRK side 50점)에 적용해 agreement/OA를 측정하고, (c) 강원 analog 없이 학습한 기존 dry/hillside 단일 class probe와 **paired McNemar**로 비교해 analog 도입이 DPRK hillside 탐지를 유의하게 개선하는지 검정한다. 개선이 없거나 역효과라면(즉 강원 고랭지 특유의 商業작물 신호가 오히려 DPRK 자급작물 패턴과 괴리를 만든다면) analog domain 가설은 반증되고, 이 결과 자체를 domain-gap의 정량적 증거로 보고한다.

## 5. Flagship 수치 제거 후에도 논문이 주장할 수 있는 것 (revised claim list)

1. **RQ2 transfer 결과는 그대로 유지**: AEF ROK in-region OA 0.842 vs S2 0.715(+12.7 pt), cross-border agreement AEF 0.750 vs S2 0.677(+7.3 pt), WorldCover-vs-Dynamic World concordance ceiling 0.674 대비 우위 — 이 수치들은 DMZ/CCZ 표본 오염과 무관(픽셀 표본이 이미 넓은 프레임 전역에서 뽑혔으므로 재검토는 필요하나 근본 논리는 살아있음, 다만 표본에서 DMZ/CCZ 픽셀을 제외한 재계산이 필요).
2. **RQ1은 축소된 형태로 유지 또는 null로 재구성**: 5-30 km band trend가 유의하면 "관리 불연속은 DMZ/CCZ 근접부뿐 아니라 배후지까지 완만하게 이어진다"는 약화된 버전의 주장; band trend가 null이면 "국경효과는 access-restriction에 국한되며 5 km 밖은 covariate shift로 설명된다"는 정직한 negative 주장 — 둘 다 출판 가치가 있으나 후자는 flagship에서 secondary finding으로 격하.
3. **RQ3 change-detection/timing 결과는 완전히 유지**: Jungpyong z=9.8 vs S2 z=3.0, Songhwa 구조적 miss, 2024 Yalu flood sub-annual sensitivity — 이 결과들은 DMZ/CCZ와 무관한 site 기반 결과이므로 영향받지 않음.
4. **vMF kappa 결과는 재검토 필요**: 기존 kappa 비교(DPRK ≥ ROK in 5/6 class)가 DMZ/CCZ 인접 표본을 포함했는지 재확인하고, 포함되었다면 5-30 km band 표본으로 재계산.
5. **새로운 주장 두 가지가 추가됨**: (a) DMZ/CCZ가 "70년 무단 재자연화 + 영농제한"이라는 access-restriction 효과를 갖는다는 것 자체를 정량적으로 보여주는 **독립적인 결과**(DMZ 내부 vs DMZ 인접 정상 경작지의 embedding 대비) — 이는 원래 flagship이 혼동했던 것을 오히려 "DMZ 생태 회복 정량화"라는 별도의 흥미로운 결과로 승격시킬 수 있음(§5-H "DMZ/CCZ ecology" in-scope 항목과 직결). (b) 강원 analog-to-DPRK transfer 검정 결과(§4) 자체가 새로운 기여로 추가됨.
6. **Journal 포지셔닝은 유지 가능하나 근거가 재분배됨**: RSE primary는 이제 "design-based area estimation + transfer + access-restriction-corrected border diagnostic"로 프레임을 옮기고, "국경이 관리 불연속"이라는 문장은 "access-restriction을 통제한 후에도 잔존하는 완만한 관리 신호(또는 그 부재)"로 조심스럽게 재기술해야 한다.

## 6. Ethics / data provenance (bucket-H rule 3.9)

본 redesign이 다루는 자료는 전부 공개(public) 출처다 — MDL/DMZ/CCZ 경계 근사는 OSM 및 공개 개형도에서, elevation/slope/aspect는 Copernicus GLO-30, 기후는 WorldClim/CHELSA, 훈련 라벨은 ROK 정부 공개 map(MoE, KFS 임상도, MAFRA 팜맵) 및 강원 analog 지역의 동일 공개 팜맵/VHR 판독에서 얻는다. 분석은 §5-H 항목 중 "DPRK hillside farming, DMZ/CCZ ecology" in-scope 범주에 정확히 해당하며, 전략적(strategic) 10 m 연annual 스케일에 머물러 개별 시설·부대·인원 식별을 하지 않는다 — hillside-field class는 순수 민간 농업 토지이용 범주이고, DMZ/CCZ 지오메트리 자체도 시설 좌표가 아니라 폭 수 km의 정책 경계선 근사일 뿐이다. 시민보호/투명성 근거는 이중적이다: (i) 식량안보 측(FAO/WFP, 통일부)에는 DPRK 다락밭 면적·분포에 대한 불확실성 정량화가 인도적 원조 계획에 직결되고, (ii) DMZ/CCZ를 access-restriction 지대로 명시적으로 분리해 다루는 것 자체가 "생태 회복이 자동으로 관리 우수성의 증거로 오독되지 않도록" 하는 방법론적 투명성 기여다. Dual-use 위험은 Stage-3 원안과 동일하게 존재(건설·경작 변화 탐지가 원리상 감시에 전용 가능)하나, county/지역 단위 집계와 공개 방법론 게시로 완화하며, 어떤 산출물도 §5-H out-of-scope(표적화, 병력·차량 추적, 실시간 전술 사용, 특정 무기체계·군사시설 식별)에 해당하지 않는다.
