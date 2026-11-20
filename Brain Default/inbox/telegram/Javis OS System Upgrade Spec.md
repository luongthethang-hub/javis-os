# SYSTEM UPGRADE DIRECTIVE: JAVIS CORE ENGINE ENHANCEMENT
**Target System:** Javis OS (Multi-Agent Core Architecture)  
**Objective:** Upgrade context efficiency, model resilience, memory persistence, auto-configuration, and continuous skill evolution based on advanced coding-agent patterns.  
**Execution Mode:** Autonomous / Step-by-step with Guardrails & Verification Gates.

---

## 1. ARCHITECTURAL OVERVIEW & CORE PRINCIPLES

You are instructed to implement 5 core sub-systems into Javis OS. All code must adhere to the following guardrails:
1. **Local-First & Data Privacy:** All context compression, memory extraction, and log analysis must run locally. Redact secrets/tokens before any external model API calls.
2. **Hook Loop Prevention:** Set explicit `is_internal_hook` flags and recursion depth limits (`depth <= 2`) to prevent cascading hook executions.
3. **Graceful Failover:** Primary model failures must trigger secondary model fallbacks within the same capability tier without failing the user task.
4. **Human-in-the-Loop Gate:** Self-evolving skills or workspace overrides must be stored in staging and require explicit user/test approval before production rollout.

---

## 2. SUB-SYSTEM SPECIFICATIONS & INTEGRATION TASKS

### PHASE 1: Dynamic Model Router & Failover Gateway (OmniRoute Pattern)
- **Goal:** Provide uninterrupted task execution across multiple AI providers and free tiers.
- **Tasks to Execute:**
  1. Create module `core/router/model_gateway.py` (or equivalent in Javis codebase).
  2. Implement Provider Pool Configuration: support primary model (e.g., Claude 3.5 Sonnet / GPT-4o) and backup chain (e.g., Gemini Flash, DeepSeek, Local Ollama).
  3. Implement automatic failover logic on HTTP status `429` (Rate Limit), `500/503` (Server Error), or timeout (>30s).
  4. Log failover telemetry (`session_id`, `from_model`, `to_model`, `reason`, `latency`).
  5. Add Circuit Breaker: disable a failing provider for 60 seconds after 3 consecutive failures.

### PHASE 2: Context Compression Engine & Artifact Store (Headroom Pattern)
- **Goal:** Reduce input token consumption by 30-60% without sacrificing task context.
- **Tasks to Execute:**
  1. Create module `core/context/compressor.py`.
  2. Implement pre-flight token reduction for tool outputs, build logs, terminal stdout, and raw JSON.
     - *Rules:* Preserve error stacktraces, header lines, summary counts, and diff boundaries. Trim redundant repetitive logs.
  3. Create local `Artifact Store` (`.javis/artifacts/`): dump raw/uncompressed tool outputs here and attach an `artifact_id` in the prompt so agents can re-query full details if needed.
  4. Measure and log token savings ratio per agent turn (`tokens_in_raw` vs `tokens_in_compressed`).

### PHASE 3: Episodic & Semantic Persistent Memory (Claude-Mem Pattern)
- **Goal:** Retain cross-session context, file modifications, and project decisions.
- **Tasks to Execute:**
  1. Create module `core/memory/persistent_mem.py`.
  2. Register lifecycle hooks:
     - `on_tool_end`: Collect tool execution summary.
     - `on_session_end`: Extract structured observation (`summary`, `modified_files`, `key_decisions`, `unresolved_issues`).
  3. Implement Memory Indexing: store observations in lightweight local SQLite/Vector index partitioned by `workspace_id`.
  4. Implement `on_session_start` context injection: load top relevant summaries for the active workspace, bounded by a maximum token budget (e.g., max 1000 tokens).

### PHASE 4: Workspace Profiler & Auto-Configuration (Claude Code Setup Pattern)
- **Goal:** Auto-detect project stack and configure subagents, skills, and tools upon initialization.
- **Tasks to Execute:**
  1. Create module `core/workspace/profiler.py`.
  2. Implement project scanner: detect tech stack, linter, test runner, package manager, and folder structure.
  3. Generate recommended configuration `javis.config.json` containing:
     - Pre-commit/Post-edit Hooks (e.g., auto-formatting).
     - Active Skills (e.g., frontend design, database migration).
     - Subagents (e.g., code reviewer, security scanner).
     - MCP Servers (e.g., local docs lookup).
  4. Prompt user for approval before activating generated profile.

### PHASE 5: Background Task Observer & Skill Evolution (Task Observer Pattern)
- **Goal:** Learn operator preferences and iteratively improve skills.
- **Tasks to Execute:**
  1. Create module `core/evolution/observer.py`.
  2. Listen to user feedback events (`corrections`, `overrides`, `format_preferences`).
  3. Maintain skill versioning (`skills/v1/`, `skills/v2/`).
  4. Generate skill improvement patches based on repeated patterns.
  5. Enforce safety gate: staged skill changes must be stored in `.javis/staging/` and presented to the operator/test suite with a `diff` preview for confirmation.

---

## 3. VERIFICATION & ACCEPTANCE CRITERIA

Upon completing the implementation, Javis OS must run the following validation suite:

1. **Failover Test:** Simulate a 429 response on the primary model -> Confirm task completes successfully via fallback model.
2. **Compression Test:** Feed a 50,000 token log output -> Confirm compressed context sent to model is <25,000 tokens while maintaining error identification accuracy.
3. **Memory Continuity Test:** End session -> Start new session on same workspace -> Confirm agent accurately recalls modified files without re-explaining.
4. **Recursion Guard Test:** Trigger nested hooks -> Confirm system caps execution depth without infinite loops.

---

## 4. EXECUTION COMMAND FOR JAVIS

```bash
# Direct command to initialize upgrade process:
javis execute --spec javis_upgrade_instructions.md --auto-test --verbose
```