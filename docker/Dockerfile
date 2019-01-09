FROM python:3.6.3-alpine3.6
LABEL author Mihai Dobre <mihai.dobre89@gmail.com>

COPY ./windopen /windopen
COPY ./requirements.txt /windopen

RUN apk add --no-cache gcc libgcc
RUN apk add --no-cache python3-dev
RUN apk add --no-cache uwsgi-python3

RUN pip install -r /windopen/requirements.txt

WORKDIR /windopen

ENTRYPOINT ["./manage.py", "runserver", "0.0.0.0:8000"]
