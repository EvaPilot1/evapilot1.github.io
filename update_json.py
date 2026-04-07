import requests
import json
from datetime import datetime
import re

# ===== CONFIG =====
steam_profile_id = "EvaPilot1"      # Your Steam custom URL
steam_json_file = "steam.json"

tsa_user = "EvaPilot1"              # Your TrueSteamAchievements username
tsa_json_file = "tsa.json"

# ===== STEAM LAST PLAYED =====
steam_xml_url = f"https://steamcommunity.com/id/{steam_profile_id}/?xml=1"

try:
    res = requests.get(steam_xml_url)
    if res.status_code == 200:
        xml = res.text
        # Extract most recent game played
        match = re.search(r"<mostRecentGame>(.*?)</mostRecentGame>", xml)
        last_game = match.group(1) if match else "No recent game"
    else:
        last_game = "Unavailable"
except:
    last_game = "Unavailable"

steam_data = {
    "steam_profile": f"https://steamcommunity.com/id/{steam_profile_id}",
    "last_played": last_game,
    "updated": datetime.utcnow().isoformat()
}

with open(steam_json_file, "w") as f:
    json.dump(steam_data, f, indent=2)

print(f"Updated {steam_json_file}")

# ===== TSA STATS =====
tsa_api_url = f"https://truesteamachievements.com/api/userstats/{tsa_user}.json"

try:
    res = requests.get(tsa_api_url)
    data = res.json()
    tsa_data = {
        "profile_url": f"https://truesteamachievements.com/user/{tsa_user}",
        "total_achievements": data.get("totalAchievements", 0),
        "total_points": data.get("totalPoints", 0),
        "updated": datetime.utcnow().isoformat()
    }
except:
    tsa_data = {
        "profile_url": f"https://truesteamachievements.com/user/{tsa_user}",
        "total_achievements": 0,
        "total_points": 0,
        "updated": datetime.utcnow().isoformat()
    }

with open(tsa_json_file, "w") as f:
    json.dump(tsa_data, f, indent=2)

print(f"Updated {tsa_json_file}")
