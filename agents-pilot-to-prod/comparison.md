# Tools and platforms for production agents (as of 2026-10-17)

Legend as in `research.md`: ✅ verified on primary page/repo, 🟡 vendor claim, 🟠 secondary, 🧪 used in our workshop.
GitHub numbers are from the GitHub API on 2026-10-17 (stars change daily; they indicate adoption, not quality).

## 1. Observability + evals platforms

| Tool | What it is | License / hosting | OTel story | Status / ownership (2026) | Notes |
|---|---|---|---|---|---|
| **Langfuse** | Tracing, prompt management, datasets, evals, LLM-as-judge on traces | Core MIT, `ee/` commercial; self-host (Docker/K8s; Postgres + ClickHouse + Redis + S3) or Cloud | OTLP ingest; Datadog maps Langfuse spans 🟡 | **Acquired by ClickHouse (Jan 2026)**; "no planned changes to licensing" ✅ [blog](https://langfuse.com/blog/joining-clickhouse); repo 36k★, v4.63.0 (2026-10-16) ✅ | Most popular OSS option; self-host stack is heavier than Phoenix |
| **Arize Phoenix** | Tracing + evals + datasets/experiments UI | **Elastic License 2.0** (source-available, free to self-host, no feature gates; not OSI) ✅ [license](https://arize.com/docs/phoenix/self-hosting/license); single container | Native OTel + **OpenInference** conventions ✅ | Repo 11.9k★, v20.23.0 (2026-10-16) ✅; commercial big brother: Arize AX | 🧪 used as our trace backend (one `docker run`) |
| **LangSmith** (LangChain) | Tracing, evals, prompt hub, deployment | SaaS; **self-host only on Enterprise plan** (K8s, license key) 🟠 [docs](https://docs.langchain.com/langsmith/self-hosted) | OTel ingest supported 🟠 [docs](https://docs.langchain.com/langsmith/trace-with-opentelemetry) | Runs the State of Agent Engineering survey | Best fit if the client is on LangGraph |
| **Braintrust** | Evals-first platform + observability ("Brainstore" trace DB) | SaaS; hybrid self-host (data plane in your cloud, control plane managed) 🟠 [docs](https://www.braintrust.dev/docs/admin/self-hosting) | OTel ingest 🟠 | **$80M Series B (Feb 2026, ICONIQ)** ✅ [blog](https://www.braintrust.dev/blog/announcing-series-b); customers named: Notion, Replit, Cloudflare, Ramp, Dropbox 🟡 | Strong eval/experiment UX |
| **Opik** (Comet) | Tracing + evals + guardrails | Apache-2.0, self-host ✅ | OTel ingest (not verified ❌) | Repo 22.7k★ ✅ | OSS alternative to Langfuse |
| **MLflow 3** (GenAI) | Tracing + evaluation inside MLflow | Apache-2.0 ✅ | OTel-compatible tracing (not verified ❌) | Repo 28.4k★, v3.17.1 ✅ | Natural for Databricks shops |
| **OpenLLMetry** (Traceloop) | OTel instrumentation libraries for LLM SDKs/frameworks | Apache-2.0 ✅ | Pure OTel | v0.62.4 (2026-09-29) ✅ | Instrumentation, not a backend |
| **OpenInference** (Arize) | OTel instrumentation + conventions | Apache-2.0 ✅ | OTel, own attribute names | active (2026-10) ✅ | Used by Phoenix; Datadog ingests it 🟡 |
| **Datadog Agent/LLM Observability** | APM vendor's LLM/agent module | SaaS | **Native OTel GenAI semconv v1.37+** and OpenInference ingest 🟡 [blog](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) | | Good if the client already runs Datadog |
| **OpenAI Agents SDK tracing / Evals** | Built-in tracing to OpenAI dashboard; trace grading; evals | MIT SDK (30k★ ✅); dashboard is OpenAI-hosted | Custom trace processors to other backends (not verified ❌) | Promptfoo being integrated into **OpenAI Frontier** ✅ | Easiest when all-in on OpenAI; data leaves to OpenAI |

## 2. Eval and red-team frameworks (code-first)

| Tool | Focus | License | Status | Notes |
|---|---|---|---|---|
| **Promptfoo** | Eval + red-teaming CLI/YAML, CI-friendly | MIT ✅ | **OpenAI to acquire (Mar 9 2026)**, "will continue building the open-source project" ✅ [OpenAI](https://openai.com/index/openai-to-acquire-promptfoo/); 26k★ ✅; claims use by >25% of Fortune 500 🟡 | Watch vendor neutrality going forward |
| **Inspect** (UK AI Security Institute) | Evals for agents: datasets, solvers, scorers, tools, sandboxes (Docker/K8s) | MIT ✅ | v0.3.281 (2026-10-15), 3k★ ✅ [docs](https://inspect.aisi.org.uk/) | Rigorous, safety-research grade; great for agentic/sandboxed tasks |
| **DeepEval** (Confident AI) | pytest-style LLM metrics | Apache-2.0 ✅ | 18.9k★ ✅ | Many prebuilt judge metrics - calibrate them |
| **OpenEvals** (LangChain) | Prebuilt evaluators (LLM-as-judge, trajectory) | MIT ✅ | 1.2k★ ✅ | |
| **Plain pytest + JSONL** | Deterministic trajectory checks + gate | - | 🧪 our `ex2_evals/` | Zero lock-in; enough to start |

## 3. Guardrails

| Tool | Type | License | Status | Notes |
|---|---|---|---|---|
| **NVIDIA NeMo Guardrails** | Programmable rails (input, output, dialog, retrieval, execution) | Apache-2.0 (GitHub shows NOASSERTION) | v0.24.1 (2026-09-16) ✅ | Heavier, flexible; Colang DSL |
| **Guardrails AI** | Validators / output contracts (schema, PII, toxicity...) | Apache-2.0 ✅ | v0.11.0 (2026-08-14) ✅ | Good for structured output contracts |
| **LLM Guard** (Protect AI) | Input/output scanners | MIT ✅ | last push 2026-07 ✅ | Lightweight scanners |
| **Safety classifiers**: Llama Guard family, **NVIDIA Nemotron 3.5 Content Safety** (4B, from Gemma-3-4B) | Classify prompts/responses into harm categories | open weights | Nemotron CS available free on OpenRouter 🧪 | Content-safety, not authorization; false positives on business requests 🧪 |
| **Lakera** (now Check Point) | Commercial prompt-injection/AI firewall | SaaS | acquired, closed Oct 22 2025 ✅ | Vendor consolidation into security platforms |
| **Policy engines at the tool boundary**: Cedar (AWS AgentCore Policy), OPA/Rego, plain code | Deterministic authorization of agent actions | OSS | AgentCore Policy GA Mar 2026 🟡 | 🧪 our `agent/guards.py:tool_policy` - the only layer with hard guarantees |

## 4. Hyperscaler agent-governance stacks

| Stack | Governance pieces | Status |
|---|---|---|
| **AWS Bedrock AgentCore** | Runtime, Identity, Gateway, Observability (OTel/ADOT), **Policy (Cedar)**, **Evaluations** | Policy + Evaluations GA March 2026 🟡 [AWS](https://aws.amazon.com/about-aws/whats-new/2026/03/agentcore-evaluations-generally-available/) |
| **Microsoft Agent 365 + Entra Agent ID + Foundry** | Agent registry, identities, Conditional Access, observability | Agent 365 GA May 1 2026, licensed per user 🟠 [Microsoft](https://www.microsoft.com/en-us/security/blog/2026/05/01/microsoft-agent-365-now-generally-available-expands-capabilities-and-integrations/) |
| **Google Gemini Enterprise / Vertex AI Agent Engine** | build, run and govern multi-step agents | not verified in this round ❌ |
| **OpenAI Frontier** | platform for "AI coworkers"; Promptfoo security testing being integrated | ✅ (per Promptfoo announcement) |

## 5. How to choose (decision guide)

| Client situation | Suggested stack |
|---|---|
| Must self-host, open source preferred, small team | OTel instrumentation (GenAI semconv) → **Langfuse** (MIT core) or **Phoenix** (ELv2, single container) + Promptfoo/pytest evals in CI |
| Already on Datadog / an APM vendor | OTel GenAI semconv → existing APM; add an eval framework in CI |
| All-in on AWS / Microsoft | AgentCore (Policy + Evaluations) / Agent 365 + Entra Agent ID; keep OTel so traces stay portable |
| Heavy LangGraph usage | LangSmith (Enterprise for self-host) |
| Eval-heavy product teams | Braintrust or Langfuse datasets/experiments |
| Regulated, needs audit evidence | Any of the above + deterministic tool policy + immutable trace retention + eval reports per release |

**Lock-in hedge:** instrument with OpenTelemetry using the GenAI semantic conventions (plus OpenInference attributes
if the backend needs them), keep eval datasets as files in git, and keep authorization in your own policy layer.
