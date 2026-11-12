FROM python:3.11-slim

WORKDIR /app

COPY *.py ./
COPY inventory.json ./

# When run with the volume mount (-v "${PWD}:/app"), the local .py files
# and inventory.json replace these copies, so edits need no rebuild.
CMD ["python", "-u", "main.py"]
