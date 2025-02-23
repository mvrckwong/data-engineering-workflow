# FROM python:3.9-slim

# WORKDIR /usr/src/app
# ENV DAGSTER_HOME=/usr/src/app

# RUN pip install dagster dagster-webserver dagit dagster-postgres SQLAlchemy==1.4.49 pandas pyarrow

# # Copy our code and workspace to /usr/src/app
# COPY dagster.yaml workspace.yaml .
# COPY etl ./etl
# COPY pyproject.toml .
# COPY setup.cfg .
# COPY setup.py .

# EXPOSE 3000

# CMD ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]



# Build stage
FROM python:3.11-slim as builder

WORKDIR /usr/src/app
ENV DAGSTER_HOME=/usr/src/app

# Copy only dependency files first
COPY pyproject.toml setup.cfg setup.py ./

# Install dependencies in a single layer with cleanup
RUN pip install --no-cache-dir dagster dagster-webserver dagit \
    dagster-postgres dagster-dbt SQLAlchemy==1.4.49 pandas pyarrow && \
    rm -rf /root/.cache/pip/*

# Final stage
FROM python:3.11-slim

WORKDIR /usr/src/app
ENV DAGSTER_HOME=/usr/src/app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application files
COPY dagster.yaml workspace.yaml ./
COPY etl ./etl