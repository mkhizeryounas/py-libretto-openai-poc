import constants
import asyncio
from libs.libretto import Client as LibrettoClient
import openai
import logging
import time
import argparse


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

libretto = LibrettoClient(constants.LIBRETTO_API_KEY, constants.LIBRETTO_API_NAME)
libretto.send_event("Hello", "Hi, how are you?")

openai_client = openai.Client(api_key=constants.OPENAI_API_KEY)


def wait_for_run_completion(thread_id, run_id):
    """This function waits for the run to complete and returns the run."""
    run = openai_client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    while run.status != "completed":
        time.sleep(1)
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id
        )
    return run


def get_assistant_response(thread_id):
    """This function retrieves the assistant's response from the thread."""
    messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
    if hasattr(messages, "__iter__"):
        # Iterate through the messages and find the assistant's response
        for message in messages:
            if message.role == "assistant":
                # Check if content is a list and has at least one item
                if isinstance(message.content, list) and len(message.content) > 0:
                    # Check if the first item of content has a 'text' attribute
                    if hasattr(message.content[0], "text"):
                        return message.content[0].text.value
                else:
                    logging.error("Message content is empty or not in expected format.")
    return None


async def main():
    """The main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Process prompt with openai assistant and logs in libretto."
    )
    parser.add_argument(
        "-p",
        "--prompt",
        metavar="PROMPT",
        type=str,
        nargs="+",
        help="Specify a prompt",
    )
    args = parser.parse_args()
    prompt = args.prompt
    if prompt:
        prompt = " ".join(prompt)
    else:
        raise ValueError("Prompt is required")

    thread = openai_client.beta.threads.create()
    message = openai_client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=prompt
    )
    logger.info("message:: %s", message)
    wait_for_run_completion(
        thread.id,
        openai_client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=constants.OPENAI_ASSISTANT_ID
        ).id,
    )
    response = get_assistant_response(thread.id)
    logger.info("run:: %s", response)
    libretto.send_event(prompt, response)


if __name__ == "__main__":
    asyncio.run(main())
