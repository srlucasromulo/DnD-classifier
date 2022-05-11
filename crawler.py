from urllib.request import urlopen
from bs4 import BeautifulSoup


site_url = 'https://www.dndwiki.io'
monsters_url = 'https://www.dndwiki.io/monsters'
url = monsters_url

monsters_links = []

# while True:
#
#     html = urlopen(url)
#     soup = BeautifulSoup(html, 'html.parser')
#
#     monsters = soup.find_all('a', {'class': 'menu-link-block w-inline-block'})
#
#     monsters_links = monsters_links + [site_url + m['href'] for m in monsters]
#
#     next_button = soup.find_all('a', {'class': 'w-pagination-next pagination-button'})
#     if next_button:
#         url = monsters_url + next_button[0]['href']
#     else:
#         break

url = 'https://www.dndwiki.io/monsters/adult-black-dragon'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

name = soup.find('h1', class_='entry-heading').get_text()
status = soup.find_all('div', class_='monster-stat-entry')
status = [s.find('h2', class_='entry-metalabel-content').get_text() for s in status]

entry_metadata = soup.find_all('div', class_='entry-metadata')

race = entry_metadata[0].find_all('h2', class_='entry-metadata-label')[0].get_text()
alignment = entry_metadata[0].find_all('h2', class_='entry-metadata-label')[2].get_text()
armor_class = entry_metadata[1].find_all('h2', class_='entry-metadata-label')[1].get_text().split()[0]
hit_points = entry_metadata[2].find_all('h2', class_='entry-metalabel-content')[0].get_text().split()[0]

# aqui ja comeca a treta
speed = entry_metadata[3].find_all('h2', class_='entry-metalabel-content')[0].get_text().split(', ')

print(name, race, alignment, armor_class, hit_points, speed)
print(status)
