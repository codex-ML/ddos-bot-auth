# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y nmap
# Copy your pre-compiled C binary into the container
COPY udp.py /app/udp.py
COPY udpp.py /app/udpp.py
# Make the binary executable
RUN chmod +x /app/udpp.py
RUN chmod +x /app/udp.py
# Run python script when the container launches
CMD ["python", "main.py"]


