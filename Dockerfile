# Use an official Python runtime as a parent image
FROM python:3.8

# Install inotify-tools for the inotifywait command
RUN apt-get update && apt-get install -y inotify-tools

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app 

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make sure the script is executable
RUN chmod +x /app/monitor-watchdog-windows.sh

# Run app.py when the container launches
ENTRYPOINT ["/app/docker-start.sh"]