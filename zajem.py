import re
import orodja

url = 'https://www.nepremicnine.net/oglasi-oddaja/stanovanje/'

mapa = 'zajeti_podatki'


# zajem podatkov iz glavnih strani
def stanovanja_na_strani(st_strani=57):
    for i in range(st_strani):
        url = f'https://www.nepremicnine.net/oglasi-oddaja/stanovanje/{i}/'
        datoteka = f'zajete_strani/stanovanja/stanovanja{i * 30 + 1}-{(i+1) * 30}.html'
        orodja.shrani_spletno_stran(url, datoteka)


stanovanja_na_strani()
# zajem podatkov iz strani vsake nepremicnine posebej