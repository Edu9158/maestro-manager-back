# 1. Using the base image of Python 3.14 slim
FROM python:3.14-rc-slim

# 2. Define the working directory inside the container
WORKDIR /app

# 3. Set environment variables to prevent Python from writing .pyc files and to ensure output is sent straight to the terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Install system dependencies that may be required for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy only the requirements.txt first to take advantage of Docker's caching
COPY requirements.txt .

# 6. Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the entire project content into the container
COPY . .

# 8. Expose the port your application uses (e.g., 8000, 5000, or 8080)
EXPOSE 8000

# 9. Command to run the application
CMD ["python", "app.py"]