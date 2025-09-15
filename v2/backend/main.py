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

@app.post("/check-conflicts")
async def check_conflicts(request: Dict[str, Any]):
    """Seçilen dersler arasında çakışma kontrolü yapar"""
    try:
        course_codes = request.get("courses", [])
        conflicts = []
        
        # Seçilen dersleri bul
        selected_courses = []
        for course_code in course_codes:
            for course in courses_data["courses"]:
                if course["code"] == course_code:
                    selected_courses.append(course)
                    break
        
        # Çakışma kontrolü
        for i, course1 in enumerate(selected_courses):
            for section1 in course1["sections"]:
                for slot1 in section1["schedule"]:
                    for j, course2 in enumerate(selected_courses[i+1:], i+1):
                        for section2 in course2["sections"]:
                            for slot2 in section2["schedule"]:
                                # Aynı gün ve saatte çakışma kontrolü
                                if (slot1["day"] == slot2["day"] and 
                                    slot1["start"] == slot2["start"]):
                                    conflicts.append({
                                        "course1": course1["code"],
                                        "section1": section1["section"],
                                        "course2": course2["code"],
                                        "section2": section2["section"],
                                        "day": slot1["day"],
                                        "time": slot1["start"],
                                        "room": slot1.get("room", "EF 210")
                                    })
        
        return {
            "has_conflicts": len(conflicts) > 0,
            "conflicts": conflicts
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Çakışma kontrolü hatası: {str(e)}")

@app.post("/generate-schedule")
async def generate_schedule(request: Dict[str, Any]):
    """Seçilen dersler için program oluşturur"""
    try:
        selected_course_codes = request.get("selected_courses", [])
        schedule = {}
        
        # Günler listesi
        days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
        
        # Her gün için boş program oluştur
        for day in days:
            schedule[day] = {}
            for hour in range(8, 19):  # 08:00 - 18:00
                for minute in [0, 30]:  # Her yarım saat
                    time_key = f"{hour:02d}:{minute:02d}"
                    schedule[day][time_key] = []
        
        # Seçilen dersleri programa ekle
        for course_code in selected_course_codes:
            for course in courses_data["courses"]:
                if course["code"] == course_code:
                    # İlk section'ı al (frontend'de seçim yapılacak)
                    if course["sections"]:
                        section = course["sections"][0]
                        for slot in section["schedule"]:
                            day = slot["day"]
                            start_time = slot["start"]
                            
                            if day in schedule and start_time in schedule[day]:
                                schedule[day][start_time].append({
                                    "code": course["code"],
                                    "name": course["name"],
                                    "section": section["section"],
                                    "instructor": section["instructor"],
                                    "duration": slot["duration"],
                                    "room": slot.get("room", "EF 210")
                                })
                    break
        
        return {"schedule": schedule}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Program oluşturma hatası: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
