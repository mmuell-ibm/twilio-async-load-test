import os
import asyncio
from twilio.rest import Client
from typing import List

# Twilio credentials
account_sid: str = os.environ.get("TWILIO_ACCOUNT_SID", "")
auth_token: str = os.environ.get("TWILIO_AUTH_TOKEN", "")
twilio_number: str = os.environ.get("TWILIO_NUMBER", "")
target_number: str = os.environ.get("TARGET_CALL_CENTER_NUMBER", "")
script: str = os.environ.get("TWIML_SCRIPT", "")
concurrent_calls: int = int(os.environ.get("CONCURRENT_CALLS", 1))
call_delay: float = float(os.environ.get("CALL_DELAY", 1))

client: Client = Client(account_sid=account_sid, password=auth_token)


# Asynchronous function to make a call with a specific twiml file
async def make_call() -> None:
    await asyncio.to_thread(
        client.calls.create,
        twiml=script,
        to=target_number,
        from_=twilio_number,
        record=True,
    )


# Asynchronous function to run concurrent calls with a staggered start
async def load_test(
    concurrent_calls: int = concurrent_calls, call_delay: float = call_delay
) -> None:
    tasks: List[asyncio.Task] = []

    for _ in range(concurrent_calls):
        # Schedule the make_call function as a task
        task: asyncio.Task = asyncio.create_task(make_call())
        tasks.append(task)

        # Stagger the calls slightly
        await asyncio.sleep(call_delay)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Run the load_test function in an asyncio event loop
    asyncio.run(load_test(concurrent_calls=concurrent_calls, call_delay=call_delay))
