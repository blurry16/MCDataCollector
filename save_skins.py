import requests
from __data__ import cvdbdata

mode = input("1: url, 2: name. ")

data = cvdbdata.load()
for i in data:
    url = data[i]["skin_url"]
    if url != None:
        try:           
            name = data[i]["name"] if mode == "2" else url[38:]
            response = requests.get(url=url)
            with open(rf"skins\{name}.png" if mode == "2" else rf"skins_url\{name}.png", "wb") as file:
                file.write(response.content)
            print(f"Saved {name}.png")
        except:
            pass