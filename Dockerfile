# Step 1 — Start from official Python image
# Think of this as: "use a machine that already has Python installed"

FROM python:3.12-slim

# Step 2 — Set working directory inside the container
# All commands after this run from /app folder inside container
WORKDIR /app

# Step 3 — Copy requirements first (for faster rebuilds)
# Docker caches this layer — if requirements don't change, skip reinstall
COPY requirements.txt .

# Step 4 — Install Python dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Step 5 — Copy your entire app into the container
COPY . .

# Step 6 — Tell Docker this container uses port 5000
EXPOSE 5000

# Step 7 — Command to run when container starts
CMD ["python", "app.py"]