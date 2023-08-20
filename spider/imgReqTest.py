import requests

url = "http://i0.hdslb.com/bfs/bangumi/image/38e2a273f528fd01c34f1fc4df0f69c64487efad.png"

response = requests.get(url)
if response.status_code == 200:
    filename = './f1.png'
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Image downloaded and saved as {filename}")
else:
    print("Failed to download image")