# I like this docker base image for its stability/ease of use
FROM python:3.9-slim

# Copy the current requirements into the container
COPY ./requirements.txt ./requirements.txt

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# I Hate having to reinstall libraries after code changes
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Start the UI
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000"]