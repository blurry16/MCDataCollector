# MCDataCollector pre1-v1.4.0 ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/blurry16/MCDataCollector/main?label=last%20commit%20to%20main) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/blurry16/MCDataCollector/dev?label=last%20commit%20to%20dev)

Well, remember I was trolling CV staff by saying people's last online time? This is what I used to know when you were
last on.

### Requirements

Clone the repo and use `pip install -r requirements.txt`.

### How do I run it? (outdated)

Install requirements ofc :p  
First of all replace `LOG_PATH` constant in `.env` with your latest.log path with your
values.  
Then create a .json file at `DATA_PATH` (you should replace it with your value) and run `tracker.py` script.  
It will write Mojang API data and last&first (in unix timestamp) time seen date in the file you gave it.  
If you want to have my main data.json file, please contact me in Discord (blurry16) or
in [![Telegram Badge](https://img.shields.io/badge/Telegram-blue?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/blurry16)
(clickable).  
Good luck in collecting data!

### Meaning of collected points

- "id" — Mojang UUID. Usually used to identify your account.
- "name" — Mojang account nickname. E.g., my is blurry16.
- "last_seen" — Time in Unix timestamp when the player was seen for the last time.
- "first_time_seen" — Time in Unix timestamp when the player was seen for the first time.
- "skin_variant" — Variant of player's skin. It can be "classic" or "slim".
- "cape_url" — URL to player's cape. If the player doesn't have a cape, it's null.
- "skin_url" — URL to player's skin.
- "db_id" — ID of a player in .json file. Pretty useless but cool at the same time.
- "does_exist" — This thing is there since people like AddictiveOracle exist.
  Those who have their name faked or accounts cracked.  
  Please mind that you can't update cracked account data with "update with nicknames" tool.
  _Just buy license lol._

### Example of collected data

Well, if you read this, it means you still care about your privacy, and you probably don't trust me (or you just wonder
what I collect lol).
I don't really care about your trust, but here is an example of collected data.  
Points meaning can be found at "Meaning of collected points" paragraph.

```json
{
  "id": "ef2b9013f4ca4749b3bfaf83146c538e",
  "name": "blurry16",
  "last_seen": 1724104859,
  "first_time_seen": 1708259854,
  "skin_variant": "slim",
  "cape_url": null,
  "skin_url": "https://textures.minecraft.net/texture/98a8dfc4ce0181897c225584cd0f3c1fef486a80ce957347cea3c38e74cbac6a",
  "db_id": 0,
  "does_exist": true
}
```

### Notes for followers

If you want to continue collecting data just like I did, I'm always happy to contribute to your forks or projects.  
If you need help, contact me (I left my contacts at the top of the file).