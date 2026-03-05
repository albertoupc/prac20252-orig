import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = FastAPI()

# Database connection parameters from environment variables
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@app.get("/api/planets")
async def get_planets():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error connecting to database")
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM planets")
            planets = cur.fetchall()
            
            response = {
                "planets": planets,
                "student": DB_USER,
                "created": datetime.now().isoformat()
            }
            return response
    except Exception as e:
        print(f"Error executing query: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving data from database")
    finally:
        conn.close()

# Serve static files
app.mount("/", StaticFiles(directory="public", html=True), name="public")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
