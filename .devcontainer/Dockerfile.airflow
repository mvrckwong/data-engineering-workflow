# Getting the base image.
FROM apache/airflow:2.10.5

# Copying the requirements.
COPY requirements.txt /opt/requirements.txt

# Upgrade to the latest pip and install python dependencies.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /opt/requirements.txt