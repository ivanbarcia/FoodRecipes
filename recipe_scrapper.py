from bs4 import BeautifulSoup
import requests
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_recetas_gratis(ingredients): # https://www.recetasgratis.net/busqueda?q=tomate
    website = 'https://www.recetasgratis.net'
    ingredient = ingredients.replace(" ",'+')

    url = f'{website}/busqueda/q/{ingredient}/pag/1'
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')

    with open('recetasgratis.csv', 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        names = soup.select(".resultado")
        for i in range(len(names)):
            lst = []
            try:
                name = soup.select(".titulo--resultado")[i].get_text().strip()
                link = soup.select(".titulo--resultado")[i].attrs.get("href")
            except:
                name = ""
            lst = [name,link]
            writer.writerow(lst)

    print("Done!!")

def get_cookpad(ingredients): # https://cookpad.com/ar/buscar/tomate?event=search.typed_query
    website = 'https://cookpad.com'
    ingredient = ingredients.replace(" ",'+')

    url = f'{website}/ar/buscar/{ingredient}`?event=search.typed_query'
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')

    with open('cookpad.csv', 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        names = soup.select("div.flex.flex-col.h-full")
        for i in range(len(names)):
            lst = []
            try:
                name = soup.select("a.block-link__main")[i].get_text().strip()
                link = soup.select("a.block-link__main")[i].attrs.get("href")
                link = website + str(link)
            except:
                name = ""
            lst = [name,link]
            writer.writerow(lst)

    print("Done!!")

def get_cocineros_argentinos(ingredients): # https://cocinerosargentinos.com/busqueda?q=tomate
    website = 'https://cocinerosargentinos.com'
    ingredient = ingredients.replace(" ",'+')

    url = f'{website}/busqueda?q={ingredient}'
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')

    with open('cocinerosargentinos.csv', 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        names = soup.select("div.item-title")
        for i in range(len(names)):
            lst = []
            try:
                name = soup.select("div.item-title")[i].get_text().strip()
                link = names[i].find('a')['href']
                link = website + str(link)
            except:
                name = ""
            lst = [name,link]
            writer.writerow(lst)

    print("Done!!")

if __name__ == "__main__":
    ingredient = input("Que ingrediente tenes?\n")
    # get_recetas_gratis(ingredient)
    get_cookpad(ingredient)
    # get_cocineros_argentinos(ingredient)