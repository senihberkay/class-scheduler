import streamlit as st
import pandas as pd
import random
import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import plotly.express as px

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

def strip_html_tags(text):
    """HTML etiketlerini temizler"""
    clean = re.sub(r'<.*?>', '', text)
    return clean.strip()

def _add_course_to_schedule(course, color):
    days_list = course['Saat'].split(" / ")
    for session in days_list:
        day, start_time, end_time = parse_time_slot(session)
        if not day or not start_time or not end_time:
            st.error(f"Gün ve saat aralığı eksik veya yanlış format: {session}")
            continue
        
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
                # Çakışan dersleri kırmızı renkle göster
                schedule.at[hour_slot, day] = f"{schedule.at[hour_slot, day]} / <span style='background-color:red;padding:5px'>{section}</span>"
                st.error(f"{course['Ders Adı']} ({section}) çakışma yaşıyor: {day}, {hour_slot}. Mevcut ders: {schedule.at[hour_slot, day]}")

def add_course_to_schedule(course, color):
    """Dersleri programa ekler ve çakışmaları kontrol eder."""
    days_list = course['Saat'].split(" / ")
    for session in days_list:
        day, start_time, end_time = parse_time_slot(session)
        if not day or not start_time or not end_time:
            st.error(f"Gün ve saat aralığı eksik veya yanlış format: {session}")
            continue
        
        matching_slots = [slot for slot in hours if start_time in slot or end_time in slot]
        if not matching_slots:
            st.error(f"Başlangıç saati geçerli değil: {start_time} veya bitiş saati geçerli değil: {end_time}")
            continue
        
        start_index = hours.index(matching_slots[0])
        end_index = hours.index(matching_slots[-1]) + 1

        for i in range(start_index, end_index):
            hour_slot = hours[i]
            section = course['Ders Section']

            # HTML formatında renkli ders bilgisi
            course_html = f"<span style='background-color:{color};padding:5px'>{section}</span>"

            if pd.isna(schedule.at[hour_slot, day]):
                # Çakışma yoksa dersi ekle (RENKLİ)
                schedule.at[hour_slot, day] = course_html
            else:
                # Çakışan dersi al ve HTML etiketlerini temizle
                existing_content = schedule.at[hour_slot, day]
                clean_existing_content = strip_html_tags(existing_content)
                new_entry = f"{existing_content} / {course_html}"

                # Çakışma mesajı (ancak RENGİ KORU)
                schedule.at[hour_slot, day] = new_entry
                st.error(f"{course['Ders Adı']} ({section}) çakışma yaşıyor: {day}, {hour_slot}. Mevcut ders: {clean_existing_content}")

def remove_course_from_schedule(course):
    """Seçilen dersi programdan kaldırır."""
    # Dersin programdan kaldırılacağı gün ve saatleri belirle
    days_list = course['Saat'].split(" / ")
    
    for session in days_list:
        day, start_time, end_time = parse_time_slot(session)
        if not day or not start_time or not end_time:
            continue
        
        matching_slots = [slot for slot in hours if start_time in slot or end_time in slot]
        if not matching_slots:
            continue
        
        start_index = hours.index(matching_slots[0])
        end_index = hours.index(matching_slots[-1]) + 1

        for i in range(start_index, end_index):
            hour_slot = hours[i]
            section = course['Ders Section']

            # Eğer ders bu saat diliminde varsa kaldır
            if not pd.isna(schedule.at[hour_slot, day]):
                existing_content = schedule.at[hour_slot, day]

                # Seçilen section'ı kaldır
                section_str = f"<span style='background-color:{get_course_color(course['Ders Kodu'])};padding:5px'>{section}</span>"
                if section_str in existing_content:
                    existing_content = existing_content.replace(section_str, "").replace(" / ", "").strip()

                # Eğer satır tamamen boş kaldıysa NaN yap
                schedule.at[hour_slot, day] = existing_content if existing_content else pd.NA

    # Seçili derslerden tamamen kaldır
    st.session_state['selected_courses'] = [
        selected_course for selected_course in st.session_state['selected_courses']
        if not (selected_course[0]['Ders Kodu'] == course['Ders Kodu'])
    ]

