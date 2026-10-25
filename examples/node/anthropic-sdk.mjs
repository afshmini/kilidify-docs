// The official Anthropic SDK, pointed at Kilidify.
//
// Kilidify answers the Anthropic Messages API as well as the OpenAI one, so
// this needs no shim. It is the same path Claude Code uses.
//
//   npm install @anthropic-ai/sdk
//   KILIDIFY_API_KEY=kl_live_… node anthropic-sdk.mjs "your prompt"

import Anthropic from "@anthropic-ai/sdk";

// No /v1 here. This SDK appends /v1/messages itself, so including it gives a
// 404 on a doubled path. The OpenAI SDK is the opposite and wants the /v1.
const client = new Anthropic({
  baseURL: "https://api.kilidify.com",
  apiKey: process.env.KILIDIFY_API_KEY,
});

const prompt = process.argv[2] ?? "Say hello in Persian.";

const message = await client.messages.create({
  model: process.env.MODEL ?? "anthropic/claude-sonnet-5.5",
  max_tokens: 1024,
  messages: [{ role: "user", content: prompt }],
});

console.log(message.content[0].text);
