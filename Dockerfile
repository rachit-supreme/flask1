# Use the official Python image from the Docker Hub
FROM python:3.12.3-bookworm
ENV PYTHONUNBUFFERED True
# Set the working directory in the container

ENV APP_HOME /back-end
WORKDIR /app
# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
