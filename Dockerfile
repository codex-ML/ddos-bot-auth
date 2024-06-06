# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages
RUN apt-get update && apt-get install -y nmap

# Ensure the necessary scripts have execution permissions
RUN chmod +x /app/udp.py
RUN chmod +x /app/udpp.py
RUN chmod +x /app/bgmi
# Expose the ports the app will run on
EXPOSE 5000
EXPOSE 4040
EXPOSE 5900

# Run the application
CMD ["python", "main.py"]
