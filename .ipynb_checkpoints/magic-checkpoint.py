import requests

# 1. Supply a unique, custom User-Agent to satisfy Scryfall's API rules
headers = {
    "User-Agent": "MyMTGProject/1.0 (contact: your_email@example.com)",
    "Accept": "application/json",
}

# 2. Get the list of all available bulk data entries
metadata_url = "https://api.scryfall.com/bulk-data"
response = requests.get(metadata_url, headers=headers)

if response.status_code == 200:
    bulk_data_list = response.json()["data"]

    # 3. Filter for the file type you need (e.g., 'oracle_cards' or 'default_cards')
    oracle_cards_meta = next(
        item for item in bulk_data_list if item["type"] == "oracle_cards"
    )

    # 4. Grab the active download URI (the exact static file path updates twice daily)
    download_url = oracle_cards_meta["jsonl_download_uri"]
    print(f"Downloading from latest dynamic URI: {download_url}")

    # 5. Execute the actual file download stream
    file_response = requests.get(download_url, headers=headers, stream=True)

    if file_response.status_code == 200:
        with open("oracle-cards.jsonl.gz", "wb") as f:
            for chunk in file_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Success! Bulk data downloaded.")
    else:
        print(f"Failed to fetch file. Status code: {file_response.status_code}")
else:
    print(f"Metadata lookup failed. Status code: {response.status_code}")
    print(response.text)
