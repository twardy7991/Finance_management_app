FROM continuumio/miniconda3

WORKDIR /app

COPY enviroment.yaml .

RUN conda env create -f enviroment.yaml python=3.13

# Make sure the environment is activated when container runs
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

COPY ./app ./app

EXPOSE 8000

CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]