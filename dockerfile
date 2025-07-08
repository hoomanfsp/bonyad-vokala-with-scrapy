# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# If you don't have a requirements.txt, create one with `Scrapy` and any other dependencies
RUN pip install --no-cache-dir scrapy

# Install any project-specific dependencies (if any, e.g., other libraries your spiders use)
# For example, if you use pandas or numpy, add them to requirements.txt and install here.

# Command to run the spiders (this will be overridden by docker-compose)
CMD ["bash", "run_spiders.sh"]