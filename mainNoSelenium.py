from scraperNoSelenium import ImmoVlanScraper

try:
    scraper = ImmoVlanScraper()

    # All methods work by writing into or reading from
    # internal lists: property_links[1 el = a link to 1 property]
    # and property_data[1 el = parameters for 1 property as a string with ; as a separator].
    #
    # If you want to create a csv file with parameters in one go, use methods 1,3(the input param. will be neglected),4.
    # If you want in addition to create an intermediate txt file with links, use methods 1,2,3,4 (or first 1,2 then 3,4).
    # If you already have a txt file with links, run 3,4 only.
    # 
    # Filters defining searched properties are set at the beginning of ImmoVlanScraper.py in variables FILTER*.
    # Currently searched property is defined as a house or apartment (all subtypes) in the provinces
    # louvain,tervuren,bruxelles,anvers,hasselt, that are on sale (but not on "public sale"/auction?).
    # Note that only 1000 properties will be added to a list/file of links in one run of the progam (so likely no hasselt listings)
    # because of the limitations imposed by immoweb: max 50 pages x 20 properties.
    # You may want to create file of links in several separate steps (note that the output txt file will be overwritten each run,
    # so save previous copies somewhere to be merged later in one file for running the scraping data methods).
    # 
    # Methods 3,4 save the following 7 parameters per property (as defined at the beginning of scrape_data_of_properties method):
    # property_params="Link; Immovlan_code; Location; Subtype; Type; Price in €; Number of bedrooms".
    # Classification into types (house or apartment) is determined in the lists HOUSES_SUBTYPES and APARTMENTS_SUBTYPES,
    # based on the property subtype.
    # Error in finding a particular parameter will produce a row with <- ERROR pointing to the first missing parameter
    # and the rest parameters will be skipped.
    # Individual exception handling would have to be introduced to every parameter to mark with None-s all missing parameters.
    #
    # Because of lack of time, scrapping was only defined in the method scrape_data_of_properties for 6 parameters (plus link),
    # but can be extended further.

    scraper.get_links_of_properties() 
    scraper.save_links_of_properties("immovlanPropertyLinks.txt") # one line per row corresponding to one property 
    scraper.scrape_data_of_properties("immovlanPropertyLinks.txt") # one line per row corresponding to link to one property
    scraper.save_data_of_properties("immovlanPropertyData.csv") # file name should have a csv extention
    
except Exception as ex:
    print(f"Running scraper failed: {ex}")