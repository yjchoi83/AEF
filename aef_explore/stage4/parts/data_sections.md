###### TB01
## 4. Data
- **AEF**: `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` 2019–2024 (event year Y ∈ 2020–2023, 각 Y에 `e_{Y-1},e_Y,e_{Y+1}` 필요). 카탈로그 문구 확인됨 — AEF year = calendar year이므로 label도 calendar-year로 정렬 [V].
- **Regions/tiles**: 2×2° ROI 3곳 — (a) Pará/Mato Grosso, BR(unimodal dry season, Stage-2 pilot ROI 포함), (b) Congo Basin, DRC 적도대 `[23,0,24,1]` 확장(**bimodal**, decisive test), (c) Riau/Kalimantan, ID(약한 계절성) — 계절 캘린더 대비를 3단계로 확보.
- **Reference**: RADD confirmed alert(YYDDD Date field 확인됨 [V]) + Hansen `lossyear` (`unmask(0)` 필수) + treecover2000>50로 clearing 정의; stable forest는 tc>80 & no loss & no alert.
- **Independent validation**: RADD Date는 *detection* date이므로 month label이 늦게 편향된다. 이를 끊기 위해 stratified 표본 n≈600(지역×분기)에 대해 Sentinel-2/Planet-NICFI image time series **수동 판독 event date**를 별도 생성하고, 광학 기반 GLAD-S2 alert와 DETER-B를 cross-date로 사용한다. 독립성 논거: AEF는 S1+S2를 입력으로 흡수하므로 센서 수준 독립은 불가능하다 — 독립성은 *label 생성 알고리즘* 수준(radar RADD vs 광학 GLAD-S2 vs 인간 판독)에서 주장하고, 관측 캘린더 공유라는 잔여 의존성은 동일 캘린더를 공유하는 S2 composite baseline을 confound control로 사용해 흡수한다.
- **Sampling design**: 지역×연도×사건월 stratified, 120 px/month → n=1440/region-year (Stage-2와 동일), 총 ~17k clearing px + stable 표본; 0.1° block을 GroupKFold 단위(>10 km)로 사용하며 region-year당 **usable block ≥50**을 확보하도록 ROI를 2×2°로 확대.

###### TB02
## 4. Data
AEF `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` **2017-2025**(calendar-year semantics [V]; 2025 layer는 공개 논문 범위 밖이라 **provisional**로 분리 보고, 주 분석 2019-2024). Treatment 정의용: `COPERNICUS/S1_GRD`(IW + `listContains(...Polarisation,'VV')` 필수 — HH-only scene 혼입), cloud covariate `COPERNICUS/S2_SR_HARMONIZED`, nuisance climate `ECMWF/ERA5_LAND/MONTHLY_AGGR`. **GRACE 사용 불가**: `NASA/GRACE/MASS_GRIDS_V04/MASCON`은 2024-09-30 종료 + 2017/18 GRACE-FO gap(n=238)이라 연구 기간을 못 덮음 → ERA5-Land만 사용.
표본: Stage-2의 6 ROI를 **S1 retention(5계층) × biome × cloud regime** 층화 global sample **200-300 ROI(0.5°)**로 확장, ROI별 stable pixel ≥1,000 → ~2-3×10⁵ pixel × 6-7 year. Stable stratum(보수적): Hansen `..._2025_v1_13` lossyear=0 & gain=0 & datamask=1, Dynamic World mode(2018)==mode(2024) & non-water/built/snow, 모든 label band `.unmask(0)`.
독립성: Hansen/DW/RADD는 AEF와 무관한 파이프라인이므로 label independence가 성립하지만, **retention은 AEF의 input에서 계산되므로 reference가 아니라 treatment 변수**임을 명시한다. 외생성 근거: S1B 태양전지판 고장(2021-12)은 지표 상태와 무관한 하드웨어 사건이다. Stable stratum 자체의 검증에는 RADD alert(`projects/radar-wur/raddalert/v1`, GEE 접근성 미확인 [U])과 VHR(Planet NICFI / Google VHR) 500점 spot-check를 쓴다.

