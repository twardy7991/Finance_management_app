FROM continuumio/miniconda3

WORKDIR /server

COPY environment.yml .

RUN conda env create --file environment.yml

COPY server/. .

CMD ["bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate finance_app_compute_server && uvicorn main:app --host 0.0.0.0 --port 8000"]