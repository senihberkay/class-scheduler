#!/usr/bin/env python3
"""
Demo script showing powerful SQLite queries for course data analysis
"""

import sqlite3
import pandas as pd
from utils import load_courses_data

def demonstrate_queries():
    print("🎓 COURSE DATABASE ANALYSIS DEMO")
    print("=" * 50)
    
    # Connect to database
    conn = sqlite3.connect('courses.db')
    
    # 1. Basic Statistics
    print("\n📊 1. DATABASE STATISTICS")
    print("-" * 30)
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM courses")
    total_sections = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT "Ders Kodu") FROM courses')
    unique_courses = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT term) FROM courses")
    unique_terms = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT faculty) FROM courses")
    unique_faculties = cursor.fetchone()[0]
    
    print(f"Total course sections: {total_sections}")
    print(f"Unique courses: {unique_courses}")
    print(f"Terms tracked: {unique_terms}")
    print(f"Faculties: {unique_faculties}")
    
    # 2. Terms breakdown
    print("\n📅 2. COURSES BY TERM")
    print("-" * 30)
    
    query = """
    SELECT term_name, term, COUNT(*) as course_count,
           COUNT(DISTINCT "Ders Kodu") as unique_courses
    FROM courses 
    GROUP BY term_name, term 
    ORDER BY term DESC
    """
    
    df = pd.read_sql_query(query, conn)
    for _, row in df.iterrows():
        print(f"{row['term_name']}: {row['course_count']} sections ({row['unique_courses']} unique courses)")
    
    # 3. Faculty and Program breakdown
    print("\n🏫 3. COURSES BY FACULTY & PROGRAM")
    print("-" * 30)
    
    query = """
    SELECT faculty, program_name, COUNT(*) as course_count
    FROM courses 
    GROUP BY faculty, program_name 
    ORDER BY course_count DESC
    """
    
    df = pd.read_sql_query(query, conn)
    for _, row in df.iterrows():
        print(f"{row['faculty']} - {row['program_name']}: {row['course_count']} courses")
    
    # 4. Most Popular Instructors
    print("\n👨‍🏫 4. TOP INSTRUCTORS (by course count)")
    print("-" * 30)
    
    query = """
    SELECT "Hoca", COUNT(*) as course_count,
           COUNT(DISTINCT "Ders Kodu") as unique_courses
    FROM courses 
    WHERE "Hoca" IS NOT NULL AND "Hoca" != ''
    GROUP BY "Hoca"
    ORDER BY course_count DESC
    LIMIT 10
    """
    
    df = pd.read_sql_query(query, conn)
    for i, row in df.iterrows():
        print(f"{i+1:2d}. {row['Hoca']}: {row['course_count']} sections ({row['unique_courses']} unique courses)")
    
    # 5. Schedule Analysis
    print("\n⏰ 5. SCHEDULE ANALYSIS")
    print("-" * 30)
    
    query = """
    SELECT 
        CASE 
            WHEN "Saat" LIKE '%Pazartesi%' THEN 'Monday'
            WHEN "Saat" LIKE '%Salı%' THEN 'Tuesday'
            WHEN "Saat" LIKE '%Çarşamba%' THEN 'Wednesday'
            WHEN "Saat" LIKE '%Perşembe%' THEN 'Thursday'
            WHEN "Saat" LIKE '%Cuma%' THEN 'Friday'
            WHEN "Saat" LIKE '%Cumartesi%' THEN 'Saturday'
            WHEN "Saat" LIKE '%Pazar%' THEN 'Sunday'
            ELSE 'Other'
        END as day_of_week,
        COUNT(*) as course_count
    FROM courses 
    WHERE "Saat" IS NOT NULL AND "Saat" != ''
    GROUP BY day_of_week
    ORDER BY course_count DESC
    """
    
    df = pd.read_sql_query(query, conn)
    for _, row in df.iterrows():
        print(f"{row['day_of_week']}: {row['course_count']} courses")
    
    # 6. Course Code Analysis
    print("\n📚 6. COURSE DEPARTMENTS (by course code)")
    print("-" * 30)
    
    query = """
    SELECT 
        SUBSTR("Ders Kodu", 1, INSTR("Ders Kodu", ' ') - 1) as department,
        COUNT(*) as course_count,
        COUNT(DISTINCT "Ders Kodu") as unique_courses
    FROM courses 
    WHERE "Ders Kodu" LIKE '% %'
    GROUP BY department
    ORDER BY course_count DESC
    LIMIT 10
    """
    
    df = pd.read_sql_query(query, conn)
    for _, row in df.iterrows():
        print(f"{row['department']}: {row['course_count']} sections ({row['unique_courses']} unique courses)")
    
    # 7. Recent Updates
    print("\n🔄 7. RECENT DATA UPDATES")
    print("-" * 30)
    
    query = """
    SELECT DATE(scraped_at) as date, COUNT(*) as courses_scraped
    FROM courses 
    GROUP BY DATE(scraped_at)
    ORDER BY date DESC
    LIMIT 5
    """
    
    df = pd.read_sql_query(query, conn)
    for _, row in df.iterrows():
        print(f"{row['date']}: {row['courses_scraped']} courses scraped")
    
    conn.close()
    
    # 8. Using the load_courses_data function
    print("\n🔍 8. FILTERED DATA LOADING DEMO")
    print("-" * 30)
    
    # Example: Load only current term MIS courses
    df_filtered = load_courses_data('courses.db', 
                                   term_filter='202510', 
                                   program_filter='BAMIS')
    
    print(f"Loaded {len(df_filtered)} MIS courses for current term")
    
    # Show some sample courses
    if len(df_filtered) > 0:
        print("\nSample courses:")
        sample = df_filtered[['Ders Kodu', 'Ders Adı', 'Hoca', 'Saat']].head(3)
        for _, row in sample.iterrows():
            print(f"  {row['Ders Kodu']}: {row['Ders Adı']} - {row['Hoca']}")

if __name__ == "__main__":
    demonstrate_queries()
