# GHC Base API

## Description
The GHC Base API provides an overview of compatibility between Haskell GHC versions and base library versions. Its goal is to make it easy for developers to automatically select the correct GHC version for a project based on its cabal file.

### Links

- API: https://webdevred.github.io/ghc-base-api/ghc_base_versions.json
- Website: https://webdevred.github.io/ghc-base-api

### Example

Suggested directory layout in your project:
```
.github/script_helpers/select_ghc_by_base.jq
.github/script_helpers/extact_upper_base_bound.awk
.github/scripts/get-newest-ghc-version.sh
.github/workflows/future-proofing.yaml
```

**.github/script_helpers/extact_upper_base_bound.awk:**
```awk
/base[[:space:]]*>=/ {
    match($0, /<([0-9.]+)/, m)
    if (m[1] != "") { print m[1]; exit }
}
```

**.github/script_helpers/select_ghc_by_base.jq:**
```jq
def pad3:
  if length == 1 then "00" + .
  elif length == 2 then "0" + .
  else .
end;

map(. + {
        base_sort:
          (.base | split(".") | map(pad3) | join(""))
      })
  | map(select(.base_sort < ($ub | split(".") | map(pad3) | join(""))))
  | max_by(.base_sort)
  | .ghc
```

**.github/scripts/get-newest-ghc-version.sh:**
```bash
#!/usr/bin/env bash

if [[ -z "$CABAL_FILE" || ! -f "$CABAL_FILE" ]]; then
  echo "Cabal file missing: $CABAL_FILE"
  exit 1
fi

upper=$(awk -f ./.github/script_helpers/extact_upper_base_bound.awk "$CABAL_FILE")

if [ -z "$upper" ]; then
    echo "No upper bound found."
    exit 1
fi

JSON=$(curl -f -s -S https://webdevred.github.io/ghc-base-api/ghc_base_versions.json) || {
    echo "Couldnt fetch GHC versions."
    exit 1
}

ghc_version=$(jq -r --arg ub "$upper" -f ./.github/script_helpers/select_ghc_by_base.jq <<< "$JSON")

echo "GHC version: $ghc_version"

if [[ "$GITHUB" != "" ]]; then
  echo "ghc-version=${ghc_version}" >> "$GITHUB_OUTPUT"
fi
```

**.github/workflows/future-proofing.yaml:**
```yaml
      - name: Checkout code
        uses: actions/checkout@v5
      - name: Get latest supported GHC version
        id: get-ghc
        run: bash ./.github/scripts/get-newest-ghc-version.sh
        shell: bash
        env:
          CABAL_FILE: jbeam-edit.cabal
      - name: Set up GHC latest and Cabal
        id: setup-ghc
        uses: haskell-actions/setup@v2.8.2
```
