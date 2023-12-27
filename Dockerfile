FROM python:3.11

# Set the working directory within the docker container to /scrobbler
WORKDIR /scrobbler

COPY scrobbler /scrobbler

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Check if /env/setup_done exists
RUN if [ -e /env/setup_done ]; then \
    echo "Setup already done. Running."; \
    CMD ["python", "scrobbler.py"] \
else \
    echo "Setup not done."; \
    CMD [] \
fi
