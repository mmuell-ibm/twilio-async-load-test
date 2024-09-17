# I like this docker base image for its stability/ease of use
FROM python:3.9-slim

# Copy the current requirements into the container
COPY ./requirements.txt ./requirements.txt

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# I Hate having to reinstall libraries after code changes
COPY . .

# Run the load test script
CMD ["python", "load_test.py"]