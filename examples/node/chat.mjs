// One completion through Kilidify, using the OpenAI SDK.
//
//   npm install openai
//   KILIDIFY_API_KEY=kl_live_… node chat.mjs "your prompt"

import OpenAI from "openai";

// The OpenAI SDK appends paths to baseURL, so it needs the /v1 included.
// The Anthropic SDK does not; see anthropic-sdk.mjs.
const client = new OpenAI({
  baseURL: "https://api.kilidify.com/v1",
  apiKey: process.env.KILIDIFY_API_KEY,
});

const prompt = process.argv[2] ?? "Say hello in Persian.";

const reply = await client.chat.completions.create({
  model: process.env.MODEL ?? "anthropic/claude-sonnet-5.5",
  messages: [{ role: "user", content: prompt }],
});

console.log(reply.choices[0].message.content);

// What you are billed on. Worth printing while developing: it is the cheapest
// way to notice a prompt is much longer than you assumed.
console.error(
  `\n[${reply.usage.prompt_tokens} in, ${reply.usage.completion_tokens} out]`,
);
