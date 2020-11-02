import re
import orodja

# zajem podatkov iz strani vsake nepremicnine posebej

def zajem_posameznega_oglasa(seznam):
    for url, id in seznam:
        datoteka = f'zajete_strani/oglasi/{id}.html'
        orodja.shrani_spletno_stran(url, datoteka)
        print(f'Uspesno shranjen oglas id: {id}')

# zajem podatkov iz glavnih strani
def zajem_strani(st_strani=57):
    
    seznam = []
    vzorec_url_id = r'<!--<meta itemprop="url" content="(.+stanovanje_(.+)/)" />--'
    
    for i in range(st_strani):
        url_strani = f'https://www.nepremicnine.net/oglasi-oddaja/stanovanje/{i}/'
        datoteka = f'zajete_strani/stanovanja/stanovanja{i * 30 + 1}-{(i+1) * 30}.html'
        orodja.shrani_spletno_stran(url_strani, datoteka)
        print(f'Uspesno sharnjena stran{i}')

        #ustvari seznam naborov (url, id)
        seznam_url_id = re.findall(vzorec_url_id, orodja.vsebina_datoteke(datoteka))
        seznam += seznam_url_id
        print(f'Dolzina seznama: {len(seznam)}')
    
    #zajamemo še vsako stran posebaj
    zajem_posameznega_oglasa(seznam)


zajem_strani()

