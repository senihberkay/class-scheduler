import json
import yaml
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import os

def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def read_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def load_mappings():
    """Load all mapping files for terms, faculties, and programs"""
    mappings = {}
    
    # Load term mapping
    try:
        with open('config/term_mapping.yaml', 'r', encoding='utf-8') as f:
            mappings['terms'] = yaml.safe_load(f)
    except FileNotFoundError:
        mappings['terms'] = {'terms': {}, 'default_term': '2025 - 2026 Güz'}
    
    # Load faculty mapping
    try:
        with open('config/faculty_mapping.yaml', 'r', encoding='utf-8') as f:
            mappings['faculties'] = yaml.safe_load(f)
    except FileNotFoundError:
        mappings['faculties'] = {'faculties': {}, 'default_faculty': 'İşletme Fakültesi'}
    
    # Load program mapping
    try:
        with open('config/program_mapping.yaml', 'r', encoding='utf-8') as f:
            mappings['programs'] = yaml.safe_load(f)
    except FileNotFoundError:
        mappings['programs'] = {'codes': {}, 'default_program': 'BAMIS'}
    
    return mappings


def resolve_term_code(term_name, mappings):
    """Convert user-friendly term name to term code"""
    if not term_name:
        return None
    
    # If it's already a code (6 digits), return as is
    if isinstance(term_name, str) and term_name.isdigit() and len(term_name) == 6:
        return term_name
    
    # Look up in mapping
    term_mapping = mappings['terms']['terms']
    return term_mapping.get(term_name)


def resolve_faculty_name(faculty_name, mappings):
    """Resolve faculty name (including aliases)"""
    if not faculty_name:
        return None
    
    # Check direct mapping
    faculties = mappings['faculties']['faculties']
    if faculty_name in faculties:
        return faculties[faculty_name]
    
    # Check aliases
    aliases = mappings['faculties'].get('aliases', {})
    if faculty_name in aliases:
        return aliases[faculty_name]
    
    # Return as is if not found (might be correct already)
    return faculty_name


def resolve_program_code(program_name, mappings):
    """Convert user-friendly program name to program code"""
    if not program_name:
        return None
    
    # If it's already a code, check if valid
    codes = mappings['programs']['codes']
    if program_name in codes:
        return codes[program_name]
    
    # Search in all faculty programs
    for faculty_key, programs in mappings['programs'].items():
        if faculty_key.endswith('_faculty') and isinstance(programs, dict):
            if program_name in programs:
                return programs[program_name]
    
    # Return as is if not found (might be correct already)
    return program_name


def save_courses_data(df, output_file, term_info=None):
    """Save courses data to CSV or SQLite based on file extension"""
    file_extension = os.path.splitext(output_file)[1].lower()
    
    if file_extension == '.db':
        # Save to SQLite database
        conn = sqlite3.connect(output_file)
        
        # Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL,
            term_name TEXT,
            faculty TEXT,
            program TEXT,
            program_name TEXT,
            "Ders Kodu" TEXT NOT NULL,
            "Ders Section" TEXT NOT NULL,
            "Ders Adı" TEXT NOT NULL,
            "Hoca" TEXT,
            "Saat" TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(term, "Ders Section") ON CONFLICT REPLACE
        )
        """
        conn.execute(create_table_query)
        
        # Add metadata columns to dataframe if term_info is provided
        if term_info:
            df = df.copy()
            df['term'] = term_info.get('term_code')
            df['term_name'] = term_info.get('term_name')
            df['faculty'] = term_info.get('faculty')
            df['program'] = term_info.get('program_code')
            df['program_name'] = term_info.get('program_name')
            
            # Reorder columns to match database schema
            column_order = ['term', 'term_name', 'faculty', 'program', 'program_name', 
                           'Ders Kodu', 'Ders Section', 'Ders Adı', 'Hoca', 'Saat']
            df = df[column_order]
        
        # Insert data - append mode to keep historical data
        df.to_sql('courses', conn, if_exists='append', index=False)
        
        conn.close()
        print(f"Data saved to SQLite database: {output_file}")
        
        # Show some stats
        conn = sqlite3.connect(output_file)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM courses")
        count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(DISTINCT "Ders Kodu") FROM courses')
        unique_courses = cursor.fetchone()[0]
        
        if term_info:
            cursor.execute("SELECT COUNT(*) FROM courses WHERE term = ?", (term_info.get('term_code'),))
            current_term_count = cursor.fetchone()[0]
            print(f"Added {current_term_count} courses for {term_info.get('term_name')}")
        
        cursor.execute("SELECT COUNT(DISTINCT term) FROM courses")
        unique_terms = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"Database contains {count} total course sections from {unique_courses} unique courses across {unique_terms} terms")
        
    else:
        # Default to CSV (no metadata for CSV)
        df.to_csv(output_file, index=False)
        print(f"Data saved to CSV file: {output_file}")


def load_courses_data(file_path, term_filter=None, faculty_filter=None, program_filter=None):
    """Load courses data from CSV or SQLite based on file extension with optional filters"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.db':
        # Load from SQLite database
        if not os.path.exists(file_path):
            print(f"Database file {file_path} not found!")
            return pd.DataFrame()
        
        conn = sqlite3.connect(file_path)
        
        # Build query with filters
        query = 'SELECT * FROM courses'
        conditions = []
        params = []
        
        if term_filter:
            conditions.append('term = ?')
            params.append(term_filter)
        if faculty_filter:
            conditions.append('faculty = ?')
            params.append(faculty_filter)
        if program_filter:
            conditions.append('program = ?')
            params.append(program_filter)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY "Ders Kodu"'
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
        
    else:
        # Default to CSV (no filtering for CSV)
        if not os.path.exists(file_path):
            print(f"CSV file {file_path} not found!")
            return pd.DataFrame()
        
        return pd.read_csv(file_path)


