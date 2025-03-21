FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .
RUN chmod +x "./entrypoint.sh"

EXPOSE 8000 8505
ENTRYPOINT ["./entrypoint.sh"]
