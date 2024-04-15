FROM registry.git.agridatavalue.eu/agridatavalue/platform-integration/xai-fulfilment:base
RUN mkdir -p /home/adv_xai
ENV ENV_HOME /home/adv_xai
WORKDIR $ENV_HOME

COPY requirements.txt $ENV_HOME/requirements.txt
RUN pip install -r requirements.txt


COPY constants.py $ENV_HOME/constants.py
COPY xai_functions.py $ENV_HOME/xai_functions.py
COPY xai_builder.py $ENV_HOME/xai_builder.py
COPY xai_methods.py $ENV_HOME/xai_methods.py

ENTRYPOINT ["uvicorn", "xai_builder:app", "--reload", "--host=0.0.0.0", "--port=8000"]