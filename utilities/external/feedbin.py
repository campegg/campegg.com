#!/usr/bin/env python3

import json
import httpx
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


data_dir = str(Path(__file__).parents[2]) + "/data/blogroll/"

feedbin_user = os.getenv("FEEDBIN_USER")
feedbin_pass = os.getenv("FEEDBIN_PASS")
feedbin_api = "https://api.feedbin.com/v2"
feedbin_subs = "subscriptions.json"
feedbin_tags = "taggings.json"


def get_data(type):
    if type == "subs":
        data = f"{feedbin_api}/{feedbin_subs}"
        file = f"{data_dir}/{feedbin_subs}"
    elif type == "tags":
        data = f"{feedbin_api}/{feedbin_tags}"
        file = f"{data_dir}/{feedbin_tags}"

    try:
        response = httpx.get(data, auth=(feedbin_user, feedbin_pass))
        payload = response.text
    except Exception as e:
        return f"Feedbin {type} update failed because {e} :("

    try:
        output_file = Path(file)
        with output_file.open("w+") as target:
            output_file.write_text(payload)
        return f"Feedbin {type} update complete :)"
    except Exception as e:
        return f"Feedbin {type} update failed because {e} :("


if __name__ == "__main__":
    print(get_data("subs"))
    print(get_data("tags"))
