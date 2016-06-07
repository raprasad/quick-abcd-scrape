# quick-abcd-scrape
Scrape past events HTML from the ABCD page

# Install

```
mkvirtualenv quick-scrape
pip install -r requirements.txt
```

# Run

This starts at the Past Events page and checks the links.  Any links going to an event detail page within the site are followed--and those detail pages are downloaded.

```
python scrape_old_events.py
```

Shell Output:

```
$ python scrape_old_events.py
----------------------------------------
Check page: http://w3.abcd.harvard.edu/past-events/
----------------------------------------
Download: http://w3.abcd.harvard.edu/past-events/
output_filename: (your path).../quick-abcd-scrape/html_pages/past-events.html
(1) file written: (your path).../quick-abcd-scrape/html_pages/past-events.html
----------------------------------------
Check page: http://w3.abcd.harvard.edu/ai1ec_event/automated-testing/
----------------------------------------
Download: http://w3.abcd.harvard.edu/ai1ec_event/automated-testing/
output_filename: (your path).../quick-abcd-scrape/html_pages/2016_05_11-automated-testing.html
(2) file written: (your path).../quick-abcd-scrape/html_pages/2016_05_11-automated-testing.html
----------------------------------------

(etc, etc)
```

Folder Output

```
html_pages/
  ....
  - 2016_03_09-ed-carlevale-re-imagining-web-development-for-academic-research-centers.html
  - 2016_03_15-user-experience-principles-harvards-teaching-learning-technologies-tlt-2.html
  - 2016_05_11-automated-testing.html
  - past-events.html
```
