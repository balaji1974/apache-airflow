ARG AIRFLOW_IMAGE_NAME=apache/airflow:3.1.5
FROM ${AIRFLOW_IMAGE_NAME}

USER airflow
RUN pip install --no-cache-dir scikit-learn
RUN pip install --no-cache-dir matplotlib
RUN pip install --no-cache-dir apache-airflow-providers-postgres

