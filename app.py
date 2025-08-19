#!/usr/bin/env python3
"""
TMDb Movie Scraper - Web Dashboard
A modern web interface for the TMDb movie scraper.
"""

import asyncio
import json
import logging
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import uvicorn

# Import our optimized scraper
from tmdb_scraper import TMDbScraperOptimized, logger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TMDb Movie Scraper Dashboard", version="1.1.0")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Global state for scraping sessions
active_sessions: Dict[str, dict] = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                disconnected.append(connection)
        
        for connection in disconnected:
            self.disconnect(connection)

manager = ConnectionManager()

def save_data(df: pd.DataFrame, filename: str, format_type: str) -> bool:
    """Save DataFrame in the specified format"""
    try:
        if format_type.lower() == 'csv':
            df.to_csv(filename, index=False)
            
        elif format_type.lower() == 'json':
            df.to_json(filename, orient='records', indent=2)
            
        elif format_type.lower() == 'xlsx':
            df.to_excel(filename, index=False, engine='openpyxl')
            
        elif format_type.lower() == 'sqlite':
            # Create SQLite database
            conn = sqlite3.connect(filename)
            df.to_sql('movies', conn, if_exists='replace', index=False)
            conn.close()
            
        else:
            logger.error(f"Unsupported format: {format_type}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to save {format_type.upper()} file: {e}")
        return False

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    current_year = datetime.now().year
    return templates.TemplateResponse("index.html", {"request": request, "current_year": current_year})

@app.get("/api/config")
async def get_config():
    api_key = os.getenv("TMDB_API_KEY")
    include_adult = os.getenv("TMDB_INCLUDE_ADULT", "false").lower() == "true"
    
    return {
        "has_api_key": bool(api_key),
        "api_key_preview": api_key[:8] + "*" * (len(api_key) - 12) + api_key[-4:] if api_key and len(api_key) > 12 else "Not configured",
        "include_adult": include_adult
    }

@app.post("/api/scrape")
async def start_scrape(
    count: int = Form(1000),
    format: str = Form("csv"),
    concurrent: int = Form(8),
    include_adult: bool = Form(False)
):
    # Validate inputs
    if count < 1 or count > 10000:
        raise HTTPException(status_code=400, detail="Count must be between 1 and 10,000")
    
    if concurrent < 1 or concurrent > 20:
        raise HTTPException(status_code=400, detail="Concurrent requests must be between 1 and 20")
    
    if format not in ["csv", "json", "xlsx", "sqlite"]:
        raise HTTPException(status_code=400, detail="Format must be csv, json, xlsx, or sqlite")
    
    session_id = str(uuid.uuid4())
    session = {
        "id": session_id,
        "status": "starting",
        "count": count,
        "format": format,
        "concurrent": concurrent,
        "include_adult": include_adult,
        "scraped": 0,
        "start_time": datetime.now(),
        "filename": None,
        "error": None,
        "cancel_requested": False
    }
    
    active_sessions[session_id] = session
    asyncio.create_task(run_scraper(session))
    
    return {"session_id": session_id, "message": "Scraping started"}

@app.post("/api/sessions/{session_id}/abort")
async def abort_session(session_id: str):
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = active_sessions[session_id]
    session["cancel_requested"] = True
    session["status"] = "cancelling"

    await manager.broadcast({
        "type": "session_update",
        "session_id": session_id,
        "status": "cancelling"
    })
    return {"detail": "Abort requested"}

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    return {
        "id": session["id"],
        "status": session["status"],
        "count": session["count"],
        "scraped": session["scraped"],
        "progress": round((session["scraped"] / session["count"]) * 100, 1) if session["count"] > 0 else 0,
        "format": session["format"],
        "filename": session["filename"],
        "error": session["error"],
        "elapsed_time": str(datetime.now() - session["start_time"]) if "start_time" in session else None,
        "skipped": session.get("skipped", 0)
    }

