# INK-talks-scraper

A webscraper that collects data on INK talks from the INKtalks.com website.

## To run
```
pip3 install requirements.txt
python3 web_scraper.py
```

## Data
The ```INKtalks.csv``` file contains video data on INK talks uploaded to the INKtalks.com website upto November 4th, 2020.

### Features
The features in the ```INKtalks.csv``` file are
* Id - The Id of the talk extracted from it's video URL.
* Title - The title of the talk. Includes both speakers and name of the talk.
* Duration - Duration of the talk.
* Speakers - a list of the speakers in the talk.
* Tags - the themes associated with the talk.
* Views - the number of views on the talk.
* Recommended Videos - A list of dictionaries of recommended videos to watch next.
* Description - A description of the talk as provided on the video site.
* Talk URL - The URL of the video talk.
* Talk Thumbnail URL - The URL of the thumbnail image of the talk.

```INKtalks_metadata.csv``` is a reduced dataset with only the Title, Speakers, Talk URL and Talk Thumbnail URL features included.
