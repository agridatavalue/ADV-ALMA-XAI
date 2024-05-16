FROM continuumio/miniconda3

ENV HOME=/home/app
RUN mkdir $HOME
WORKDIR $HOME

RUN addgroup --system app && adduser --system --no-create-home --group app
RUN chown -R app:app /home/app && chmod -R 755 /home/app

COPY . $HOME

#Chown all the files to the app user
RUN chown -R app:app $HOME

# Create conda env from environment.yml
ADD ./environment.yml ./environment.yml
RUN chmod 777 ./environment.yml
RUN conda env create -f ./environment.yml

# ENV VAR LISTS

RUN pip3 install waitress


#Change to the app user
USER app

RUN chmod +x "./entrypoint.sh"
ENTRYPOINT ["./entrypoint.sh"]