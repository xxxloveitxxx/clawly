# OpenCLAW Docker Image
FROM python:3.10-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt if exists
# COPY requirements.txt .

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install OpenCLAW and its dependencies
RUN pip install --no-cache-dir openclaw

# Install JupyterLab for notebook support
RUN pip install --no-cache-dir jupyterlab

# Expose Jupyter port
EXPOSE 8888

# Default command - start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
