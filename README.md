# FastAPI Air-Gap UI

FastAPI app that serves Swagger UI, ReDoc, and the favicon from local files. The
documentation pages do not load their UI bundles or styling from a CDN.

## Project structure

```text
.
├── main.py
├── requirements.txt
└── static/
    ├── favicon.ico
    ├── favicon.png
    ├── redoc.standalone.js
    ├── redocly-logo.svg
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

## Install and run

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for Swagger UI or
`http://127.0.0.1:8000/redoc` for ReDoc. The OpenAPI schema is served at
`/openapi.json`; replace it with your API routes as needed. The `/health`
endpoint returns `{"status":"ok"}` while the application is responding.

## OpenTelemetry

OpenTelemetry is disabled by default. Set `OTEL_ENABLED=true` to instrument
incoming FastAPI requests for traces and HTTP metrics and export them over
OTLP/HTTP. When enabled, the exporters send to an OpenTelemetry Collector at
`http://localhost:4318` by default. Set the standard
`OTEL_EXPORTER_OTLP_ENDPOINT` environment variable to use another collector;
the exporters also support the standard signal-specific endpoint, headers, and
timeout environment variables. Set `OTEL_SERVICE_NAME` to override the default
service name, `fastapi-airgap-ui`.

Set `OTEL_ENABLED=false` to keep telemetry disabled. When enabled, telemetry
export is asynchronous and does not make API requests depend on the collector
being available. Run a collector with an OTLP/HTTP receiver when you want to
receive telemetry. The docs UI itself remains served from local assets.

To customize branding, replace `static/favicon.png` with your own favicon.
Keep the other files in `static/` available when deploying, and update the
`/static/...` URLs in `main.py` if you change their names or mount path.

## Vendored documentation assets

The browser assets are checked into `static/` so the docs can be viewed without
an internet connection:

- Swagger UI: `swagger-ui-dist` 5.33.0, from
  <https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/>
- ReDoc: `redoc` 2.5.4, from
  <https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js>
- ReDoc's logo is stored locally as `redocly-logo.svg`; its URL in the bundle
  points to `/static/redocly-logo.svg` instead of the upstream CDN.
- The ReDoc HTML disables FastAPI's default Google Fonts stylesheet.
- Swagger UI's online spec validator is disabled.
- Favicon: FastAPI's default favicon, from
  <https://fastapi.tiangolo.com/img/favicon.png>

Use these pages with a locally reachable FastAPI server. If your OpenAPI schema
references external resources, those resources must also be made available
locally for a fully air-gapped deployment.
