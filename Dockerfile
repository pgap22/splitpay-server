# Use the official Ubuntu image as the base image
FROM ubuntu:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the current directory to the container's /app directory
COPY . /app

# Update and upgrade the package list
RUN apt update -y && apt upgrade -y

# Install necessary packages
RUN apt install -y git python3 python3-pip pipx

# Configure pip to avoid breaking system packages
RUN pip config set global.break-system-packages true

RUN bash
# Install packages using pipx
RUN pipx install prisma
RUN pipx install flask
RUN pipx install waitress

# Ensure that the pipx-installed packages' executables are in PATH
RUN pipx ensurepath

# Install Python packages listed in requirements.txt
RUN pip install --user -r requirements.txt

# Make the start.sh script executable
RUN chmod +x ./start.sh

RUN export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.local/bin'
EXPOSE 8000
# Set the default command to run when the container starts
CMD ["bash", "./start.sh"]
