FROM python:3.11-slim

WORKDIR /app

# Copy the source, the tests folder and the data files (products.csv,
# inventory.json). .dockerignore keeps screenshots, documents and caches out.
COPY . .

# When run with the volume mount (-v "${PWD}:/app"), the local files replace
# these copies, so edits need no rebuild.
CMD ["python", "-u", "main.py"]