###### TC01
## 4. Data
- **AEF** `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` 2021 primary, 2020으로 temporal replication (calendar-year semantics [V]).
- **Regions**: 4대륙 12 region pair(≥8 필수), relief × climate로 stratify(저기복 습윤 Amazon/Congo, 고기복 Andes/East Africa rift, 반건조 Cerrado/Sahel, 온대). ROI scale ladder 25/100/400/1000 km — 동일 pair를 4척도에서 반복.
- **Labels**: `ESA/WorldCover/v200/2021` primary(product label, ground truth 아님) + 독립 참조 **MapBiomas collection 9**(Brazil), **LandCoverNet**, Dynamic World. 독립성 논거: WorldCover는 AEF training label과 계보가 다르고, MapBiomas/LandCoverNet은 별개 legend·별개 해석자 기반 → 2개 이상 product가 합의하는 pixel만 남긴 **arbitration set**을 2차 evaluation set으로 사용해 label-product bias를 흡수한다.
- **Statics**: `COPERNICUS/DEM/GLO30_2024_1`(elev/slope/aspect), `ECMWF/ERA5_LAND/MONTHLY_AGGR`(annual T, ΣP). GRACE mascon은 0.5°이므로 ≥1000 km 척도에서만 predictor로 투입(100 km ROI 내 상수 [V]).
- **Sampling**: label-only `stratifiedSample` → 300점 chunk `sampleRegions` 2단계(pilot에서 77-band stack timeout 해결), region당 3000점 완전균형, 0.1°(~11 km) block group.

###### TD01
**4. Data.** AEF `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` 2017-2024, calendar-year [V] → (Y-1, Y) pair. Regions: Pará 주 primary 2 ROI + Mato Grosso(Feliz Natal)·Rondônia(Jamari) — Sustainable Landscapes Brazil ALS footprint와 겹치도록 선택; **whole-basin hold-out = DRC Tshopo** (23.5-24.5E/0-1N). Stratification source(등급 산출에는 절대 미사용): `projects/JRC/TMF/v1_2024/{AnnualChanges, DegradationYear, DeforestationYear}` + `UMD/hansen/global_forest_change_2025_v1_13`. **Grading reference(독립)**: (i) Sustainable Landscapes Brazil ALS 1 m CHM, ORNL DAAC HTTP 다운로드 ~60 GB, 사건연도를 사이에 두는 pre/post acquisition 사이트만 사용; (ii) ICESat-2 **ATL08 v006** 100 m segment canopy height, NSIDC를 `icepyx`로 off-GEE 취득(~15 GB); (iii) **DETER-B** polygon은 terrabrasilis.dpi.inpe.br WFS/shapefile로 off-GEE 취득 후 Aug-Jul → calendar-year 재binning하여 driver(logging/burn/mining) 귀속에 사용, 보조로 MapBiomas C9 class 30 + `MODIS/061/MCD64A1`. 독립성 논거: ALS·ATL08·DETER는 AEF 입력이 아니며 TMF의 자동 Landsat classifier와도 독립(DETER는 사람이 판독). **GEDI는 AEF 입력이므로 등급 검증에서 배제**하고 순환성을 명시한 consistency check로만 보고한다. Sampling: (intensity stratum × f-quintile × region) 층화무작위, cell당 n≈1200, 포함확률 보존, 0.1°(~11 km) block을 GroupKFold 단위로 유지; GEE timeout 회피를 위해 30 m에서 점 선택 후 10 m `sampleRegions`를 ≤900점씩 chunk (pilot에서 검증된 회피책).

###### TE02
## 4. Data
AEF `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` **2017-2025**(calendar-year semantics [V]; 2025는 논문 범위 밖이므로 provisional 별표, 주 분석 **2018-2024**). Climate treatment: `ECMWF/ERA5_LAND/MONTHLY_AGGR`(n=108 확인, 6 ROI 전월 커버, calendar-year 정합) precip·soil-moisture·2m-T의 annual z와 **Δz**. Nuisance: `COPERNICUS/S1_GRD`(IW + `listContains(...Polarisation,'VV')` 필수) retention, `COPERNICUS/S2_SR_HARMONIZED` clear-obs count. Label: `UMD/hansen/global_forest_change_2025_v1_13`, `ESA/WorldCover/v200/2021`, `GOOGLE/DYNAMICWORLD/V1`(모든 band `.unmask(0)`). **GRACE 미사용**(2024-09 종료 + 2017-18 gap, TB02 판정 채택).
표본: Stage-2의 6 dryland ROI(ET_somali, KE_marsa, SN_ferlo, ZW_mata, US_az, BR_caat)를 **aridity index(0.05-0.65) × transition frequency × S1 retention** 3중 층화 global sample **250-350개 0.5° ROI**로 확장, ROI당 stable pixel ≥1,000 → ~3×10⁵ pixel × 7 year. Stable stratum(보수적): Hansen lossyear=0 & gain=0 & datamask=1, WorldCover∈{tree,shrub,grass}, DW mode(2018)==DW mode(2024) & ∈{trees,grass,shrub}.
**독립성 논거**: ERA5-Land는 AEF의 **direct model input**이므로 reference가 아니라 **treatment 변수**다(이 결합을 leakage가 아니라 climate-input dependence로 서술한다). 따라서 검증 독립성은 (i) ERA5·AEF와 무관한 파이프라인인 Hansen/DW/WorldCover, (ii) **rangeland 현장자료**(national rangeland monitoring / GLPS류 목초지 조사, 확보 가능성 W3-4에 판정), (iii) **VHR spot-check 600점**(Planet NICFI / Google VHR, 2인 해석자, κ 보고)에서 확보한다. Genuine-change reference는 DW mode 변화 + VHR 확인 이중 조건.
**artefact vs true signal 정의(사전 확정)**: 어떤 stable pixel의 초과 drift는, (a) transition 후 **k≥2년** 시점에 DW/WorldCover class와 VHR 구조지표(woody cover, bare fraction)가 불변이고, (b) anomaly가 baseline으로 복귀할 때 drift도 복귀하거나 climate regress-out으로 제거되면 → **artefact**. anomaly 완화 후에도 drift가 잔존(hysteresis)하고 VHR woody-cover 손실/bare-soil 증가로 확증되면 → **true ecological signal**이며 이는 별도 계층으로 보고한다.

