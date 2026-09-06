# D5 — Data-acquisition checklist (외부 데이터 7건)

표기: **[V]** = 본 세션에서 실제 fetch/검색으로 확인. **[U]** = 확인 불가(추정/미확인), 그렇게 표시된 URL을 확정된 것처럼 쓰지 말 것.

---

## 1. ROK 환경부 토지피복지도 (EGIS) — TH01 gate C2 (label acquisition), `data/rok/` 비어있음

- **목적**: TH01의 training label 8-class harmonisation의 1축. `LABELS=FALLBACK` 해제 조건이며 W3 말까지 미확보 시 fallback(hillside cultivation 주장 강등) 발동.
- **URL**: `https://egis.me.go.kr` [V, 301 redirect 확인] → 실제 현 주소 `https://aid.mcee.go.kr/intro/land.do` [V] (환경부가 "기후에너지환경부"로 개편되며 도메인 이전됨). 지도/다운로드 인터페이스 `https://aid.mcee.go.kr/map/map.do` [V]. 로그인 `https://aid.mcee.go.kr/member/login.do` [U, JS 렌더링이라 WebFetch로 내용 미확인].
- **계정/언어 장벽**: 실제 파일 다운로드에는 로그인 필요(로그인 버튼 확인). 전면 한국어, 영어 미제공.
- **click-path**: 지도서비스 → 토지피복지도 메뉴 → 도엽명/도엽번호 검색 또는 행정구역/영역선택 → 도엽 선택 → 다운로드. (게시판에 "대용량 세분류 토지피복 다운로드" 별도 안내 존재 — 로그인 후 확인 필요.)
- **format/CRS/volume**: SHP + GeoTIFF (뷰용 PDF 별도). 대분류 7class/30 m/1:50,000(1998~), 중분류 22class/5 m/1:25,000(2000~, 초기 EPSG:5174), 세분류 41class/1 m/1:5,000(2010~, 현재 **EPSG:5186**). 전국 도엽 단위 타일.
- **licence**: KOGL 제1유형(출처표시, 상업적·변형 이용 가능) [V].
- **preprocessing**: EPSG:5186 → EPSG:4326 재투영, 10 m rasterize, 8-class harmonisation(TH01 §4 정의: forest/paddy/dry-hillside cropland/built/grass-bare/water/wetland/orchard)로 재분류.
- **wall-clock/person-hours**: 회원가입 + 도엽 다운로드 자동화 스크립트 작성 1~2일, 전국 재투영·rasterize·harmonisation 2~3일 (약 20-30 person-hour).
- **blocking risk / fallback**: 도메인 이전 과도기(구 URL redirect는 되나 문서상 구 URL 참조 시 혼선), 로그인 이후 실제 대량 다운로드 절차 미확인. 실패 시 TH01 §11 fallback대로 RQ1(label-free discontinuity)·RQ2(transfer)만 주장, RQ3 강등.

## 2. 산림청 임상도 (산림공간정보서비스) — TH01 gate C2 보완

- **목적**: 환경부 토지피복지도와 함께 forest class 세분화(수종/영급) 보강, TH01 8-class harmonisation의 2번째 소스.
- **URL**: `https://www.forest.go.kr/newkfsweb/kfs/idx/SubIndex.do?orgId=fgis&mn=KFS_03_08_01` [V]. 자료신청(신청형 다운로드) `https://ob.forest.go.kr/newkfsweb/kfi/kfs/fgis/fgisTermsAgreePage.do?mn=KFS_02_04_02_03&orgId=fgis` [U, 검색으로만 확인]. 대체 경로 — 공공데이터포털 미러 `https://www.data.go.kr/data/15093362/fileData.do` [V].
- **계정/언어 장벽**: forest.go.kr 직접 경로는 "자료신청" 방식 — 공공기관/연구기관/학교 등 이용목적 심사가 있는 신청서 제출형(즉시 다운로드 아님). data.go.kr 미러는 상대적으로 접근이 쉬움. 전면 한국어.
- **click-path (forest.go.kr)**: 산림공간정보 → 자료유통서비스 → 자료신청 → 이용약관 동의 → 신청대상(임상도) 선택 → 신청위치 설정 → 이용목적 기재 → 제출 → 심사 후 다운로드 링크 발급. **data.go.kr 경로**: 데이터 검색 → "임상도(1:5,000)" → 파일데이터 다운로드(즉시).
- **format/CRS/volume**: SHP, 1:5,000(보조로 1:25,000). CRS는 forest.go.kr/data.go.kr 어느 쪽도 명시 안 됨 [U] — 타 국가 지리정보와 일관되게 **EPSG:5186 추정**(미확인). 전국 약 17,576 레코드(1:5,000 기준, data.go.kr 표기).
- **licence**: data.go.kr 미러 기준 KOGL **제3유형**(출처표시 + 변경금지) [V] — 환경부 데이터(제1유형)보다 제약적. 연간 갱신.
- **preprocessing**: EPSG 확인 후 재투영, rasterize, 임상 class → TH01 forest subclass 매핑.
- **wall-clock/person-hours**: data.go.kr 경로면 즉시(수 시간); forest.go.kr 정식 신청은 심사 대기 포함 **1~3주** 소요 가능(미확인, 리스크로 표시). 처리 1~2일.
- **blocking risk / fallback**: "변경금지" 라이선스 조항이 재분류·재가공을 전제로 하는 본 연구와 상충할 수 있어 산림청에 직접 확인 필요. 자료신청 심사에서 개인 연구자 자격 여부 불확실. 실패 시 환경부 토지피복지도 세분류만으로 forest class를 대체(정밀도 저하 감수).

