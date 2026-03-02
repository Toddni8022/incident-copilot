FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package source and install it
COPY src/ ./src/
COPY pyproject.toml setup.py ./
RUN pip install --no-cache-dir -e .

# Create output directory
RUN mkdir -p output

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit using the packaged app
CMD ["streamlit", "run", "src/incident_copilot/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
