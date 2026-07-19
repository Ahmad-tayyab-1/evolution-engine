import os
import json
import subprocess
import sys
from datetime import datetime
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeTimedSerializer, BadSignature
import hashlib
import secrets as _secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from agent.db import (
    get_session, StrategyState, Video, Genome, TopicScore,
    NicheScore, AnalyticsSnapshot, Rule, Experiment, CommentQueue
)

app = FastAPI(title="Evolution OS", docs_url=None, redoc_url=None, openapi_url=None)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

SECRET_KEY = os.getenv("DASHBOARD_SECRET_KEY", _secrets.token_hex(32))
serializer = URLSafeTimedSerializer(SECRET_KEY)

DASHBOARD_USER = os.getenv("DASHBOARD_USER", "ahmad")
DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "Ahmad@6428195")


def _hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def get_current_user(request: Request):
    token = request.cookies.get("__evo_sess")
    if not token:
        return None
    try:
        data = serializer.loads(token, max_age=86400 * 7)
        if data.get("u") == _hash_pw(DASHBOARD_USER):
            return DASHBOARD_USER
    except (BadSignature, Exception):
        return None
    return None


def require_auth(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})
    return user


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    if get_current_user(request):
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request=request, name="login.html", context={"error": error})


@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == DASHBOARD_USER and password == DASHBOARD_PASSWORD:
        token = serializer.dumps({"u": _hash_pw(username), "t": datetime.utcnow().isoformat()})
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="__evo_sess", value=token, httponly=True,
            max_age=86400 * 7, samesite="strict", secure=False,
        )
        return response
    return templates.TemplateResponse(
        request=request, name="login.html",
        context={"error": "Access denied. Invalid credentials."}
    )


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("__evo_sess")
    return response


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, user: str = Depends(require_auth)):
    return templates.TemplateResponse(request=request, name="index.html", context={"username": user})


@app.get("/api/overview")
async def api_overview(user: str = Depends(require_auth)):
    session = get_session()
    try:
        svc = "unknown"
        try:
            res = subprocess.run(["systemctl", "is-active", "yt-agent"], capture_output=True, text=True, timeout=2)
            svc = res.stdout.strip()
        except Exception:
            pass

        state = session.query(StrategyState).first()
        state_data = {}
        if state:
            state_data = {
                "phase": state.phase or "niche_discovery",
                "locked_niche": state.locked_niche or "Not locked yet",
                "active_track": state.active_track or "long",
                "subs": state.subs or 0,
                "watch_hours_12mo": round(state.watch_hours_12mo or 0, 2),
                "shorts_views_90d": state.shorts_views_90d or 0,
                "last_evaluated_at": state.last_evaluated_at.strftime("%Y-%m-%d %H:%M UTC") if state.last_evaluated_at else "Never",
            }

        total_videos = session.query(Video).count()
        uploaded = session.query(Video).filter(Video.status == "uploaded").count()
        failed = session.query(Video).filter(Video.status == "failed").count()

        return JSONResponse({
            "service": svc,
            "strategy": state_data,
            "total_videos": total_videos,
            "uploaded": uploaded,
            "failed": failed,
        })
    finally:
        session.close()


@app.get("/api/niches")
async def api_niches(user: str = Depends(require_auth)):
    session = get_session()
    try:
        niches = session.query(NicheScore).order_by(NicheScore.opportunity_score.desc()).all()
        result = []
        for n in niches:
            result.append({
                "niche": n.niche,
                "opportunity_score": round(n.opportunity_score or 0, 2),
                "avg_ctr": round(n.avg_ctr or 0, 4),
                "avg_retention": round(n.avg_retention or 0, 1),
                "videos_count": n.videos_count or 0,
            })
        return JSONResponse(result)
    finally:
        session.close()


@app.get("/api/videos")
async def api_videos(user: str = Depends(require_auth)):
    session = get_session()
    try:
        videos = session.query(Video).order_by(Video.created_at.desc()).limit(10).all()
        result = []
        for v in videos:
            result.append({
                "id": v.id,
                "title": v.title or "Untitled",
                "niche": v.niche or "—",
                "topic": v.topic or "—",
                "format": v.format or "—",
                "status": v.status or "planned",
                "youtube_id": v.youtube_id,
                "views": v.views or 0,
                "likes": v.likes or 0,
                "ctr": round((v.ctr or 0) * 100, 2),
                "avg_view_duration_sec": round(v.avg_view_duration_sec or 0, 1),
                "fitness": round(v.fitness or 0, 3),
                "genome_version": v.genome_version,
                "created_at": v.created_at.strftime("%Y-%m-%d %H:%M") if v.created_at else "",
                "error": None,
            })
        return JSONResponse(result)
    finally:
        session.close()


