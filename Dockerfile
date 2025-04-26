FROM python:3.9-slim

WORKDIR /app

# Set Python path to include /app and /app/backend
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/backend"

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]