@app.get("/api/download/{session_id}")
async def download_file(session_id: str):
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    if session["status"] != "completed" or not session["filename"]:
        raise HTTPException(status_code=400, detail="File not ready for download")
    
    filename = session["filename"]
    if not Path(filename).exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get appropriate media type and download name
    format_ext = session["format"]
    media_types = {
        "csv": "text/csv",
        "json": "application/json", 
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "sqlite": "application/x-sqlite3"
    }
    
    download_name = f"tmdb_movies_{session['count']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_ext}"
    
    return FileResponse(
        filename,
        media_type=media_types.get(format_ext, "application/octet-stream"),
        filename=download_name
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message({"type": "pong", "data": data}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def run_scraper(session: dict):
    session_id = session["id"]
    
    try:
        session["status"] = "running"
        await manager.broadcast({
            "type": "session_update",
            "session_id": session_id,
            "status": "running"
        })
        
        class WebProgressTracker:
            def __init__(self, session, manager):
                self.session = session
                self.manager = manager
                self.last_update = 0
            
            def update(self, amount):
                self.session["scraped"] += amount
                if self.session.get("cancel_requested"):
                    raise asyncio.CancelledError("Cancelled by user")
                if self.session["scraped"] - self.last_update >= 10:
                    asyncio.create_task(self.manager.broadcast({
                        "type": "progress_update",
                        "session_id": session_id,
                        "scraped": self.session["scraped"],
                        "total": self.session["count"],
                        "progress": round((self.session["scraped"] / self.session["count"]) * 100, 1)
                    }))
                    self.last_update = self.session["scraped"]
        
        progress_tracker = WebProgressTracker(session, manager)
        
        async with TMDbScraperOptimized(
            target_movies=session["count"],
            concurrent_requests=session["concurrent"],
            include_adult=session["include_adult"]
        ) as scraper:

            
            original_process_method = scraper.process_movie_data
            def enhanced_process_method(movies):
                if session.get("cancel_requested"):
                    raise asyncio.CancelledError("Cancelled by user")
                processed = original_process_method(movies)
                # Only count up to the target
                remaining = session["count"] - session["scraped"]
                to_add = min(len(processed), remaining)
                progress_tracker.update(to_add)
                return processed

            scraper.process_movie_data = enhanced_process_method
            
            try:
                df = await scraper.scrape_all_movies()
            except asyncio.CancelledError:
                session["status"] = "cancelled"
                session["skipped"] = max(0, session["count"] - session["scraped"])
                await manager.broadcast({
                    "type": "session_update",
                    "session_id": session_id,
                    "status": "cancelled"
                })
                return
            
            if df.empty:
                session["status"] = "error"
                session["error"] = "No data scraped. Check API key and connection."
                return
            
            # Save file in requested format
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tmdb_movies_{timestamp}_{session_id[:8]}.{session['format']}"
            
            success = save_data(df, filename, session["format"])
            if not success:
                session["status"] = "error"
                session["error"] = f"Failed to save {session['format'].upper()} file"
                return
            
            session["filename"] = filename
            session["status"] = "completed"
            session["scraped"] = len(df)
            session["skipped"] = max(0, session["count"] - session["scraped"])

            await manager.broadcast({
                "type": "session_complete",
                "session_id": session_id,
                "scraped": len(df),
                "skipped": session["skipped"],
                "filename": filename
            })
            
    except Exception as e:
        session["status"] = "error"
        session["error"] = str(e)
        logger.error(f"Scraping error for session {session_id}: {e}")
        
        await manager.broadcast({
            "type": "session_error",
            "session_id": session_id,
            "error": str(e)
        })

if __name__ == "__main__":
    Path("templates").mkdir(exist_ok=True)
    
    print("🌐 Starting TMDb Movie Scraper Web Dashboard...")
    print("📱 Open your browser to: http://localhost:8000")
    
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
