FROM python:3.11

# Set the working directory within the docker container to /scrobbler
WORKDIR /scrobbler

# Install nano
RUN apt-get update && apt-get install -y nano

COPY scrobbler /scrobbler

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run start.sh after the container starts
CMD ["sh", "/scrobbler/start.sh"]