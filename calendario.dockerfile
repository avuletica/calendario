FROM python:3.8-alpine

WORKDIR /app
COPY . .


# libffi-dev (for python-jose[cryptography])
# everything else is for psycopg2

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev && \
    pip install --upgrade pip && pip install -r requirments.txt && \
    apk --purge del .build-deps

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "run.py"]