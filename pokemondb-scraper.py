from bs4 import BeautifulSoup
import requests

pokedex_url = "https://pokemondb.net/pokedex/all"
pokedex_response = requests.get(pokedex_url)
pokedex_soup = BeautifulSoup(pokedex_response.text, "html.parser")

# list all pokemon names without duplicates
pokemon_name_list = [name.text for name in list(dict.fromkeys(pokedex_soup.find_all("a", class_ = "ent-name")))]

# for name in pokemon_name_list:
#TODO     ADD CODE HERE!!

#TODO ADD THIS CODE AFTER TESTING!!  
pokemon_url = "https://pokemondb.net/pokedex/bulbasaur"
pokemon_response = requests.get(pokemon_url)
pokemon_soup = BeautifulSoup(pokemon_response.text, "html.parser")

# Pokemon Info
pokemon_id = int(pokemon_soup.find("th", string = "National №").find_next("td").text)
pokemon_name = pokemon_soup.find("h1").text
pokemon_type = [type.text for type in pokemon_soup.find("th", string = "Type").find_next("td").find_all("a")]
pokemon_description = " ".join([desc.text for desc in pokemon_soup.find("div", class_ = "tabset-basics").find_all_previous("p")][::-1])

print(pokemon_description)