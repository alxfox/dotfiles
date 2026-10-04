#!/bin/sh
set -eu

local_profile="$HOME/.zprofile.local"
[ -f "$local_profile" ] || exit 0

temporary_file=$(mktemp "${TMPDIR:-/tmp}/zprofile-local.XXXXXX")
trap 'rm -f "$temporary_file"' EXIT HUP INT TERM

awk '
  $0 == "# Secrets that are intentionally not committed." { next }
  $0 == "[[ -r \"$HOME/.secrets\" ]] && source \"$HOME/.secrets\"" { next }
  { print }
' "$local_profile" > "$temporary_file"

if ! cmp -s "$local_profile" "$temporary_file"; then
  chmod 600 "$temporary_file"
  mv "$temporary_file" "$local_profile"
fi
