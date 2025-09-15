# Course Scraper for Özyeğin University

This scraper extracts course information from Özyeğin University's course catalog system with user-friendly configuration.

## Quick Start

1. Edit `config/config.yaml` with user-friendly names:

```yaml
mis_courses:
  scrape_url: "https://www.ozyegin.edu.tr/tr/acilan-dersler"
  scrape_output: "courses.csv"  # or "courses.db" for SQLite
  scrape_term: "2025 - 2026 Güz"
  scrape_faculty: "İşletme Fakültesi"
  scrape_program: "Yönetim Bilişim Sistemleri"
```

2. Run the scraper:
```bash
python scrape.py
```

## Configuration Options

### User-Friendly Configuration (Recommended)

Use human-readable names that are automatically mapped to the correct codes:

```yaml
mis_courses:
  scrape_url: "https://www.ozyegin.edu.tr/tr/acilan-dersler"
  scrape_output: "courses.csv"
  scrape_term: "2025 - 2026 Güz"  # Will be mapped to "202510"
  scrape_faculty: "Business"  # English alias for "İşletme Fakültesi"
  scrape_program: "Yönetim Bilişim Sistemleri"  # Will be mapped to "BAMIS"
```

### Advanced Configuration

You can also mix user-friendly names with direct codes:

```yaml
mis_courses:
  scrape_url: "https://www.ozyegin.edu.tr/tr/acilan-dersler"
  scrape_output: "courses.csv"
  scrape_term: "202510"  # Direct term code
  scrape_faculty: "İşletme Fakültesi"  # Turkish faculty name
  scrape_program: "BAMIS"  # Direct program code
```

### Legacy Configuration (Backward Compatibility)

```yaml
mis_courses:
  scrape_url: "https://www.ozyegin.edu.tr/tr/acilan-dersler?program=BAMIS"
  scrape_output: "courses.csv"
```

## Available Terms (User-Friendly Names)

- **"2026 - 2027 Yaz"** → 202630
- **"2026 - 2027 Bahar"** → 202620  
- **"2026 - 2027 Güz"** → 202610
- **"2025 - 2026 Yaz"** → 202530
- **"2025 - 2026 Bahar"** → 202520
- **"2025 - 2026 Güz"** → 202510 (current default)
- **"2024 - 2025 Yaz"** → 202430
- **"2024 - 2025 Bahar"** → 202420
- **"2024 - 2025 Güz"** → 202410

You can also use direct term codes (6 digits) like "202510".

## Available Faculties

### Turkish Names
- İşletme Fakültesi
- Mühendislik Fakültesi
- Sosyal Bilimler Fakültesi
- Hukuk Fakültesi
- Mimarlık ve Tasarım Fakültesi
- Uygulamalı Bilimler Fakültesi
- Havacılık ve Uzay Bilimleri Fakültesi

### English Aliases
- **"Business"** → İşletme Fakültesi
- **"Engineering"** → Mühendislik Fakültesi
- **"Law"** → Hukuk Fakültesi
- **"Social Sciences"** → Sosyal Bilimler Fakültesi
- **"Architecture"** → Mimarlık ve Tasarım Fakültesi
- **"Applied Sciences"** → Uygulamalı Bilimler Fakültesi
- **"Aviation"** → Havacılık ve Uzay Bilimleri Fakültesi

## Available Programs

### İşletme Fakültesi (Business Faculty)
- **"Yönetim Bilişim Sistemleri"** → BAMIS
- **"İşletme"** → BABUS
- **"Girişimcilik"** → BAENT
- **"Uluslararası Finans"** → BABAF
- **"Ekonomi"** → BAECON
- **"Uluslararası Ticaret ve İşletmecilik"** → BAIBUS
- **"Uluslararası İşletmecilik ve Ticaret"** → BAIB

### Mühendislik Fakültesi (Engineering Faculty)
- **"Bilgisayar Mühendisliği"** → BACS
- **"Elektrik-Elektronik Mühendisliği"** → BAEE
- **"Endüstri Mühendisliği"** → BAIE
- **"Makine Mühendisliği"** → BAME
- **"İnşaat Mühendisliği"** → BACE

### Other Faculties
- **"Uluslararası İlişkiler"** → BAIR (Social Sciences)
- **"Psikoloji"** → BAPSY (Social Sciences)
- **"Hukuk"** → BALAW (Law)
- **"Mimarlık"** → BAARC (Architecture)

You can also use direct program codes like "BAMIS", "BABUS", etc.

## Mapping Files

The scraper uses three mapping files for user-friendly configuration:

- `config/term_mapping.yaml` - Maps friendly term names to codes
- `config/faculty_mapping.yaml` - Maps faculty names and English aliases
- `config/program_mapping.yaml` - Maps program names to codes by faculty

These files are automatically loaded and used to convert user-friendly names to the correct internal codes.

## Configuration Examples

