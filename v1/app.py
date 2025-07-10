import streamlit as st
import pandas as pd
import random

# data = pd.read_csv("courses.csv")
# Veriyi yükle
data = pd.read_csv("courses_202420.csv")
data = data.sort_values(by=['Ders Kodu', 'Ders Section'])

st.set_page_config(page_title="OZUchedule",
                page_icon="https://favicon.streamlit.app/~/+/media/6d7aed983016f84fb9d23e9cd290577cb8cf1ed4297f756dfb10a1d0.png", 
                layout="wide",
                initial_sidebar_state="expanded")

# OZU logo
st.image("https://www.ozyegin.edu.tr/sites/default/files/logo-tr.png")

days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]

# class time intervals
def generate_dynamic_hours():
    hours = [
        "08:40-09:30", "09:40-10:30", "10:40-11:30", "11:40-12:30", 
        "12:40-13:30", "13:40-14:30", "14:40-15:30", "15:40-16:30", 
        "16:40-17:30", "17:40-18:30"
    ]
    return hours

hours = generate_dynamic_hours()

st.title("OZUchedule Ders Programı Uygulaması")

# course and color relation created and colors will remain constant
if 'course_colors' not in st.session_state:
    st.session_state['course_colors'] = {}

# assign colors to each of the lessons 
def get_course_color(course_code):
    if course_code not in st.session_state['course_colors']:
        st.session_state['course_colors'][course_code] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return st.session_state['course_colors'][course_code]

schedule = pd.DataFrame(index=hours, columns=days)

def add_course_to_schedule(course, color):
    days_list = course['Saat'].split(" / ")
    for session in days_list:
        # since day and hour intervals are together in courses it is splitted
        if len(session.split(" ")) < 2:
            st.error(f"Gün ve saat aralığı eksik veya yanlış format: {session}") # check courses.csv file
            continue
        
        day_time = session.split(" ", 1)
        day = day_time[0]  
        time_range = day_time[1].split("-")  

        if len(time_range) < 2:
            st.error(f"Başlangıç ve bitiş saatleri eksik: {session}") # check courses.csv file
            continue

        start_time = time_range[0].strip()
        end_time = time_range[1].strip()

        # time intervals on schedule 
        matching_slots = [slot for slot in hours if start_time in slot or end_time in slot]
        if not matching_slots:
            st.error(f"Başlangıç saati geçerli değil: {start_time} veya bitiş saati geçerli değil: {end_time}") # check courses.csv file
            continue
        
        start_index = hours.index(matching_slots[0])
        end_index = hours.index(matching_slots[-1]) + 1

        for i in range(start_index, end_index):
            hour_slot = hours[i]
            section = course['Ders Section']  # Section bilgisi ile tabloyu güncelliyoruz
            if pd.isna(schedule.at[hour_slot, day]):
                schedule.at[hour_slot, day] = f"<span style='background-color:{color};padding:5px'>{section}</span>"
            else:
                st.error(f"{course['Ders Adı']} çakışma yaşıyor: {day}, {hour_slot}")
                existing_content = schedule.at[hour_slot, day]
                schedule.at[hour_slot, day] = f"{existing_content} / <span style='background-color:{color};padding:5px'>{section}</span>"

# Sidebar'da Ders Listesi ve Section Seçimi
selected_courses = []

with st.sidebar:
    st.header("Dersler")
    
    # TODO: add search and filter courses on the sidebar
    
    unique_courses = data.drop_duplicates(subset=['Ders Kodu'])

    for _, course in unique_courses.iterrows():
        if st.checkbox(f"{course['Ders Kodu']} - {course['Ders Adı']}"):
            sections = data[data['Ders Kodu'] == course['Ders Kodu']]
            section_options = sections.apply(
                lambda x: f"{x['Ders Section']} - {x['Hoca']} - {x['Saat']}", axis=1)
            selected_section = st.selectbox(f"{course['Ders Kodu']} için section seçin:", section_options)
            
            selected_section_details = sections[section_options == selected_section].iloc[0]
            selected_courses.append((selected_section_details, get_course_color(selected_section_details['Ders Kodu'])))

# append selected courses into the program
# st.header("Program")
st.subheader("📅 Ders Programı")

# table width and height adjustments based on the number of hours (rows) and days (columns)
num_hours = len(hours)
num_days = len(days)

# call add_course_to_schedule func. for each classes
for course, color in selected_courses:
    add_course_to_schedule(course, color)

# NaN to -
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
# display the program as a table (HTML supported cell styles)
# st.write(schedule.to_html(escape=False), unsafe_allow_html=True)
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
st.markdown(html_table, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center;'>SBA7© 2024 - Tüm Hakları Saklıdır</p>", unsafe_allow_html=True)
