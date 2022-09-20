# Scraping-Zoon
The site zoon.ru was scraped for all cities of all categories.

Parsing of one category of one city is performed in about 30 seconds, while 300 objects are always taken.
The web driver needs to be installed.

Primary information about:
- Url
- Name
- Address
- Work
- Metro
- Distance
- Tags
- Rating
- Comments

If the parameter is not found, it is assigned the value "Unknown". You can extract additional information by parsing data from the received links.

Launch:
```
python main.py
```
