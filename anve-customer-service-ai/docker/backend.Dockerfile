FROM python:3.9-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ backend/

# Set environment variables
ENV PYTHONPATH=/app
ENV MODULE_NAME=backend.app.main
ENV VARIABLE_NAME=app
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 