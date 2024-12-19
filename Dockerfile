FROM python:3.12.5

# Set the working directory inside the container
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install any dependencies (including Flask)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000, the default port for Flask
EXPOSE 5000

# Set the command to run the Flask app when the container starts
CMD ["flask run"]
