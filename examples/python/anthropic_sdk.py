"""The official Anthropic SDK, pointed at Kilidify.

Kilidify answers the Anthropic Messages API as well as the OpenAI one, so this
needs no shim and no proxy. It is the same path Claude Code uses.

    pip install anthropic
    KILIDIFY_API_KEY=kl_live_… python anthropic_sdk.py "your prompt"
"""

import os
import sys

from anthropic import Anthropic

# No /v1 here. The Anthropic SDK appends /v1/messages itself, so including it
# produces a 404 on a doubled path. The OpenAI SDK is the opposite and wants
# the /v1. This is the most common setup mistake with Kilidify.
client = Anthropic(
    base_url="https://api.kilidify.com",
    api_key=os.environ["KILIDIFY_API_KEY"],
)

prompt = sys.argv[1] if len(sys.argv) > 1 else "Say hello in Persian."

message = client.messages.create(
    model=os.environ.get("MODEL", "anthropic/claude-sonnet-5.5"),
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
)

print(message.content[0].text)
