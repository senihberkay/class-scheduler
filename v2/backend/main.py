from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import pandas as pd
import json
from datetime import datetime
import os

app = FastAPI(
    title="OZUchedule V2 API",
    description="Özyeğin Üniversitesi Ders Programı API'si",
    version="2.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Veri yükleme fonksiyonu
def load_courses_data():
    """CSV dosyasından ders verilerini yükler ve JSON formatına dönüştürür"""
    try:
        csv_path = "courses_202420.csv"
        if not os.path.exists(csv_path):
            return create_sample_data()
        
        df = pd.read_csv(csv_path)
        courses_dict = {}
        
        for _, row in df.iterrows():
            course_code = row['Ders Kodu']
            course_name = row['Ders Adı']
            section = row['Ders Section']
            instructor = row['Hoca'] if pd.notna(row['Hoca']) else "Belirtilmemiş"
            schedule_str = row['Saat'] if pd.notna(row['Saat']) else ""
            
            if course_code not in courses_dict:
                courses_dict[course_code] = {
                    "code": course_code,
                    "name": course_name,
                    "sections": []
                }
            
            # Saat bilgisini parse et
            schedule_slots = []
            if schedule_str:
                time_slots = schedule_str.split(" / ")
                for slot in time_slots:
                    if " " in slot:
                        day_time = slot.split(" ", 1)
                        if len(day_time) == 2:
                            day = day_time[0]
                            time_range = day_time[1].split("-")
                            if len(time_range) == 2:
                                start_time = time_range[0].strip()
                                end_time = time_range[1].strip()
                                
                                # Süreyi hesapla - Daha doğru hesaplama
                                try:
                                    start_hour = int(start_time.split(":")[0])
                                    start_minute = int(start_time.split(":")[1])
                                    end_hour = int(end_time.split(":")[0])
                                    end_minute = int(end_time.split(":")[1])
                                    
                                    # Toplam dakika hesaplama
                                    start_total_minutes = start_hour * 60 + start_minute
                                    end_total_minutes = end_hour * 60 + end_minute
                                    
                                    # Süre hesaplama (dakika cinsinden)
                                    duration_minutes = end_total_minutes - start_total_minutes
                                    
                                    # Saat cinsine çevir (minimum 1 saat)
                                    duration_hours = max(1, duration_minutes // 60)
                                    
                                    schedule_slots.append({
                                        "day": day,
                                        "start": start_time,
                                        "end": end_time,  # Bitiş saati eklendi
                                        "duration": duration_hours,  # Saat cinsinden
                                        "room": "EF 210"
                                    })
                                except Exception as e:
                                    print(f"Slot parse hatası: {slot}, Hata: {e}")
                                    continue
            
            courses_dict[course_code]["sections"].append({
                "section": section,
                "instructor": instructor,
                "schedule": schedule_slots
            })
        
        return {"courses": list(courses_dict.values())}
    
    except Exception as e:
        print(f"Veri yükleme hatası: {e}")
        return create_sample_data()

def create_sample_data():
    return {
        "courses": [
            {
                "code": "MAT101",
                "name": "Matematik I",
                "sections": [
                    {
                        "section": "A1",
                        "instructor": "Dr. Ahmet Yılmaz",
                        "schedule": [
                            {"day": "Pazartesi", "start": "09:40", "duration": 2, "room": "EF 210"},
                            {"day": "Çarşamba", "start": "14:40", "duration": 2, "room": "EF 310"}
                        ]
                    }
                ]
            }
        ]
    }

# Global veri
courses_data = load_courses_data()

@app.get("/")
async def root():
    return {
        "message": "OZUchedule V2 API",
        "version": "2.0.0",
        "status": "running"
    }

@app.get("/courses")
async def get_courses():
    return courses_data

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
