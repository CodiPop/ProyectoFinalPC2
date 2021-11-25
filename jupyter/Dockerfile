FROM jupyter/minimal-notebook:latest
WORKDIR /src
COPY ./src/requirements.txt requirements.txt
RUN ["pip3","install","-r","requirements.txt"]
CMD ["jupyter","notebook","--allow-root","--no-browser","--ip=0.0.0.0","--NotebookApp.token=''", "--NotebookApp.password=''"]
EXPOSE 8888 8051
 
