#!/usr/bin/env python3
import httpx
import os
from pathlib import Path
from dotenv import load_dotenv
import logging


logging.basicConfig(level=logging.INFO)


data_dir = Path(__file__).resolve().parents[2] / "data" / "blogroll"
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)


feedbin_user = os.getenv("FEEDBIN_USER")
feedbin_pass = os.getenv("FEEDBIN_PASS")
feedbin_api = "https://api.feedbin.com/v2"
feedbin_endpoints = {"subs": "subscriptions.json", "tags": "taggings.json"}


def fetch_json(endpoint):
    try:
        response = httpx.get(endpoint, auth=(feedbin_user, feedbin_pass))
        response.raise_for_status()
        return response.text
    except httpx.RequestError as e:
        logging.error(f"Feedbin: request error {e}")
    except httpx.HTTPStatusError as e:
        logging.error(f"Feedbin: HTTP error {e}")
    return None


def write_json(file_path, data):
    if data:
        try:
            with file_path.open("w") as target:
                target.write(data)
            return True
        except IOError as e:
            logging.error(f"Feedbin: file write error {e}")
    return False


def get_feeds(data_type):
    endpoint = f"{feedbin_api}/{feedbin_endpoints[data_type]}"
    file_path = data_dir / feedbin_endpoints[data_type]

    data = fetch_json(endpoint)
    if write_json(file_path, data):
        return f"Feedbin {data_type} update complete :)"
    else:
        return f"Feedbin {data_type} update failed :("


if __name__ == "__main__":
    for data_type in feedbin_endpoints:
        print(get_feeds(data_type))
