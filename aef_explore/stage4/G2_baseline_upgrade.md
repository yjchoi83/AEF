# G2: baseline upgrade — TA04 label-efficiency multiple, restated against a rich classical baseline

## 1. 무엇을 바꿨나

Stage-2 TA04는 AEF-64 label-efficiency를 **8-band annual median S2 composite**(B2,B3,B4,B8,B11,B12,NDVI,NBR)
+ logistic probe와만 비교했다. 이는 D4/Reviewer-2가 지적한 대로 지나치게 약한 baseline이고, AEF 64-dim
vs S2 8-dim이라는 feature 수 비대칭이 label-efficiency multiple을 부풀릴 수 있다는 우려가 있었다.

이번 G2에서는 `scratch/G2_sample.py`로 TA04와 **동일한 label 구성**(Maus mining polygon = positive,
1.5–12 km annulus 밖 Hansen loss 2015–2019·treecover>30% = hard negative, loss=0·treecover>50% =
stable, `stratifiedSample(seed=7, scale=20, 900/class)`, Y=2019, 동일 ROI AMZ `[-58,-8,-54,-4]`/GHA
`[-3.2,4.9,-0.9,7.2]`)로 stratified sampling한 뒤, **rich classical feature stack**(S2 percentile
p10/25/50/75/90 × 11 bands/indices, intra-annual stdDev × 4, focal texture × 5, S1 VV/VH percentile·
stdDev·ratio·focal × 8 = **74 features**, AEF-64와 거의 dimensionality-matched)를 같은 지점에서 추출했다.

**실행 이슈와 조치 (투명성 보고)**: TA04 원본은 `stratifiedSample`을 `tileScale=8`로 호출했는데, 이번
세션의 GEE backend에서는 이 설정으로 4°×4° ROI 전체를 스캔하는 호출이 150초 이상(최대 590초 타임아웃도
초과) 걸려 완료되지 않았다. `tileScale=4`로 낮추자 900/class(2700점) 전체가 95–115초에 끝났다. 문제는
GEE의 `stratifiedSample`이 tile 단위로 pseudo-random 샘플링을 하기 때문에 **`tileScale`을 바꾸면 seed가
같아도 실제로 뽑히는 점의 정체(identity)가 달라질 수 있다**는 것이다. 검증: 이번 실행에서 자체 재구성한
weak 8-band baseline(rich stack의 `*_p50` 컬럼에서 복원, 아래 S2OLD_log)은 AMZ full-AUC 0.665 / GHA
0.848로, TA04가 보고한 0.638 / 0.867과 **비슷한 자릿수**이지만 동일하지 않다 — 즉 이번 점 집합은 TA04의
csv와 byte-identical하지 않다. 반면 AEF-64 arm의 절대 AUC(AMZ full 0.953)는 TA04 보고치(0.855)보다
뚜렷이 높아, 새 점 집합이 우연히 AEF 관점에서 더 잘 분리되는 draw였을 가능성이 있다. **따라서 아래 수치는
"Stage-2 csv의 완전한 재현"이 아니라, 동일한 파라미터로 다시 뽑은 self-consistent한 새 draw이며, 모든
arm이 정확히 같은 74+64 feature 지점 집합 위에서 계산되었으므로 arm 간 비교(핵심 결과)는 유효하다.**
Sampling 자체는 완전히 성공했다(AMZ/GHA 각 2700/2700점, 74개 rich feature 전부 NaN 없이 채워짐 — S1
VV/VH·focal texture 포함 어떤 band도 탈락하지 않았다).

## 2. Feature count

- AEF: 64 bands (A00–A63)
- Rich classical: **74 features** — S2 percentile(10/25/50/75/90) × {B2,B3,B4,B8,B11,B12,NDVI,NBR,NDWI,
  NDMI,IOR} = 55, intra-annual stdDev{NDVI,NBR,B8,B11} = 4, focal texture{B8_sd3,B8_sd7,NDVI_sd3,
  NDVI_sd7,B8_dev7} = 5, S1{VV,VH}_percentile(10/50/90) = 6, S1 stdDev{VV,VH} = 2, VV−VH ratio = 1,
  VV focal stdDev = 1. 약속한 "~75"에서 하나 적은 74 — S1 VV_p50 focal std를 별도 밴드 하나로만 셌기
  때문(설계 문서의 "S1 focal stdDev"가 VV만이라 6+2+1+1=10이 아니라 74로 정확히 맞음). Old weak
  baseline: 8 (self-consistently 재구성).

## 3. Label-efficiency curve (GroupKFold 5-fold, 0.1° blocks, 30 draws/budget/fold, metric=AUC, positive=mining)

