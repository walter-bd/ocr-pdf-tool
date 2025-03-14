# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app

COPY ./requirements.txt /app

RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install uv
RUN uv pip install --system -r requirements.txt


RUN apt-get update && apt-get install poppler-utils ffmpeg libsm6 libxext6 -y

COPY . /app


# Expose port 80 for the Flask app

EXPOSE 80

# Run the command to start the Flask app when the container launches
CMD ["sanic", "app", "--port", "5000", "--host", "0.0.0.0"]
