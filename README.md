# This branch is an experiment.
If you want to checkout main branch please head to https://github.com/blurry16/MCDataCollector/blob/main.  
Code at this branch can be unstable.

# MCDataCollector
Well, remember I was trolling CV staff by saying people's last online time? This is what I used to know when you were last on.

### Requirements
Just clone the repo and use `pip install -r requirements.txt`. If I missed anything in that file please pull request fixed version or open an issue.

### How do I run it?
Install requirements ofc :p  
So first of all replace `LOGPATH` constant in `__data__.py` with your latest.log path (don't mind those I have already left :p) with your values.  
Then create a .json file at `DATAPATH` (you should replace it with your value) and run `main.py` script.  
It will write Mojang API data and last&first (in unix timestamp) time seen date in the file you gave it.  
If you want to have my main data.json file please contact me in Discord (blurry16) or in [![Telegram Badge](https://img.shields.io/badge/Telegram-blue?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/blurry16) (clickable).  
Good luck in collecting data!

### Meaning of collected points
- "id" - Mojang UUID. Usually used to identify your account.
- "name" - Mojang account nickname. E.g my is blurry16.
- "last_seen" - Time in Unix timestamp when the player was seen for the last time.
- "first_time_seen" - Time in Unix timestamp when the player was seen for the first time.
- "skin_variant" - Variant of player's skin. Can be "classic" or "slim".
- "cape_url" - URL to player's cape. If the player doesn't have a cape it's null.
- "skin_url" - URL to player's skin.
- "db_id" - ID of a player in .json file. Pretty useless but cool at the same time.
- "does_exist" - This thing is there since people like AddictiveOracle exist. Those who have their name faked or accounts cracked.

### Example of collected data
Well, if you read this it means you still care about your privacy and you probably don't trust me (or you just wonder what I collect lol). I don't really care about your trust but here is an example of collected data.  
Points meaning can be found at "Meaning of collected points" paragraph.
```json
{
    "id": "ef2b9013f4ca4749b3bfaf83146c538e",
    "name": "blurry16",
    "last_seen": 1718031633,
    "first_time_seen": 1708259854,
    "skin_variant": "slim",
    "cape_url": null,
    "skin_url": "http://textures.minecraft.net/texture/bc77f0eb5be2e69d320144242a29dcbeedfe2fc42df48638d86bac470fdab786",
    "db_id": 0,
    "does_exist": true
}
```

### Notes for followers
If you want to continue collecting data just like I did I'm always happy to contribute to your forks or projects. If you need help, contact me (I left my contacts at the top of the file).