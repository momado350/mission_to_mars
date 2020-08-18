
# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd



# # Mac Users

#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#browser = Browser('chrome', **executable_path, headless=False)


# # Windows Users

# In[5]:

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    import time
    time.sleep(10)
def scrape():
    browser = init_browser()
    final_data = {}
    output = marsNews()
    final_data["mars_title"] = output[0]
    final_data["mars_p"] = output[1]
    final_data["featured_image_url"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()
        
    return final_data
    browser.quit


def marsNews():
    import time
    time.sleep(10)
   # browser = init_browser()
    # Visit the NASA Mars News Site
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html=browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:
        slide_soup = news_soup.select_one("ul.item_list li.slide")
        mars_title = slide_soup.find("div", class_="content_title").text
        mars_p = slide_soup.find("div", class_="article_teaser_body").text
        output = [mars_title, mars_p]
    except AttributeError:
        return None, None    
    return output
    browser.quit
    # ### JPL Mars Space Images - Featured Image

    # In[11]:
def marsImage():
    import time
    browser = init_browser()
    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(10)
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    results = soup.find("ul", class_="articles")
    href = results.find("a",class_='fancybox')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + href
    #featured_image_url
    return featured_image_url
    browser.quit


def marsWeather():
    import time
    browser = init_browser()
    weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(10)
    twitter=browser.html
    twitter_page=BeautifulSoup(twitter, 'html.parser')
    tweet=twitter_page.find('article')
    tweet

    mars_weather=tweet.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    mars_weather=mars_weather[4].text
    #print(mars_weather)
    return mars_weather
    browser.quit

    
def marsFacts():
    import pandas as pd
    browser = init_browser()
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    print(mars_facts)
    return mars_facts
    browser.quit


def marsHem():
    
    import time 
    browser = init_browser()
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
    browser.quit
    



