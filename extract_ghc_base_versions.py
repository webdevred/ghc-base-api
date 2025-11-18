#!/usr/bin/env python3
import yaml
import json
import requests
import argparse

URL = "https://raw.githubusercontent.com/haskell/ghcup-metadata/refs/heads/develop/ghcup-0.0.9.yaml"

def extract_ghc_base_versions(data):
    ghc_entries = data.get("ghcupDownloads", {}).get("GHC", {})
    results = []

    for ghc_version, info in ghc_entries.items():
        base_version = None
        for tag in info.get("viTags", []):
            if isinstance(tag, str) and tag.startswith("base-"):
                base_version = tag.replace("base-", "")
                break
        results.append({"ghc": ghc_version, "base": base_version})

    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="ghc_base_versions.json")
    parser.add_argument("--url", default=URL)
    args = parser.parse_args()

    print(f"Hämtar YAML från: {args.url}")
    resp = requests.get(args.url)
    resp.raise_for_status()

    data = yaml.safe_load(resp.text)
    extracted = extract_ghc_base_versions(data)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(extracted, f, ensure_ascii=False, indent=2)

    print(f"Sparat till: {args.out}")

if __name__ == "__main__":
    main()
