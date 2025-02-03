# Use an official Python runtime as a parent image
FROM python:3.12.8-slim

# Set the working directory in the container
WORKDIR /app

# Install Pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies using Pipenv
RUN pipenv install --dev --deploy
RUN pipenv install python-dotenv

# Copy the rest of the application code
COPY . .

# Run the bot inside the Pipenv environment
CMD ["pipenv", "run", "python", "main.py"]