from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #declare urls
    url1 = 'https://redplanetscience.com/'
    url2 = 'https://spaceimages-mars.com/'
    url3 = 'https://galaxyfacts-mars.com/'
    url4 = 'https://marshemispheres.com/'

    results = {}

    #scrape news
    browser.visit(url1)
    html = browser.html
    soup = bs(html, 'html.parser')

    results['news_title'] = soup.find('div', class_='content_title').text
    results['news_p'] = soup.find('div', class_='article_teaser_body').text
    
    #scrape featured image
    browser.visit(url2)
    html = browser.html
    soup = bs(html, 'html.parser')

    results['featured_image_url'] = url2 + soup.find('img', class_='headerimage')['src']

    #scrape facts in pandas
    tables = pd.read_html(url3)
    #select table for mars facts
    mars_facts_df = tables[0]
    #rename columns
    renamed_mars_facts_df = mars_facts_df.rename(columns={0:'Description', 1:'Mars', 2:'Earth'})
    #render html table from pandas
    mars_facts_table = renamed_mars_facts_df.to_html(index=False)
    #clean 
    results['final_mars_facts_table'] = mars_facts_table.replace('\n', '')

    #scrape 4 hemispheres
    browser.visit(url4)
    html = browser.html
    soup = bs(html, 'html.parser')

    #get 4 hemispheres
    hemispheres = soup.find_all('div', class_='description')

    #set up hemi url list
    hemisphere_image_urls = []

    #loop through each hemisphere div
    for hemi in hemispheres:
        hemi_dict = {}
        
        #extract hemisphere title
        hemi_title = hemi.find('h3').text
        
        #go to the link in div
        browser.links.find_by_partial_text(hemi_title).click()
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, 'html.parser')
        
        #pull href to complete image urls
        temp_div = hemi_soup.find('div', class_='downloads')
        hemi_image = temp_div.find('a')['href']
        hemi_image_link = url4 + hemi_image
        
        #add values to dictionary
        hemi_dict['title'] = hemi_title
        hemi_dict['img_url'] = hemi_image_link
        
        #add dictionary to list hemisphere_image_urls
        hemisphere_image_urls.append(hemi_dict)
        
        #go back a page
        browser.back()

    results['hemisphere_image_urls'] = hemisphere_image_urls


    #results["headline"] = soup.find("a", class_="title").get_text()
    #results["price"] = soup.find("h4", class_="price").get_text()
    #results["reviews"] = soup.find("p", class_="pull-right").get_text()

    # Quit the browser
    browser.quit()



    return results