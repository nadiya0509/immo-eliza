from scraperNoSelenium import ImmoVlanScraper

try:
    scraper = ImmoVlanScraper()

    # First run these two lines:
    #scraper.get_links_of_houses()
    #scraper.save_links_of_properties("immovlanPropertyLinks.txt")

    # Then run this line:
    #scraper.read_links_of_properties("immovlanPropertyLinks.txt")
    #scraper.save_data_of_properties("immovlanPropertyData.csv")
    
except Exception as ex:
    print(f"Running scraper failed: {ex}")