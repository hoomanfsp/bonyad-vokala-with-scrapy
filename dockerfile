FROM python:3.11-slim

# Set working directory
WORKDIR /app

COPY debian.sources /etc/apt/sources.list.d/debian.sources
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -i https://mirror-pypi.runflare.com/simple -r requirements.txt


# Copy project files
COPY . .

# Make the shell script executable
RUN chmod +x run_spiders.sh

# Create directories for logs and data
RUN mkdir -p logs data

# Run the spider script
CMD ["./run_spiders.sh"]