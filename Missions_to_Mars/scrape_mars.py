#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import fnmatch


def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## NASA Mars News


    # Visit https://redplanetscience.com/
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")



    # Get the news title
    headline = soup.find('div', {'class':'content_title'})
    # Get the tesaser text
    paratext = soup.find('div', {'class':'article_teaser_body'})

    #convert to strings
    headlineStr = headline.get_text()
    paratextStr = paratext.get_text()

    print(f"{headlineStr}: {paratextStr}")
    # Close the browser after scraping
    browser.quit()


    ##JPL Mars Space Images—Featured Image

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit https://redplanetscience.com/
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")



    # Get the image url source, appended to the base url
    featured_image_url = url + soup.find('img', {'class':'headerimage'})['src']

    # Close the browser after scraping
    browser.quit()
    featured_image_url

    ## Mars Facts!!

    # Visit https://redplanetscience.com/
    url = "https://galaxyfacts-mars.com/"

    #read in html 
    #take the 2nd table found
    #convert it to html
    #delete all line feeds (\n)

    mars_html_table = pd.read_html(url)[1].to_html().replace('\n', '')
    mars_html_table

    ########
    ## Mars Hemispheres
    ########
    
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit https://redplanetscience.com/
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Close the browser after scraping
    browser.quit()

    # find all links with the correct tag

    link_list = soup.find_all('a', {'class':'itemLink product-item'})
    href = []
    link_titles = []
    for a in link_list:
        if a['href'] != '#':
            link = url + a['href']
            if link not in href:
                href.append(link)
            

    print(href)

    # find all of the images that end with 'thumbnail', grab the alt-text from the image associated with it
    # and strip off the 'enhanced thumbnail' bit, leaving just the name of the hemisphere PHEW

    link_list = soup.find_all('img', {'alt': lambda L: L and L.endswith('thumbnail')})

    hemispheres = []

    for link in link_list:
        name = link['alt']
        name = name.replace(' Enhanced thumbnail', '')
        hemispheres.append(name)
    hemispheres

    # find all links that link to the image directory in each of the four websites found above

    long_list = []
    for a in href:

        # Set up Splinter
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(a)
        html = browser.html
        soup = bs(html, "html.parser")
        long_list.append(soup.find_all('a', {'href': lambda L: L and L.startswith('images')}))
        
        # Close the browser after scraping
        browser.quit()
    long_list

    # the first image in each item is the jpg we want, fortunately, so we can just use index notation to grab it's href
    # for some reason there is a blank link at the end, so the safest way to handle it is just to jump over any duff links.

    jpg = []
    for a in long_list:
        try: 
            link = url + a[0]['href']
            jpg.append(link)
        except IndexError:
            next
            
    jpg

    # zip together the titles and the urls into a dictionary.

    hemisphere_image_urls = []

    for (a,b, c) in zip(hemispheres, jpg, href):
        hemisphere_image_urls.append({
            'title': a,
            'img_url':b,
            'href':c
        })
        
    hemisphere_image_urls
    
    # Store data in a dictionary
    mars_data = {
        "headline": headlineStr,
        "intro": paratextStr,
        "image": featured_image_url,
        "data_table": mars_html_table,
        "image_urls_dict": hemisphere_image_urls
    }


    # Return results
    return mars_data
