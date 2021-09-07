FROM python:3.9

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./agent-testing /agent_testing

CMD ["uvicorn", "agent_testing.RESTful_API:app", "--host", "0.0.0.0", "--port", "80"]
