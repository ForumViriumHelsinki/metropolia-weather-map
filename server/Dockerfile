FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app \
    MPLCONFIGDIR=/tmp/matplotlib

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with home directory
RUN addgroup --system --gid 1001 python && \
    adduser --system --uid 1001 --gid 1001 --home /home/python python

WORKDIR /app

# Change ownership of the working directory
RUN chown python:python /app

# Switch to non-root user
USER python

# Copy requirements and install Python dependencies
COPY --chown=python:python requirements.txt .
RUN pip install --user -r requirements.txt

# Add user's local bin to PATH
ENV PATH="/home/python/.local/bin:$PATH"

# Copy source code
COPY --chown=python:python . .

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]