def visualize_schedule(schedule):
    # DataFrame'i uzun forma çevir
    schedule_long = schedule.reset_index().melt(id_vars=['index'], var_name='Gün', value_name='Ders')

    # Kolonları düzenle
    schedule_long.rename(columns={'index': 'Saat'}, inplace=True)

    # NaN olan hücreleri temizle
    schedule_long = schedule_long.dropna()

    # Boş dersleri filtrele
    schedule_long = schedule_long[schedule_long['Ders'] != '-']

    # Grafik oluşturma
    fig = px.scatter(schedule_long, x='Gün', y='Saat', text='Ders', 
                     title='Ders Programı Görselleştirme', 
                     labels={'Gün': 'Gün', 'Saat': 'Saat'},
                     size_max=60)
    
    # Text etiketlerini ekleyerek göster
    fig.update_traces(textposition='top center')
    st.plotly_chart(fig)

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
        is_selected = st.checkbox(
            f"{course['Ders Kodu']} - {course['Ders Adı']}",
            key=f"checkbox_{course['Ders Kodu']}",
            value=any(course['Ders Kodu'] == selected_course[0]['Ders Kodu'] and course['Ders Section'] == selected_course[0]['Ders Section'] for selected_course in st.session_state['selected_courses'])
        )
        
        if is_selected:
            # Ders zaten seçilmiş mi kontrol et
            if not any(course['Ders Kodu'] == selected_course[0]['Ders Kodu'] and course['Ders Section'] == selected_course[0]['Ders Section'] for selected_course in st.session_state['selected_courses']):
                sections = data[data['Ders Kodu'] == course['Ders Kodu']]
                section_options = sections.apply(
                    lambda x: f"{x['Ders Section']} - {x['Hoca']} - {x['Saat']}", axis=1)
                selected_section_key = f"section_{course['Ders Kodu']}_{hash(str(course['Ders Section']))}"
                selected_section = st.selectbox(f"{course['Ders Kodu']} için section seçin:", section_options, key=selected_section_key)
                
                selected_section_details = sections[section_options == selected_section].iloc[0]
                st.session_state['selected_courses'].append((selected_section_details, get_course_color(selected_section_details['Ders Kodu'])))
            else:
                # Zaten seçilmişse, mevcut seçimi bul ve göster
                for i, selected_course in enumerate(st.session_state['selected_courses']):
                    if selected_course[0]['Ders Kodu'] == course['Ders Kodu'] and selected_course[0]['Ders Section'] == course['Ders Section']:
                        selected_section_details = selected_course[0]
                        break
                
                sections = data[data['Ders Kodu'] == course['Ders Kodu']]
                section_options = sections.apply(
                    lambda x: f"{x['Ders Section']} - {x['Hoca']} - {x['Saat']}", axis=1)
                selected_section_key = f"section_{course['Ders Kodu']}_{hash(str(course['Ders Section']))}"
                selected_section = st.selectbox(f"{course['Ders Kodu']} için section seçin:", section_options, key=selected_section_key, index=section_options.tolist().index(f"{selected_section_details['Ders Section']} - {selected_section_details['Hoca']} - {selected_section_details['Saat']}"))
                
                # Seçilen bölümün session state'de güncellenmesi
                selected_section_details = sections[section_options == selected_section].iloc[0]
                st.session_state['selected_courses'][i] = (selected_section_details, get_course_color(selected_section_details['Ders Kodu']))
        else:
            # Dersin seçimi kaldırıldıysa, session state'ten ve programdan kaldır
            st.session_state['selected_courses'] = [
                selected_course for selected_course in st.session_state['selected_courses']
                if not (selected_course[0]['Ders Kodu'] == course['Ders Kodu'] and selected_course[0]['Ders Section'] == course['Ders Section'])
            ]
            # Seçilen dersi programdan kaldır
            remove_course_from_schedule(course)

# Seçilen dersleri programa ekle
st.header("Program")
schedule = pd.DataFrame(index=hours, columns=days)
for course, color in st.session_state['selected_courses']:
    add_course_to_schedule(course, color)

# Tabloyu göster
schedule = schedule.fillna('-')
st.write(schedule.to_html(escape=False), unsafe_allow_html=True)

# Ders Programını Görselleştirme
st.subheader("Ders Programı Görselleştirme")
visualize_schedule(schedule)

# Ders Programını PDF Olarak İndirme
def create_pdf(schedule):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Ders Programı")
    y = 730
    for day in schedule.columns:
        p.drawString(100, y, f"{day}:")
        y -= 20
        for hour in schedule.index:
            if schedule.at[hour, day] != '-':
                p.drawString(120, y, f"{hour}: {schedule.at[hour, day]}")
                y -= 20
    p.save()
    buffer.seek(0)
    return buffer

if st.button("Ders Programını PDF Olarak İndir"):
    pdf_buffer = create_pdf(schedule)
    st.download_button(
        label="PDF İndir",
        data=pdf_buffer,
        file_name="ders_programi.pdf",
        mime="application/pdf"
    )

# Ders Programını Excel Olarak İndirme
def create_excel(schedule):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        schedule.to_excel(writer, sheet_name='Ders Programı')
    output.seek(0)
    return output

if st.button("Ders Programını Excel Olarak İndir"):
    excel_buffer = create_excel(schedule)
    st.download_button(
        label="Excel İndir",
        data=excel_buffer,
        file_name="ders_programi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Ders Programını Sıfırlama Butonu
if st.button("Ders Programını Sıfırla"):
    st.session_state['selected_courses'] = []
    st.rerun()

# Seçilen Derslerin Detaylarını Gösterme
st.subheader("Seçilen Dersler")
for course, color in st.session_state['selected_courses']:
    st.write(f"""
        **Ders Kodu:** {course['Ders Kodu']}  
        **Ders Adı:** {course['Ders Adı']}  
        **Section:** {course['Ders Section']}  
        **Hoca:** {course['Hoca']}  
        **Saat:** {course['Saat']}
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>SBA7© 2024 - Tüm Hakları Saklıdır</p>", unsafe_allow_html=True)