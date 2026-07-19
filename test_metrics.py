import datetime, sys
sys.path.insert(0, "/var/www/yt-agent")
from agent.youtube_client import _youtube_analytics, _get_channel_id, _youtube

ya = _youtube_analytics()
ch = _get_channel_id(_youtube())
today = datetime.date.today()
vid = "QY_IHExWTMI"

# Test 1: basic metrics only
for combo_name, metrics in [
    ("views+likes+avgDur", "views,likes,averageViewDuration"),
    ("add estimatedMinutesWatched", "views,likes,averageViewDuration,estimatedMinutesWatched"),
    ("add subscribersGained", "views,likes,averageViewDuration,estimatedMinutesWatched,subscribersGained"),
    ("add shares", "views,likes,averageViewDuration,estimatedMinutesWatched,subscribersGained,shares"),
    ("add comments", "views,likes,averageViewDuration,estimatedMinutesWatched,subscribersGained,shares,comments"),
]:
    try:
        r = ya.reports().query(
            ids=f"channel=={ch}", startDate="2020-01-01", endDate=str(today),
            metrics=metrics, filters=f"video=={vid}"
        ).execute()
        print(f"OK [{combo_name}]: {r.get('rows')}")
    except Exception as e:
        msg = str(e).split("returned ")[-1][:80] if "returned" in str(e) else str(e)[:80]
        print(f"FAIL [{combo_name}]: {msg}")
