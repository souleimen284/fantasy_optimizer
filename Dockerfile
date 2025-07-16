# Use Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install build essentials needed for cvxpy and numpy
RUN apt-get update && apt-get install -y build-essential

# Copy requirements file first (for caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy the rest of your app code
COPY . .

# Command to run your app using gunicorn
CMD ["gunicorn", "app:app"]
