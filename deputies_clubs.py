import requests
import lxml.html as lh


def which_is(text, elem):
    return [i for i,j in enumerate(text) if j == elem][0]


def remove_annotations(name):
    if '[' in name:
        idx = which_is(name, '[')
        return name[:idx]
    else:
        return name


def deputies_subset(from_club, to_club):
    from_ids = which_is(deputies, from_club) +1
    if to_club == 0:
        to_ids = len(deputies)
    else:
        to_ids = which_is(deputies, to_club)
    dep = deputies[from_ids:to_ids]
    dep = list(map(remove_annotations, dep))
    print(dep[:3])
    print(dep[-3:])
    return dep


def to_dict(label, data):
    return { dep: label for dep in data}



url = 'https://pl.wikipedia.org/wiki/Pos%C5%82owie_na_Sejm_Rzeczypospolitej_Polskiej_VIII_kadencji#Stan_aktualny'
page = requests.get(url)
doc = lh.fromstring(page.content)

deputies = doc.xpath('/html/body/div[3]/div[3]/div[4]/div/table[3]')[0]
deputies = deputies.text_content().split('\n')
deputies = [ d for d in deputies if len(d)]

pis = deputies_subset(
    'Klub Parlamentarny Prawo i Sprawiedliwość',
    'Klub Parlamentarny Platforma Obywatelska – Koalicja Obywatelska'
)

poko = deputies_subset(
    'Klub Parlamentarny Platforma Obywatelska – Koalicja Obywatelska',
    'Klub Poselski Polskiego Stronnictwa Ludowego – Unii Europejskich Demokratów[af]'
)

psl = deputies_subset(
    'Klub Poselski Polskiego Stronnictwa Ludowego – Unii Europejskich Demokratów[af]',
    'Klub Poselski Kukiz’15'
)

kukiz = deputies_subset(
    'Klub Poselski Kukiz’15',
    'Koło Poselskie Konfederacja'
)

konf = deputies_subset(
    'Koło Poselskie Konfederacja',
    'Koło Poselskie Unia Polityki Realnej'
)

upr = deputies_subset(
    'Koło Poselskie Unia Polityki Realnej',
    'Koło Poselskie Przywrócić Prawo'
)

pp = deputies_subset(
    'Koło Poselskie Przywrócić Prawo',
    'Koło Poselskie Teraz!'
)

teraz = deputies_subset(
    'Koło Poselskie Teraz!',
    'Posłowie niezrzeszeni'
)

niez = deputies_subset(
    'Posłowie niezrzeszeni',
    0
)

dep = to_dict('PiS', pis)
dep.update(to_dict('PO-KO', poko))
dep.update(to_dict('PSL-UED', psl))
dep.update(to_dict('Kukiz15', kukiz))
dep.update(to_dict('Konfederacja', konf))
dep.update(to_dict('UPR', upr))
dep.update(to_dict('PP', pp))
dep.update(to_dict('TERAZ!', teraz))
dep.update(to_dict('niez.', niez))

len(dep)

dep.update({'Kornel Morawiecki': 'niez.'})

import json
with open('deputies.json', 'w') as f:
    json.dump(dep, f)