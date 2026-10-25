#!/usr/bin/env bash
# The catalogue, with prices per million tokens in USD.
#
# Without a key this lists everything Kilidify serves. With one, it lists only
# what that key is permitted to use, which is how you diagnose a
# 403 model_not_allowed: if the model is missing here, the key is restricted.
#
#   ./models.sh                       # everything
#   KILIDIFY_API_KEY=kl_live_… ./models.sh   # only what this key may use
#   ./models.sh claude                # filter by substring
set -euo pipefail

# An if/else around the whole call rather than an array of extra arguments:
# "${ARR[@]}" on an empty array is an unbound variable under `set -u` in bash
# 3.2, which is still what macOS ships.
fetch() {
  if [ -n "${KILIDIFY_API_KEY:-}" ]; then
    curl -sS https://api.kilidify.com/v1/models \
      -H "Authorization: Bearer $KILIDIFY_API_KEY"
  else
    curl -sS https://api.kilidify.com/v1/models
  fi
}

FILTER="${1:-}"

fetch | jq -r --arg filter "$FILTER" '
  .data
  | map(select($filter == "" or (.id | test($filter; "i"))))
  | .[]
  # Prices come back per token, which is unreadable. Per million is the unit
  # everyone actually quotes.
  | [ .id,
      ((.pricing.prompt     // "0") | tonumber * 1000000 | . * 100 | round / 100 | tostring),
      ((.pricing.completion // "0") | tonumber * 1000000 | . * 100 | round / 100 | tostring)
    ]
  | @tsv
' | sort | awk -F'\t' 'BEGIN { printf "%-44s %12s %12s\n", "MODEL", "IN $/M", "OUT $/M" }
                        { printf "%-44s %12s %12s\n", $1, $2, $3 }'
