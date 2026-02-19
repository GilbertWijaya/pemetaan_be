# FROM python:3.11-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:8000", "--workers", "2"]

# FROM python:3.11-slim
# WORKDIR /app
# ENV PYTHONPATH=/app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# EXPOSE 8000
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app", "--workers", "2"]

FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Copy dependencies dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode
COPY . .

# Expose port
EXPOSE 8000

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Jalankan entrypoint
ENTRYPOINT ["/entrypoint.sh"]
