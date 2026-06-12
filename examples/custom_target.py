"""Example custom adapter. Run with:  pijack --target examples.custom_target:MyTarget
Wire `send()` to your real endpoint (OpenAI, Anthropic, internal gateway)."""
from pijack.targets import Target


class MyTarget(Target):
    name = "my-llm"

    def send(self, user_message: str) -> str:
        # Replace with a real call, e.g.:
        #   import os, anthropic
        #   client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        #   msg = client.messages.create(model="claude-3-5-sonnet-latest",
        #         max_tokens=512, system="...", messages=[{"role":"user","content":user_message}])
        #   return msg.content[0].text
        return "I can't help with that request."
