#Adapted from: https://www.youtube.com/watch?v=XVv6mJpFOb0
from bs4 import BeautifulSoup
import requests

def get_article_text(article_url):
    #Use requests to get the article's HTML, parse it using BeautifulSoup and LXML
    article_text = requests.get(article_url).text
    return BeautifulSoup(article_text, 'lxml')

def find_audiodrama_title(audiodrama_article):
    #Find the title of the audiodrama, which is in the article title, remove the '(audio story)' section and any whitespace 
    title = audiodrama_article.find('h1', id = 'firstHeading').text.replace('(audio story)', '').strip()
    return title 

def get_infobox_data(audiodrama_article):
    #Find the infobox for the wiki article for the audiodrama
    infobox_data = audiodrama_article.find('aside', class_ = 'portable-infobox noexcerpt searchaux pi-background pi-theme-infobox pi-layout-default')

    #Find the infobox headings and values, and put them in a dictionary of [infobox heading] : [infobox value]
    infobox_headings = infobox_data.find_all('h3', 'pi-data-label pi-secondary-font')
    infobox_values = infobox_data.find_all('div', class_ = 'pi-data-value pi-font')
    infobox_data = {}

    for heading, value in zip(infobox_headings, infobox_values):
        infobox_data[heading.text.replace(":", "")] = value.text
    
    return infobox_data


def get_plot_summary(audiodrama_article):
    #Find the publisher's summary heading
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

    return plot_summary 

def assemble_audiodrama_data(article_url):
    #Find the article text for the URL, and pass it through to the above functions
    audiodrama_article_text = get_article_text(article_url)
    audiodrama_title = find_audiodrama_title(audiodrama_article_text)
    audiodrama_infobox_data = get_infobox_data(audiodrama_article_text)
    audiodrama_plot_summary = get_plot_summary(audiodrama_article_text)

    set_audiodrama_data(audiodrama_title, audiodrama_infobox_data, audiodrama_plot_summary)

        

    return audiodrama_title

def set_audiodrama_data(title, infobox_data, plot_summary):
    #Create a dictionary of scraped audiodrama data from the wiki page's title heading, it's infobox, and the found plot summary
    #Prefill in dictionary
    audiodrama_data = {'Title' : '', 'Number of parts' : '', 'Release number' : '', 'Release date' : '', 'Doctor' : '', 'Companion(s)' : '', 'Plot_Summary' : '', 'Main setting' : '', 'Main enemy' : '', 'Writer' : '', 'Director' : '', 'Producer' : '', 'Music' : '', 'Sound' : '', 'Cover Art' : ''}
    #Manually set values which have different headings compared to the infobox
    audiodrama_data['Title'] = title
    audiodrama_data['Plot_Summary'] = plot_summary
    audiodrama_data['Cover Art'] = infobox_data['Cover by']

    #Loop through the infobox data, and fill in the relevant headings with their values
    for heading in infobox_data:
        if heading in audiodrama_data:
            audiodrama_data[heading] = infobox_data[heading]
    
    for key in audiodrama_data:
        print(f"{key}: {audiodrama_data[key]}")
    
    return audiodrama_data


assemble_audiodrama_data('https://tardis.wiki/wiki/Max_Warp_(audio_story)')




