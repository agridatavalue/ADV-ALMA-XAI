FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel

# First install only the NVIDIA packages
RUN grep '^nvidia-' requirements.txt > /tmp/req_nvidia.txt && \
    pip install --no-cache-dir -r /tmp/req_nvidia.txt && \
    rm /tmp/req_nvidia.txt

# Then install everything else
RUN grep -v '^nvidia-' requirements.txt > /tmp/req_other.txt && \
    pip install --no-cache-dir -r /tmp/req_other.txt && \
    rm /tmp/req_other.txt

# User management for security
RUN addgroup --system app \
    && adduser --system --no-create-home --group app

# install cv2 dependencies
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy application files
COPY . .

# Set permissions
RUN chown -R app:app /app && chmod -R 755 /app

# Ensure entrypoint script is executable
RUN chmod +x "./entrypoint.sh"

# Use non-root user
USER app

VOLUME ["/app/data_temp"]
RUN mkdir -p /app/data_temp && chown -R app:app /app/data_temp

EXPOSE 8000 8505
ENTRYPOINT ["./entrypoint.sh"]
