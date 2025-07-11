# Use official Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy everything from your local folder into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose Flask default port
EXPOSE 5000

# Start the Flask app
CMD ["python", "app/app.py"]
