FROM python:3.6.3-alpine3.6
LABEL author Mihai Dobre <mihai.dobre89@gmail.com>

COPY ./windopen /windopen
COPY ./requirements.txt /windopen

COPY ./ssl /tmp

RUN apk add --no-cache linux-headers
RUN apk add --no-cache gcc libgcc
RUN apk add --no-cache python3-dev
RUN apk add --no-cache uwsgi-python3
RUN apk add --no-cache curl
RUN apk add --no-cache musl-dev
RUN apk add --no-cache libffi libffi-dev openssl-dev

RUN pip install -r /windopen/requirements.txt

RUN mkdir /var/log/windopen
RUN rm -rf /windopen/windopen_starter/settings/settings_local.py
RUN touch /windopen/windopen_starter/settings/settings_local.py
WORKDIR /windopen

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
