import asyncio
from typing import List
from twilio.rest import Client


# Twilio credentials and configuration parameters will be passed directly to the load_test function
async def make_call(
    client: Client, twiml_script: str, twilio_number: str, target_number: str
) -> None:
    await asyncio.to_thread(
        client.calls.create,
        twiml=twiml_script,
        to=target_number,
        from_=twilio_number,
        record=True,
    )


async def load_test(
    account_sid: str,
    auth_token: str,
    twilio_number: str,
    target_number: str,
    script: str,
    concurrent_calls: int = 1,
    call_delay: float = 1.0,
) -> None:
    client = Client(account_sid, auth_token)

    tasks: List[asyncio.Task] = []

    for _ in range(concurrent_calls):
        # Schedule the make_call function as a task
        task: asyncio.Task = asyncio.create_task(
            make_call(client, script, twilio_number, target_number)
        )
        tasks.append(task)

        # Stagger the calls slightly
        await asyncio.sleep(call_delay)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)
