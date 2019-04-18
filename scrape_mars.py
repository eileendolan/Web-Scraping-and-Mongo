def scrape():

    # Import Dependencies 
    from bs4 import BeautifulSoup
    from splinter import Browser
    import requests
    import pandas as pd


    # ## NASA Mars News

    # The executable path to driver for Mac user
    # Launch Mars Nasa News website on Chrome
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)

    # HTML object and Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # Retrieve latest news: title and paragraph
    news_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    news_p = soup.find("li", class_="slide").find("div", class_="article_teaser_body").text

    #  Mars Space Images - Featured Image

    # Mars Space Images: splinter module
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)


    # HTML object and Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # Scraping featured image url 
    featured_img_1 = "https://www.jpl.nasa.gov"
    featured_img_url = soup.find("div", class_="carousel_items").find("article")["style"]
    featured_img_2 = featured_img_url.split("'")[1]
    featured_img_2 = featured_img_1 + featured_img_2
    featured_img_2


    # ## Mars Weather: Tweet


    # Visit Mars Weather via Twitter 
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # HTML Object and Parse HTML with Beautiful Soup
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, 'html.parser')

    # Find the latest tweet elements
    tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Retrieve all elements that contain news title in the specified scope
    # Look for weather related words and prevent non weather related tweets 
    for tweet in tweets: 
    mars_weather = tweet.find('p').text
    if 'Sol' and 'pressure' in mars_weather:
    print(mars_weather)
    break
    else: 
    pass

    # ## Mars Facts


    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use the `read_html` to parse the url
    mars_url = pd.read_html(facts_url)

    # Find the mars url df in the list and assign it to mars df
    mars_df = mars_url[0]

    # Name the columns
    mars_df.columns = ['Name','Value']

    # Set the index to the Name column without row indexing
    mars_df.set_index('Name', inplace=True)

    # Save html 
    mars_df.to_html()

    # Show mars data frame
    mars_df


    # ## Mars Hemispheres


    # Visit main and mars hemispheres urls 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Main url
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
    # Store title
    title = i.find('h3').text

    # Store link to full image website
    partial_img_url = i.find('a', class_='itemLink product-item')['href']

    # Visit the link that has the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)

    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html

    # Parse HTML with Beautiful Soup for hemisphere information 
    soup = BeautifulSoup( partial_img_html, 'html.parser')

    # Retrieve full image 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']

    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})


    # all info dictionary

    mars_info_dict = {'news_title': news_title,
            'news_p': news_p,
            'image_url_featured ': image_url_featured ,
            'mars_weather': mars_weather,
            'mars_facts': mars_df,
            'hemisphere_image_urls': hemisphere_image_urls
            }

    return mars_info_dict
