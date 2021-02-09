from splinter import Browser
from bs4 import BeautifulSoup as bs
browser = Browser('chrome')
import time
import pandas as pd
import re
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
   # NASA Mars News Titles
    url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    
    browser.visit(url)
    
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    article_title = soup.find_all('li', class_='slide')[0]
    article_title = article_title.find('div', {"class":'content_title'})
    article_title = article_title.find('a').get_text()
    print(f' ARTICLE TITLE: {article_title}')
    
    # NASA Mars News Text
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    article_p = soup.find('div', class_='article_teaser_body').text.strip()

    # Mars Facts
    mars_df = pd.read_html('http://space-facts.com/mars/',attrs={'id':'tablepress-p-mars-no-2'})
    mars_df = mars_df[0]
    mars_df.columns = ["Category", "Data"]
    mars_df_html = mars_df.to_html(index = False)
    
    
    # Mars Hemispheres
    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    image_url=[]
    browser.visit(mars_url)
    mars_links = browser.find_by_css("a.product-item h3")
    
    
    for i in range(len(mars_links)):
        mars_hemispheres = {}
        browser.find_by_css("a.product-item h3")[i].click()
        mars = browser.links.find_by_text("Sample").first
        mars_hemispheres['img_url'] = mars['href']
        mars_hemispheres['title'] = browser.find_by_css('h2.title').text
        image_url.append(mars_hemispheres)
        browser.back()
        
    for image in image_url:
        print(f' Image url: {image}')

    # Create combine dict
    mars_data = {
        'latest_title': article_title,
        'latest_paragraph': article_p,
        'data_table': mars_df_html,
        'hemisphere': image_url
    }
#     print(f' Data from Mars: {mars_data}')
    return mars_data