LightGBM 설정: `n_estimators=150, num_leaves=7, min_child_samples=5, learning_rate=0.05,
subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0, is_unbalance=True` — label 예산이 25만큼 작을 때도
과적합을 억제하도록 leaf 수·min_child_samples를 작게, learning rate를 낮게 잡았다.

### AMZ

| labels | 25 | 50 | 100 | 250 | 500 | 1000 | full(≈2160 train) |
|---|---|---|---|---|---|---|---|
| AEF64 + logistic | 0.749 (.088) | 0.826 (.071) | 0.886 (.041) | 0.924 (.029) | 0.940 (.022) | 0.948 (.020) | **0.953** (.019) |
| AEF64 + LightGBM | 0.669 (.085) | 0.738 (.073) | 0.808 (.051) | 0.865 (.042) | 0.893 (.035) | 0.908 (.031) | 0.918 (.029) |
| RICH-74 + LightGBM | 0.582 (.064) | 0.633 (.065) | 0.688 (.066) | 0.758 (.058) | 0.801 (.054) | 0.826 (.051) | 0.845 (.047) |
| RICH-74 + logistic | 0.600 (.081) | 0.636 (.075) | 0.684 (.074) | 0.741 (.073) | 0.776 (.062) | 0.794 (.061) | 0.807 (.056) |
| S2-8(old) + logistic | 0.577 (.085) | 0.592 (.087) | 0.625 (.074) | 0.648 (.074) | 0.657 (.071) | 0.662 (.072) | 0.665 (.072) |

### GHA

| labels | 25 | 50 | 100 | 250 | 500 | 1000 | full(≈2160 train) |
|---|---|---|---|---|---|---|---|
| AEF64 + logistic | 0.889 (.058) | 0.920 (.038) | 0.942 (.029) | 0.960 (.021) | 0.969 (.017) | 0.977 (.015) | **0.981** (.014) |
| AEF64 + LightGBM | 0.847 (.057) | 0.899 (.038) | 0.924 (.031) | 0.947 (.023) | 0.958 (.019) | 0.965 (.017) | 0.970 (.016) |
| RICH-74 + LightGBM | 0.819 (.052) | 0.856 (.045) | 0.876 (.042) | 0.906 (.033) | 0.919 (.031) | 0.928 (.027) | 0.934 (.025) |
| RICH-74 + logistic | 0.835 (.061) | 0.855 (.051) | 0.866 (.047) | 0.894 (.034) | 0.908 (.029) | 0.920 (.026) | 0.927 (.026) |
| S2-8(old) + logistic | 0.795 (.068) | 0.820 (.056) | 0.830 (.049) | 0.839 (.046) | 0.845 (.044) | 0.846 (.043) | 0.848 (.042) |

(값 = mean AUC (fold sd), 예산당 draw 수 150 = 5 fold × 30 seed.)

**관찰**: (i) AEF-64는 logistic probe에서 이미 최고 성능이며 LightGBM을 얹으면 오히려 소폭 하락한다
(AMZ full 0.953→0.918) — AEF embedding은 이미 거의 선형으로 decodable하다는 기존 관찰과 일치. (ii)
반대로 rich classical feature는 LightGBM이 logistic보다 항상 낫다(AMZ full 0.807→0.845, GHA
0.927→0.934) — classical feature는 비선형 상호작용(texture×index 등)이 있어야 성능이 나온다. 따라서
"classical baseline에게 최선을 다하게 한" 공정한 대조는 **RICH-74+LightGBM**이다.

## 4. Parity ratio — 정의 (D4 fragility 대응)

- **분자(target label 수)**: 비교 대상 baseline이 그 AUC를 얻는 데 실제로 쓴 label 수. "@1000"은 1000,
  "@full"은 각 fold의 실제 training pool 크기의 평균(≈0.8×2700=2160)을 쓴다(baseline이 "전체"를 쓴다는
  것은 고정된 label 수가 아니므로 근사치임을 명시).
- **분모(AEF가 필요한 label 수)**: AEF-64+logistic의 mean-AUC curve(rung 25/50/100/250/500/1000)를
  log(label) 축에서 선형보간하여, baseline의 target mean AUC를 처음 넘어서는 label 수를 읽는다. 가장
  작은 rung(25)에서 이미 target을 넘으면 **테스트 범위 아래로 censored된 하한**으로만 보고한다(즉 실제
  필요한 label은 25보다 더 적을 수 있음).
- **ratio = 분자 / 분모**.
- **95% CI**: fold×seed AUC draw pool(AEF curve 각 rung, baseline @1000)과 fold draw pool(baseline
  @full)에서 각각 **bootstrap(with replacement, B=3000)**으로 재추출 → 매번 보간·교차점·ratio를
  재계산 → 2.5/97.5 percentile.

