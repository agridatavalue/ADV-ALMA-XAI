FROM ubuntu:22.04
RUN mkdir -p /home/adv_xai
ENV ENV_HOME /home/adv_xai
WORKDIR $ENV_HOME
 
COPY constants.py $ENV_HOME/constants.py
COPY xai_functions.py $ENV_HOME/xai_functions.py
COPY xaibuilder.py $ENV_HOME/xaibuilder.py
COPY environment.yml $ENV_HOME/environment.yml
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl

#Install Miniconda
RUN mkdir -p ~/miniconda3
 
RUN curl -LO "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda
#Create environment
RUN apt-get update
RUN apt install build-essential -y
RUN apt-get install libjpeg-dev zlib1g-dev -y
RUN pip install --upgrade pip setuptools wheel
RUN conda env create -f environment.yml
RUN conda init
ENTRYPOINT ["bash", "-c", "conda run -n XAI_AgriDataValue uvicorn xaibuilder:app --reload --host=0.0.0.0 --port=8000"]