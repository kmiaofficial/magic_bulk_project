import gzip
import shutil
import requests

# 1 make header to follow scryfall api rules
headers = {
    "User-Agent": "MyMTGProject/1.0 (contact: your_email@example.com)",
    "Accept": "application/json",
}

response = requests.get('https://api.scryfall.com/bulk-data/', headers=headers)


data = response.json()
for options in data["data"]:
    if options["type"] == "default_cards":
        download_url = options["jsonl_download_uri"]
        print('found the link', download_url)

        print('downloading')
        file_response = requests.get(download_url, stream=True)
        compressed_file = "default-cards.jsonl.gz"
        destination_file = "default-cards.jsonl"
        #open file on computer in wb mode
        if file_response.status_code == 200:
            with open(compressed_file, "wb") as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            with gzip.open(compressed_file, "rb") as f_in:
                with open(destination_file, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                print("download completed, file extracted")
        else:
            print("error downloading file")