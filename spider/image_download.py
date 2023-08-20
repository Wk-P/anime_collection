import requests, json

def get_urls():
    urls = []
    file_path = './files/collection_dup.json'
    with open(file_path, 'r', encoding='utf-8') as fi:
        all_data = json.load(fi)
        for item in all_data:
            urls.append({
                "name": item['title'],
                "url": item['cover']
            })
    return urls

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded and saved as {filename}")
    else:
        print("Failed to download image")


def main():
    urls = get_urls()
    for u in urls:
        fn = f"./images/{u['name']}.png"
        download_image(u, fn)