## 3. Sustainable Landscapes Brazil 항공 lidar (ALS) — TD01 조건 (i) 게이팅

- **목적**: TD01의 독립 구조손실 calibration reference(ALS ΔRH98). W1-2에 사이트 ≥4개, class당 ≥400 matched footprint 확보가 CONDITIONAL-GO 조건.
- **DOI/URL**: **10.3334/ORNLDAAC/1644** [V] "LiDAR Surveys over Selected Forest Research Sites, Brazilian Amazon, 2008-2018" (dos-Santos, Keller & Morton 2019); landing `https://daac.ornl.gov/cgi-bin/dsviewer.pl?ds_id=1644` → redirect `https://www.earthdata.nasa.gov/data/catalog/ornl-cloud-lidar-forest-inventory-brazil-1644-1` [V]; user guide PDF `https://data.ornldaac.earthdata.nasa.gov/public/cms/LiDAR_Forest_Inventory_Brazil/comp/LiDAR_Forest_Inventory_Brazil.pdf` [V, 전문 확인]. 관련 데이터셋: CMS Forest Inventory Pará (10.3334/ORNLDAAC/1301), CMS LiDAR Paragominas (10.3334/ORNLDAAC/1302), LiDAR/PALSAR AGB Paragominas (10.3334/ORNLDAAC/1648) [V].
- **계정/언어 장벽**: **NASA Earthdata Login 필요**(무료 가입), 영어.
- **click-path/API**: Earthdata Login 가입 → dataset landing page → HTTPS bulk download (또는 `wget`/Earthdata `.netrc` 스크립트) → 3,152개 .laz + 1 .csv + 1 .kmz 인덱스 다운로드.
- **format/CRS/volume**: **원자료는 CHM GeoTIFF가 아니라 LAS/LAZ point cloud**(~10 pts/m², 1 km² 타일) — 브리핑의 "1 m CHM" 가정은 point cloud에서 사용자가 직접 rasterize해야 함. CRS는 UTM zone 19S-24S(EPSG 32719-32724, 타일별로 다름), WGS84. **총 용량 117.203 GB, 3,154 파일** [V] — 사전 가정 60 GB보다 약 2배 큼.
- **licence**: NASA EOSDIS 공개/public-domain 이용정책.
- **preprocessing**: LAS/LAZ → 1 m CHM 생성(ground/canopy classification, DTM-DSM 차분; lidR/PDAL 등), UTM zone별 처리 후 EPSG:4326/AEF 10 m grid로 리샘플링. pre/post 쌍 사이트 식별: Table 1 기준 DUC(2012→2017), FN1/FN2(2013→2016), FN3(2014→2017), TAN(2012→2014), AND(2013→2017), ST1/ST2(2013→2016), ST3(2014→2017), TAP_A01-03(2012/13→2016/17), JAM_A02(2011→2013), CAN_A01/A02(2014→2017), SDM_A01(2012→2017) [V] — Pará/Mato Grosso/Rondônia 위주로 TD01 ROI와 부합.
- **wall-clock/person-hours**: Earthdata 가입 즉시. 117 GB 다운로드(대학 네트워크 기준) **1~2일**; CHM 생성 파이프라인 구축·처리 **1주(40 person-hour)**.
- **blocking risk / fallback**: 용량 2배, point-cloud 처리 부담. 사이트 ≥4개 pre/post 조건은 위 목록으로 충족 가능해 보이나 TMF DegradationYear와의 시기 교차 확인은 미완. 실패(적격 사이트 <4 또는 matched footprint <400) 시 TD01 §11 fallback: ICESat-2 ATL08 단독으로 축소, 주장 범위를 100 m segment로 하향.