def scrape_mis_courses():
    config = read_config(config_path='config/config.yaml')
    mappings = load_mappings()
    
    base_url = config['mis_courses']['scrape_url']
    output_file = config['mis_courses']['scrape_output']
    
    # Get user-friendly parameters and resolve them
    user_term = config['mis_courses'].get('scrape_term')
    user_faculty = config['mis_courses'].get('scrape_faculty')
    user_program = config['mis_courses'].get('scrape_program')
    
    # Resolve to actual codes/names
    scrape_term = resolve_term_code(user_term, mappings)
    scrape_faculty = resolve_faculty_name(user_faculty, mappings)
    scrape_program = resolve_program_code(user_program, mappings)
    
    print(f"Configuration:")
    if user_term:
        print(f"  Term: {user_term} → {scrape_term}")
    if user_faculty:
        print(f"  Faculty: {user_faculty} → {scrape_faculty}")
    if user_program:
        print(f"  Program: {user_program} → {scrape_program}")
    
    session = requests.Session()
    
    # If we have the old style config (URL with program parameter), use direct GET
    if '?program=' in base_url or (not scrape_term and not scrape_faculty and not scrape_program):
        print("Using direct URL approach")
        response = session.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        # Use the new form-based approach
        print("Using form-based approach")
        # Build URL with query parameters
        url_params = []
        if scrape_term:
            url_params.append(f"term={scrape_term}")
        if scrape_faculty:
            url_params.append(f"faculty={scrape_faculty}")
        if scrape_program:
            url_params.append(f"program={scrape_program}")
        
        if url_params:
            url = f"{base_url}?{'&'.join(url_params)}"
        else:
            url = base_url
        
        print(f"Trying URL: {url}")
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # If that doesn't work, try the form submission approach
        if not soup.find_all('tr'):
            print("No table rows found, trying form submission")
            initial_response = session.get(base_url)
            initial_soup = BeautifulSoup(initial_response.content, 'html.parser')
            
            form = initial_soup.find('form', {'id': 'ozuacilanDersler-block-form'})
            if form:
                form_build_id = form.find('input', {'name': 'form_build_id'})['value']
                
                # Prepare form data
                form_data = {
                    'form_build_id': form_build_id,
                    'form_id': '_ozu_acilanDersler_form'
                }
                
                if scrape_term:
                    form_data['term'] = scrape_term
                if scrape_faculty:
                    form_data['faculty'] = scrape_faculty
                if scrape_program:
                    form_data['program'] = scrape_program
                
                print(f"Form data: {form_data}")
                response = session.post(base_url, data=form_data)
                soup = BeautifulSoup(response.content, 'html.parser')
    
    print(f"Response status code: {response.status_code}")
    
    # Look for tables
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")

    # courses' HTML tag is <tr>
    rows = soup.find_all('tr')
    print(f"Found {len(rows)} table rows")

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
        except AttributeError as e:
            # if parameters to append not find then pass
            continue
        except Exception as e:
            continue


    # course list to pandas dataframe
    df = pd.DataFrame(course_list, columns=['Ders Kodu', 'Ders Section', 'Ders Adı', 'Hoca', 'Saat']).sort_values(by=['Ders Kodu'])
    
    # Prepare metadata for database storage
    term_info = {
        'term_code': scrape_term,
        'term_name': user_term,
        'faculty': scrape_faculty,
        'program_code': scrape_program,
        'program_name': user_program
    }
    
    # Save data based on file extension
    save_courses_data(df, output_file, term_info)
    
    return df
