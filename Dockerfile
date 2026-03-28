FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install pandas pyyaml

ENTRYPOINT ["python", "run.py"]