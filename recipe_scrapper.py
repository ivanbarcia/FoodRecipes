from bs4 import BeautifulSoup
import requests
import csv
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_recetas_gratis(ingredients): # https://www.recetasgratis.net/busqueda?q=tomate
    website = 'https://www.recetasgratis.net'
    ingredient = ingredients.replace(" ",'+')

    url = f'{website}/busqueda/q/{ingredient}/pag/1'
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')

    names = soup.select(".resultado")[:3]
    result = []

    for i in range(len(names)):
        try:
            # name = soup.select(".titulo--resultado")[i].get_text().strip()
            link = soup.select(".titulo--resultado")[i].attrs.get("href")
            result.append(link)
        except:
            continue
        
    pprint(result)
    return result

def get_cookpad(ingredients): # https://cookpad.com/ar/buscar/tomate?event=search.typed_query
    website = 'https://cookpad.com'
    ingredient = ingredients.replace(" ",'+')

    url = f'{website}/ar/buscar/{ingredient}`?event=search.typed_query'
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    result = []

    names = soup.select("div.flex.flex-col.h-full")[:3]
    for i in range(len(names)):
        try:
            # name = soup.select("a.block-link__main")[i].get_text().strip()
            link = soup.select("a.block-link__main")[i].attrs.get("href")
            link = website + str(link)
            result.append(link)
        except:
            continue

    pprint(result)
    return result 

def get_cocineros_argentinos(ingredients): # https://cocinerosargentinos.com/busqueda?q=tomate
    website = 'https://cocinerosargentinos.com'
    ingredient = ingredients.replace(" ",'+')

    url = f'{website}/busqueda?q={ingredient}'
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    result = []

    names = soup.select("div.item-title")[:3]
    for i in range(len(names)):
        try:
            # name = soup.select("div.item-title")[i].get_text().strip()
            link = names[i].find('a')['href']
            link = website + str(link)
            result.append(link)
        except:
            continue

    pprint(result)
    return result

def get_recipes(ingredients):
    print('BUSCANDO RECETAS...')

    recipes = []

    result = get_recetas_gratis(ingredients)
    recipes.append(result)

    result = get_cookpad(ingredients)
    recipes.append(result)

    result = get_cocineros_argentinos(ingredients)
    recipes.append(result)

    return recipes

if __name__ == "__main__":
    ingredient = input("Que ingrediente tenes?\n")

    get_recipes(ingredient)

    print('FIN!')
    
    