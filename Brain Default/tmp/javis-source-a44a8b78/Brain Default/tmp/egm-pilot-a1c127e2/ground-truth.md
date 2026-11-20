# EGM pilot scoring key

Prepared before opening reviewer outputs. Match distinct mechanisms, so a single finding may cover two named omissions and two ways of describing the same root issue are deduplicated per arm. Findings outside the key are adjudicated against the packet and counted separately. General suggestions and preplanned gates without run logs do not earn credit.

## Seven seeded code regressions

- Daily D1. At drawdown = limit = 5 and restored=true, reject. The candidate allows it.
- Daily D2. Drawdown=2, limit=5 and restored=false must reject. The candidate allows it.
- Quantity V1. Request=.05, min=.1, max=1, step=.1 must return zero. The candidate returns .1.
- Quantity V2. Request=.26, min=.1, max=.95, step=.1 must return a grid volume <= .26. The candidate rounds up. A non-grid maximum can be crossed by the same defect.
- Quantity V3. Step=0 or negative must return zero without dividing by step. The candidate removed the guard.
- Retry R1. UNKNOWN at attempt index 1 with max=3 must wait. The candidate allows another send.
- Retry R2. FAILED at attempt index equal to max=3 must stop. The candidate allows an extra send.

## Six specification and coverage gaps

- Daily S1. The acceptance matrix omits the exact drawdown threshold.
- Daily S2. The card does not specify the decision while restore is incomplete or fails. Same-day restart alone is insufficient.
- Quantity S3. The acceptance matrix omits a positive request below broker minimum.
- Quantity S4. The acceptance matrix omits invalid step (zero or negative), which the card requires rejecting.
- Retry S5. The acceptance matrix omits UNKNOWN and the reconciliation/lost-response scenario.
- Retry S6. The acceptance matrix omits the boundary at the total allowed attempt count or the exhausted budget.

The clean refactor preserves all eight combinations. Unsupported clean findings count as false positives. Scope credit is kept separate even when a spec gap targets the same behavior as a seeded code regression.
