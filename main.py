import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).parent / "static"
otel_enabled_value = os.getenv("OTEL_ENABLED", "false").strip().lower()
if otel_enabled_value not in {"true", "false"}:
    raise ValueError("OTEL_ENABLED must be either 'true' or 'false'")
OTEL_ENABLED = otel_enabled_value == "true"

if OTEL_ENABLED:
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
        OTLPMetricExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter,
    )
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.metrics import set_meter_provider
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.trace import set_tracer_provider

    resource = Resource.create(
        {"service.name": os.getenv("OTEL_SERVICE_NAME", "fastapi-airgap-ui")}
    )

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    set_tracer_provider(tracer_provider)

    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[
            PeriodicExportingMetricReader(OTLPMetricExporter()),
        ],
    )
    set_meter_provider(meter_provider)

app = FastAPI(
    title="FastAPI Air-Gapped API",
    docs_url=None,
    redoc_url=None,
)

if OTEL_ENABLED:
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=tracer_provider,
        meter_provider=meter_provider,
    )

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(
        STATIC_DIR / "favicon.ico",
        media_type="image/vnd.microsoft.icon",
    )


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.png",
        swagger_ui_parameters={"validatorUrl": None},
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.png",
        with_google_fonts=False,
    )


@app.get("/", tags=["status"])
async def root():
    return {"message": "FastAPI is running"}
