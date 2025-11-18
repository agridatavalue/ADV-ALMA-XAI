FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir nvidia-cublas-cu12==12.4.5.8 \
    && pip install --no-cache-dir YOLOv8-Explainer==0.0.5 \
    && pip install --no-cache-dir nvidia-cuda-cupti-cu12==12.4.127 \
    && pip install --no-cache-dir nvidia-cuda-nvrtc-cu12==12.4.127 \
    && pip install --no-cache-dir nvidia-cuda-runtime-cu12==12.4.127 \
    && pip install --no-cache-dir nvidia-cudnn-cu12==9.1.0.70 \
    && pip install --no-cache-dir nvidia-cufft-cu12==11.2.1.3 \
    && pip install --no-cache-dir nvidia-curand-cu12==10.3.5.147 \
    && pip install --no-cache-dir nvidia-cusolver-cu12==11.6.1.9 \
    && pip install --no-cache-dir nvidia-cusparse-cu12==12.3.1.170 \
    && pip install --no-cache-dir nvidia-cusparselt-cu12==0.6.2 \
    && pip install --no-cache-dir nvidia-nccl-cu12==2.21.5 \
    && pip install --no-cache-dir nvidia-nvjitlink-cu12==12.4.127 \
    && pip install --no-cache-dir nvidia-nvtx-cu12==12.4.127

RUN pip install --no-cache-dir -r requirements.txt

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
