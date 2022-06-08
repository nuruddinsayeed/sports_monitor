FROM python:3.10.5

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "run.py"]