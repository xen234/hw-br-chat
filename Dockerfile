FROM python:3.8

WORKDIR /mafia

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port
EXPOSE 50010

# Run the application
CMD [ "python", "server_main.py" ]