FROM python:3.11-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    libz-dev \
    curl \
    git \
    python3-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python packages
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Make run script executable
RUN chmod +x run_spiders.sh

# Run the spiders
CMD ["sh", "run_spiders.sh"]
