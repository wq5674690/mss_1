FROM ubuntu:18.04
LABEL maintainer="mss"
ENV LANG C

RUN apt-get update \
  #&& apt-get upgrade \
  && apt-get install -y python3-pip python3-dev locales\
  && pip3 install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV LANG C.UTF-8  # 解决中文乱码
ENTRYPOINT ["python3"]
CMD ["app.py"]
#CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
