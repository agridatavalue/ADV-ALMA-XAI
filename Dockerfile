FROM continuumio/miniconda3

ENV HOME=/home/adv_xai
RUN mkdir $HOME
WORKDIR $HOME

RUN addgroup --system app && adduser --system --no-create-home --group app
RUN chown -R app:app /home/app && chmod -R 755 /home/app

COPY . $HOME

#Chown all the files to the app user
RUN chown -R app:app $HOME

# Create environment
RUN pip3 install -r requirements.txt
RUN pip3 install waitress

# ENV VAR LISTS


#Change to the app user
USER app

RUN chmod +x "./entrypoint.sh"
ENTRYPOINT ["./entrypoint.sh"]