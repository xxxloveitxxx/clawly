# Jupyter Docker Image
FROM python:3.10-slim

WORKDIR /workspace

# Install JupyterLab
RUN pip install --no-cache-dir jupyterlab

# Expose Jupyter port
EXPOSE 8888

# Default command - start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
