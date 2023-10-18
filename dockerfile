FROM tiangolo/uvicorn-gunicorn:python3.10

RUN mkdir /code

WORKDIR /code

EXPOSE 8000:8000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000
