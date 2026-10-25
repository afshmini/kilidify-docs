"""One completion through Kilidify, using the OpenAI SDK.

    pip install openai
    KILIDIFY_API_KEY=kl_live_… python chat.py "your prompt"
"""

import os
import sys

from openai import OpenAI

# The OpenAI SDK appends paths to base_url, so it needs the /v1 included.
# The Anthropic SDK does not; see anthropic_sdk.py.
client = OpenAI(
    base_url="https://api.kilidify.com/v1",
    api_key=os.environ["KILIDIFY_API_KEY"],
)

prompt = sys.argv[1] if len(sys.argv) > 1 else "Say hello in Persian."

reply = client.chat.completions.create(
    model=os.environ.get("MODEL", "anthropic/claude-sonnet-5.5"),
    messages=[{"role": "user", "content": prompt}],
)

print(reply.choices[0].message.content)

# usage is reported the same way OpenAI reports it, and is what you are billed
# on. Printing it while developing is the cheapest way to notice that a prompt
# is far longer than you thought.
print(
    f"\n[{reply.usage.prompt_tokens} in, {reply.usage.completion_tokens} out]",
    file=sys.stderr,
)
