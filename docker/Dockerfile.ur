FROM mambaorg/micromamba:1.5.8
WORKDIR /app

COPY requirements/c_urduhack.yml /tmp/environment.yml

USER root

RUN micromamba create -y -n urduhackcsv -f /tmp/environment.yml && micromamba clean -a -y

ENV MAMBA_DOCKERFILE_ACTIVATE=1

RUN micromamba run -n urduhackcsv urduhack download

#FROM python:3.8-slim
#WORKDIR /app
#COPY requirements/d_ur.txt /app/requirements.txt
#RUN pip install --no-cache-dir -r /app/requirements.txt
#RUN urduhack download
