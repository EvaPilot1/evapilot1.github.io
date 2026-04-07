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
    url = f"https://truesteamachievements.com/user/EvaPilot1"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    html = res.text

    # Extract total achievements
    ach_match = re.search(r'([\d,]+)\s+Achievements Earned', html)

    # Extract total points
    pts_match = re.search(r'([\d,]+)\s+TSA', html)

    if ach_match and pts_match:
        total_achievements = int(ach_match.group(1).replace(",", ""))
        total_points = int(pts_match.group(1).replace(",", ""))
    else:
        raise Exception("Could not find TSA stats")

except Exception as e:
    print("TSA scrape error:", e)

    # Fallback to existing JSON
    try:
        with open(tsa_json_file, "r") as f:
            existing = json.load(f)
            total_achievements = existing.get("total_achievements", 0)
            total_points = existing.get("total_points", 0)
    except:
        total_achievements = 0
        total_points = 0

# Save JSON
tsa_data = {
    "profile_url": f"https://truesteamachievements.com/user/EvaPilot1",
    "total_achievements": total_achievements,
    "total_points": total_points,
    "updated": datetime.utcnow().isoformat()
}

with open(tsa_json_file, "w") as f:
    json.dump(tsa_data, f, indent=2)

print(f"TSA: {total_achievements} achievements, {total_points} points")
