# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser =  Browser('chrome', **executable_path, headless=False)
    
    # Blank dictionary for storing scraped mars information
    mars_data = {}

    ## NASA Mars News
    # NASA Mars News URL
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Results are returned as an iterable list
    results = soup.find_all('div', class_="slide")

    news = []
    # Loop through returned results to scrape headline and paragraph
    for result in results:
        # Identify and return title of headline
        title = result.find('div', class_="content_title").text
        # Identify and return paragraph of headline
        paragraph = result.find('div', class_="rollover_description_inner").text
        news.append({'title': title, 'paragraph': paragraph})
    
    # Appends the news to mars data
    mars_data["news"] = news


    ## JPL Mars Space Images
    # JPL Mars URL and root URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/'
    root_url = 'https://www.jpl.nasa.gov'

    browser.visit(url)
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    # Creates another BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    featured_image_url_list = []
    # Get featured large, high resolution link to featured image
    for image in soup.find_all('figure', class_='lede'):
        # Store title and paragraph into respective lists
        featured_image_url_list.append(root_url + image.a.get('href'))
        # Appends the featured image to mars data
        mars_data["featured_image"] = featured_image_url_list[0]

    ## Mars Weather
    # Mars Weather Twitter URL
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url) 

    # Creates another BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    mars_weather_list = []
    # Loop through returned results
    for result in soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        # Store tweet in mars weather list
        mars_weather_list.append(result.text)
        # Store first (and most recent) tweet into mars weather
        mars_data["mars_weather"] = mars_weather_list[0]

    ## Mars Facts
    # URL of page to be scraped
    url = 'http://space-facts.com/mars/'

    # Reads the URL as a list
    fact_list = pd.read_html(url)

    # Converts list to dataframe
    fact_df = fact_list[0]

    # Converts the dataframe to an html friendly table
    mars_data["mars_facts"] = fact_df.to_html(header=False, index=False)

    ## Mars Hemispheres
    # Mars Hemispheres URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    images = soup.find('div', class_='result-list')
    hemispheres = images.find_all('div', class_='item')

    # Loop through returned results
    for hemisphere in hemispheres:
        # Narrows down to extract clean title
        title = hemisphere.find('div', class_='description')
        title_text = title.a.text
        title_text = title_text.replace(' Enhanced', '')
        browser.click_link_by_partial_text(title_text)
        time.sleep(5)
        
        # Formats browser URL for parsing
        soup = bs(browser.html, 'html.parser')
        
        img_url = []
        titles = []
        # Narrows down to extract full hemisphere images
        photos = soup.find('div', class_='downloads').find('ul').find('li')
        img = photos.a['href']
        
        # Store image url and image titles into respective lists
        img_url.append(img)
        titles.append(title_text)
        
        browser.click_link_by_partial_text('Back')
        time.sleep(5)
    
    hemisphere_image_urls = []
    # For function to append image title and image url values to dictionary
    for x in range(0,4):
        hemisphere_image_urls.append({'title': titles[x], 'img_url': img_url[x]})
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    
    # Close the browser after scraping
    browser.quit()

    # Return mars data dictionary
    return(mars_data)

print(scrape)