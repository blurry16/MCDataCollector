"""Simple Mojang API client :P"""

import base64
import json
from dataclasses import dataclass

import requests


@dataclass()
class UserProfile:
    id: str
    timestamp: int
    name: str
    skin_variant: str
    cape_url: str
    skin_url: str


class NotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


def get_uuid(username: str) -> str:
    resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if "errorMessage" in resp.json():
        raise NotFoundException(f"Player '{username}' doesn't exist")
    return resp.json()["id"]


def get_profile(uuid: str = None, username: str = None) -> UserProfile:
    """ Username lookup is prioritized """
    if uuid is None and username is None:
        raise Exception("Either uuid or username must be provided")

    if username is not None:
        uuid = get_uuid(username)
    """{'id': 'ef2b9013f4ca4749b3bfaf83146c538e', 'timestamp': 1750034642780, 'name': 'blurry16', 'is_legacy_profile': False, 'skin_variant': 'slim', 'cape_url': None, 'skin_url': 'http://textures.minecraft.net/texture/98a8dfc4ce0181897c225584cd0f3c1fef486a80ce957347cea3c38e74cbac6a'}"""
    resp = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
    raw = resp.json()
    if "errorMessage" in raw:
        raise NotFoundException(uuid)

    username = raw["name"]
    properties = json.loads(base64.b64decode(raw["properties"][0]["value"]))

    userprofile = UserProfile(
        id=properties["profileId"],
        timestamp=properties["timestamp"],
        name=properties["profileName"],
        skin_variant="classic" if "metadata" not in properties["textures"] else "slim",
        cape_url=None if "CAPE" not in properties["textures"] else properties["textures"]["CAPE"]["url"],
        skin_url=properties["textures"]["SKIN"]["url"]
    )
    return userprofile
