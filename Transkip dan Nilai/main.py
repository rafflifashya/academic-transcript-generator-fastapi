from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Sistem Transkrip Akademik - Raffli Islami Fashya")

# --- Database Sederhana (In-Memory) ---
grades_db = []
audit_trail = []

# --- Business Logic & Constants ---
GRADE_MAP = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "E": 0.0}

class GradeEntry(BaseModel):
    nim: str
    nama: str
    kode_mk: str
    nama_mk: str
    sks: int
    semester: int
    nilai_huruf: str  # A, B, C, D, E
    presensi: float   # Persentase (0-100)

class UpdateGrade(BaseModel):
    nilai_huruf: str
    changed_by: str
    reason: str

# --- Helper Functions ---
def calculate_mutu(sks: int, nilai_huruf: str) -> float:
    return sks * GRADE_MAP.get(nilai_huruf, 0.0)

def get_predikat(ipk: float) -> str:
    if ipk >= 3.5: return "Cum Laude"
    if ipk >= 3.0: return "Sangat Memuaskan"
    if ipk >= 2.0: return "Memuaskan"
    return "Cukup"

# --- Endpoints ---

@app.post("/grades/", tags=["Grade Management"])
def input_nilai(entry: GradeEntry):
    # Business Rule: Presensi minimal 75% 
    if entry.presensi < 75:
        raise HTTPException(status_code=400, detail="Nilai tidak bisa diinput jika presensi < 75%")
    
    if entry.nilai_huruf not in GRADE_MAP:
        raise HTTPException(status_code=400, detail="Grade tidak valid (A/B/C/D/E)")
    
    grades_db.append(entry.dict())
    return {"message": "Nilai berhasil diinput"}

@app.put("/grades/{nim}/{kode_mk}", tags=["Audit Trail"])
def update_nilai(nim: str, kode_mk: str, update: UpdateGrade):
    # Cari data lama untuk audit trail [cite: 11, 43]
    for idx, entry in enumerate(grades_db):
        if entry["nim"] == nim and entry["kode_mk"] == kode_mk:
            old_value = entry["nilai_huruf"]
            
            # Update data
            grades_db[idx]["nilai_huruf"] = update.nilai_huruf
            
            # Log Audit Trail [cite: 44]
            log = {
                "nim": nim,
                "kode_mk": kode_mk,
                "old_value": old_value,
                "new_value": update.nilai_huruf,
                "changed_by": update.changed_by,
                "changed_at": datetime.now().isoformat(),
                "reason": update.reason
            }
            audit_trail.append(log)
            return {"message": "Update berhasil", "audit_log": log}
    
    raise HTTPException(status_code=404, detail="Data tidak ditemukan")

@app.get("/transcript/{nim}", tags=["GPA Calculator & PDF"])
def get_transcript(nim: str):
    # Filter data mahasiswa
    mhs_grades = [g for g in grades_db if g["nim"] == nim]
    
    if not mhs_grades:
        return {"nim": nim, "ipk": 0.0, "message": "Belum ada nilai"} [cite: 30]

    # Logika Nilai Tertinggi jika Mengulang 
    latest_grades = {}
    for g in mhs_grades:
        kode = g["kode_mk"]
        nilai_angka = GRADE_MAP[g["nilai_huruf"]]
        if kode not in latest_grades or nilai_angka > GRADE_MAP[latest_grades[kode]["nilai_huruf"]]:
            latest_grades[kode] = g

    # Filter hanya yang lulus (Nilai >= D / 1.0) [cite: 22, 28]
    # Catatan: Di modul tertulis >= D (2.0), namun secara standar akademik D=1.0. 
    # Saya gunakan logika nilai_angka >= 1.0 sesuai grade map.
    passed_grades = [g for g in latest_grades.values() if GRADE_MAP[g["nilai_huruf"]] >= 1.0]

    total_sks = sum(g["sks"] for g in passed_grades)
    total_mutu = sum(calculate_mutu(g["sks"], g["nilai_huruf"]) for g in passed_grades)
    
    ipk = total_mutu / total_sks if total_sks > 0 else 0.0

    return {
        "header": "TRANSKRIP AKADEMIK",
        "biodata": {"NIM": nim, "Nama": mhs_grades[0]["nama"]},
        "records": passed_grades,
        "summary": {
            "total_sks": total_sks,
            "ipk": round(ipk, 2),
            "predikat": get_predikat(ipk)
        },
        "footer": "TTD Dekan - Versi Digital"
    }

@app.get("/audit-logs", tags=["Audit Trail"])
def get_audit_logs():
    return audit_trail