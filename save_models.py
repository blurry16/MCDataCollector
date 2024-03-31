from __data__ import cvdbdata

data = cvdbdata.load()

MODELS_FOLDER_PATH = r"C:\Users\Blurry\PycharmProjects\playersData\models"

for i in data:
    name = data[i]["name"]
    try:
        to_save = rf'<iframe src="https://minerender.org/embed/skin/?skin={name}&shadow=true" frameborder="0" width="1920px" height="972px"></iframe>'
        with open(rf"{MODELS_FOLDER_PATH}\{name}.html", "x") as file:
            file.write(to_save)
        print(f"Saved {name}.html")
    except Exception as e:
        pass
