FROM python:3.10.12-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]
