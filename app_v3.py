import streamlit as st
import pandas as pd
import random

# Veriyi yükle
data = pd.read_csv("courses_202420.csv")
data = data.sort_values(by=['Ders Kodu', 'Ders Section'])

# Sayfa ayarları
st.set_page_config(
    page_title="OZUchedule",
    page_icon="https://favicon.streamlit.app/~/+/media/6d7aed983016f84fb9d23e9cd290577cb8cf1ed4297f756dfb10a1d0.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# OZU logo
st.image("https://www.ozyegin.edu.tr/sites/default/files/logo-tr.png")

# Günler ve saatler
days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]

def generate_dynamic_hours():
    hours = [
        "08:40-09:30", "09:40-10:30", "10:40-11:30", "11:40-12:30", 
        "12:40-13:30", "13:40-14:30", "14:40-15:30", "15:40-16:30", 
        "16:40-17:30", "17:40-18:30"
    ]
    return hours

hours = generate_dynamic_hours()

# Başlık
st.title("OZUchedule Ders Programı Uygulaması")

# Session state başlatma
if 'course_colors' not in st.session_state:
    st.session_state['course_colors'] = {}

if 'selected_courses' not in st.session_state:
    st.session_state['selected_courses'] = []

def get_course_color(course_code):
    if course_code not in st.session_state['course_colors']:
        st.session_state['course_colors'][course_code] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return st.session_state['course_colors'][course_code]

# Program tablosu
schedule = pd.DataFrame(index=hours, columns=days)

def add_course_to_schedule(course, color):
    days_list = course['Saat'].split(" / ")
    for session in days_list:
        if len(session.split(" ")) < 2:
            st.error(f"Gün ve saat aralığı eksik veya yanlış format: {session}")
            continue
        
        day_time = session.split(" ", 1)
        day = day_time[0]  
        time_range = day_time[1].split("-")  

        if len(time_range) < 2:
            st.error(f"Başlangıç ve bitiş saatleri eksik: {session}")
            continue

        start_time = time_range[0].strip()
        end_time = time_range[1].strip()

        matching_slots = [slot for slot in hours if start_time in slot or end_time in slot]
        if not matching_slots:
            st.error(f"Başlangıç saati geçerli değil: {start_time} veya bitiş saati geçerli değil: {end_time}")
            continue
        
        start_index = hours.index(matching_slots[0])
        end_index = hours.index(matching_slots[-1]) + 1

        for i in range(start_index, end_index):
            hour_slot = hours[i]
            section = course['Ders Section']
            if pd.isna(schedule.at[hour_slot, day]):
                schedule.at[hour_slot, day] = f"<span style='background-color:{color};padding:5px'>{section}</span>"
            else:
                st.error(f"{course['Ders Adı']} çakışma yaşıyor: {day}, {hour_slot}")
                existing_content = schedule.at[hour_slot, day]
                schedule.at[hour_slot, day] = f"{existing_content} / <span style='background-color:{color};padding:5px'>{section}</span>"

# Sidebar'da Arama ve Filtreleme
with st.sidebar:
    st.header("Dersler")
    
    # Arama kutusu
    search_term = st.text_input("Ders Ara (Ad veya Kod)")
    
    # Filtreleme seçenekleri
    filter_day = st.selectbox("Güne Göre Filtrele", ["Hepsi"] + days)
    filter_instructor = st.text_input("Hocaya Göre Filtrele")
    
    # Dersleri filtrele
    filtered_data = data
    if search_term:
        filtered_data = filtered_data[
            filtered_data['Ders Adı'].str.contains(search_term, case=False) |
            filtered_data['Ders Kodu'].str.contains(search_term, case=False)
        ]
    if filter_day != "Hepsi":
        filtered_data = filtered_data[filtered_data['Saat'].str.contains(filter_day)]
    if filter_instructor:
        filtered_data = filtered_data[filtered_data['Hoca'].str.contains(filter_instructor, case=False)]
    
    # Filtrelenmiş dersleri göster
    unique_courses = filtered_data.drop_duplicates(subset=['Ders Kodu'])
    
    # Seçilen dersleri kontrol et ve güncelle
    for _, course in unique_courses.iterrows():
        # Dersin seçilip seçilmediğini kontrol et
        is_selected = st.checkbox(
            f"{course['Ders Kodu']} - {course['Ders Adı']}",
            key=f"checkbox_{course['Ders Kodu']}",
            value=any(course['Ders Kodu'] == selected_course[0]['Ders Kodu'] for selected_course in st.session_state['selected_courses'])
        )
        
        if is_selected:
            # Dersin section'larını al
            sections = data[data['Ders Kodu'] == course['Ders Kodu']]
            section_options = sections.apply(
                lambda x: f"{x['Ders Section']} - {x['Hoca']} - {x['Saat']}", axis=1)
            
            # Section seçimi için benzersiz bir key oluştur
            selected_section = st.selectbox(
                f"{course['Ders Kodu']} için section seçin:",
                section_options,
                key=f"selectbox_{course['Ders Kodu']}",
                index=section_options.tolist().index(
                    next(
                        (f"{selected_course[0]['Ders Section']} - {selected_course[0]['Hoca']} - {selected_course[0]['Saat']}"
                         for selected_course in st.session_state['selected_courses']
                         if selected_course[0]['Ders Kodu'] == course['Ders Kodu']),
                        section_options[0]
                    )
                )
            )
            
            # Seçilen section'ın detaylarını al
            selected_section_details = sections[section_options == selected_section].iloc[0]
            
            # Ders zaten seçilmiş mi kontrol et
            if any(course['Ders Kodu'] == selected_course[0]['Ders Kodu'] for selected_course in st.session_state['selected_courses']):
                # Eski section'ı kaldır
                st.session_state['selected_courses'] = [
                    selected_course for selected_course in st.session_state['selected_courses']
                    if selected_course[0]['Ders Kodu'] != course['Ders Kodu']
                ]
            
            # Yeni section'ı ekle
            st.session_state['selected_courses'].append((selected_section_details, get_course_color(selected_section_details['Ders Kodu'])))
        
        # Dersin seçimi kaldırıldıysa, session state'ten de kaldır
        elif not is_selected:
            st.session_state['selected_courses'] = [
                selected_course for selected_course in st.session_state['selected_courses']
                if selected_course[0]['Ders Kodu'] != course['Ders Kodu']
            ]

# Seçilen dersleri programa ekle
st.header("Program")
for course, color in st.session_state['selected_courses']:
    add_course_to_schedule(course, color)

# Tabloyu göster
schedule = schedule.fillna('-')
st.write(schedule.to_html(escape=False), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>SBA7© 2024 - Tüm Hakları Saklıdır</p>", unsafe_allow_html=True)