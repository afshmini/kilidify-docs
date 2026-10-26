# شروع سریع

[English](../quickstart.md)

پنج دقیقه از صفر تا گرفتن اولین پاسخ جریانی.

## ۱. حساب و کلید

1. در [kilidify.com/register](https://kilidify.com/register) حساب بسازید. یک
   نشانی ایمیل کافی است و هنگام ثبت‌نام هیچ کارتی خواسته نمی‌شود.
2. از پنل و از طریق درگاه بانکی ایرانی حساب را شارژ کنید. مبلغ به ریال پرداخت
   می‌شود و اعتبار در همان لحظه و با نرخ بازار آزاد به دلار در کیف پول شما
   می‌نشیند. همان نرخ روی تراکنش ثبت می‌ماند.
3. در [kilidify.com/api-keys](https://kilidify.com/api-keys) کلید بسازید. کلید
   به شکل `kl_live_…` است و فقط یک بار نمایش داده می‌شود.

اگر دورهٔ آزمایشی رایگانی در جریان باشد، شاید بتوانید از گام ۲ بگذرید؛ پنل در
صورت باز بودن چنین پیشنهادی آن را اعلام می‌کند. کلید آزمایشی به چند مدل ارزان
محدود است، پس اگر مدلی که خواسته‌اید با `model_not_allowed` برگشت، دلیلش همین
است.

## ۲. کتابخانه را به آن وصل کنید

آدرس پایه `https://api.kilidify.com/v1` است و کلید در `Authorization: Bearer …`
یا در `x-api-key` می‌رود. هر کدام را که کتابخانهٔ شما از قبل می‌فرستد به کار
ببرید؛ هر دو همه‌جا پذیرفته می‌شوند.

### curl

```bash
curl https://api.kilidify.com/v1/chat/completions \
  -H "Authorization: Bearer $KILIDIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-5.5",
    "messages": [{"role": "user", "content": "به فارسی سلام کن."}]
  }'
```

### پایتون، با SDK شرکت OpenAI

```bash
pip install openai
```

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.kilidify.com/v1",
    api_key=os.environ["KILIDIFY_API_KEY"],
)

reply = client.chat.completions.create(
    model="anthropic/claude-sonnet-5.5",
    messages=[{"role": "user", "content": "به فارسی سلام کن."}],
)
print(reply.choices[0].message.content)
```

### Node، با SDK شرکت OpenAI

```bash
npm install openai
```

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://api.kilidify.com/v1",
  apiKey: process.env.KILIDIFY_API_KEY,
});

const reply = await client.chat.completions.create({
  model: "anthropic/claude-sonnet-5.5",
  messages: [{ role: "user", content: "به فارسی سلام کن." }],
});

console.log(reply.choices[0].message.content);
```

### پایتون، با SDK شرکت Anthropic

کلیدیفای به Anthropic Messages API هم پاسخ می‌دهد، پس SDK رسمی آن تنها با عوض
کردن آدرس پایه کار می‌کند.

```bash
pip install anthropic
```

```python
import os
from anthropic import Anthropic

client = Anthropic(
    base_url="https://api.kilidify.com",     # اینجا /v1 نگذارید؛ خود SDK آن را اضافه می‌کند
    api_key=os.environ["KILIDIFY_API_KEY"],
)

message = client.messages.create(
    model="anthropic/claude-sonnet-5.5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "به فارسی سلام کن."}],
)
print(message.content[0].text)
```

به آدرس پایه دقت کنید: SDK شرکت OpenAI آدرس `https://api.kilidify.com/v1` را
می‌خواهد چون مسیرها را به انتهای آن می‌چسباند، و SDK شرکت Anthropic آدرس
`https://api.kilidify.com` را می‌خواهد چون خودش `/v1/messages` را اضافه می‌کند.
اگر به هرکدام آدرس آن یکی را بدهید، پاسخ یک خطای 404 با `/v1` تکراری در مسیر
است. این رایج‌ترین اشتباه در راه‌اندازی است.

## ۳. مطمئن شوید که کلید کار می‌کند

```bash
curl https://api.kilidify.com/v1/credits -H "Authorization: Bearer $KILIDIFY_API_KEY"
```

اگر موجودی برگشت، کلید سالم است. اگر `401 invalid_api_key` گرفتید، کلید اشتباه
یا باطل‌شده است؛ `402 not_provisioned` یعنی حساب هنوز دسترسی بالادستی ندارد و
به شارژ نیاز دارد.

## ۴. پاسخ جریانی

هر دو شکل API جریانی کار می‌کنند. با SDK شرکت OpenAI مقدار `stream=True` را
بدهید و روی پاسخ پیمایش کنید؛ تکه‌ها رویدادهای استاندارد server-sent هستند، پس
هر کتابخانه‌ای که جریان OpenAI را می‌شناسد این را هم می‌شناسد.

```python
for chunk in client.chat.completions.create(
    model="anthropic/claude-sonnet-5.5",
    messages=[{"role": "user", "content": "تا پنج بشمار."}],
    stream=True,
):
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

نمونه‌های اجراشدنی همهٔ موارد بالا در [`../../examples/`](../../examples/) هستند.

## بعد چه بخوانید

- [`models.md`](models.md) برای انتخاب مدل و شناخت `kilidify/auto`.
- [`billing.md`](billing.md) برای اینکه یک درخواست چطور به هزینه تبدیل می‌شود.
- [`errors.md`](errors.md) وقتی کدی برگشت که نمی‌شناسید.
- [`claude-code.md`](claude-code.md) برای استفاده از Claude Code با کیف پول خودتان.