@app.get("/api/genomes")
async def api_genomes(user: str = Depends(require_auth)):
    session = get_session()
    try:
        genomes = session.query(Genome).order_by(Genome.version.desc()).all()
        result = []
        for g in genomes:
            result.append({
                "id": g.id,
                "version": g.version,
                "status": g.status,
                "parent_version": g.parent_version,
                "videos_produced": g.videos_produced or 0,
                "avg_ctr": round((g.avg_ctr or 0) * 100, 2),
                "avg_retention": round(g.avg_retention or 0, 1),
                "rationale": g.mutation_rationale or "—",
                "created_at": g.created_at.strftime("%Y-%m-%d %H:%M") if g.created_at else "",
            })
        return JSONResponse(result)
    finally:
        session.close()


@app.get("/api/analytics")
async def api_analytics(user: str = Depends(require_auth)):
    session = get_session()
    try:
        snapshots = session.query(AnalyticsSnapshot).order_by(AnalyticsSnapshot.snapshot_at.desc()).limit(50).all()
        result = []
        for s in snapshots:
            result.append({
                "video_id": s.video_id,
                "youtube_id": s.youtube_id,
                "impressions": s.impressions or 0,
                "ctr": round((s.ctr or 0) * 100, 2),
                "views": s.views or 0,
                "watch_time_hours": round(s.watch_time_hours or 0, 2),
                "avg_view_duration_sec": round(s.avg_view_duration_sec or 0, 1),
                "subs_gained": s.subscribers_gained or 0,
                "likes": s.likes or 0,
                "comments": s.comments or 0,
                "shares": s.shares or 0,
                "fitness": round(s.fitness_score or 0, 3),
                "snapshot_at": s.snapshot_at.strftime("%Y-%m-%d %H:%M") if s.snapshot_at else "",
            })
        return JSONResponse(result)
    finally:
        session.close()


@app.get("/api/topics")
async def api_topics(user: str = Depends(require_auth)):
    session = get_session()
    try:
        topics = session.query(TopicScore).order_by(TopicScore.weight.desc()).limit(20).all()
        result = []
        for t in topics:
            result.append({
                "topic": t.topic,
                "format": t.format or "short",
                "avg_ctr": round((t.avg_ctr or 0) * 100, 2),
                "avg_retention": round(t.avg_retention or 0, 1),
                "videos_count": t.videos_count or 0,
                "weight": round(t.weight or 0, 2),
            })
        return JSONResponse(result)
    finally:
        session.close()


@app.get("/api/experiments")
async def api_experiments(user: str = Depends(require_auth)):
    session = get_session()
    try:
        exps = session.query(Experiment).order_by(Experiment.created_at.desc()).limit(20).all()
        result = []
        for e in exps:
            result.append({
                "id": e.id,
                "variable": e.variable,
                "hypothesis": e.hypothesis,
                "old_value": (e.old_value or "")[:80],
                "new_value": (e.new_value or "")[:80],
                "result": e.result,
                "created_at": e.created_at.strftime("%Y-%m-%d %H:%M") if e.created_at else "",
            })
        return JSONResponse(result)
    finally:
        session.close()


@app.get("/api/rules")
async def api_rules(user: str = Depends(require_auth)):
    session = get_session()
    try:
        rules = session.query(Rule).order_by(Rule.confidence.desc()).all()
        result = []
        for r in rules:
            result.append({
                "rule": r.rule,
                "category": r.category,
                "confidence": round(r.confidence or 0, 2),
                "evidence_count": r.evidence_count or 0,
            })
        return JSONResponse(result)
    finally:
        session.close()


@app.get("/api/logs")
async def api_logs(user: str = Depends(require_auth)):
    try:
        res = subprocess.run(
            ["journalctl", "-u", "yt-agent", "-n", "80", "--no-pager"],
            capture_output=True, text=True, timeout=3
        )
        return JSONResponse({"logs": res.stdout or "No logs available."})
    except Exception as e:
        return JSONResponse({"logs": f"Error: {str(e)}"})