## 4. DETER / DETER-B — TD01 driver 귀속용 보조 데이터

- **목적**: TD01에서 degradation driver(logging/burn/mining) 귀속 및 사람 판독 기반의 TMF-independent stratification 보조. Aug-Jul → calendar-year 재binning 필요.
- **URL**: WFS `https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/wfs` [V, GetCapabilities 확인, OGC WFS 2.0.0]. 다운로드 포털 `https://terrabrasilis.dpi.inpe.br/downloads/` [V], 영문 `https://terrabrasilis.dpi.inpe.br/en/download-files/` [V]. 라이선스 `https://terrabrasilis.dpi.inpe.br/en/citations-and-use-licence/` [V].
- **계정/언어 장벽**: 로그인 불필요, 공개 WFS/shapefile. 영문 페이지 존재(포르투갈어 병기).
- **click-path/API**: `GetFeature` 예시 — `.../geoserver/deter-amz/wfs?service=WFS&version=2.0.0&srsName=EPSG:4674&request=GetFeature&typeName=deter_public&CQL_FILTER=date BETWEEN '2019-01-01' AND '2019-02-01'&outputFormat=SHAPE-ZIP` [U, 패턴은 검색으로 확인, 직접 실행 안 함] — 대량 조회 시 `count`/`startIndex` 페이징 필요.
- **format/CRS/volume**: Shapefile 또는 WFS output GeoJSON/SHAPE-ZIP; **SIRGAS2000 (EPSG:4674)**. 클래스: DESMATAMENTO_CR/DESMATAMENTO_VEG/MINERACAO(deforestation), DEGRADACAO/CICATRIZ_DE_QUEIMADA/CS_DESORDENADO/CS_GEOMETRICO(degradation) [V]. 전 Amazônia Legal 연간 알람 volume은 <1 GB(polygon 벡터).
- **licence**: **CC BY-SA 4.0** [V].
- **preprocessing**: **AMZ legal year = 전년 8월~해당년 7월** [V] → calendar-year로 재binning(사건월 정보가 있으면 월 단위 재배분, 없으면 균등/보수적 가정 명시). DETER Pantanal·Não-Floresta 서브 제품은 "실험적 단계"로 명시되어 있어 **core `deter-amz:deter_amz`만 안정 산출물로 사용**해야 함 [V].
- **wall-clock/person-hours**: WFS 스크립트 작성·페이징 처리 반나절, 재binning·검증 반나절 (~1 person-day).
- **blocking risk / fallback**: 대용량 날짜범위 조회 시 서버 페이징/timeout 가능성, 일부 서브 제품 불안정. 실패 시 MapBiomas C9 class 30(보조 driver 귀속)만으로 대체.

## 5. ELDOR — 검증 결과: 실재하나 브리핑 설명과 불일치

- **검증**: **ELDOR: A Dataset and Benchmark for Illegal Gold Mining in the Amazon Rainforest**, arXiv:2605.15397 (2026-05-14 제출), Kangning Cui 등 [V, abstract/PDF 직접 fetch]. `https://arxiv.org/abs/2605.15397` [V], `https://arxiv.org/pdf/2605.15397` [V].
- **정정 필요**: PROMPT.md의 "Earth Genome... embedding statistics" 서술은 실제 논문 내용과 **불일치**한다. ELDOR은 임베딩 통계 산출물이 아니라 **UAV/드론 orthomosaic 기반 픽셀-레벨 semantic segmentation 데이터셋/벤치마크**(아마존 >2,500 ha, mining feature + 주변 생태 라벨, semantic segmentation·인식·multi-label classification·vision-language class-presence task, 전문가 검토 플랫폼 포함)이다. TA04/TD01에서 "ELDOR을 reference로 쓴다"는 계획은 **위성(AEF 10 m annual) ↔ UAV 초고해상도 라벨 간 해상도 격차**를 반드시 다뤄야 한다는 뜻으로 재해석해야 한다.
- **취득처/라이선스**: abstract 페이지만으로는 실제 repo 링크·라이선스가 확인되지 않음 [U] — PDF 본문의 Data Availability 절 확인 필요.
- **licence/preprocessing**: [U] 미확인. UAV 해상도(cm급)를 AEF 10 m로 다운샘플링/집계하는 전처리가 필수(면적비 라벨로 변환).
- **wall-clock/person-hours**: 논문 PDF 데이터 접근 절 확인 + repo 취득 시도 **반나절**; 위성-UAV 해상도 정합 전처리 설계 **2~3일**.
- **blocking risk / fallback**: TA04 §S8 "Kill if ELDOR is unusable" 조건과 직결 — 해상도 불일치가 심하면 desk-only reference로만 쓰고 정량 계량은 Amazon Mining Watch(6항) 기반으로 대체.