### Example 1: Computer Science Student
```yaml
mis_courses:
  scrape_url: "https://www.ozyegin.edu.tr/tr/acilan-dersler"
  scrape_output: "cs_courses.csv"
  scrape_term: "2025 - 2026 Güz"
  scrape_faculty: "Engineering"
  scrape_program: "Bilgisayar Mühendisliği"
```

### Example 2: Business Student (Mixed Format)
```yaml
mis_courses:
  scrape_url: "https://www.ozyegin.edu.tr/tr/acilan-dersler"
  scrape_output: "business_courses.csv"
  scrape_term: "202520"  # Direct code
  scrape_faculty: "Business"  # English alias
  scrape_program: "İşletme"  # Turkish name
```

### Example 3: All Business Faculty Courses
```yaml
mis_courses:
  scrape_url: "https://www.ozyegin.edu.tr/tr/acilan-dersler"
  scrape_output: "all_business.csv"
  scrape_term: "2025 - 2026 Güz"
  scrape_faculty: "İşletme Fakültesi"
  # Don't specify program to get all programs in the faculty
```

## Output Formats

The scraper supports two output formats:

### CSV Output (Default)
```yaml
scrape_output: "courses.csv"
```

### SQLite Database Output 
```yaml
scrape_output: "courses.db"
```

When using SQLite output (`.db` extension), the scraper automatically:
- Creates a `courses` table with proper schema
- Handles duplicate course sections (replaces existing data)
- Adds timestamps for data tracking
- Provides database statistics after scraping

The SQLite table schema:
```sql
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT NOT NULL,                    -- Term code (e.g., "202510")
    term_name TEXT,                        -- User-friendly term (e.g., "2025 - 2026 Güz")
    faculty TEXT,                          -- Faculty name (e.g., "İşletme Fakültesi")
    program TEXT,                          -- Program code (e.g., "BAMIS")
    program_name TEXT,                     -- Program name (e.g., "Yönetim Bilişim Sistemleri")
    "Ders Kodu" TEXT NOT NULL,             -- Course code (e.g., "BUS 100")
    "Ders Section" TEXT NOT NULL,          -- Course section (e.g., "BUS 100.A")
    "Ders Adı" TEXT NOT NULL,              -- Course name
    "Hoca" TEXT,                           -- Instructor
    "Saat" TEXT,                           -- Schedule
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(term, "Ders Section") ON CONFLICT REPLACE
);
```

### Advanced SQLite Queries

With the enhanced schema, you can perform powerful queries:

```sql
-- Get all courses for current term
SELECT * FROM courses WHERE term = '202510';

-- Compare a course across different terms
SELECT term_name, "Hoca", "Saat" 
FROM courses 
WHERE "Ders Kodu" = 'BUS 100' 
ORDER BY term;

-- Count courses by faculty and term
SELECT faculty, term_name, COUNT(*) as course_count
FROM courses 
GROUP BY faculty, term_name;

-- Find courses taught by specific instructor
SELECT DISTINCT "Ders Kodu", "Ders Adı", term_name
FROM courses 
WHERE "Hoca" LIKE '%PROF%'
ORDER BY "Ders Kodu";

-- Get latest data for each course
SELECT "Ders Kodu", "Ders Adı", MAX(scraped_at) as latest_update
FROM courses 
GROUP BY "Ders Kodu";
```

### Demo Script

Run `python demo_queries.py` to see advanced analytics capabilities including:
- Multi-term course comparisons
- Instructor analysis
- Schedule distribution
- Department breakdowns
- Historical data tracking

## Database Management

### Database Statistics
```bash
python db_manager.py stats
```

### Clean Old Data
```bash
# Keep only the 2 most recent terms
python db_manager.py clean --keep 2
```

### Export Term Data
```bash
# Export latest term to CSV
python db_manager.py export

# Export specific term
python db_manager.py export --term 202510 --output fall_2025.csv
```

### Optimize Database
```bash
python db_manager.py vacuum
```

## Output

The scraper shows the mapping process:
```
Configuration:
  Term: 2025 - 2026 Güz → 202510
  Faculty: Business → İşletme Fakültesi
  Program: Yönetim Bilişim Sistemleri → BAMIS
```

Then scrapes and saves courses to the specified format (CSV or SQLite).

### CSV Format
Saves courses to CSV with columns:
- **Ders Kodu**: Course code (e.g., "BUS 100")
- **Ders Section**: Course section (e.g., "BUS 100.A")
- **Ders Adı**: Course name in Turkish
- **Hoca**: Instructor name
- **Saat**: Schedule information

### SQLite Format  
Saves courses to SQLite database with additional features:
- **Historical data tracking** - Multiple terms in same database
- **Rich metadata** - Term, faculty, and program information
- **Advanced filtering** - Query by term, faculty, or program
- **Duplicate handling** - Unique constraint on (term, section)
- **Timestamps** - Track when data was scraped
- **Relational queries** - Compare courses across terms

## Requirements

```bash
pip install requests beautifulsoup4 pandas PyYAML
```
