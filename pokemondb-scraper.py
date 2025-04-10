from bs4 import BeautifulSoup
import requests

pokedex_url = "https://pokemondb.net/pokedex/all"
pokedex_result = requests.get(pokedex_url)

pokedex_doc = BeautifulSoup(pokedex_result.text, "html.parser")

pokemon_list = list(dict.fromkeys(pokedex_doc.find_all('a', class_="ent-name")))

print(pokemon_list)