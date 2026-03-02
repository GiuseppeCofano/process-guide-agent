# ---------- Build stage ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir --upgrade pip

# Copy project files
COPY pyproject.toml ./
COPY process_guide_agent/ ./process_guide_agent/
COPY sample_process.docx ./

# Install the package and its dependencies
RUN pip install --no-cache-dir .

# ---------- Runtime stage ----------
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=builder /app /app

# Cloud Run sets PORT env var (default 8080)
ENV PORT=8080

# Use Vertex AI on GCP (authenticates via service account, no API key needed)
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE

# Default process document
ENV PROCESS_DOCUMENT_PATH=sample_process.docx

EXPOSE ${PORT}

# Start the ADK API server
CMD adk api_server --port ${PORT} process_guide_agent
