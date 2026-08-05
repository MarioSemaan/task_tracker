# ---- Builder stage: install dependencies into a venv ----
FROM python:3.11-slim AS builder

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Runtime stage: copy only the venv + app code, no build tools ----
FROM python:3.11-slim AS runtime

# Create a non-root user
RUN useradd -m -s /bin/bash app

# Bring in the pre-built dependency venv from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /home/app

# Copy only what the running app needs (see .dockerignore for exclusions)
COPY app/ ./app/
COPY frontend/ ./frontend/

RUN chown -R app:app /home/app
USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
