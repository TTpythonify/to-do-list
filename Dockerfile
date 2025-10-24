FROM python:3.14

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]