FROM mtgupf/essentia:stretch-python2

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Use apt-get to install pip even though it's old, because it pulls in a bunch of dependencies
RUN apt-get update && apt-get install -y python-pip python-dev wget && rm -rf /var/lib/apt/lists*
RUN pip install --upgrade pip

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 && chmod +x /usr/local/bin/dumb-init

RUN mkdir /code && mkdir /code/src && mkdir /dataset
RUN mkdir /webroot && mkdir /webroot/images && mkdir /webroot/static
WORKDIR /code

COPY requirements.txt /code
RUN pip --no-cache-dir install -r requirements.txt

COPY dataset/ /dataset/
COPY images/ /webroot/images/
COPY static/ /webroot/static/
COPY index.html /webroot

COPY uwsgi.ini /code
COPY sawaaljawaab.py /code
COPY src/ /code/src/
