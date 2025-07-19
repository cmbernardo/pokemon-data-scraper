from bs4 import BeautifulSoup
import requests
import pandas as pd

pokedex_url = "https://pokemondb.net/pokedex/all"
pokedex_response = requests.get(pokedex_url)
pokedex_soup = BeautifulSoup(pokedex_response.text, "html.parser")

# list all pokemon names without duplicates
pokemon_href = list(dict.fromkeys(pokedex_soup.find_all("a", class_ = "ent-name")))

pokemon_details = []
pokemon_stats = []
pokemon_data = []

for href in pokemon_href:
    pokemon_url = "https://pokemondb.net" + href["href"]
    pokemon_response = requests.get(pokemon_url)
    pokemon_soup = BeautifulSoup(pokemon_response.text, "html.parser")

    # Pokemon Details
    pokemon_id = int(pokemon_soup.find("th", string = "National №").find_next("td").text)
    pokemon_name = pokemon_soup.find("h1").text
    pokemon_type = [type.text for type in pokemon_soup.find("th", string = "Type").find_next("td").find_all("a")]
    pokemon_type1 = pokemon_type[0]
    pokemon_type2 = ""
    
    if (len(pokemon_type) == 2):
        pokemon_type2 = pokemon_type[1]
        
    pokemon_description = ""
    
    if (pokemon_soup.find("h2", string = "Pokédex entries")):
        pokemon_description = pokemon_soup.find("h2", string = "Pokédex entries").find_next("div").find("td", class_ = "cell-med-text").text
        
    pokemon_abilities = ', '.join([ability.text for ability in pokemon_soup.find("th", string = "Abilities").find_next("td").find_all("a")])
    pokemon_catch_rate = pokemon_soup.find("th", string = "Catch rate").find_next("td").text.strip().split()[0]
    pokemon_gender = ', '.join([gender.text for gender in pokemon_soup.find("th", string = "Gender").find_next("td").find_all("span")])
    pokemon_generation = pokemon_soup.find("abbr").text.strip().split()[-1]

    # Pokemon Stats
    pokemon_hp = pokemon_soup.find("th", string = "HP").find_next("td").text
    pokemon_attack = pokemon_soup.find("th", string = "Attack").find_next("td").text
    pokemon_defense = pokemon_soup.find("th", string = "Defense").find_next("td").text
    pokemon_sp_atk = pokemon_soup.find("th", string = "Sp. Atk").find_next("td").text
    pokemon_sp_def = pokemon_soup.find("th", string = "Sp. Def").find_next("td").text
    pokemon_speed = pokemon_soup.find("th", string = "Speed").find_next("td").text
    pokemon_stats_total = pokemon_soup.find("th", string = "Total").find_next("td").text
    
    pokemon_data.append({
        "Pokemon ID": pokemon_id, 
        "Name": pokemon_name, 
        "Type 1": pokemon_type1, 
        "Type 2": pokemon_type2, 
        "Description": pokemon_description, 
        "Abilities": pokemon_abilities, 
        "Catch Rate": pokemon_catch_rate, 
        "Gender": pokemon_gender,
        "Generation": pokemon_generation,
        "HP": pokemon_hp,
        "Attack": pokemon_attack,
        "Defense": pokemon_defense,
        "Sp. Atk": pokemon_sp_atk,
        "SP. Def": pokemon_sp_def,
        "Speed": pokemon_speed,
        "Total": pokemon_stats_total
    })

data_df = pd.DataFrame(pokemon_data)

data_df.to_csv("./pokemon-data.csv", header = True, index = False, encoding = "utf-8-sig")
    
print("Done")