# FastAPI Air-Gap UI

FastAPI app that serves Swagger UI, ReDoc, and the favicon from local files. The
documentation pages do not load their UI bundles or styling from a CDN.

## Project structure

```text
.
├── main.py
├── requirements.txt
└── static/
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
`/openapi.json`; replace it with your API routes as needed.

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
