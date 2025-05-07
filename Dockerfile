# Use an official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app/ .

# Set environment variables
ENV PORT=8051
ENV HOST=0.0.0.0

# Expose the port
EXPOSE 8051

# Run the application with the correct port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8051", "--proxy-headers", "--forwarded-allow-ips", "*", "--log-level", "debug"]
