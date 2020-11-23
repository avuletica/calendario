FROM python:3.8-alpine

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install -r requirments.txt

ENTRYPOINT ["python", "run.py"]