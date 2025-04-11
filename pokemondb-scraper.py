from bs4 import BeautifulSoup
import requests

pokedex_url = "https://pokemondb.net/pokedex/all"
pokedex_result = requests.get(pokedex_url)

pokedex_doc = BeautifulSoup(pokedex_result.text, "html.parser")

# list all pokemon names without duplicates
pokemons = list(dict.fromkeys(pokedex_doc.find_all("a", class_ = "ent-name")))

pokemon_name_list = []

for pokemon in pokemons:
    pokemon_name_list.append(pokemon.string)

print(pokemon_name_list)