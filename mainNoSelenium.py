from scraperNoSelenium import ImmoVlanScraper

try:
    scraper = ImmoVlanScraper()

    # You can first run these two lines:
    #scraper.get_links_of_properties()
    #scraper.save_links_of_properties("immovlanPropertyLinks.txt")

    # ... and then run the two lines below:
    scraper.scrape_data_of_properties("immovlanPropertyLinks.txt")
    scraper.save_data_of_properties("immovlanPropertyData.csv")

    # ... or you can run all four lines together.
    
except Exception as ex:
    print(f"Running scraper failed: {ex}")