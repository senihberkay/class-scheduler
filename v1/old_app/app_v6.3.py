import streamlit as st
import pandas as pd
import random
import re

# Veriyi yükle
data = pd.read_csv("courses_202420.csv")
data = data.sort_values(by=['Ders Kodu', 'Ders Section'])

# NaN değerleri kontrol et ve temizle
data['Saat'] = data['Saat'].fillna("")

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

def parse_time_slot(slot):
    match = re.match(r"(\w+)\s+(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})", slot)
    if match:
        day, start_time, end_time = match.groups()
        return day, start_time, end_time
    return None, None, None

def add_course_to_schedule(course, color):
    days_list = course['Saat'].split(" / ")
    for session in days_list:
        day, start_time, end_time = parse_time_slot(session)
        if not day or not start_time or not end_time:
            # st.error(f"Gün ve saat aralığı eksik veya yanlış format: {session}")
            continue
        
        matching_slots = [slot for slot in hours if start_time in slot or end_time in slot]
        if not matching_slots:
            # st.error(f"Başlangıç saati geçerli değil: {start_time} veya bitiş saati geçerli değil: {end_time}")
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

def remove_course_from_schedule(course):
    if isinstance(course['Saat'], str):
        days_list = course['Saat'].split(" / ")
        for session in days_list:
            day, start_time, end_time = parse_time_slot(session)
            if not day or not start_time or not end_time:
                # st.error(f"Gün ve saat aralığı eksik veya yanlış format: {session}")
                continue
            
            matching_slots = [slot for slot in hours if start_time in slot or end_time in slot]
            if not matching_slots:
                # st.error(f"Başlangıç saati geçerli değil: {start_time} veya bitiş saati geçerli değil: {end_time}")
                continue
            
            start_index = hours.index(matching_slots[0])
            end_index = hours.index(matching_slots[-1]) + 1

            for i in range(start_index, end_index):
                hour_slot = hours[i]
                section = course['Ders Section']
                if not pd.isna(schedule.at[hour_slot, day]):
                    existing_content = schedule.at[hour_slot, day]
                    if f"<span style='background-color:{get_course_color(course['Ders Kodu'])};padding:5px'>{section}</span>" in existing_content:
                        # Sadece seçilen bölümün kaldırılması
                        existing_content = existing_content.replace(f"<span style='background-color:{get_course_color(course['Ders Kodu'])};padding:5px'>{section}</span>", "")
                        existing_content = existing_content.replace(" / ", "").strip()
                        if existing_content:
                            schedule.at[hour_slot, day] = existing_content
                        else:
                            schedule.at[hour_slot, day] = pd.NA

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
            filtered_data['Ders Adı'].str.contains(search_term, case=False, na=False) |
            filtered_data['Ders Kodu'].str.contains(search_term, case=False, na=False)
        ]
    if filter_day != "Hepsi":
        filtered_data = filtered_data[filtered_data['Saat'].str.contains(filter_day, na=False)]
    if filter_instructor:
        filtered_data = filtered_data[filtered_data['Hoca'].str.contains(filter_instructor, case=False, na=False)]
    
    # Filtrelenmiş dersleri göster
    unique_courses = filtered_data.drop_duplicates(subset=['Ders Kodu'])

    # Seçilen dersleri kontrol et ve güncelle
    for _, course in unique_courses.iterrows():
        # Dersin seçilip seçilmediğini kontrol et
        is_selected = any(course['Ders Kodu'] == selected_course[0]['Ders Kodu'] and course['Ders Section'] == selected_course[0]['Ders Section'] for selected_course in st.session_state['selected_courses'])
        
        checkbox_key = f"checkbox_{course['Ders Kodu']}_{course['Ders Section']}"
        checkbox_value = st.checkbox(
            f"{course['Ders Kodu']} - {course['Ders Adı']}",
            key=checkbox_key,
            value=is_selected
        )
        
        if checkbox_value:
            # Ders zaten seçilmiş mi kontrol et
            if not is_selected:
                sections = data[data['Ders Kodu'] == course['Ders Kodu']]
                section_options = sections.apply(
                    lambda x: f"{x['Ders Section']} - {x['Hoca']} - {x['Saat']}", axis=1)
                selected_section_key = f"section_{course['Ders Kodu']}_{course['Ders Section']}"
                selected_section = st.selectbox(f"{course['Ders Kodu']} için section seçin:", section_options, key=selected_section_key)
                
                selected_section_details = sections[section_options == selected_section].iloc[0]
                st.session_state['selected_courses'].append((selected_section_details, get_course_color(selected_section_details['Ders Kodu'])))
        else:
            # Dersin seçimi kaldırıldıysa, session state'ten ve programdan kaldır
            st.session_state['selected_courses'] = [
                selected_course for selected_course in st.session_state['selected_courses']
                if not (selected_course[0]['Ders Kodu'] == course['Ders Kodu'] and selected_course[0]['Ders Section'] == course['Ders Section'])
            ]
            # Seçilen dersi programdan kaldır
            remove_course_from_schedule(course)

