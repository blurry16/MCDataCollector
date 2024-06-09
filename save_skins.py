import requests
from __data__ import cvdbdata, MODELSPATH, UKNOWNVALUEEXCEPTION

mode = input("1: url, 2: name, 3: html model\n")
if mode not in ["1", "2", "3"]:
    raise UKNOWNVALUEEXCEPTION

data = cvdbdata.load()
if mode == "3":
    for i in data:
        name = data[i]["name"]
        try:
            to_save = rf'<iframe src="https://minerender.org/embed/skin/?skin={name}&shadow=true" frameborder="0" width="1920px" height="972px"></iframe>'
            with open(rf"{MODELSPATH}\{name}.html", "x") as file:
                file.write(to_save)
            print(f"Saved {name}.html")
        except Exception as e:
            print(e)
else:
    for i in data:
        url = data[i]["skin_url"]
        if url != None:
            try:
                name = data[i]["name"] if mode == "2" else url[38:]
                response = requests.get(url=url)
                with open(
                    rf"skins\{name}.png" if mode == "2" else rf"skins_url\{name}.png",
                    "wb",
                ) as file:
                    file.write(response.content)
                print(f"Saved {name}.png")
            except Exception as e:
                print(e)
