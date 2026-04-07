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
steam_xml_url = f"https://steamcommunity.com/id/EvaPilot1/?xml=1"

try:
    res = requests.get(steam_xml_url, timeout=10)
    res.raise_for_status()
    xml = res.text

    # Extract first game from mostPlayedGames
    match = re.search(
        r"<mostPlayedGame>.*?<gameName>\s*<!\[CDATA\[(.*?)\]\]>\s*</gameName>",
        xml,
        re.DOTALL
    )

    last_game = match.group(1) if match else "No recent activity"

except Exception as e:
    print("Steam XML error:", e)
    last_game = "Unavailable"

steam_data = {
    "steam_profile": f"https://steamcommunity.com/id/EvaPilot1",
    "last_played": last_game,
    "updated": datetime.utcnow().isoformat()
}

with open(steam_json_file, "w") as f:
    json.dump(steam_data, f, indent=2)

print(f"Updated {steam_json_file}")

# ===== TSA STATS =====
tsa_api_url = f"https://truesteamachievements.com/api/userstats/EvaPilot1.json"

try:
    res = requests.get(tsa_api_url)
    data = res.json()
    tsa_data = {
        "profile_url": f"https://truesteamachievements.com/user/EvaPilot1",
        "total_achievements": data.get("totalAchievements", 0),
        "total_points": data.get("totalPoints", 0),
        "updated": datetime.utcnow().isoformat()
    }
except:
    tsa_data = {
        "profile_url": f"https://truesteamachievements.com/user/EvaPilot1",
        "total_achievements": 0,
        "total_points": 0,
        "updated": datetime.utcnow().isoformat()
    }

with open(tsa_json_file, "w") as f:
    json.dump(tsa_data, f, indent=2)

print(f"Updated {tsa_json_file}")
