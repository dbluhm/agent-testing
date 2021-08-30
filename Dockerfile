FROM python:3.9

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.RESTful_API:app", "--host", "0.0.0.0", "--port", "80"]