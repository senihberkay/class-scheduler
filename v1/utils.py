import json
import yaml
import requests
from bs4 import BeautifulSoup
import pandas as pd

def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def read_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def scrape_mis_courses():
    config = read_config(config_path='config/config.yaml')
    url = config['mis_courses']['scrape_url']
    output_file = config['mis_courses']['scrape_output']

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # courses' HTML tag is <tr>
    rows = soup.find_all('tr')

    course_list = []

    for row in rows:
        td_elements = row.find_all('td')

        # some courses may not have day and time information then pass 
        if len(td_elements) < 3:
            continue

        try:
            # first column courses section (exp. BUS 100.A)
            course_section = td_elements[0].find('a').text.strip()
            # in order to group sections (exp. both BUS 100.A and BUS 100.B sections are BUS 100)
            course_code = course_section.split('.')[0]
            # since course name and course's instructor in one cell splitted 
            course_name = td_elements[1].text.strip().split(',')[0]

            # instructor (check if there is <a> tag)
            instructor_links = td_elements[1].find_all('a')
            if instructor_links:
                instructor = instructor_links[0].text.strip()  # if there is <a> tag
            else:
                instructor = td_elements[1].text.strip()  # else take it a text

            # last column is day and course interval
            schedule_spans = td_elements[2].find_all('span')
            # some courses might have more than one day and time (exp. Salı 14.40-16.30 / Perşembe 13.40-14.30)
            schedule = ' / '.join([span.text.strip() for span in schedule_spans])

            course_list.append([course_code, course_section, course_name, instructor, schedule])
        except AttributeError:
            # if parameters to append not find then pass
            continue


    # course list to pandas dataframe
    df = pd.DataFrame(course_list, columns=['Ders Kodu', 'Ders Section', 'Ders Adı', 'Hoca', 'Saat']).sort_values(by=['Ders Kodu'])
    df.to_csv(output_file, index=False)
    return df
