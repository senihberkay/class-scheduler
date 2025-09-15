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
        csv_path = "courses.csv"
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
                                    
                                    # Slot sayısına çevir - Her slot 50 dakika + 10 dakika ara
                                    # 13:40-16:30 = 170 dakika = 3 slot (13:40-14:30, 14:40-15:30, 15:40-16:30)
                                    if duration_minutes >= 150:  # 2.5+ saat ise 3 slot
                                        duration_hours = 3
                                    elif duration_minutes >= 90:  # 1.5+ saat ise 2 slot
                                        duration_hours = 2
                                    else:
                                        duration_hours = 1
                                        
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

def time_to_minutes(time_str):
    """Saat:dakika formatını toplam dakikaya çevirir"""
    try:
        hour, minute = map(int, time_str.split(':'))
        return hour * 60 + minute
    except:
        return 0

def time_intervals_overlap(start1, end1, start2, end2):
    """İki zaman aralığının kesişip kesişmediğini kontrol eder"""
    start1_min = time_to_minutes(start1)
    end1_min = time_to_minutes(end1)
    start2_min = time_to_minutes(start2)
    end2_min = time_to_minutes(end2)
    
    # Aralıklar kesişiyor mu kontrol et
    return start1_min < end2_min and start2_min < end1_min

@app.post("/check-conflicts")
async def check_conflicts(request: Dict[str, Any]):
    """Seçilen dersler arasında çakışma kontrolü yapar"""
    try:
        # Request formatı: {"course_selections": [{"course_code": "MAT101", "section": "A1"}, ...]}
        course_selections = request.get("course_selections", [])
        conflicts = []
        
        # Seçilen ders-section kombinasyonlarını bul
        selected_schedule_slots = []
        for selection in course_selections:
            course_code = selection.get("course_code")
            selected_section = selection.get("section")
            
            # İlgili dersi bul
            for course in courses_data["courses"]:
                if course["code"] == course_code:
                    # Belirtilen section'ı bul
                    for section in course["sections"]:
                        if section["section"] == selected_section:
                            # Bu section'ın tüm saat slotlarını ekle
                            for slot in section["schedule"]:
                                selected_schedule_slots.append({
                                    "course_code": course_code,
                                    "course_name": course["name"],
                                    "section": selected_section,
                                    "instructor": section["instructor"],
                                    "slot": slot
                                })
                            break
                    break
        
        # Çakışma kontrolü - sadece seçilen slot'lar arasında
        for i, slot_info1 in enumerate(selected_schedule_slots):
            for j, slot_info2 in enumerate(selected_schedule_slots[i+1:], i+1):
                slot1 = slot_info1["slot"]
                slot2 = slot_info2["slot"]
                
                # Aynı gün kontrolü
                if slot1["day"] == slot2["day"]:
                    # Bitiş zamanlarını hesapla (eğer yoksa duration kullan)
                    end1 = slot1.get("end")
                    if not end1 and "duration" in slot1:
                        # Duration'dan bitiş zamanını hesapla
                        start_minutes = time_to_minutes(slot1["start"])
                        end_minutes = start_minutes + (slot1["duration"] * 60)
                        end_hour = end_minutes // 60
                        end_min = end_minutes % 60
                        end1 = f"{end_hour:02d}:{end_min:02d}"
                    
                    end2 = slot2.get("end")
                    if not end2 and "duration" in slot2:
                        # Duration'dan bitiş zamanını hesapla
                        start_minutes = time_to_minutes(slot2["start"])
                        end_minutes = start_minutes + (slot2["duration"] * 60)
                        end_hour = end_minutes // 60
                        end_min = end_minutes % 60
                        end2 = f"{end_hour:02d}:{end_min:02d}"
                    
                    # Zaman aralığı kesişimi kontrolü
                    if time_intervals_overlap(
                        slot1["start"], 
                        end1 or slot1["start"],  # Fallback olarak start zamanını kullan
                        slot2["start"], 
                        end2 or slot2["start"]
                    ):
                        conflicts.append({
                            "course1": slot_info1["course_code"],
                            "course1_name": slot_info1["course_name"],
                            "section1": slot_info1["section"],
                            "instructor1": slot_info1["instructor"],
                            "course2": slot_info2["course_code"],
                            "course2_name": slot_info2["course_name"],
                            "section2": slot_info2["section"],
                            "instructor2": slot_info2["instructor"],
                            "day": slot1["day"],
                            "time1": f"{slot1['start']}-{end1 or slot1['start']}",
                            "time2": f"{slot2['start']}-{end2 or slot2['start']}",
                            "room1": slot1.get("room", "EF 210"),
                            "room2": slot2.get("room", "EF 210")
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
        # Request formatı: {"course_selections": [{"course_code": "MAT101", "section": "A1"}, ...]}
        course_selections = request.get("course_selections", [])
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
        
        # Seçilen ders-section kombinasyonlarını programa ekle
        for selection in course_selections:
            course_code = selection.get("course_code")
            selected_section = selection.get("section")
            
            # İlgili dersi bul
            for course in courses_data["courses"]:
                if course["code"] == course_code:
                    # Belirtilen section'ı bul
                    for section in course["sections"]:
                        if section["section"] == selected_section:
                            # Bu section'ın saat slotlarını programa ekle
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
                    break
        
        return {"schedule": schedule}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Program oluşturma hatası: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
