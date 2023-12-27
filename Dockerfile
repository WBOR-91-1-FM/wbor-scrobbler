FROM python:3.11

# Set the working directory within the docker container to /scrobbler
WORKDIR /scrobbler

COPY scrobbler /scrobbler

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Check if /env/setup_done exists
CMD if [ -e /env/setup_done ]; then \
    echo "Starting scrobbler." && python scrobbler.py; \
else \
    echo "Setup needs to be completed." && exit 1; \
fi
