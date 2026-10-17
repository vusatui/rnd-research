"""OpenTelemetry setup for the workshop agent.

Spans follow the OpenTelemetry GenAI semantic conventions (status: Development, see research.md):
  invoke_agent {agent}  ->  chat {model}  /  execute_tool {tool}
and *also* carry OpenInference attributes (openinference.span.kind, input.value, llm.token_count.*) so the
Arize Phoenix UI renders them nicely. Two conventions side by side is the real-world state in 2026.

Exporters:
  - always: JSONL file out/traces.jsonl (one span per line) - used by summarize.py, evals and budget reports;
  - if OTEL_EXPORTER_OTLP_TRACES_ENDPOINT is set: OTLP/HTTP (Phoenix, Langfuse, Jaeger, any OTel backend).
Prompt/response *content* is opt-in in the semconv (privacy); set CAPTURE_CONTENT=0 to drop it.
"""
from __future__ import annotations

import json
import os
from typing import Sequence

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, SpanExporter, SpanExportResult

from .paths import OUT

TRACES = OUT / "traces.jsonl"
CAPTURE_CONTENT = os.environ.get("CAPTURE_CONTENT", "1") != "0"


class JsonlExporter(SpanExporter):
    def __init__(self, path=TRACES):
        self.path = path

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        with open(self.path, "a") as f:
            for s in spans:
                f.write(json.dumps({
                    "trace_id": f"{s.context.trace_id:032x}", "span_id": f"{s.context.span_id:016x}",
                    "parent_id": f"{s.parent.span_id:016x}" if s.parent else None, "name": s.name,
                    "start": s.start_time / 1e9, "end": s.end_time / 1e9,
                    "status": s.status.status_code.name, "attributes": dict(s.attributes or {}),
                    "events": [{"name": e.name, "attributes": dict(e.attributes or {})} for e in s.events],
                }) + "\n")
        return SpanExportResult.SUCCESS

    def shutdown(self):
        pass


_provider = None


def setup(service_name: str = "shopbot-workshop") -> trace.Tracer:
    global _provider
    if _provider is None:
        _provider = TracerProvider(resource=Resource.create({"service.name": service_name,
                                                              "openinference.project.name": service_name}))
        _provider.add_span_processor(SimpleSpanProcessor(JsonlExporter()))
        endpoint = os.environ.get("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
        if endpoint:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
            _provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, timeout=5)))
        trace.set_tracer_provider(_provider)
    return trace.get_tracer("shopbot")


def flush():
    if _provider:
        _provider.force_flush(10_000)


def content(value) -> str | None:
    """Return a string for a content attribute, or None when content capture is off."""
    if not CAPTURE_CONTENT:
        return None
    return value if isinstance(value, str) else json.dumps(value, default=str)[:20000]


def set_attrs(span, attrs: dict):
    for k, v in attrs.items():
        if v is not None:
            span.set_attribute(k, v)


def load_spans(path=TRACES) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
