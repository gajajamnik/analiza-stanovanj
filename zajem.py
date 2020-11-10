import re
import orodja
import os

# VZORCI REGULARNIH IZRAZOV
#vzorci za glavno stran
vzorec_url_id = r'<!--<meta itemprop="url" content="(?P<url>.+stanovanje_(?P<id>.+)/)" />--'
vzorec_id_stran = r'<!--<meta itemprop="url" content=".+stanovanje_(?P<id>.+)/" />--'

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

# PROGRAM

# zajame podatke iz strani vsake nepremicnine posebej in spravi v seznam slovarjev
def zajem_posameznega_oglasa(seznam):
    seznam_slovarjev = []
    for url, id in seznam:
        datoteka = f'zajete_strani/oglasi/{id}.html'
        orodja.shrani_spletno_stran(url, datoteka)
        print(f'Uspesno shranjen oglas id: {id}')
        vsebina = orodja.vsebina_datoteke(datoteka)
        slovar_podatkov = izloci_podatke(vsebina)
        seznam_slovarjev.append(slovar_podatkov)
    #slovarje uredimo po id-ju
    seznam_slovarjev.sort(key=lambda stan: stan['id'])
    return seznam_slovarjev

# zajem podatkov iz glavnih strani
def zajem_strani(st_strani=57):  
    seznam = []  #seznam naborov (url, id)
    
    #shrani glavne strani in iz njih izloci id stanovanj ter pripadajoc url
    for i in range(1, st_strani + 1):
        url_strani = f'https://www.nepremicnine.net/oglasi-oddaja/stanovanje/{i}/'
        datoteka = f'zajete_strani/stanovanja/stanovanja{i * 30 + 1}-{(i+1) * 30}.html'
        orodja.shrani_spletno_stran(url_strani, datoteka)
        print(f'Uspesno sharnjena stran{i}')

        #ustvari seznam naborov (url, id)
        seznam_url_id = re.findall(vzorec_url_id, orodja.vsebina_datoteke(datoteka))
        seznam += seznam_url_id
    
    print(seznam)
    #zajamemo še vsako stran posebej in sprejme seznam slovarjev z obdelanimi podatki
    seznam_slovarjev = zajem_posameznega_oglasa(seznam)
    
    #shranimo podatke iz posamezne strani v csv
    orodja.zapisi_csv(
        seznam_slovarjev,
        ['id', 'kvadratura', 'tip', 'leto', 'cena', 'regija', 'upravna', 'obcina'],
        'obdelani-podatki/podatki.csv'
    )

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
    obdelaj_podatke(slovar)
    return slovar


def obdelaj_podatke(slovar):
    slovar['id'] = slovar['id'].strip('\'')
    slovar['kvadratura'] = slovar['kvadratura'].strip('\'')
    slovar['cena'] = slovar['cena'].strip('\'')

def zajem_studentskih_stanovanj(st_strani=12):
    seznam_slovarjev = []
    for i in range(1, st_strani + 1):
        url = ''
        if i == 1:
            url = 'https://www.nepremicnine.net/za-studente.html'
        else:
            url = f'https://www.nepremicnine.net/za-studente.html/{i}/'
        datoteka = f'zajete_strani/studenti/za_studente{i}'
        orodja.shrani_spletno_stran(url, datoteka)
        vsebina = orodja.vsebina_datoteke(datoteka)
        for zadetek in re.finditer(vzorec_id_stran, vsebina):
            slovar = zadetek.groupdict()
            seznam_slovarjev.append(slovar)
    orodja.zapisi_csv(
        seznam_slovarjev,
        ['id'],
        'obdelani-podatki/studenti.csv'
    )

zajem_strani()

zajem_studentskih_stanovanj()