from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3
from pathlib import Path

DB_PATH = Path("./db/finance_control.db")

app = FastAPI()

class Gasto(BaseModel):
    data: datetime
    local: str
    valor: float

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/add-gasto")
def add_gasto(gasto: Gasto):
    if not gasto.local.strip():
        raise HTTPException(status_code=400, detail="Local inválido")

    if gasto.valor <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido")

    data_formatada = gasto.data.replace(hour=0, minute=0, second=0, microsecond=0)\
                               .strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO gastos (data, local, valor)
        VALUES (?, ?, ?)
        """,
        (data_formatada, gasto.local.strip(), gasto.valor)
    )

    conn.commit()
    gasto_id = cursor.lastrowid
    conn.close()

    return {
        "status": "ok",
        "id": gasto_id,
        "data": data_formatada,
        "local": gasto.local.strip(),
        "valor": gasto.valor
    }