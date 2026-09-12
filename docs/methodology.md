# Methodology: Real-time Airfare Price Index (APIx)

## 1. Fixed Sampling Design
To eliminate sample composition bias:
- **Routes**: 16 directional domestic high-traffic city pairs (e.g., DEL-BOM, BOM-DEL).
- **Horizons**: T+1, T+7, T+15, T+30, T+45 days.
- **Collection Times**: Fixed windows at 09:00 IST and 18:00 IST.
- **Fare Product**: Economy, 1 adult passenger, one-way, mandatory total fare.

## 2. Mathematical Aggregation

### Step 1: Route-Horizon Price
$$P(r,h,t) = \text{median}(\text{valid canonical total fares for route } r, \text{horizon } h, \text{date } t)$$

### Step 2: Price Relative
$$R(r,h,t) = \frac{P(r,h,t)}{P(r,h,0)}$$
where period $0$ is the frozen base period.

### Step 3: Route Price Index
$$\text{RouteIndex}(r,t) = 100 \times \sum_{h} \left[ v(h) \times R(r,h,t) \right]$$
Default horizon weights $v(h)$:
- T+1: 0.10
- T+7: 0.25
- T+15: 0.30
- T+30: 0.20
- T+45: 0.15

### Step 4: Headline National APIx
$$\text{APIx}(t) = \sum_{r} \left[ w(r) \times \text{RouteIndex}(r,t) \right]$$
Weights $w(r)$ sum to 1.0 and are derived from DGCA passenger traffic volume proxies.

## 3. Missing Data & Imputation Rules
1. Use canonical quotes collected on day $t$.
2. Single-window outage: use remaining collection window and flag reduced coverage.
3. Full-day outage: carry forward the last valid route-horizon price for **at most 2 days** (`imputed_last_observation`).
4. Beyond 2 days: exclude component, dynamically re-normalise remaining horizon weights, lower quality score, label index `partial_coverage`.
5. If weighted basket coverage drops below 70%, suppress headline index generation to prevent misleading signals.
