import re
from urllib.request import urlopen, Request
import pandas as pd
from bs4 import BeautifulSoup
from monster import Monster

difficulties = {
    'Harmless': 0,
    'Trivial': 1,
    'Easy': 2,
    'Medium': 3,
    'Hard': 4,
    'Challenging': 5
}

occurrences = {
    'Common': 1,
    'Uncommon': 3,
    'Rare': 2,
    'Very Rare': 4
}

monsters_types = [
    'https://www.tibiawiki.com.br/wiki/Anf%C3%ADbios',
    'https://www.tibiawiki.com.br/wiki/Aqu%C3%A1ticos',
    'https://www.tibiawiki.com.br/wiki/Aves',
    'https://www.tibiawiki.com.br/wiki/Constructos',
    'https://www.tibiawiki.com.br/wiki/Criaturas_M%C3%A1gicas',
    'https://www.tibiawiki.com.br/wiki/Dem%C3%B4nios',
    'https://www.tibiawiki.com.br/wiki/Drag%C3%B5es',
    'https://www.tibiawiki.com.br/wiki/Elementais',
    'https://www.tibiawiki.com.br/wiki/Extra_Dimensionais',
    'https://www.tibiawiki.com.br/wiki/Fadas',
    'https://www.tibiawiki.com.br/wiki/Gigantes',
    'https://www.tibiawiki.com.br/wiki/Humanos',
    'https://www.tibiawiki.com.br/wiki/Human%C3%B3ides',
    'https://www.tibiawiki.com.br/wiki/Licantropos',
    'https://www.tibiawiki.com.br/wiki/Mam%C3%ADferos',
    'https://www.tibiawiki.com.br/wiki/Mortos-Vivos',
    'https://www.tibiawiki.com.br/wiki/Plantas_(Criatura)',
    'https://www.tibiawiki.com.br/wiki/R%C3%A9pteis',
    'https://www.tibiawiki.com.br/wiki/Slimes',
    'https://www.tibiawiki.com.br/wiki/Vermes'
]

tibiafandom_base_url = 'https://tibia.fandom.com'
monsters_url = []
monsters = []


def get_monsters_url():
    for monster_type in monsters_types:
        request = Request(monster_type, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(request)
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find_all('div', class_='mw-parser-output')[1].find('table', id='tabelaDPL').find_all('tr')[1:]

        exclude = [tr for row in table
                   for td in row.find_all('td')
                   for tr in td.find_all('tr')]

        table_rows = [row for row in table if row not in exclude]

        for row in table_rows:
            monster_href = row.find('a')['href']

            monster_href = monster_href if 'Criatura' not in monster_href \
                else monster_href.replace('Criatura', 'Creature')
            monster_href = monster_href if 'Of' not in monster_href \
                else monster_href.replace('Of', 'of')
            monster_href = monster_href if 'The' not in monster_href \
                else monster_href.replace('The', 'the')
            if 'Horse_(' in monster_href:
                monster_href = '/wiki/Horse_(Grey)'
            if 'Devourer_(' in monster_href:
                monster_href = '/wiki/Devourer'
            if 'Butterfly_(' in monster_href:
                monster_href = '/wiki/Butterfly_(Blue)'
            if monster_href == '/wiki/Nomad':
                monster_href = '/wiki/Nomad_(Basic)'

            monsters_url.append(tibiafandom_base_url + monster_href)


def get_monsters_info():
    for monster_url in monsters_url:
        request = Request(monster_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(request)
        soup = BeautifulSoup(html, 'html.parser')

        hp = exp = speed = armor = damage = None
        elements = 1
        illusionable = pushable = pushes = None
        difficulty = occurrence = None
        paralysable = sense_invisibility = None
        resistances = {}

        monster_info = \
            soup.find('aside', class_='portable-infobox pi-background pi-border-color pi-theme-twbox pi-layout-default')

        name = monster_info.find('h2', class_='pi-item pi-item-spacing pi-title pi-secondary-background').get_text()
        # print(name)

        properties = monster_info.find_all('section', class_='pi-item pi-group pi-border-color')

        # combat properties
        divs = properties[0].find_all('div', 'pi-item pi-data pi-item-spacing pi-border-color')
        for div in divs:
            prop = div.find('h3', class_='pi-data-label pi-secondary-font').get_text()
            value = div.find('div', class_='pi-data-value pi-font').get_text()
            if prop == 'Health':
                hp = int(value)
            elif prop == 'Experience':
                exp = int(value)
            elif prop == 'Speed':
                speed = int(value)
            elif prop == 'Armor':
                armor = int(value)
            elif prop == 'Elements':
                elements = len(value.split())
            elif prop == 'Est. Max Dmg':
                damage = get_damage(value)

        # general properties
        divs = properties[1].find_all('div', 'pi-item pi-data pi-item-spacing pi-border-color')
        illusionable = 1 if divs[2].find('div', class_='pi-data-value pi-font').get_text() == '✓' else 0
        pushable = 1 if divs[3].find('div', class_='pi-data-value pi-font').get_text() == '✓' else 0
        pushes = 1 if divs[4].find('div', class_='pi-data-value pi-font').get_text() == '✓' else 0

        # bestiary properties
        divs = properties[2].find_all('div', 'pi-item pi-data pi-item-spacing pi-border-color')
        difficulty = difficulties[divs[1].find('a')['title']]
        occurrence = occurrences[divs[2].find('a')['title']]

        # immunity properties
        divs = properties[3].find_all('div', 'pi-item pi-data pi-item-spacing pi-border-color')
        paralysable = 1 if divs[0].find('div', class_='pi-data-value pi-font').get_text() == '✓' else 0
        sense_invisibility = 1 if divs[1].find('div', class_='pi-data-value pi-font').get_text() == '✓' else 0

        # resistances
        element_res = soup.find('div', class_='twbox').find('div', id='creature-resistance-table')
        element_res = element_res.find('div', id='creature-resistance-d') \
            .find_all('div', class_='creature-resistance-el')
        for r in element_res:
            text = r.get_text().strip('%').split()
            resistances.update({text[0]: text[1]})

        try:
            monster = Monster(name, hp, exp, speed, armor, damage, elements, resistances, illusionable, pushable,
                              pushes, difficulty, occurrence, paralysable, sense_invisibility)
            monsters.append(monster)
        except Exception:
            pass


def save_info():
    df = pd.DataFrame([monster.__dict__ for monster in monsters],
                      columns=['name', 'difficulty', 'occurrence',
                               'hp', 'exp', 'speed', 'armor', 'damage', 'elements',
                               'physical', 'death', 'holy', 'ice', 'fire', 'energy', 'earth',
                               'illusionable', 'pushable', 'pushes', 'paralysable', 'sense_invis'])
    df.to_csv('output')


def get_damage(text):
    value = re.findall(r'\d+', text)
    return int(value[0]) if value else None


if __name__ == '__main__':
    get_monsters_url()
    get_monsters_info()
    save_info()
