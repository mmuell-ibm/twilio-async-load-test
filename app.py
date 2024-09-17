from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import os
from load_test import load_test

app = FastAPI()


# Helper function to read XML file
def read_xml_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


@app.get("/", response_class=HTMLResponse)
async def read_form():
    # Get the XML file path from environment variable
    twiml_script_path = os.getenv("TWIML_SCRIPT_PATH", "")
    if os.path.isfile(twiml_script_path):
        twiml_script = read_xml_file(twiml_script_path)
    else:
        twiml_script = ""

    settings = {
        "TWILIO_ACCOUNT_SID": os.environ.get("TWILIO_ACCOUNT_SID", ""),
        "TWILIO_AUTH_TOKEN": os.environ.get("TWILIO_AUTH_TOKEN", ""),
        "TWILIO_NUMBER": os.environ.get("TWILIO_NUMBER", ""),
        "TARGET_CALL_CENTER_NUMBER": os.environ.get("TARGET_CALL_CENTER_NUMBER", ""),
        "CONCURRENT_CALLS": os.environ.get("CONCURRENT_CALLS", ""),
        "CALL_DELAY": os.environ.get("CALL_DELAY", ""),
        "TWIML_SCRIPT": twiml_script,  # XML content from file
    }

    html_content = f"""
    <html>
        <body>
            <form action="/update" method="post">
                <label for="twilio_account_sid">Twilio Account SID:</label>
                <input type="text" id="twilio_account_sid" name="twilio_account_sid" value="{settings['TWILIO_ACCOUNT_SID']}"><br><br>
                <label for="twilio_auth_token">Twilio Auth Token:</label>
                <input type="text" id="twilio_auth_token" name="twilio_auth_token" value="{settings['TWILIO_AUTH_TOKEN']}"><br><br>
                <label for="twilio_number">Twilio Number:</label>
                <input type="text" id="twilio_number" name="twilio_number" value="{settings['TWILIO_NUMBER']}"><br><br>
                <label for="target_call_center_number">Target Call Center Number:</label>
                <input type="text" id="target_call_center_number" name="target_call_center_number" value="{settings['TARGET_CALL_CENTER_NUMBER']}"><br><br>
                <label for="concurrent_calls">Concurrent Calls:</label>
                <input type="number" id="concurrent_calls" name="concurrent_calls" value="{settings['CONCURRENT_CALLS']}"><br><br>
                <label for="call_delay">Call Delay:</label>
                <input type="number" step="any" id="call_delay" name="call_delay" value="{settings['CALL_DELAY']}"><br><br>
                <label for="twiml_script">Twiml Script:</label><br>
                <textarea id="twiml_script" name="twiml_script" rows="10" cols="50">{settings['TWIML_SCRIPT']}</textarea><br><br>
                <input type="submit" value="Run">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/update")
async def update_settings(
    twilio_account_sid: str = Form(...),
    twilio_auth_token: str = Form(...),
    twilio_number: str = Form(...),
    target_call_center_number: str = Form(...),
    concurrent_calls: int = Form(...),
    call_delay: float = Form(...),
    twiml_script: str = Form(...),
):

    # Call the load_test function with parameters directly
    await load_test(
        account_sid=twilio_account_sid,
        auth_token=twilio_auth_token,
        twilio_number=twilio_number,
        target_number=target_call_center_number,
        script=twiml_script,
        concurrent_calls=concurrent_calls,
        call_delay=call_delay,
    )
    return {"message": "Load test initiated with the provided settings"}