# Seçilen dersleri programa ekle
schedule = pd.DataFrame(index=hours, columns=days)
for course, color in st.session_state['selected_courses']:
    add_course_to_schedule(course, color)

# Tabloyu göster
schedule = schedule.fillna('-')


# CSS stilleri
css = """
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
    _background-color: #0f1117;
    _background-color: #2c545c;
    margin: 0;
    padding: 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    _background-color: #fff; 
    _background-color: #262730;
    background-color: #0f1117;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
}

th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: center;
}

th {
    background-color: #f2f2f2;
    color: #333;
    border-bottom: 2px solid #ddd;
}

tr:nth-child(even) {
    _background-color: #f9f9f9;
    background-color: #262730;
}

tr:hover {
    _background-color: #f5f5f5;
    background-color: #2c545c;
}

span {
    display: inline-block;
    margin: 2px;
    padding: 5px 10px;
    border-radius: 16px;
    font-weight: bold;
    color: #fff;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

/* Kenarlıkların yumuşatılması */
th:first-child, td:first-child {
    border-left: none;
}

th:last-child, td:last-child {
    border-right: none;
}

tr:first-child th {
    border-top: none;
}

tr:last-child td {
    border-bottom: none;
}

/* Genel sadeleştirme */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    text-align: center;
    margin-bottom: 20px;
}

.logo {
    max-width: 200px;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    margin-top: 20px;
    color: #888;
    font-size: 14px;
}
</style>
"""

# CSS stillerini ekle
st.markdown(css, unsafe_allow_html=True)

# HTML tablosu oluştur
html_table = "<table>"
html_table += "<thead><tr><th>Saat</th>" + "".join(f"<th>{day}</th>" for day in days) + "</tr></thead>"
html_table += "<tbody>"

for hour in hours:
    html_table += f"<tr><td>{hour}</td>"
    for day in days:
        content = schedule.at[hour, day]
        if pd.isna(content) or content == '-':
            html_table += "<td>-</td>"
        else:
            html_table += f"<td>{content}</td>"
    html_table += "</tr>"

html_table += "</tbody></table>"

st.header("Program")
st.markdown(html_table, unsafe_allow_html=True)

# # Debugging: Seçilen dersleri göster
# st.subheader("Seçilen Dersler")
# for course, color in st.session_state['selected_courses']:
#     st.write(f"Ders Kodu: {course['Ders Kodu']}, Ders Section: {course['Ders Section']}, Ders Adı: {course['Ders Adı']}, Hoca: {course['Hoca']}, Saat: {course['Saat']}")

# # Debugging: Session State'i göster
# st.subheader("Session State")
# st.write(st.session_state)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>SBA7© 2024 - Tüm Hakları Saklıdır</p>", unsafe_allow_html=True)