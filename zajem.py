import re
import orodja
import os

#VZORCI REGULARNIH IZRAZOV
#vzorci za glavno stran
vzorec_url_id = r'<!--<meta itemprop="url" content="(?P<url>.+stanovanje_(?P<id>.+)/)" />--'

vzorec_bloka = re.compile(
    r'<div class="oglas_container oglasbold oglasi.*?'
    r'</div>\n\W*<div class="clearer"></div>\n\W*</div>\n\W*</div>'
)

vzorec_stanovanja = re.compile(
    r'oglasi.*?id="o(?P<id>\d{7})"'
    r'<span class="tipi">(?P<tip>.*?)</span>'
)

#vzorci na posamezni strani oglasa
vzorec_bloka_stran =(
    r'<div class="clearer"></div><div class="more_info">.*?'
    r'EUR/mes</div>'
)
vzorec_id_oglas = re.compile(r'Referenčna št.:.*(?P<id>\d{7})</strong>')
vzorec_podatki = re.compile(
    r'<div class="kratek" itemprop="description"><strong class="rdeca">.*'
    r', (?P<kvadratura>[\d,]*) m2,'
    r'(?P<tip>.*?),'
    r' .*l\.\s?(?P<leto>\d{4}).*'
    r'Cena:.*?(?P<cena>[\d,.]*) EUR.*?'
)

vzorec_lokacije = re.compile(
    r'<div class="more_info">.*'
    r'Regija: (?P<regija>.*) \| '
    r'Upravna enota:(?P<upravna>.*) \| '
    r'Občina: (?P<obcina>.*)</div>'
)



# zajem podatkov iz strani vsake nepremicnine posebej
def zajem_posameznega_oglasa(seznam):
    seznam_slovarjev = []
    for url, id in seznam:
        datoteka = f'zajete_strani/oglasi/{id}.html'
        orodja.shrani_spletno_stran(url, datoteka)
        print(f'Uspesno shranjen oglas id: {id}')
        vsebina = orodja.vsebina_datoteke(datoteka)
        slovar_podatkov = izloci_podatke(vsebina)
        seznam_slovarjev.append(slovar_podatkov)
    return seznam_slovarjev

# zajem podatkov iz glavnih strani
def zajem_strani(st_strani=57):  
    seznam = []  #seznam naborov (url, id)
    
    
    for i in range(st_strani):
        url_strani = f'https://www.nepremicnine.net/oglasi-oddaja/stanovanje/{i}/'
        datoteka = f'zajete_strani/stanovanja/stanovanja{i * 30 + 1}-{(i+1) * 30}.html'
        orodja.shrani_spletno_stran(url_strani, datoteka)
        print(f'Uspesno sharnjena stran{i}')

        #ustvari seznam naborov (url, id)
        seznam_url_id = re.findall(vzorec_url_id, orodja.vsebina_datoteke(datoteka))
        seznam += seznam_url_id
    
    #zajamemo še vsako stran posebaj
    seznam_slovarjev = zajem_posameznega_oglasa(seznam)
    
    #shranimo podatke iz posamezne strani v csv
    orodja.zapisi_csv(
        seznam_slovarjev,
        ['id', 'kvadratura', 'tip', 'leto', 'cena', 'regija', 'upravna', 'obcina'],
        'obdelani-podatki/podatki.csv'
    )

    #iz seznama naborov naredimo slovar
    #slovar_urljev = dict(seznam)
    #ta slovar pretvorimo v csv
    #orodja.zapisi_csv()
    print(f'Dolzina seznama je {len(seznam)}')


def izloci_podatke(stran):
    slovar = {}
    for zadetek in re.finditer(vzorec_id_oglas, stran):
        slovar_url = zadetek.groupdict()
        slovar.update(slovar_url)
        #print(slovar_url_id)
    for zadetek in re.finditer(vzorec_podatki, stran):
        slovar_podatkov = zadetek.groupdict()
        slovar.update(slovar_podatkov)
        #print(slovar_podatkov)
    for zadetek in re.finditer(vzorec_lokacije, stran):
        slovar_lokacije = zadetek.groupdict()
        slovar.update(slovar_lokacije)
    print(slovar)
    return slovar

zajem_strani(1)

