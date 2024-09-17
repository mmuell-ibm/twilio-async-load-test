# Twilio Load Test

## Project Overview

This project performs a load test using the Twilio API to simulate multiple concurrent phone calls. It uses a provided TwiML script in XML format to dictate the call's content and behavior. The setup includes a Docker environment to ensure consistent execution.

## Environment Variables

The project relies on several environment variables. Ensure these are set in your `.env` file:

- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID.
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token.
- `TWILIO_NUMBER`: The Twilio phone number to use for making calls.
- `TARGET_CALL_CENTER_NUMBER`: The target phone number for the calls.
- `CONCURRENT_CALLS`: The number of concurrent calls to initiate.
- `CALL_DELAY`: The delay (in seconds) between starting each call.
- `TWIML_SCRIPT_PATH`: The file path to the TwiML XML script that dictates the call's content.

## Dockerfile

The Dockerfile sets up a Python environment to run the load test script:

1. **Base Image**: Uses `python:3.9-slim` for a lightweight and stable environment.
2. **Requirements**: Copies `requirements.txt` and installs the necessary Python packages.
3. **Code**: Copies the project code into the container.
4. **Command**: Specifies the command to run the load test script.

## `load_test.py`

This script performs the following:

1. **Imports and Configuration**: Loads environment variables and sets up the Twilio client.
2. **`make_call` Function**: Asynchronously creates a call using the TwiML script.
3. **`load_test` Function**: Manages the creation of multiple concurrent calls with a staggered start.
4. **Execution**: Runs the `load_test` function using `asyncio`.

## FastAPI Application

The FastAPI application provides a web interface to manage and update the TwiML script and other settings:

1. **Read Form**: Displays a form to enter or update Twilio settings and the TwiML script.
2. **Update Settings**: Handles form submissions to update the TwiML script and other settings, saving the script to an XML file specified in the `.env` file.

## Requirements

- `twilio`: The Twilio Python library to interact with the Twilio API.
- `asyncio`: A library for asynchronous programming in Python.
- `fastapi`: For building the web interface.
- `uvicorn`: For serving the FastAPI application.

## Running the Project

To build and run the Docker container:

1. Build the Docker image:
    ```bash
    podman build -t twilio-load-test .
    ```

2. Run the Docker container with environment variables:
    ```bash
    podman run --env-file .env -p 8000:8000 --rm twilio-load-test
    ```

Alternatively, you can use the pre-built Docker container available on Quay.io:

- **Quay.io Docker Container**: `quay.io/mattmule/twilio-load`

  To pull and run the container directly from Quay.io:
    ```bash
    podman pull quay.io/mattmule/twilio-load:main
    podman run --env-file .env -p 8000:8000 --rm quay.io/mattmule/twilio-load:main
    ```

Ensure your `.env` file is properly configured with the necessary environment variables, including the path to the XML file for the TwiML script, before running the container.

## Notes

- Ensure that all environment variables are correctly set to avoid issues during execution.
- Adjust `CONCURRENT_CALLS` and `CALL_DELAY` as needed for your testing requirements.
- The TwiML script should be stored in an XML file, and the path to this file should be specified in the `TWIML_SCRIPT_PATH` environment variable.