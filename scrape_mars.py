# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

# Dictionary 
mars_info = {}


# NASA MARS NEWS
def scrape_mars_news():
#    try: 
 
        browser = init_browser()
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info


# FEATURED IMAGE
def scrape_mars_image():
 #   try: 
 
        browser = init_browser()
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)

        html_image = browser.html
        soup = BeautifulSoup(html_image, 'html.parser')
 
        mars_image = soup.find_all('img')[3]['src']

        main_url = 'https://www.jpl.nasa.gov'

        featured_image_url = main_url + mars_image

        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info

        
# MARS WEATHER 
def scrape_mars_weather():
 #   try: 

        browser = init_browser()
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        html_weather = browser.html
        soup = BeautifulSoup(html_weather, 'html.parser')

        latest_tweets = soup.find_all('p', class_='tweet-text')
 
        for tweet in latest_tweets: 
            mars_weather_text = tweet.text
            if 'pressure' and 'daylight' in mars_weather_text:
                mars_weather = mars_weather_text.split('pic.twitter.com')[0]
                break
            else: 
                pass

        mars_info['weather_tweet'] = mars_weather
        
        return mars_info


# MARS FACTS
def scrape_mars_facts():
 
    facts_url = 'http://space-facts.com/mars/'

    mars_facts = pd.read_html(facts_url)

    mars_facts_df = mars_facts[0]

    mars_facts_df.columns = ['Property','Value']

    mars_facts_df.set_index('Property', inplace=True)

    mars_facts_html = mars_facts_df.to_html()

    mars_info['mars_facts'] = mars_facts_html

    return mars_info


# MARS HEMISPHERES
def scrape_mars_hemispheres():
 #   try: 
 
        browser = init_browser() 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        html_hemispheres = browser.html
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        images = soup.find_all('div', class_='item')

        hemisphere_image_urls = []

        hemispheres_original_url = 'https://astrogeology.usgs.gov' 

        for image in images: 
            title = image.find('img', class_='thumb')['alt']
            partial_image_url = image.find('img', class_='thumb')['src'] 
            image_url = hemispheres_original_url + partial_image_url
            hemisphere_image_urls.append({"title" : title, "img_url" : image_url})

        mars_info['mars_hemispheres'] = hemisphere_image_urls

        print(hemisphere_image_urls)

        return mars_info
