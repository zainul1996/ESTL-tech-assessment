FROM postgres

ENV POSTGRES_PASSWORD postgres

COPY tables.sql /docker-entrypoint-initdb.d/