#!/usr/bin/env python3
"""
Database management utilities for course scraper
"""

import sqlite3
import argparse
import sys
from datetime import datetime

def show_stats(db_path='courses.db'):
    """Show database statistics"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"📊 Database Statistics for {db_path}")
        print("=" * 50)
        
        # Basic stats
        cursor.execute("SELECT COUNT(*) FROM courses")
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT "Ders Kodu") FROM courses')
        unique_courses = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT term) FROM courses")
        terms = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT faculty) FROM courses")
        faculties = cursor.fetchone()[0]
        
        print(f"Total sections: {total}")
        print(f"Unique courses: {unique_courses}")
        print(f"Terms: {terms}")
        print(f"Faculties: {faculties}")
        
        # Terms breakdown
        print(f"\n📅 Terms:")
        cursor.execute("""
            SELECT term_name, term, COUNT(*) 
            FROM courses 
            GROUP BY term_name, term 
            ORDER BY term DESC
        """)
        
        for row in cursor.fetchall():
            print(f"  {row[0]} ({row[1]}): {row[2]} courses")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"Database file {db_path} not found!")

def clean_old_data(db_path='courses.db', keep_terms=2):
    """Remove old term data, keeping only the most recent terms"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all terms ordered by term code (newest first)
        cursor.execute("SELECT DISTINCT term FROM courses ORDER BY term DESC")
        all_terms = [row[0] for row in cursor.fetchall()]
        
        if len(all_terms) <= keep_terms:
            print(f"Only {len(all_terms)} terms found, nothing to clean.")
            conn.close()
            return
        
        # Terms to delete (older than keep_terms)
        terms_to_delete = all_terms[keep_terms:]
        
        print(f"Keeping {keep_terms} most recent terms...")
        print(f"Will delete {len(terms_to_delete)} older terms: {terms_to_delete}")
        
        # Confirm deletion
        confirm = input("Continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Cancelled.")
            conn.close()
            return
        
        # Delete old data
        for term in terms_to_delete:
            cursor.execute("DELETE FROM courses WHERE term = ?", (term,))
            deleted = cursor.rowcount
            print(f"Deleted {deleted} courses from term {term}")
        
        conn.commit()
        conn.close()
        print("✅ Cleanup completed!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def export_term_data(db_path='courses.db', term=None, output_file=None):
    """Export specific term data to CSV"""
    try:
        conn = sqlite3.connect(db_path)
        
        if term is None:
            # Get latest term
            cursor = conn.cursor()
            cursor.execute("SELECT term FROM courses ORDER BY term DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                term = result[0]
            else:
                print("No data found in database!")
                return
        
        if output_file is None:
            output_file = f"courses_{term}.csv"
        
        # Export data
        import pandas as pd
        query = "SELECT * FROM courses WHERE term = ? ORDER BY \"Ders Kodu\""
        df = pd.read_sql_query(query, conn, params=(term,))
        
        df.to_csv(output_file, index=False)
        print(f"✅ Exported {len(df)} courses from term {term} to {output_file}")
        
        conn.close()
        
    except Exception as e:
        print(f"Export error: {e}")

def vacuum_db(db_path='courses.db'):
    """Optimize database by running VACUUM"""
    try:
        conn = sqlite3.connect(db_path)
        print("Running database optimization...")
        conn.execute("VACUUM")
        conn.close()
        print("✅ Database optimized!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Course Database Management Utilities')
    parser.add_argument('--db', default='courses.db', help='Database file path')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    
    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean old term data')
    clean_parser.add_argument('--keep', type=int, default=2, 
                             help='Number of recent terms to keep (default: 2)')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export term data to CSV')
    export_parser.add_argument('--term', help='Term code to export (default: latest)')
    export_parser.add_argument('--output', help='Output CSV file (default: courses_TERM.csv)')
    
    # Vacuum command
    vacuum_parser = subparsers.add_parser('vacuum', help='Optimize database')
    
    args = parser.parse_args()
    
    if args.command == 'stats':
        show_stats(args.db)
    elif args.command == 'clean':
        clean_old_data(args.db, args.keep)
    elif args.command == 'export':
        export_term_data(args.db, args.term, args.output)
    elif args.command == 'vacuum':
        vacuum_db(args.db)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
