import requests
from __data__ import cvdbdata

data = cvdbdata.load()
for i in data:
    url = data[i]["skin_url"]
    if url != None:
        name = data[i]["name"]
        response = requests.get(url=url)
        with open(rf"skins\{name}.png", "wb") as file:
            file.write(response.content)
        print(f"Saved {name}.png")
