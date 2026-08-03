FROM python:3.11-slim

# Install system dependencies for PDF parsing
RUN apt-get update && apt-get install -y poppler-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY app/ /app/
COPY prompts/ /app/prompts/

# Build Vector DB from Hormozi books (if books exist)
# This is a no-op if hormozi_books/ is empty
COPY hormozi_books/ /app/hormozi_books/
COPY app/build_db.py /app/build_db.py
RUN if [ -n "$(ls -A /app/hormozi_books/*.pdf 2>/dev/null)" ]; then \
    python /app/build_db.py; \
    fi || true

# Create output directory for generated content
RUN mkdir -p /app/generated

# Set Python path
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

CMD ["python", "/app/executor.py"]
