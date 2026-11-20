Objective: simplify ordering in a pure send decision helper for an EA. MQL5, SendGuard.mqh.
SENT means the broker acknowledged the request and terminates retry. FAILED means broker explicitly rejected it and retry is allowed within the attempt budget. UNKNOWN means await reconciliation by request identifier and retry only if that reconciliation establishes that the broker did not accept the request.
The helper can allow the initial send when it receives READY. Attempt index starts at zero. Allowed indexes are strictly less than the total configured maximum (minimum one).
Acceptance: ready, sent, retryable failure with remaining budget. Log state and attempt index upstream. Run strict compile and compare fixed scenario regression with the last known good result.

Before/after capture required for the single checklist target SendGuard.mqh: BEFORE.txt and AFTER.txt in this fixture.
