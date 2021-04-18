# syntax = docker/dockerfile:1.2
# ---- Base image ----------------------------------------------------------------------------------

FROM python:3.9 as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Dependencies that are shared across services ------------------------------------------------

FROM base AS dependencies

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

# ---- Copies application files --------------------------------------------------------------------

FROM dependencies AS build

WORKDIR /app
COPY . .

# --- Production image -----------------------------------------------------------------------------

FROM python:3.9-slim-buster AS release

WORKDIR /app

COPY --from=dependencies /root/.cache /root/.cache
COPY --from=build /app/ .

RUN pip install --upgrade pip setuptools wheel
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

RUN groupadd -r dataset_catalog && useradd -r -m -g dataset_catalog dataset_catalog
RUN chown -R dataset_catalog:dataset_catalog /app
USER dataset_catalog

EXPOSE 8000

ENTRYPOINT ["python", "main.py"]
