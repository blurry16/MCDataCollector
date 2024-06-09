# mcPlayersData (collector)
Well, remember I was trolling CV staff by saying people's last online time? This is what I used to know when you were last on.

### Requirements
Just clone the repo and use `pip install -r requirements.txt`. If I missed anything in that file please pull request fixed version or open an issue.

### How do I run it?
Install requirements ofc :p  
So first of all replace `LOGPATH` constant in `__data__.py` with your latest.log path (don't mind those I have already left :p) with your values.  
Then create a .json file at `DATAPATH` (you should replace it with your value) and run `main.py` script.  
It will write Mojang API data and last&first (in unix timestamp) time seen date in the file you gave it.  
If you want to have my main data.json file please contact me in Discord (blurry16) or Telegram (@blurry16).  
Good luck in collecting data!

### Meaning of collected points
- "id" - Mojang UUID. Usually used to identify your account.
- "name" - Mojang account nickname. E.g my is blurry16.
- "last_seen" - Time in Unix timestamp when the player was seen for the last time.
- "first_time_seen" - Time in Unix timestamp when the player was seen for the first time.
- "is_legacy_profile" - Something pretty useless but because Mojang API has it why not collect it? Anyways, it's there since migration process ig.
- "skin_variant" - Variant of player's skin. Can be "classic" or "slim".
- "cape_url" - URL to player's cape. If the player doesn't have a cape it's null.
- "skin_url" - URL to player's skin.
- "db_id" - ID of a player in .json file. Pretty useless but cool at the same time.
- "does_exist" - This thing is there since people like AddictiveOracle exist. Those who have their name faked or accounts cracked.

### Notes for followers
If you want to continue collecting data just like I did I'm always happy to contribute to your forks or projects. If you need help, contact me (I left my contacts at the top of the file).