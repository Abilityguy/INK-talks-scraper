import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

"""
Extracts talk data from the talk URL page.
"""
def TalkPageDataExtractor(talkSoup):
    description = ''
    tagList = list()
    recommendedVideoList = list()

    views = talkSoup.find('h3', class_='ink-talk-video-views').text

    descriptionDiv = talkSoup.find('div', class_='ink-col-border-right')

    for para in descriptionDiv.find_all('p'):
        description += para.text

    tagDiv = talkSoup.find('div', class_='ink-profile-topics')

    for tagSpan in tagDiv.find_all('span'):
        tagList.append(tagSpan.text)

    recommendedDivs = talkSoup.find_all('div', class_='ink-talk-item')

    for rDiv in recommendedDivs:
        recommendedUrl = 'http://www.inktalks.com' \
                          + rDiv.find('a', class_='ink-talk-url')['href']
        recommendedId = recommendedUrl.split('/')[4]
        recommendedVideoList.append({'Id':recommendedId, 'Url':recommendedUrl})

    return (views, description, tagList, recommendedVideoList)

"""
Extracts talk data from the talks page of the INK website.

Assumptions:
Expected format of talk URL: http://www.inktalks.com/discover/{talk-Id}/..
talkId is extracted from the talk URL assuming this format
"""
def SearchPageTalkDataExtractor(talkDiv):
    speakersList = list()

    talkUrl = 'http://www.inktalks.com' \
               + talkDiv.find('a', class_='ink-talk-url')['href']
    talkId = talkUrl.split('/')[4]
    talkDuration = talkDiv.find('h6', class_='ink-talk-duration').text
    talkTitle = talkDiv.find('h6', class_='ink-talk-title').text
    talkImageUrl = talkDiv.find('img', class_='img-responsive')['src']
    speakerDiv = talkDiv.find('div', class_='ink-speakers-list')

    for speakerSpan in speakerDiv.find_all('span'):
        speakersList.append(speakerSpan.text)

    return (talkUrl, talkId, talkDuration,
            talkTitle, talkImageUrl, speakersList)

def SaveData(data, filename):
    df = pd.DataFrame(data, columns = ['Id', 'Title', 'Duration', 'Speakers', \
                                        'tags', 'Views', 'Recommended Videos', \
                                        'Description', 'Talk URL', \
                                        'Talk Thumbnail URL'])
    df.to_csv(filename, index=False)

if(__name__ == "__main__"):
    # Talks page of INK website
    website = 'http://www.inktalks.com/talks/everything'

    driver = webdriver.Chrome()
    driver.get(website)
    data = list()
    nTalks = 0
    nextPageExists = True

    saveFilename = 'INKtalks.csv'
    while(nextPageExists):
        try:
            # Wait for 10 seconds until the video cards in the new page
            # are loaded. If not loaded within 10 secs, the program saves data
            # and exits.
            element = WebDriverWait(driver, 10).until( \
                EC.presence_of_element_located((By.CLASS_NAME, \
                                                "ink-talk-item-medium")))
        except:
            driver.quit()
            print("Page taking too long to load")
            SaveData(data, saveFilename)
            print("Number of talks scraped-- ",len(data))
            exit()

        searchPageHtml = driver.page_source
        searchPageSoup = BeautifulSoup(searchPageHtml, 'lxml')

        for talk in searchPageSoup.find_all('div', \
                                            class_='ink-talk-item-medium'):
            # Exract talk data from the talks page.
            talkUrl, talkId, talkDuration, talkTitle, talkImageUrl, \
                    speakersList = SearchPageTalkDataExtractor(talk)

            # A request to retrieve HTML from the talk URL page.
            # This HTML is then used to scrape for some additional stats.
            talkPageHtml = requests.get(talkUrl).text
            talkPageSoup = BeautifulSoup(talkPageHtml, 'lxml')

            views, description, tagList, recommendedVideoList = \
                    TalkPageDataExtractor(talkPageSoup)

            data.append([talkId, talkTitle, talkDuration, speakersList, \
                        tagList, views, recommendedVideoList, description, \
                        talkUrl, talkImageUrl])

        try:
            # Find the 'Next Page' button which retrieves the video cards of the
            # next page. If the 'Next Page' element dosen't exist, then we are
            # in the final page.
            button = driver.find_element_by_link_text('Next Page')
            button.click()

        except NoSuchElementException as e:
            nextPageExists = False

    driver.quit()
    SaveData(data, saveFilename)
    print("Number of talks scraped-- ",len(data))
