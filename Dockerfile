# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .


# Run FastAPI app
CMD ["uvicorn", "entrypoint:application", "--host", "0.0.0.0", "--port", "9000"]