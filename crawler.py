import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

difficulties = {
    '/images/a/a9/Besti%C3%A1rio_Inofensivo.gif': 0,
    '/images/8/8f/Besti%C3%A1rio_Trivial.gif': 1,
    '/images/1/1b/Besti%C3%A1rio_F%C3%A1cil.gif': 2,
    '/images/6/60/Besti%C3%A1rio_M%C3%A9dio.gif': 3,
    '/images/1/1e/Besti%C3%A1rio_Dif%C3%ADcil.gif': 4,
    '/images/a/a1/Besti%C3%A1rio_Desafiador.gif': 5
}

occurrences = {
    '/images/f/ff/Besti%C3%A1rio_Ocorr%C3%AAncia_Comum.gif': 1,
    '/images/c/cc/Besti%C3%A1rio_Ocorr%C3%AAncia_Rara.gif': 3,
    '/images/d/df/Besti%C3%A1rio_Ocorr%C3%AAncia_Incomum.gif': 2,
    '/images/4/48/Besti%C3%A1rio_Ocorr%C3%AAncia_Muita_Rara.gif': 4
}

tibiafandom_base_url = 'https://tibia.fandom.com'
tibiawiki_base_url = 'https://www.tibiawiki.com.br'
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

wiki_monsters_url = []
fandom_monsters_url = []

# get monsters urls
for monster_type in monsters_types:
    request = Request(monster_type, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(request)
    soup = BeautifulSoup(html, 'html.parser')
    #
    table = soup.find_all('div', class_='mw-parser-output')[1].find('table', id='tabelaDPL').find_all('tr')[1:]

    exclude = [tr for row in table
               for td in row.find_all('td')
               for tr in td.find_all('tr')]

    table_rows = [row for row in table if row not in exclude]

    for row in table_rows:
        monster_href = row.find('a')['href']

        wiki_monsters_url.append(tibiawiki_base_url + monster_href)

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

        fandom_monsters_url.append(tibiafandom_base_url + monster_href)

for i in range(len(wiki_monsters_url)):
    print(wiki_monsters_url[i], fandom_monsters_url[i])
    request = Request(wiki_monsters_url[i], headers={'User-Agent': 'Mozilla/5.0'})
    request = Request(fandom_monsters_url[i], headers={'User-Agent': 'Mozilla/5.0'})

# from tibiawiki br
# for monster_url in monsters_url:
#     print(monster_url)
#     request = Request(monster_url, headers={'User-Agent': 'Mozilla/5.0'})
#     html = urlopen(request)
#     soup = BeautifulSoup(html, 'html.parser')
#     #
#     # table = soup.find('table', class_='infobox')
#     #
#     # data = table.find_all('td')
#     #
#     # name = data[2].get_text()
#     # hp = data[3].get_text().split()[0]
#     # difficulty = difficulties[data[4].find('img')['src']]
#     # xp = data[5].get_text().split()[0]
#     # occurrence = occurrences[data[6].find('img')['src']]
#     # speed = data[7].get_text().split()[0]
#     # charm = data[8].get_text().split()[0]
#     # armor = data[9].get_text().split()[0]
#     #
#     # damage_resistane = data[10].find_all('span', class_='tooltip')
#     # physical_resistance = damage_resistane[0].get_text().strip('%')
#     # earth_resistance = damage_resistane[1].get_text().strip('%')
#     # fire_resistance = damage_resistane[2].get_text().strip('%')
#     # death_resistance = damage_resistane[3].get_text().strip('%')
#     # energy_resistance = damage_resistane[4].get_text().strip('%')
#     # holy_resistance = damage_resistane[5].get_text().strip('%')
#     # ice_resistance = damage_resistane[6].get_text().strip('%')
#     # healing_resistance = damage_resistane[7].get_text().strip('%')
#     #
#     # print(data[29])
#     # print(data[30])
#     # print(data[31])
#     # print(data[32])
#     # input()
#
#     # data[29] = imunidades
#     # data[30] = pode ser puxado
#     # data[31] = passa por
#     # data[32] = empurra
#
#     # habilities = table.find('div', class_='column-count column-count-1')
#
#     # for i in tds[0:]:
#     #     print(i)
#     #     input()
#
#     # input()
