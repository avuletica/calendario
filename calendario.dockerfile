FROM python:3.8-alpine

WORKDIR /app
COPY . .

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --upgrade pip && pip install -r requirments.txt && \
    apk --purge del .build-deps

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "run.py"]