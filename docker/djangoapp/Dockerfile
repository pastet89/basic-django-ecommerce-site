FROM python:3.6-alpine

EXPOSE 8000

ARG working_dir

WORKDIR $working_dir

COPY . ./

RUN pip install -U pip

# Install dependencies

RUN apk add --update mariadb-dev python3-dev jpeg-dev

# Install build-dependencies
RUN apk add --update --virtual build-dependencies \
     alpine-sdk make gcc libxslt-dev \
     libxml2-dev libc-dev openssl-dev libffi-dev openssh \
     bash py3-lxml  py3-numpy cython py-ipaddr \
    && rm -rf /var/cache/apk/*

# Run pip install so that it skips the packages that are already installed
# from the Alpine Linux repos
RUN pip install $(grep -ivE "Cython|ipaddr|numpy|lxml" requirements.txt)

#Install Gunicorn
RUN pip install gunicorn

# Remove packages dependencies
RUN apk del build-dependencies
