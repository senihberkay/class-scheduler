#!/usr/bin/env python3
"""
Helper script to show available configuration options for the course scraper.
"""

import yaml
from utils import load_mappings

def show_available_options():
    """Display all available configuration options"""
    print("=" * 60)
    print("COURSE SCRAPER - AVAILABLE CONFIGURATION OPTIONS")
    print("=" * 60)
    
    try:
        mappings = load_mappings()
        
        # Show available terms
        print("\n📅 AVAILABLE TERMS:")
        print("-" * 20)
        terms = mappings['terms']['terms']
        default_term = mappings['terms'].get('default_term', 'Not specified')
        
        for term_name, term_code in sorted(terms.items(), key=lambda x: x[1], reverse=True):
            marker = " (DEFAULT)" if term_name == default_term else ""
            print(f"  '{term_name}' → {term_code}{marker}")
        
        # Show available faculties
        print("\n🏛️  AVAILABLE FACULTIES:")
        print("-" * 22)
        faculties = mappings['faculties']['faculties']
        aliases = mappings['faculties'].get('aliases', {})
        default_faculty = mappings['faculties'].get('default_faculty', 'Not specified')
        
        print("  Turkish Names:")
        for faculty in sorted(faculties.keys()):
            marker = " (DEFAULT)" if faculty == default_faculty else ""
            print(f"    '{faculty}'{marker}")
        
        if aliases:
            print("\n  English Aliases:")
            for alias, turkish_name in sorted(aliases.items()):
                print(f"    '{alias}' → {turkish_name}")
        
        # Show available programs by faculty
        print("\n🎓 AVAILABLE PROGRAMS:")
        print("-" * 21)
        
        programs = mappings['programs']
        default_program = programs.get('default_program', 'Not specified')
        
        for faculty_key, program_list in programs.items():
            if faculty_key.endswith('_faculty') and isinstance(program_list, dict):
                faculty_display = faculty_key.replace('_faculty', '').replace('_', ' ').title()
                print(f"\n  {faculty_display} Faculty:")
                for program_name, program_code in sorted(program_list.items()):
                    marker = " (DEFAULT)" if program_code == default_program else ""
                    print(f"    '{program_name}' → {program_code}{marker}")
        
        # Show direct codes
        if 'codes' in programs:
            print("\n  Direct Program Codes (can be used directly):")
            for code in sorted(programs['codes'].keys()):
                marker = " (DEFAULT)" if code == default_program else ""
                print(f"    '{code}'{marker}")
        
        # Show configuration examples
        print("\n" + "=" * 60)
        print("CONFIGURATION EXAMPLES")
        print("=" * 60)
        
        print("\n1. User-Friendly Configuration (Recommended):")
        print("```yaml")
        print("mis_courses:")
        print("  scrape_url: \"https://www.ozyegin.edu.tr/tr/acilan-dersler\"")
        print("  scrape_output: \"courses.csv\"")
        print(f"  scrape_term: \"{default_term}\"")
        print(f"  scrape_faculty: \"{default_faculty}\"")
        print("  scrape_program: \"Yönetim Bilişim Sistemleri\"")
        print("```")
        
        print("\n2. Using English Aliases:")
        print("```yaml")
        print("mis_courses:")
        print("  scrape_url: \"https://www.ozyegin.edu.tr/tr/acilan-dersler\"")
        print("  scrape_output: \"courses.csv\"")
        print(f"  scrape_term: \"{default_term}\"")
        print("  scrape_faculty: \"Business\"")
        print(f"  scrape_program: \"{default_program}\"")
        print("```")
        
        print("\n3. Direct Codes:")
        print("```yaml")
        print("mis_courses:")
        print("  scrape_url: \"https://www.ozyegin.edu.tr/tr/acilan-dersler\"")
        print("  scrape_output: \"courses.csv\"")
        print("  scrape_term: \"202510\"")
        print(f"  scrape_faculty: \"{default_faculty}\"")
        print(f"  scrape_program: \"{default_program}\"")
        print("```")
        
        print("\n4. Legacy Format (Backward Compatibility):")
        print("```yaml")
        print("mis_courses:")
        print(f"  scrape_url: \"https://www.ozyegin.edu.tr/tr/acilan-dersler?program={default_program}\"")
        print("  scrape_output: \"courses.csv\"")
        print("```")
        
        print("\n" + "=" * 60)
        print("To use these options, edit config/config.yaml and run: python scrape.py")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error loading mappings: {e}")
        print("Make sure mapping files exist in config/ directory")

if __name__ == "__main__":
    show_available_options()
