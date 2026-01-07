# Use Python 3.11 as base image
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Command to run the app
# FastAPI example:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
