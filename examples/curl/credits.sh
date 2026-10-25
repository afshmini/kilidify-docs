#!/usr/bin/env bash
# Balance, limits and permitted models for the key you are holding. The fastest
# way to tell whether a key works and what it is allowed to do.
set -euo pipefail
: "${KILIDIFY_API_KEY:?set KILIDIFY_API_KEY to your kl_live_… key}"

curl -sS https://api.kilidify.com/v1/credits \
  -H "Authorization: Bearer $KILIDIFY_API_KEY" | jq .
