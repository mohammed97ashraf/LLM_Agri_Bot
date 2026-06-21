FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create required directories
RUN mkdir -p uploads app/static/audio

EXPOSE 10000

CMD ["gunicorn", "app:create_app()", "--config", "gunicorn.conf.py", "--factory"]
