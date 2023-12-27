FROM python:3.11

# Set the working directory within the docker container to /scrobbler
WORKDIR /scrobbler

# Copy the current directory contents into the container at /scrobbler
COPY . /scrobbler

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Entrypoint script to perform setup after container starts
COPY entrypoint.sh /scrobbler/entrypoint.sh
RUN chmod +x /scrobbler/entrypoint.sh

# Run
CMD ["/scrobbler/entrypoint.sh"]
