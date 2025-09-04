FROM postgres:16.10

LABEL maintainer="Postgres image based on postgres:16.10 with pg_cron extension."

RUN apt-get update

RUN apt-get update \
      && apt-get install -y curl \
      && apt-get -y install postgresql-16-cron

RUN echo "shared_preload_libraries = 'pg_cron'" >> /usr/share/postgresql/postgresql.conf.sample \
    && echo "cron.database_name = 'finance_db_auth'" >> /usr/share/postgresql/postgresql.conf.sample
