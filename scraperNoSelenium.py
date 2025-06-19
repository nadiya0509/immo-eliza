from fake_headers import Headers
import random
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs
import re
import csv

class ImmoVlanScraper:
    """
    The filters below select only houses and apartments for sale in the locations
    in the FILTER_LOCATIONS list (e.g. public sales are not selected).
    Immoveb truncates output to 50 pages -> 1000 properties.
    """
    
    TOP_URL="https://immovlan.be"
    FILTER_SALE = "/fr/immobilier?transactiontypes=a-vendre&"
    FILTER_TYPE = "propertytypes=maison,appartement&"
    FILTER_SUBTYPE = "propertysubtypes=maison,villa,immeuble-mixte,maison-de-maitre,bungalow,fermette,chalet,chateau," \
    "appartement,rez-de-chaussee,penthouse,studio,duplex,loft,triplex&"
    FILTER_LOCATION = "municipals=louvain,tervuren,bruxelles,anvers,hasselt&" # !!!!!!!!!!!
    FIRST_PAGE_INDEX="noindex=1"

    def __init__(self) -> None:
        
        self.property_links = [] # list of links per individual property
        self.property_data = [] # list of dictionary per house: "code":, "location":, "type":, "price":...
        #self.HOUSES_SUBTYPES=['Maison','Villa', 'Immeuble mixte', 'Maison de maître','Bungalow','Fermette','Chalet','Château']
        #self.APARTMENTS_SUBTYPES=['Appartement','Rez-de-chausée','Studio','Duplex','Penthouse','Loft','Triplex']                

    def get_links_of_properties(self) -> None:
        """
        Retrieve links of properties on sale and save them in the list self.property_links.
        Returns:
            list[dict]: List of houses on sale with their data.
        """
        
        # Open first page per province
        province_page_link=self.TOP_URL+self.FILTER_SALE+self.FILTER_TYPE+self.FILTER_SUBTYPE+self.FILTER_LOCATION+self.FIRST_PAGE_INDEX
        
        #urljoin(TOP_URL,FILTER_SALE,FILTER_TYPE,FILTER_SUBTYPE,FILTER_LOCATION,FIRST_PAGE_INDEX)
            
        # Step through pages for this location
        morePages=True
        while morePages:  

            # Fetch links to individual houses on the page, and save them to self.houses_links list
            #print("Current page link: ", province_page_link)
            
            headers = self.get_headers()
            response = requests.get(province_page_link, headers=headers) # for immovlan without headers parameter will not work                                                  # for zimmo does not work whether using hearders or not
            html_content = response.text
            soup_main=bs(html_content,'html.parser')

            # Get links of all houses at this page (max 20 on immovlan)
            link_house="Error scraping link of a property at page "+province_page_link
            media_pics = soup_main.find_all('div', class_='media-pic')
            for media_pic in media_pics:
                link_house = media_pic.find('a').get('href')
                self.property_links.append(link_house)
                #print(link_house)             

            # Find link to the next page of the same province
            a_tags = soup_main.find_all('a', class_='page-link')
            link_next_page=""
            for a_tag in a_tags:
                href = a_tag.get('href')
                text = a_tag.text
                if text and text.strip()=="Suivant":
                    link_next_page=self.TOP_URL+href
                    province_page_link=link_next_page
                    break
            if(link_next_page==""): # no next page finish link search
                morePages=False
            

    def save_links_of_properties(self,file_name) -> None:
        """
        Saves data on properties to txt file
        """
        with open(file_name, 'w') as file:
            for item in self.property_links:
                file.write(f"{item}\n")
        print(f"Done writing property links in {file_name}.")
        print(f"Number of links: ", len(self.property_links))
                     

    def fill_property_links_list_from_txt_file(self, file_name) -> None:
        """
        Reads file with links to individual properties, one per line, e.g.
        https://immovlan.be/fr/detail/maison/a-vendre/8480/ichtegem/rbt70221/
        and fills in self.property_links list if it was empty (in the mainNoSelenium.py the two sets of methods
        are executed separately), otherwise use already filled in list (filled after
        executing the first set of two methods).
        """
        if (len(self.property_links) == 0):
            with open(file_name, 'r') as file:
                for line in file:
                    self.property_links.append(line.strip()) 
                  

    def get_headers(self) -> dict:
        """
        Generate randomized, realistic HTTP headers to reduce request blocking. 
        The function selects random combinations of browser and OS
        to generate diverse and legitimate-looking headers.
        """
        browsers = ["chrome", "firefox", "opera", "safari", "edge"]
        os_choices = ["win", "mac", "linux"]
        headers = Headers(
            browser=random.choice(browsers),
            os=random.choice(os_choices),
            headers=True
            )
        return headers.generate()


    def scrape_data_of_properties(self, file_name) -> None:
        """
        Notes on types:
        Assumes that properties are of type "house" or "apartment" (based on sub-types in the liks themselves
        and whether they belong to self.HOUSES_SUBTYPES or self.APARTMENTS_SUBTYPES);
        other sub-types will get type "other", and if sub-type can't be scraped from the link itself - type "unknown".
        """
        HOUSES_SUBTYPES=['maison','villa', 'immeuble-mixte','maison-de-maitre','bungalow','fermette','chalet','chateau']
        APARTMENTS_SUBTYPES=['appartement','rez-de-chaussee','studio','duplex','penthouse','loft','triplex']

        self.fill_property_links_list_from_txt_file(file_name)

        self.property_data.append("Filters: "+self.TOP_URL+self.FILTER_SALE+self.FILTER_TYPE+self.FILTER_SUBTYPE+self.FILTER_LOCATION)
        column_separ="; "
        property_params="Link; Immovlan_code; Location; Subtype; Type; Price in €; Number of bedrooms" # !!!!!!!!!!! column names
        self.property_data.append(property_params)

        for link_property in self.property_links:

            #print("Property link: ", link_property)
            property_data=link_property+column_separ

            try:

                headers = self.get_headers()
                response = requests.get(link_property, headers=headers) # for immovlan without headers parameter will not work                                                  # for zimmo does not work whether using hearders or not
                html_content = response.text
                soup_house=bs(html_content,'html.parser')
 
                main_span = soup_house.find('span', class_='detail__header_title_main')
                vlancode = main_span.find('span', class_='vlancode').text.strip(); property_data += (vlancode+column_separ)
                location = main_span.find('span', class_='d-none d-lg-inline').text.strip().split('- ')[-1]; property_data += (location+column_separ)
                sub_type_property_detail = main_span.find(string=True, recursive=False).text.strip()
                
                # property type/subtype from the link itself
                match = re.search(r'/detail/([^/]+)/', link_property)
                if match:
                    sub_type_property = match.group(1)
                    if sub_type_property in HOUSES_SUBTYPES:
                        type_property="house"
                    elif sub_type_property in APARTMENTS_SUBTYPES:
                        type_property = "appartment"
                    else:
                        type_property = "other"
                else:
                    sub_type_property = sub_type_property_detail
                    type_property = "unknown"
                property_data += (sub_type_property+column_separ)
                property_data += (type_property+column_separ) 

                main_span=soup_house.find('span', class_='detail__header_price_data')
                price_orig = main_span.find(string=True, recursive=False).text.strip()
                price_euro = price_orig.replace('\u202F', '').replace('€', '')
                property_data += (price_euro+column_separ)

                num_bdr=soup_house.find('h4', string='Nombre de chambres à coucher').find_next_sibling('p').text.strip()
                property_data += (num_bdr+column_separ)

            except Exception as ex:

                property_data = property_data + f"; <- ERROR : {ex}"          

            self.property_data.append(property_data)        

        print(f"Done reading property data from {file_name}") 


    def save_data_of_properties(self,file_name):
        """
        Saves data on properties to csv file
        """
        with open(file_name, mode='w', newline='', encoding='utf-8') as csvf:
            writer = csv.writer(csvf)
            for el in self.property_data:
                writer.writerow([el])
        print(f"Done writing property data in {file_name}, number of rows: {len(self.property_data)-2} plus search filters and header")    
