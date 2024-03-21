import requests


class Client:
    """A client for logging conversational events to Libretto."""

    def __init__(self, api_key, api_name=None):
        self.url = "https://app.getlibretto.com/api/event"
        self.api_key = api_key
        self.api_name = api_name

    def send_event(self, prompt: str, response: str):
        """Logs a conversation event to Libretto."""
        if not prompt or not response:
            raise ValueError("Prompt and response must be non-empty strings.")
        event = {
            "response": response,
            "params": {},
            "apiKey": self.api_key,
            "apiName": self.api_name,
            "promptTemplateChat": [{"role": "user", "content": prompt}],
            "prompt": {},
        }
        return requests.post(self.url, json=event, timeout=10).json()
