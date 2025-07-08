#Adapted from: https://www.youtube.com/watch?v=XVv6mJpFOb0
from bs4 import BeautifulSoup
import requests

def get_article_text(article_url):
    article_text = requests.get(article_url).text
    return BeautifulSoup(article_text, 'lxml')

def find_audiodrama_title(audiodrama_article):
    title = audiodrama_article.find('h1', id = 'firstHeading').text.replace('(audio story)', '').strip()
    return title 

def get_infobox_data(audiodrama_article):
    infobox_data = audiodrama_article.find('aside', class_ = 'portable-infobox noexcerpt searchaux pi-background pi-theme-infobox pi-layout-default')
    infobox_headings = infobox_data.find_all('h3', 'pi-data-label pi-secondary-font')
    infobox_values = infobox_data.find_all('div', class_ = 'pi-data-value pi-font')
    infobox_data = {}

    

    for heading, value in zip(infobox_headings, infobox_values):
        infobox_data[heading.text] = value.text
    
    print(infobox_data)
    
    return infobox_data


def get_plot_summary(audiodrama_article):
    summary_heading = audiodrama_article.find('span', id = "Publisher's_summary")
    plot_summary = ''

    #Plot summary is contained within <p> tags between the Publisher's summary H2 heading, and the Plot heading

    page_elements = summary_heading.findParent().find_next_siblings()
    for element in page_elements:
        #Find the 'Plot' heading, which is h2
        if element.name == 'h2' and 'Plot' in element.text:
            break
        #Otherwise if it finds text, append the paragraph to the plot summary
        elif element.name == 'p':
            plot_summary = plot_summary + " " + element.text.strip()  

    print(plot_summary)
    return plot_summary 

def assemble_audiodrama_data(article_url):
    audiodrama_article_text = get_article_text(article_url)
    audiodrama_title = find_audiodrama_title(audiodrama_article_text)
    audiodrama_data = get_infobox_data(audiodrama_article_text)
    audiodrama_plot_summary = get_plot_summary(audiodrama_article_text)

    return audiodrama_title

assemble_audiodrama_data('https://tardis.wiki/wiki/Max_Warp_(audio_story)')




