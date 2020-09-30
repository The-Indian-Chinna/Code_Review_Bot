# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Quart aiohttp gidgethub boto3 hypercorn requests emojis pycodestyle google-cloud-logging

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec hypercorn --bind :$PORT --workers 1 entry:app
