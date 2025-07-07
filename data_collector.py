#Adapted from: https://www.youtube.com/watch?v=XVv6mJpFOb0
from bs4 import BeautifulSoup
import requests

website_data_text = requests.get('https://tardis.wiki/wiki/Max_Warp_(audio_story)').text
soup = BeautifulSoup(website_data_text, 'lxml')

#Change this to check for '(audio story)' in the title, and remove it if so. Anthologies too?
audiodrama_title = soup.find('h1', id = 'firstHeading').text.replace('(audio story)', '').strip()
print("Audiodrama title: " + audiodrama_title)
audiodrama_infobox_data = soup.find('aside', class_ = 'portable-infobox noexcerpt searchaux pi-background pi-theme-infobox pi-layout-default')
audiodrama_data_keys = audiodrama_infobox_data.find_all('h3', 'pi-data-label pi-secondary-font')
audiodrama_data_values = audiodrama_infobox_data.find_all('div', class_ = 'pi-data-value pi-font')

#Find plot - Refactor this, once we have more spoons! - Marco
wiki_article_text = soup.find_all('p')
summary_heading = soup.find('span', id = "Publisher's_summary")
plot_summary = ''

page_elements = summary_heading.findParent().find_next_siblings()
for text in page_elements:
    if text.name == 'h2' and text.text.startswith('P'):
        break
    elif text.name == 'p':
        plot_summary = plot_summary + " " + text.text.strip()
    
print(plot_summary)

if len(audiodrama_data_keys) == len(audiodrama_data_values):
    for value_index in range(len(audiodrama_data_values)):
        heading = audiodrama_data_keys[value_index].text.strip()
        value = audiodrama_data_values[value_index].text.strip()
        print(f"{heading} {value}")
else:
    print("Parsing error: number of headings do not match number of values.")

