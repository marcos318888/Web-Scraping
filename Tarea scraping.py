import sqlite3 
from bs4 import BeautifulSoup
import requests 

conn= sqlite3.connect('Raspado.db')
c= conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS raspa (id INTEGER PRIMARY KEY, url TEXT,
src TEXT)''')
conn.commit()

url = 'https://www.elconfidencial.com/'
html = requests.get(url).text

soup = BeautifulSoup(html)

# Buscamos toda la información de cada etiqueta
tags = {
'h1': soup.find_all('h1'),
'h2': soup.find_all('h2'),
'h3': soup.find_all('h3'),
'h4': soup.find_all('h4'),
'h5': soup.find_all('h5'),
'p': soup.find_all('p'),
'blockquote': soup.find_all('blockquote'),
'cite': soup.find_all('cite'),
'a': soup.find_all('a'),
'address': soup.find_all('address'),
'img': soup.find_all('img', src=True)
}

for tag, elementos in tags.items():
    for elemento in elementos:
        url = elemento.get_text()
        text = elemento.get_text()
        src = elemento.get('src') if tag == 'img' else None

        c.execute("INSERT INTO raspa (url, src) VALUES (?, ?)", (url, src))
        
conn.commit()
conn.close()

with open('Scraping.txt', 'w', encoding='utf-8') as texto:
    for tag, elementos in tags.items():
        texto.write(f"Tag: {tag}\n")
        for elemento in elementos:
            texto.write(f" Contenido: {elemento.get_text()}\n")
            if tag == 'img':
                texto.write(f" Link: {elemento.get('src')}\n")
        texto.write("\n")

with open('Scraping.txt', 'r', encoding='utf-8') as file:
    print(file.read())