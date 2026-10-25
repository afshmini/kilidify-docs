"""A streaming completion, using the OpenAI SDK.

    pip install openai
    KILIDIFY_API_KEY=kl_live_… python stream.py "your prompt"
"""

import os
import sys

from openai import OpenAI

client = OpenAI(
    base_url="https://api.kilidify.com/v1",
    api_key=os.environ["KILIDIFY_API_KEY"],
)

prompt = sys.argv[1] if len(sys.argv) > 1 else "Count to five."

stream = client.chat.completions.create(
    model=os.environ.get("MODEL", "anthropic/claude-sonnet-5.5"),
    messages=[{"role": "user", "content": prompt}],
    stream=True,
)

for chunk in stream:
    # A chunk can carry no choices at all (for example a usage-only final
    # chunk), so index defensively rather than assuming choices[0] exists.
    if not chunk.choices:
        continue
    print(chunk.choices[0].delta.content or "", end="", flush=True)

print()
