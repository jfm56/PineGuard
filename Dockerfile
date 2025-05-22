# ── Stage 1: Build frontend (Node.js / Next.js) ─────────────
FROM node:20 AS frontend-builder
WORKDIR /app

# 1) Install your JS deps
COPY package*.json ./
RUN npm install --legacy-peer-deps

# 2) Copy your env file so Next.js picks it up at build-time
#    Make sure .dockerignore does NOT exclude .env.local
COPY .env.local .env.local

# 3) Copy the rest of your source and build
COPY . .
RUN npm run build


# ── Stage 2: Build backend (Python) ─────────────────────────
FROM continuumio/miniconda3 AS backend-builder
WORKDIR /app

# 1) Setup conda environment with geospatial & app deps
RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install -y python=3.11 fastapi uvicorn slowapi numpy pandas geopandas shapely rasterio && \
    conda clean -afy

# 2) Debug
RUN conda list && which gdal-config && gdal-config --version

# 3) Copy your backend code
COPY . .


# ── Stage 3: Production image ───────────────────────────────
FROM continuumio/miniconda3 AS production
WORKDIR /app

# 1) Install Node.js and curl (Debian)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 2) Copy conda environment from builder
COPY --from=backend-builder /opt/conda /opt/conda
ENV PATH=/opt/conda/bin:$PATH

# 3) Copy backend code
COPY --from=backend-builder /app /app

# 4) Copy frontend build output & deps
COPY --from=frontend-builder /app/.next      ./.next
COPY --from=frontend-builder /app/public     ./public
COPY --from=frontend-builder /app/node_modules ./node_modules
COPY --from=frontend-builder /app/package.json   ./package.json
COPY --from=frontend-builder /app/next.config.js ./next.config.js

# 5) Copy your env file so both Next.js and any dotenv-based Python code see it
COPY .env.local .env.local

# 6) Environment defaults (if you have any)
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    DATA_DIR=/app/data \
    MODEL_DIR=/app/models \
    LOG_DIR=/app/logs

# 7) Drop to non-root user
RUN useradd -m -r -s /bin/bash pineguard && \
    chown -R pineguard:pineguard /app
USER pineguard

# 8) Ports & healthcheck
EXPOSE 3000 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# 9) Start both backend + Next.js server
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080 & npm run start -- --port 3000"]
