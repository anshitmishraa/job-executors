# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to avoid buffering in Docker logs
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire project into the container
COPY . /app

# Expose the FastAPI port (default 8000)
EXPOSE 8000

# Command to run the FastAPI app with uvicorn, using reload for dev environment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
