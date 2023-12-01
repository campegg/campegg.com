import httpx


def archive_content(url):
    archive_url = f"https://web.archive.org/save/{url}"
    headers = {"User-Agent": "Mozilla/5.0 (Ubuntu; Linux x86_64;)"}

    try:
        with httpx.Client(headers=headers, timeout=20.0) as client:
            response = client.get(archive_url)
        if response.status_code == 200:
            print(f"Successfully archived {url}")
        else:
            print(
                f"Failed to archive {url}. Status code: {response.status_code}, Response: {response.text}"
            )
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")
