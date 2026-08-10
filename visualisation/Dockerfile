FROM python:3.10 

# Create application directory
RUN mkdir  /visualisation
# Set the working directory
WORKDIR /visualisation
# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .
# Expose ports
EXPOSE 8004

#RUN  docker-compose run --remove-orphans web django-admin startproject siteweb .

