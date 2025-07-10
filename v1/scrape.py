###########
# run this file when courses updated or when it is new semester
###########

from utils import scrape_mis_courses, read_config

def main():
    config = read_config(config_path='config/config.yaml')
    print(f"Scraping courses from {config['mis_courses']['scrape_url']}")
    df = scrape_mis_courses()
    print(f"Scraped {len(df)} courses.")
    print(f"Data saved to {config['mis_courses']['scrape_output']}")
    
    # check
    print("\nFirst few courses:")
    print(df.head())

if __name__ == "__main__":
    main()
