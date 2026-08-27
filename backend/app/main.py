from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timedelta
import sqlite3
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Database setup
DATABASE_PATH = "time_tracking.db"

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

def calculate_duration(slot):
    if slot['end_time']:
        start = datetime.fromisoformat(slot['start_time'])
        end = datetime.fromisoformat(slot['end_time'])
        delta = end - start
        hours = int(delta.total_seconds() // 3600)
        minutes = int((delta.total_seconds() % 3600) // 60)
        seconds = int(delta.total_seconds() % 60)
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return "-:--:--"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM time_slots 
        WHERE end_time IS NOT NULL
        ORDER BY start_time DESC
        LIMIT 10
    ''')
    recent_slots = cursor.fetchall()
    
    conn.close()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "recent_slots": recent_slots,
        "calculate_duration": calculate_duration
    })

@app.get("/day", response_class=HTMLResponse)
async def day_view(request: Request):
    date_param = request.query_params.get("date", datetime.now().strftime("%Y-%m-%d"))
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM time_slots 
        WHERE date(start_time) = ?
        ORDER BY start_time
    ''', (date_param,))
    slots = cursor.fetchall()
    
    conn.close()
    
    total_time = calculate_total_time(slots)
    
    return templates.TemplateResponse("day.html", {
        "request": request,
        "slots": slots,
        "date": date_param,
        "total_time": total_time
    })

@app.get("/week", response_class=HTMLResponse)
async def week_view(request: Request):
    start_date = request.query_params.get("start_date", 
        (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d"))
    
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=6)).strftime("%Y-%m-%d")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM time_slots 
        WHERE date(start_time) BETWEEN ? AND ?
        ORDER BY start_time
    ''', (start_date, end_date))
    slots = cursor.fetchall()
    
    conn.close()
    
    total_time = calculate_total_time(slots)
    
    return templates.TemplateResponse("week.html", {
        "request": request,
        "slots": slots,
        "start_date": start_date,
        "end_date": end_date,
        "total_time": total_time
    })

@app.get("/month", response_class=HTMLResponse)
async def month_view(request: Request):
    year = request.query_params.get("year", str(datetime.now().year))
    month = request.query_params.get("month", str(datetime.now().month).zfill(2))
    
    start_date = f"{year}-{month}-01"
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=32)).strftime("%Y-%m-%d")
    end_date = end_date.replace("32", "01")  # Simple way to get first of next month
    end_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM time_slots 
        WHERE date(start_time) BETWEEN ? AND ?
        ORDER BY start_time
    ''', (start_date, end_date))
    slots = cursor.fetchall()
    
    conn.close()
    
    total_time = calculate_total_time(slots)
    
    return templates.TemplateResponse("month.html", {
        "request": request,
        "slots": slots,
        "year": year,
        "month": month,
        "total_time": total_time
    })

@app.post("/start_timer")
async def start_timer(request: Request):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO time_slots (start_time, end_time, note)
        VALUES (?, ?, ?)
    ''', (datetime.now().isoformat(), None, ""))
    
    timer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"timer_id": timer_id}

@app.post("/stop_timer")
async def stop_timer(request: Request):
    data = await request.form()
    timer_id = data.get("timer_id")
    note = data.get("note", "")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE time_slots 
        SET end_time = ?, note = ?
        WHERE id = ? AND end_time IS NULL
    ''', (datetime.now().isoformat(), note, timer_id))
    
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/add_time_slot")
async def add_time_slot(request: Request):
    data = await request.form()
    
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    note = data.get("note", "")
    
    if not start_time or not end_time:
        raise HTTPException(status_code=400, detail="Start and end time are required")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO time_slots (start_time, end_time, note)
        VALUES (?, ?, ?)
    ''', (start_time, end_time, note))
    
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete_time_slot")
async def delete_time_slot(request: Request):
    data = await request.form()
    slot_id = data.get("slot_id")
    
    if not slot_id:
        raise HTTPException(status_code=400, detail="Slot ID is required")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM time_slots WHERE id = ?
    ''', (slot_id,))
    
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/", status_code=303)

def calculate_total_time(slots):
    total_seconds = 0
    for slot in slots:
        if slot['end_time']:
            start = datetime.fromisoformat(slot['start_time'])
            end = datetime.fromisoformat(slot['end_time'])
            total_seconds += (end - start).total_seconds()
    
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    
    return f"{hours}:{minutes:02d}:{seconds:02d}"
