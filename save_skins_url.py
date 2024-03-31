import requests
from __data__ import cvdbdata

data = cvdbdata.load()
for i in data:
    url = data[i]["skin_url"]
    if url != None:
        try:
            # print(url[38:])
            name = url[38:]
            response = requests.get(url=url)
            with open(rf"skins_url\{name}.png", "wb") as file:
                file.write(response.content)
            print(f"Saved {name}.png")
        except:
            pass
