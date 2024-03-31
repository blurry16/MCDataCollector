from __data__ import cvdbdata

data = cvdbdata.load()

for i in data:

    data[i]["does_exist"] = False if i == data[i]["name"].lower() else True

cvdbdata.dump(data)