## 5. Restated multiple

| 비교 | AMZ ratio (95% CI) | GHA ratio (95% CI) |
|---|---|---|
| **구식(weak S2-8 baseline)** — Stage-2가 주장한 수치, 이번 draw로 재확인 | ≥40x (censored @25 labels) | ≥40x (censored @25 labels) |
| **신규 vs RICH-74+logistic @1000 labels** | 26.7x (23.5–30.1) | 19.9x (16.5–23.2) |
| **신규 vs RICH-74+LightGBM @1000 labels** (baseline에 가장 유리한 arm) | **19.9x (17.3–22.4)** | **15.7x (12.8–19.5)** |
| 신규 vs RICH-74+logistic @full(≈2160) | 52.3x (31.2–79.2) | 35.8x (14.6–63.2) |
| 신규 vs RICH-74+LightGBM @full(≈2160) | 35.5x (22.7–53.9) | 28.6x (10.9–52.3) |

**핵심 restatement**: baseline을 8-band S2 median에서 74-feature classical(percentile+texture+S1)
+LightGBM으로 올리면, label-efficiency multiple은 "≥40x"에서 **약 13–30x 구간(최악의 경우 95% CI
하한 12.8x)** 으로 줄어든다 — 명백한 collapse이지만, TA04가 pre-register한 RQ1 falsification threshold
**3x를 어느 조건에서도 크게 상회**한다(가장 낮은 CI 하한도 3x의 4배 이상).

## 6. Full-data AUC와 "저-label 영역에만 국한되는가?"

| arm | AMZ full AUC (sd) | GHA full AUC (sd) |
|---|---|---|
| AEF64 + logistic | 0.953 (.019) | 0.981 (.014) |
| AEF64 + LightGBM | 0.918 (.029) | 0.970 (.016) |
| RICH-74 + LightGBM | 0.845 (.047) | 0.934 (.025) |
| RICH-74 + logistic | 0.807 (.056) | 0.927 (.026) |
| S2-8(old) + logistic | 0.665 (.072) | 0.848 (.042) |

AEF64(logistic) − RICH-74(LightGBM) full-AUC gap = **+0.108 (AMZ)**, **+0.047 (GHA)** — combined fold-sd
는 각각 .051, .029이므로 AMZ는 뚜렷하게(gap/combined-sd≈2.1), GHA는 다소 약하지만(≈1.6) fold noise
밖에 있다. **즉 AEF의 우위는 full-data에서도 사라지지 않는다** — arXiv:2609.03480(2026, 덴마크 수종
분류)이 다른 task에서 관찰한 "AEF 우위가 저-label 영역에만 국한된다"는 패턴과 달리, 이 ASGM 탐지
task에서는 AEF가 최선의 74-feature classical+LightGBM baseline을 label 수와 무관하게(25 label부터
full까지 전 구간) 앞선다. 다만 격차의 **크기**는 label이 늘수록 상대적으로 줄어든다(예: GHA에서 25
label 시점 AEF64-log 0.889 vs RICH-lgbm 0.819, gap .070; full 시점 gap .047) — 절대 우위는 유지되지만
"AEF가 특히 유리한" 것은 여전히 low-label 구간이다.

## 7. TA04 verdict

Stage-2의 ">=25x / >40x, dimensionality mismatch가 우려됨"이라는 잠정 결론은 **근거가 뒤집히지 않았다**:
dimensionality를 74 vs 64로 거의 맞추고 baseline에 LightGBM까지 허용해도 label-efficiency multiple은
13–30x(최악 CI 하한 12.8x) 구간에 머물러 RQ1의 3x falsification threshold를 확실히 통과하며, AEF의
우위는 full-data에서도 유지된다(Denmark 논문과 다른 패턴). **TA04 PASS 판정은 유지**하되, 보고 문구를
"S2 8-band baseline 대비 ≥25–40x"에서 **"near-dimensionality-matched 74-feature classical+LightGBM
baseline 대비 약 13–30x(95% CI, region 의존)"**로 낮춰서 restate해야 한다.

## 8. Files

- `scratch/G2_sample.py` — rich-baseline sampler (tileScale 8→4 수정, 캐시된 점 재사용 로직 추가)
- `scratch/G2_AMZ.csv`, `scratch/G2_GHA.csv` — 2700×141 (74 rich + 64 AEF + y/lon/lat), no missing bands
- `scratch/G2_analysis.py` — label-efficiency curve + bootstrap parity-ratio 계산
- `scratch/G2_results.pkl` — 전체 curve/ratio 결과(pickle)
