def download(filename: str, url: str):
    import requests
    download = requests.get(url,stream=True)
    with open(filename, 'wb') as file:
        for chunk in download.iter_content(chunk_size = 1024*1024):
            if chunk:
                file.write(chunk)