###### TE06
## 4. Data
- **AEF** `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` 2021 primary, 2020 replication (calendar-year semantics [V]).
- **Regions**: relief-stratified **14 region**(6 low-relief median slope <2°, 4 mid 2–15°, 4 high >15°), 4대륙, 기후대 교차 배치. Pilot의 Cusco Andes / Mato Grosso를 anchor로 포함.
- **Targets/reference**: (i) land cover — `ESA/WorldCover/v200/2021` (product label, ground truth 아님; label noise가 모든 feature set에 공통이므로 Δ는 비편향, 절대값은 상한 아님) + 독립 대조로 **MapBiomas col.9**(Brazil)와 2-product arbitration set. (ii) 구조 — **ETH/Meta canopy height는 headline claim에서 제외**한다(GEDI 파생 → GEDI는 AEF direct input → circularity). 대체 reference: **ICESat-2 ATL08 canopy height segments** [U, GEE asset 미확인] 및 airborne lidar(NEON AOP, Brazil Sustainable Landscapes ALS) [U] 중 최소 1개로 재구성; 둘 다 확보 실패 시 height cell을 supplementary로 강등하고 land cover 단일 target으로 진행.
- **Covariates**: `COPERNICUS/DEM/GLO30_2024_1`(elev/slope/aspect sin·cos), `ECMWF/ERA5_LAND/MONTHLY_AGGR`(annual mean T, ΣP) [V]. DEM/ERA5/GRACE는 AEF의 **direct model input**이므로 본 연구의 주제는 static/climate-**input dependence**이며 label leakage가 아니다(용어 고정).
- **Sampling**: region당 완전균형 3000점, `stratifiedSample` → 300점 chunk `sampleRegions`(pilot에서 getInfo 5000-element cap 회피), 0.1°(~11 km) block group.

###### TA02
## 4. Data
- **AEF** `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` 2017-2023 (calendar-year 정합 [V]), 64 bands 10 m. label이 2023에 종료되므로 7개 연도 전부에서 반복(연도-효과 분리).
- **Regions/tiles**: Atlantic Forest SP(-47.6..-46.4E, -24.2..-23.0S), Amazon Bragantina PA(-48.6..-47.4E, -2.4..-1.2S), Rondônia arc(신규, bin1 2.6k 확인), + **whole-region hold-out**으로 Mato Grosso 1 tile. secondary 화소가 24개뿐인 Para(-55.5..-55.0)류 박스는 사전 제외.
- **Training reference**: MapBiomas Collection 9 `secondary_vegetation_age_1986..2023` (30 m, 1-38 y, 38 = 1985/86 censoring) — 원 논문 10.1038/s41597-020-00600-4 [V].
- **독립 validation(V를 2→3으로 올리는 필수 조건)**: (i) Sustainable Landscapes Brazil **ALS** canopy height/AGB (off-GEE, Para·Mato Grosso), (ii) **ICESat-2 ATL08** 100 m segment height (NSIDC/icepyx, off-GEE) — **GEDI는 AEF 입력이므로 구조 검증에 사용 금지**; ATL08/ALS는 AEF 입력이 아니어서 구조축에서 진정 독립. (iii) 문헌 기반 **field chronosequence** plot age [U]. (iv) 부분 독립: PRODES clearance-year(Aug-Jul → calendar 재binning)로 재구성한 age — 계보가 MapBiomas와 다르나 여전히 Landsat 기반이므로 "graded independence"로 명시.
- **Sampling design**: stratum = 7 age bin × 3 region × previous land use(pasture vs cropland, MapBiomas) ; 30 m label의 100 m majority-pure 화소만; region당 ≥400개 0.1°(~11 km) block, bin당 600 px → region당 ~12.6k, 총 ~38k 표본.

