FROM python:3.9
RUN mkdir -p /home/adv_xai
ENV ENV_HOME /home/adv_xai
WORKDIR $ENV_HOME

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    zlib1g-dev \
    libjpeg-dev \
 && pip install --upgrade -r requirements.txt \
 && apt-get autoremove -y \
 && apt-get autoclean -y
