from urllib.request import urlopen, Request
import pandas as pd
from bs4 import BeautifulSoup
from monster import Monster
import re


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

monsters_url = []
monsters = []


def get_monsters_url():
    request = Request('https://tibia.fandom.com/wiki/List_of_Creatures', headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(request)
    soup = BeautifulSoup(html, 'html.parser')

    monsters_list = soup.find('div', id='mw-content-text').find('table').find('tbody').find_all('tr')

    exception = ['Piñata_Dragon']
    for i in monsters_list:
        tds = list(i.find_all('td'))
        for i in range(len(tds)):
            tds[i] = tds[i].get_text().replace('\n', '').replace(' ', '_').replace(',', '')
        if len(tds) == 4 and tds[2].isnumeric() and tds[3].isnumeric():
            if tds[0] not in exception:
                monsters_url.append('https://tibia.fandom.com/wiki/' + tds[0])


def get_monsters_info():
    for monster_url in monsters_url:
        request = Request(monster_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(request)
        soup = BeautifulSoup(html, 'html.parser')

        hp = exp = speed = armor = damage = None
        summon = convince = 0
        elements = 1
        illusionable = pushable = pushes = None
        difficulty = occurrence = None
        paralysable = sense_invisibility = None
        resistances = {}
        walk_around = walk_through = 0

        monster_info = \
            soup.find('aside',
                      class_='portable-infobox pi-background pi-border-color pi-theme-twbox pi-layout-default')

        name = monster_info.find('h2',
                                 class_='pi-item pi-item-spacing pi-title pi-secondary-background').get_text()
        # print(name) # verbose

        properties = monster_info.find_all('section', class_='pi-item pi-group pi-border-color')
        properties_list = [p.h2.get_text() for p in properties]

        if 'Bestiary Properties' in properties_list:

            # combat properties
            divs = properties[0].find_all('div', 'pi-item pi-data pi-item-spacing pi-border-color')
            for div in divs:
                prop = div.find('h3', class_='pi-data-label pi-secondary-font').get_text()
                value = div.find('div', class_='pi-data-value pi-font').get_text().replace(',', '')
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
                elif prop == 'Summon':
                    summon = (1, 0)[value == '(not possible)']
                elif prop == 'Convince':
                    convince = (1, 0)[value == '(not possible)']

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

            # behaviour properties
            divs = properties[4].find_all('div', 'pi-item pi-data pi-item-spacing pi-border-color')
            for d in divs:
                prop = d.find('h3').get_text()
                value = d.find('div').get_text()
                if prop == 'Walks Around':
                    walk_around = len(value.split())
                if prop == 'Walks Through':
                    walk_through = len(value.split())

            # resistances
            element_res = soup.find('div', class_='twbox').find('div', id='creature-resistance-table')
            element_res = element_res.find('div', id='creature-resistance-d') \
                .find_all('div', class_='creature-resistance-el')
            for r in element_res:
                text = r.get_text().strip('%').split()
                resistances.update({text[0]: text[1]})

            try:
                monster = Monster(name, hp, exp, speed, armor, damage, summon, convince,
                                  elements, resistances, illusionable, pushable, pushes,
                                  difficulty, occurrence, paralysable, sense_invisibility,
                                  walk_around, walk_through)
                monsters.append(monster)
            except Exception:
                pass


def save_info():
    df = pd.DataFrame([monster.__dict__ for monster in monsters],
                      columns=['name', 'difficulty', 'occurrence',
                               'hp', 'exp', 'speed', 'armor', 'damage', 'summon', 'convince',
                               'elements',
                               'physical', 'death', 'holy', 'ice', 'fire', 'energy', 'earth',
                               'illusionable', 'pushable', 'pushes', 'paralysable', 'sense_invis',
                               'walk_around', 'walk_through'])
    df.to_csv('output')


def get_damage(text):
    value = re.findall(r'\d+', text)
    return int(value[0]) if value else None


if __name__ == '__main__':
    get_monsters_url()
    get_monsters_info()
    save_info()