## 6. Maus et al. global mining polygons v2 — TA04 ASGM subset gate

- **목적**: TA04 RQ1의 "ASGM-only reference"를 만들기 위한 원천 polygon inventory(GEE `projects/sat-io/open-datasets/global-mining/global_mining_polygons`는 이미 접근 가능하나 off-GEE 원본과 ASGM 분리 로직 필요).
- **off-GEE 원본**: PANGAEA `https://doi.pangaea.de/10.1594/PANGAEA.942325` [V] "Maus, V. et al. (2022): Global-scale mining polygons, Version 2"; 논문 DOI 10.1038/s41597-022-01547-4, "A update on global mining land use", Scientific Data [V].
- **속성/포맷**: GeoPackage, WGS84; 필드는 ISO3_CODE/COUNTRY_NAME/AREA(km²)/FID/geom [V]; **44,929 polygon, 총 101,583 km²** [V]. **artisanal/industrial 구분 필드 없음** — 브리핑 전제 확인됨.
- **ASGM 분리 로직(제안)**: AREA 단독 threshold는 표준화된 값이 없음 [U] — 지역 연구(예: Ghana ASM 문헌, rs16101749)에서 **<5 ha (~0.05 km²)** 를 ASM 특징적 소규모 footprint로 다루는 경향이 있으나 이는 특정 지역 heuristic이지 global standard 아님. 실무적으로는 AREA + shape irregularity/fragmentation(경계 복잡도, 인접 polygon 밀도로 "산개형 vs 집중형" 구분) 조합, 그리고 국가별 known-industrial-mine 목록(예: S&P Global, USGS mineral facility) 배제 후 잔여를 ASGM 후보로 두는 방식을 권고.
- **대안 ASGM 전용 소스**: **Amazon Mining Watch** `https://amazonminingwatch.org` [V, 페이지 확인] — AI/위성 기반 아마존 전역(9개국) 금광 추적, 합법+불법 포함이나 ASGM 전용 flag는 아님; 다운로드 방식/API rate limit/라이선스는 **미확인 [U]**. WWF/Verite/USAID PIQUE 등 ASGM 전용 global dataset은 이번 조사에서 **발견되지 않음(존재 단정 금지)**.
- **licence**: Maus v2는 **CC-BY-SA-4.0** [V].
- **preprocessing**: GeoPackage → GEE 자산과 attribute join 검증(동일 v2인지 폴리곤 수 대조), threshold+shape 기반 ASGM 후보 flag 생성, Amazon Mining Watch와 공간 overlay로 교차검증.
- **wall-clock/person-hours**: PANGAEA 다운로드 즉시(용량 작음, polygon vector). ASGM 분리 로직 설계·검증 **3~5 person-day** (threshold sensitivity 포함).
- **blocking risk / fallback**: ASGM 표준 정의 부재가 근본 리스크 — TA04 RQ1의 "ASGM 전용 reference" 자체가 반증 불가능해질 수 있음. 실패 시 Amazon Mining Watch를 1차 ASGM reference로 승격하고 Maus polygon은 negative(비-ASGM) pool로만 사용.

## 7. TESSERA tiles — TC01/TD01/TH01 baseline (desk-only, GEE 미제공)

