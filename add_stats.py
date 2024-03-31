from __data__ import cvdbdata, statsdataobj
from datetime import datetime, timedelta
from json import dumps

data_len = len(cvdbdata.load())


statsdata = statsdataobj.load()
# prev_date = (datetime.now().date() - timedelta(days=2)).strftime("%Y-%m-%d")
last_date = list(statsdata)[-1]
now_date = (datetime.now().date() - timedelta(days=1)).strftime("%Y-%m-%d")
statsdata[now_date] = {
    "count": data_len,
    "delta": data_len - int(statsdata[last_date]["count"]),
}

print(dumps(statsdata, indent=4))
statsdataobj.dump(statsdata)
