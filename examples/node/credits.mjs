// Balance, limits and permitted models for a key, with no SDK at all.
//
//   KILIDIFY_API_KEY=kl_live_… node credits.mjs

const key = process.env.KILIDIFY_API_KEY;
if (!key) {
  console.error("set KILIDIFY_API_KEY to your kl_live_… key");
  process.exit(1);
}

const response = await fetch("https://api.kilidify.com/v1/credits", {
  headers: { Authorization: `Bearer ${key}` },
});

const body = await response.json();

if (!response.ok) {
  // Gateway errors carry a code to branch on and a Persian message alongside
  // the English one.
  console.error(`status ${response.status}, code ${body.error?.code}`);
  console.error(`  ${body.error?.message}`);
  console.error(`  ${body.error?.message_fa}`);
  process.exit(1);
}

const d = body.data;
console.log(`balance   $${d.balance_usd}`);
console.log(`available $${d.available_usd}  (reserved $${d.reserved_usd})`);
console.log(`rpm limit ${d.rate_limit_rpm}`);
console.log(`budget    ${d.monthly_budget_usd ? "$" + d.monthly_budget_usd : "none"}`);
console.log(`models    ${d.allowed_models ? d.allowed_models.join(", ") : "unrestricted"}`);
