FROM python:3.11-slim

WORKDIR /app

COPY inventory_manager.py .

# inventory.json lives in /data so a mounted volume keeps it outside the container
ENV INVENTORY_FILE=/data/inventory.json

CMD ["python", "-u", "inventory_manager.py"]
