// A streaming completion, using the OpenAI SDK.
//
//   npm install openai
//   KILIDIFY_API_KEY=kl_live_… node stream.mjs "your prompt"

import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://api.kilidify.com/v1",
  apiKey: process.env.KILIDIFY_API_KEY,
});

const prompt = process.argv[2] ?? "Count to five.";

const stream = await client.chat.completions.create({
  model: process.env.MODEL ?? "anthropic/claude-sonnet-5.5",
  messages: [{ role: "user", content: prompt }],
  stream: true,
});

for await (const chunk of stream) {
  // A chunk can arrive with no choices (a usage-only final chunk, for
  // instance), so do not assume choices[0] is there.
  if (!chunk.choices?.length) continue;
  process.stdout.write(chunk.choices[0].delta.content ?? "");
}

process.stdout.write("\n");