###### TA04
## 4. Data
- **AEF** `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` **2019 primary**(Maus epoch 정합), **2021·2023 replication**(calendar-year semantics [V]).
- **Regions(6)**: Amazon — Tapajos, Madre de Dios, Roraima; West Africa — Ghana SW(Tarkwa/Obuasi 산업광산은 별도 LSM stratum으로 분리), Ghana Ashanti/Offin, Côte d'Ivoire.
- **Reference**: (a) `global_mining_polygons` (Maus et al., 10.1038/s41597-022-01547-4 [V]) — GEE에서 판독 확인, 면적·형상·compactness로 **ASGM/LSM 층화**해 sampling frame으로만 사용. (b) **필수 ASGM-only reference**: Amazon은 **Amazon Mining Watch** annual ASGM mask [U, 세션 내 미검증 → 확보 실패 시 CONDITIONAL 조건 위반], Ghana는 **VHR 판독 galamsey sample**(n≥500, Planet/Google VHR, 2 독립 판독자, 판독 규칙 = 활성 pit + turbid pond + bare spoil 인접, Cohen's κ 보고, 불일치는 3자 조정). (c) Negative frame: Maus polygon 주변 1.5–12 km annulus × `UMD/hansen/global_forest_change_2025_v1_13` lossyear 2015–19(농업성 forest loss = hard negative) / loss 없음+treecover>50(stable).
- **독립성 논거**: AMW는 Sentinel-2 CNN 계보이므로 AEF와 계보가 분리되나 **S2 baseline과는 계보를 공유** → 우리 주장(AEF>S2)에 불리한 방향의 보수적 편향이다. VHR sample은 센서·판독자 모두 독립. Maus는 frame 전용이고 accuracy 산정에는 (b)만 사용해 순환을 차단.
- **Sampling design**: region당 학습 pool 3,000점(mining/hard-neg/stable 균형, pos_frac 0.333) + **별개의 design-based accuracy sample**(stratum: predicted-mining / annulus / stable, 층별 배분은 Olofsson et al. 2014 방식 최적배분). group unit = 0.1°(~11 km) block.

###### TH01
**4. Data.** AEF `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` 2017-2025(64 bands, 10 m, calendar-year semantics [V] GEE STAC). 영역: change product는 DPRK 전역, transfer는 cross-DMZ paired frame(ROK 37.35-38.05N / DPRK 38.45-39.35N, 127.0-128.4E)으로 biome·climate·DEM이 matched. **Reference set 3계층과 independence 논거:** (i) *training* — ROK Ministry of Environment land-cover map + Korea Forest Service forest-type map(임상도) + MAFRA 팜맵을 EPSG:5186/5179 → EPSG:4326 재투영, 10 m rasterize, 8 class(forest, paddy, dry/hillside cropland, built, grass/bare, water, wetland, orchard)로 harmonise. 전량 ROK 측이므로 모든 DPRK 평가 단위와 지리적으로 disjoint. (ii) *primary validation* — DPRK 측 **stratified design-based VHR interpretation**(공개 basemap 기반 Maxar/Airbus, 라이선스 시 Planet NICFI), 예비 map에서 도출한 8 strata, 두 명의 독립 interpreter가 전 표본을 판독, 제3자가 불일치 조정, Cohen's kappa 보고. 판독은 embedding과 training map 모두로부터 독립. (iii) *diagnostic 전용* — ESA WorldCover v200, Dynamic World annual mode는 stratification과 shift diagnostic에만 쓰고 **절대 accuracy로 쓰지 않는다**. DPRK에서의 상호 일치도 **0.674**를 concordance ceiling으로 함께 게재한다. 공표 일자를 가진 event inventory는 7·8항 참조. 현재 `LABELS=FALLBACK`: `data/rok/`가 비어 있고 Dynamic World는 paddy와 dry/hillside cropland를 분리할 수 없다 — 그것이 정확히 RQ3의 measurand이므로 (i)의 확보는 **gating item**(9항)이다.

