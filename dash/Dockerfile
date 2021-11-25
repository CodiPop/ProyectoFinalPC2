FROM python:3.9.9-slim-buster
WORKDIR /src
COPY ./src/requirements.txt requirements.txt
RUN ["pip","install","-r","requirements.txt"]
CMD ["python3","./main.py"]
EXPOSE 8050