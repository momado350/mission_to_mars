#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup 
import time

#Site Navigation
 
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)    
# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_title"] = output[0]
    final_data["mars_p"] = output[1]
    featured_image_url=base_url+resource_name
    final_data["featured_image_url"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data
    # # NASA Mars News
def marsNews():
    import time
    url = "https://mars.nasa.gov/news/"
    time.sleep(5)
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    slide_soup = news_soup.select_one("ul.item_list li.slide")
    slide_soup.find("div", class_="content_title")
    mars_title = slide_soup.find("div", class_="content_title").get_text()
    mars_p = slide_soup.find("div", class_="article_teaser_body").get_text()
    
    output = [mars_title, mars_p]
    #return mars_news
    return output
    # # JPL Mars Space Images - Featured Image
def marsImage():
    import time
    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(1)
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    new_page=browser.html
    feature_src=BeautifulSoup(new_page, 'html.parser')
    img_src=feature_src.find('img', class_='main_image')
    resource_name=img_src['src']
    base_url='https://jpl.nasa.gov'
    featured_image_url=base_url+resource_name
    return featured_image_url
# # Mars Weather
def marsWeather():
    import time
    weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(5)
    twitter=browser.html
    twitter_page=BeautifulSoup(twitter, 'html.parser')
    tweet=twitter_page.find('article')
    mars_weather=tweet.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    mars_weather=mars_weather[4].text
    
    return mars_weather
# # Mars Facts
def marsFacts():
    import pandas as pd
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    return mars_facts
# # Mars Hemispheres
def marsHem():
    import time 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    return mars_hemisphere