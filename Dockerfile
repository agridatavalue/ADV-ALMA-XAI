FROM continuumio/miniconda3:23.10.0-1

# Workdir.
ENV HOME=/home/adv_xai
WORKDIR $HOME

# Copy requirements.
COPY requirements.txt $HOME

# Create environment
RUN pip3 install -r requirements.txt \
 && pip3 install waitress \
 && addgroup --system app \
 && adduser --system --no-create-home --group app \
 && chown -R app:app $HOME && chmod -R 755 $HOME \
 && chown -R app:app $HOME

COPY . $HOME
RUN chmod +x "./entrypoint.sh"

USER app

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]