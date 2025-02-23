# Use a base image with both Python and Node.js
FROM nikolaik/python-nodejs:python3.9-nodejs18-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .
COPY package.json package-lock.json ./

# Install Python and Node.js dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    npm install && \
    npm install -g serve  # For serving static files if needed

# Copy entire project
COPY . .

# Build React frontend
RUN npm run railway-build

# Expose port (Railway will override with $PORT)
EXPOSE 5000

# Start Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]