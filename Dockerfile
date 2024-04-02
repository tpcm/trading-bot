# Use the official Python base image
FROM python:3.12-slim
# FROM ubuntu:latest

ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
ENV OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://otel-collector:4317
ENV OTEL_SERVICE_NAME=my-fast-api

# Set the working directory inside the container
WORKDIR /app

# RUN apt-get update
# RUN apt-get install -y python3-pip
# RUN apt-get install -y python3


# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY ./trading_controller ./trading_controller
COPY ./trading_dao ./trading_dao
COPY ./trading_service ./trading_service
COPY ./trades_db ./trades_db
COPY ./.env ./.env

# Expose the port on which the application will run
EXPOSE 8080 4317

# Run the FastAPI application using uvicorn server
CMD ["opentelemetry-instrument", "uvicorn", "trading_controller.trade_control:app", "--host", "0.0.0.0", "--port", "8080"]

# uvicorn trading_controller.trade_control:app --host 0.0.0.0 --port 8080