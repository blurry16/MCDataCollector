import json
import time
from pathlib import Path

from mcdatacollector import datafile, csvfolder


def __gendumpname(_type: str, extension: str = "csv") -> str:
    """
    :param _type: type of the data the dump has
    :param extension: the file extension without the dot
    :return: dump name as str
    """
    return f"mcdcdump-{_type}-{time.time()}.{extension}"


def dumpfullcsv() -> Path:
    """
    Makes a dump of data and puts it in a generated path
    :return: the path of the dump
    """
    data = datafile.load()
    csv = "id,name,last_seen,first_time_seen,skin_variant,cape_url,skin_url,db_id,does_exist\n"  # header
    for i in data:
        csv += ",".join([json.dumps(j) for j in data[i].values()]) + "\n"
    __dumppath = Path(f"{csvfolder}/full/{__gendumpname("full")}")
    with open(__dumppath, "x") as csvfile:
        csvfile.write(csv)
    return __dumppath


def dumpplayerscsv() -> Path:
    """
    Makes a dump of id&name data and puts it in a generated path
    :return: the path of the dump
    """
    data = datafile.load()
    filename = __gendumpname("idname")
    csv = "id,name\n" + "\n".join([f"{json.dumps(i)},{json.dumps(data[i]["name"])}" for i in data])
    __dumppath = Path(f"{csvfolder}/misc/{filename}")
    with open(__dumppath, "x") as f:
        f.write(csv)
    return __dumppath
