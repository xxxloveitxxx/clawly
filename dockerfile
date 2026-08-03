FROM python:3.11-slim

# Install system dependencies for PDF parsing
RUN apt-get update && apt-get install -y poppler-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy books and build the Vector DB during Docker build
COPY hormozi_books/ /app/hormozi_books/
COPY app/build_db.py /app/build_db.py
RUN python /app/build_db.py

# Copy the rest of the application
COPY app/ /app/
COPY prompts/ /app/prompts/

CMD ["python", "/app/executor.py"]
