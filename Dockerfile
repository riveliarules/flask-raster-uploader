ARG BASE_IMAGE=python:3.9.8-slim-bullseye
FROM ${BASE_IMAGE}
RUN apt update; apt-get install -y libgdal-dev g++ --no-install-recommends && \
    apt-get clean -y

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV FLASK_APP=uploader.py
ENV FLASK_ENV=development

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /raster-uploader

ADD . /raster-uploader

EXPOSE 5000

CMD ["python","uploader.py"]
