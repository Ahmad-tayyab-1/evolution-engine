import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

CLIENT_SECRET_FILE = os.getenv("YT_CLIENT_SECRET_FILE", "./secrets/client_secret.json")
TOKEN_FILE = os.getenv("YT_TOKEN_FILE", "./secrets/token.json")


def _get_credentials() -> Credentials:
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # one-time interactive auth - run this manually once via `python -m agent.auth_setup`
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds


def _youtube():
    return build("youtube", "v3", credentials=_get_credentials())


def _youtube_analytics():
    return build("youtubeAnalytics", "v2", credentials=_get_credentials())


def upload_video(video_path: str, title: str, description: str, tags: list,
                  thumbnail_path: str = None, category_id: str = "27",  # 27 = Education
                  privacy_status: str = "public") -> str:
    yt = _youtube()
    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": category_id,
        },
        "status": {"privacyStatus": privacy_status, "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    video_id = response["id"]

    if thumbnail_path and os.path.exists(thumbnail_path):
        yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumbnail_path)).execute()

    return video_id


def fetch_new_comments(max_per_video: int = 20) -> list:
    """Pulls recent top-level comment threads across the channel's videos."""
    yt = _youtube()
    channel_id = _get_channel_id(yt)
    threads = yt.commentThreads().list(
        part="snippet", allThreadsRelatedToChannelId=channel_id,
        maxResults=max_per_video, order="time",
    ).execute()

    out = []
    for item in threads.get("items", []):
        top = item["snippet"]["topLevelComment"]["snippet"]
        out.append({
            "comment_id": item["snippet"]["topLevelComment"]["id"],
            "video_id": top["videoId"],
            "author": top["authorDisplayName"],
            "text": top["textOriginal"],
        })
    return out


def post_reply(parent_comment_id: str, text: str):
    yt = _youtube()
    yt.comments().insert(
        part="snippet",
        body={"snippet": {"parentId": parent_comment_id, "textOriginal": text}},
    ).execute()


def _get_channel_id(yt) -> str:
    resp = yt.channels().list(part="id", mine=True).execute()
    return resp["items"][0]["id"]


def get_channel_branding() -> dict:
    yt = _youtube()
    channel_id = _get_channel_id(yt)
    resp = yt.channels().list(part="brandingSettings,snippet", id=channel_id).execute()
    item = resp["items"][0]
    return {
        "channel_id": channel_id,
        "title": item["snippet"].get("title", ""),
        "description": item["brandingSettings"]["channel"].get("description", ""),
        "keywords": item["brandingSettings"]["channel"].get("keywords", ""),
    }


def update_channel_branding(description: str = None, keywords: str = None):
    """
    Updates channel-level description and/or keywords (tags). Does NOT touch
    profile picture, banner, or channel name - those stay manual by design.
    keywords: space-separated string, YouTube's expected format (quote
    multi-word keywords, e.g. '"space facts" "ancient history" science').
    """
    yt = _youtube()
    channel_id = _get_channel_id(yt)
    current = yt.channels().list(part="brandingSettings", id=channel_id).execute()
    branding = current["items"][0]["brandingSettings"]
    branding.setdefault("channel", {})

    if description is not None:
        branding["channel"]["description"] = description
    if keywords is not None:
        branding["channel"]["keywords"] = keywords

    yt.channels().update(
        part="brandingSettings",
        body={"id": channel_id, "brandingSettings": branding},
    ).execute()


def get_channel_stats() -> dict:
    """subs, watch hours (last 12mo), shorts views (last 90d) for monetization tracking."""
    yt = _youtube()
    ya = _youtube_analytics()
    channel_id = _get_channel_id(yt)

    subs_resp = yt.channels().list(part="statistics", id=channel_id).execute()
    subs = int(subs_resp["items"][0]["statistics"]["subscriberCount"])

    today = datetime.date.today()
    d12mo = today - datetime.timedelta(days=365)
    d90 = today - datetime.timedelta(days=90)

    watch_resp = ya.reports().query(
        ids=f"channel=={channel_id}", startDate=str(d12mo), endDate=str(today),
        metrics="estimatedMinutesWatched",
    ).execute()
    watch_minutes = watch_resp.get("rows", [[0]])[0][0] if watch_resp.get("rows") else 0

    shorts_resp = ya.reports().query(
        ids=f"channel=={channel_id}", startDate=str(d90), endDate=str(today),
        metrics="views", dimensions="creatorContentType",
    ).execute()
    shorts_views = 0
    if shorts_resp.get("rows"):
        for row in shorts_resp["rows"]:
            if str(row[0]).lower() == "shorts":
                shorts_views = row[1]

    return {
        "subs": subs,
        "watch_hours_12mo": watch_minutes / 60.0,
        "shorts_views_90d": int(shorts_views),
    }


def search_public_videos(query: str, max_results: int = 8, shorts: bool = False) -> list:
    """
    Public search - no special access needed, just what's publicly visible
    (view counts, titles, tags, duration). Used for competitor/viral analysis.
    """
    yt = _youtube()
    search_resp = yt.search().list(
        part="id", q=query, type="video", order="viewCount",
        maxResults=max_results,
        publishedAfter=(datetime.datetime.utcnow() - datetime.timedelta(days=30)).isoformat("T") + "Z",
        videoDuration="short" if shorts else "medium",
    ).execute()
    video_ids = [item["id"]["videoId"] for item in search_resp.get("items", [])]
    if not video_ids:
        return []

    details_resp = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(video_ids)).execute()

    out = []
    for item in details_resp.get("items", []):
        duration_iso = item["contentDetails"]["duration"]  # e.g. PT1M30S
        out.append({
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "tags": item["snippet"].get("tags", []),
            "view_count": int(item["statistics"].get("viewCount", 0)),
            "published_at": item["snippet"]["publishedAt"],
            "duration_sec": _parse_iso_duration(duration_iso),
        })
    return out


def _parse_iso_duration(iso: str) -> int:
    """Minimal PT#H#M#S parser, no external dep needed."""
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def get_video_metrics(video_id: str) -> dict:
    ya = _youtube_analytics()
    yt = _youtube()
    channel_id = _get_channel_id(yt)
    today = datetime.date.today()
    resp = ya.reports().query(
        ids=f"channel=={channel_id}",
        startDate="2020-01-01", endDate=str(today),
        metrics="views,likes,averageViewDuration,estimatedMinutesWatched,subscribersGained,shares,comments",
        filters=f"video=={video_id}",
    ).execute()
    if not resp.get("rows"):
        return {"views": 0, "likes": 0, "avg_view_duration_sec": 0, "ctr": 0}
    row = resp["rows"][0]
    return {
        "views": row[0], "likes": row[1],
        "avg_view_duration_sec": row[2],
        "watch_minutes": row[3],
        "subs_gained": row[4],
        "shares": row[5],
        "comments": row[6],
        "ctr": 0,  # impressions/CTR not available per-video; filled by analytics collector
    }