- **목적**: TC01·TD01·TH01 등에서 "타 GFM/baseline" 항목으로 요구되는 TESSERA embedding. GEE에는 없으므로 desk-only 취득.
- **논문**: arXiv **2506.20380** [V] "TESSERA: Temporal Embeddings of Surface Spectra for Earth Representation and Analysis", Feng et al.; v2 논의 arXiv 2607.03949 [U, 검색만]. 프로젝트 사이트 `tessera.wiki` [U, DNS 실패].
- **배포 채널**: GitHub `github.com/ucam-eo/tessera`(모델/논문) [V], `github.com/ucam-eo/geotessera`(Python 접근 라이브러리, `pip install geotessera`) [V]. 실제 타일 저장소는 **Source Cooperative** `https://data.source.coop/tessera/tessera`(익명 S3 ListObjectsV2, 인증 불필요) [V, README로 확인; 브라우저 직접 접근은 403이나 라이브러리 접근은 정상]. 가중치 미러: Hugging Face `huggingface.co/geotessera/TESSERA-V-1.1` [V]. Zenodo 아카이브 `zenodo.org/records/19428267` [U, 검색만].
- **계정/언어 장벽**: 등록/API key 불필요, 영어.
- **click-path/API**: `pip install geotessera` → 라이브러리 API로 타일 좌표/연도 지정 후 Source Cooperative에서 자동 다운로드(Zarr 권장, 또는 GeoTIFF/NPY).
- **format/CRS/volume**: 0.1° grid 타일(~11×11 km), 10 m/pixel, 128-D embedding, int8 양자화(Matryoshka로 16/32/64/128-D 절단 가능), Zarr/GeoTIFF(UTM)/NPY+JSON 포맷. 총 용량 수치 미공개(on-demand 스트리밍) [U].
- **커버리지**: 전세계 **2024년**만 보장. 유럽(+미국)은 **2017-2025** 확장 완료. 그 외 지역·연도는 "요청 시"(대기열, turnaround 미공개) [V/U 혼재] — TD01 Amazon·Congo, TH01 한반도가 이 "요청 필요" 지역에 해당할 가능성이 큼.
- **licence**: 라이브러리 MIT, 임베딩/가중치 **CC0-1.0**(퍼블릭 도메인) [V] — 재배포 제약 없음.
- **preprocessing**: UTM/Zarr → AEF 10 m grid와 정합(리샘플링/좌표계 통일), 필요 시 128-D → AEF와 동일 차원으로 절단 비교.
- **wall-clock/person-hours**: 라이브러리 설치·2024년 유럽/미국 타일 시험 다운로드 **반나절**; 필요 지역(아마존/콩고/한반도) 임베딩 요청 후 대기 **기간 미확정(주 단위 리스크)**.
- **blocking risk / fallback**: 필요 ROI·연도가 미공개 지역일 경우 요청 큐 대기가 각 topic의 timeline을 지연시킬 수 있음. 실패/지연 시 "TESSERA는 GEE 미제공·desk-only"로 이미 각 제안서(TC01 등)에 기록된 대로 **desk-only 비교에서 제외하고 baseline을 S2 composite/Clay/Prithvi로 한정**.

---

## 우선순위 표 (게이팅 항목 기준)

| 순위 | 항목 | 게이팅 대상 | 이유 | 착수 시점 |
|---|---|---|---|---|
| 1 | 1. 환경부 토지피복지도 | TH01 C2 | TH01은 flagship, gate 2개 중 label 확보가 최장 리드타임(도메인 이전+로그인) | 즉시(W1) |
| 2 | 2. 산림청 임상도 | TH01 C2 | 자료신청 심사 대기(주 단위 불확실) — 병렬로 즉시 신청해야 W3 마감 준수 가능 | 즉시(W1), 1항과 동시 |
| 3 | 3. ORNL DAAC ALS | TD01 조건(i) | 117 GB 다운로드 + point cloud→CHM 처리가 W1-2 GO-gate 자체 | 즉시(W1) |
| 4 | 6. Maus v2 + ASGM 분리 | TA04 게이트 | ASGM 정의 자체가 반증가능성의 근간이므로 설계를 일찍 확정해야 pilot 재작업 방지 | W1-2 |
| 5 | 4. DETER/DETER-B | TD01 보조 | 용량 작고 즉시 접근 가능, 리스크 낮음 — 3항과 병행 가능 | W1-2 |
| 6 | 5. ELDOR | TA04 kill-switch | 해상도 정합 문제로 desk-only 재해석 필요, TA04 pilot 설계에 선행 확인 필요하나 대체 소스(Amazon Mining Watch) 존재 | W2 |
| 7 | 7. TESSERA | TC01/TD01/TH01 baseline (desk-only) | GO/NO-GO를 막지 않는 보조 baseline — 커버리지 부족 지역은 요청 큐 리스크만 지고 후순위 | W3 이후, 필요 시 병렬 요청만 W1에 넣어둠 |

**Critical path**: TH01의 두 개 외부 gate(1·2)가 W3 말 마감이며 병렬 진행이 필수 — 산림청 자료신청은 심사 대기가 있어 **가장 먼저(W1 첫날) 신청**해야 한다. TD01의 ALS(3항)는 W1-2 자체가 GO-gate 마감이라 동시 착수. TA04의 ASGM 분리(6항)는 물리적 다운로드 리스크는 낮지만 정의 확정이 pilot 재작업을 좌우하므로 W1-2 내 설계 완료가 필요. 따라서 **W1-2가 3개 토픽 모두의 병목**이며, 세 게이트가 동시에 W3 전후로 수렴한다 — 순차가 아니라 **병렬 착수**가 유일한 실행 가능 경로다.
