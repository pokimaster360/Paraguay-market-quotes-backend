# Market Quotes Backend

Backend API for the Market Quotes application.

## Requirements

- bs4  - 0.0.2
- fastapi  - 0.141.1
- pathlib  - 1.0.1
- requests  - 2.34.2
- uvicorn  - 0.53.0

## Install

```bash
uv sync https://github.com/pokimaster360/Cotization-Backend
```

## Run API
```bash
uv run uvicorn src.api.main:app --reload
```

## Update database manually
```bash
uv run python scripts/manual_update.py
```