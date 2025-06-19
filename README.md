# immo-eliza

## Description

The code allows to scrape https://immovlan.be/fr website for properties of certain types and location,
and to write url-s as well as values of 6 parameters of the properties into a csv file.
These parameters are: Location, Subtype; Type; Price in €; Number of bedrooms.
When any of these parameters is missing, a <- ERROR message will appear in the csv file.
It points to an empty cell with the first problematic parameter.

In the defaul mode an extra file with url-s of the properties is also produced.

In the current set-up the code searches for only houses and apartments (of various sub-types), on normal sale,
in the provinces of Louvain, Tervuren, Bruxelles, Anvers, and Hasselt.
Note, however, that out of 2074 filtered properties on immovlan only 1000 have been scraped, because of the
limitation of maximum 50 pages shown in immovlan.
An extra work would be needed to search per smaller groups of provinces, merge all resulting url files into one,
and re-running the code on this full file to produce output for all filtered properties. 

## Installation

The project was done in the virtual environment, requirements.txt is supplied.
In particular, libraries - requests and fake_headers - were used to gain access to the website
(alternative would be to use a selenium.webdriver, but it would cause constant pop-up of the windows
and probably slow down of the code).
BeautifulSoup library was used to navigate between tags of the source code of the webpages.   

## Usage

Launch mainNoSelenium.py: see description there how you can choose which combination of methods to run
(depending on yes/no on producing url and parameters' files in one versus two runs; yes/no on producing a separate url file).

## Notes

TO DO: 
- Replace empty cells in rows with <- ERROR message with None-s.
- Get rest of the parameters scraped.
- Make list of groups of provinces resulting in less than 1000 properties/url-s
  and loop the code through it until 10,000 properties are scraped.  
