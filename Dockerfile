# Use Python 3.11 slim base image
FROM python:3.11-slim

# Install build essentials needed for cvxpy and numpy, plus node and npm to build React
RUN apt-get update && apt-get install -y build-essential curl

# Install Node.js (v18) and npm (adjust version if needed)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs

# Set working directory for backend
WORKDIR /app

# Copy backend requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy backend code except frontend folder
COPY . .

# Build React frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Move React build files to backend static folder
RUN mkdir -p /app/static
RUN cp -r /app/frontend/build/* /app/static/

# Set working directory back to backend root
WORKDIR /app

# Expose port if needed (default Flask 8000 or your backend port)
EXPOSE 8000

# Run gunicorn to serve Flask backend (make sure Flask serves static files from /app/static)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
