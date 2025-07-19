from bs4 import BeautifulSoup
import requests
import pandas as pd

pokedex_url = "https://pokemondb.net/pokedex/all"
pokedex_response = requests.get(pokedex_url)
pokedex_soup = BeautifulSoup(pokedex_response.text, "html.parser")

# list all pokemon names without duplicates
pokemon_href = list(dict.fromkeys(pokedex_soup.find_all("a", class_ = "ent-name")))
pokemon_data = []

print(f"[FETCH DATA]: START")

for href in pokemon_href:
    data = {}
    
    pokemon_url = "https://pokemondb.net" + href["href"]
    pokemon_response = requests.get(pokemon_url)
    pokemon_soup = BeautifulSoup(pokemon_response.text, "html.parser")

    # Pokemon Details
    pokemon_id = int(pokemon_soup.find("th", string = "National №").find_next("td").text)
    pokemon_id = f"{pokemon_id:05d}"
    data["Pokemon ID"] = pokemon_id
    
    pokemon_name = pokemon_soup.find("h1").text
    data["Name"] = pokemon_name
    
    pokemon_type = [type.text for type in pokemon_soup.find("th", string = "Type").find_next("td").find_all("a")]
    pokemon_type1 = pokemon_type[0]
    data["Type 1"] = pokemon_type1
    
    pokemon_type2 = ""
    if (len(pokemon_type) == 2):
        pokemon_type2 = pokemon_type[1]
        data["Type 2"] = pokemon_type2
        
    pokemon_description = pokemon_soup.find("h2", string = "Pokédex entries")
    if (pokemon_description):
        pokemon_description = pokemon_description.find_next("div").find("td", class_ = "cell-med-text").text
        data["Description"] = pokemon_description
        
    pokemon_abilities = ', '.join([ability.text for ability in pokemon_soup.find("th", string = "Abilities").find_next("td").find_all("a")])
    data["Abilities"] = pokemon_abilities
    
    pokemon_catch_rate = pokemon_soup.find("th", string = "Catch rate").find_next("td").text.strip().split()[0]
    data["Catch Rate"] = pokemon_catch_rate
    
    pokemon_gender = ', '.join([gender.text for gender in pokemon_soup.find("th", string = "Gender").find_next("td").find_all("span")])
    data["Gender"] = pokemon_gender
    
    pokemon_generation = pokemon_soup.find("abbr").text.strip().split()[-1]
    data["Generation"] = pokemon_generation
    
    pokemon_evolution = pokemon_soup.find("div", class_ = "infocard-list-evo")
    if (pokemon_evolution):
        pokemon_evolution = ', '.join([evolution.text for evolution in pokemon_evolution.find_all("a", class_ = "ent-name")])
        data["Evolution"] = pokemon_evolution

    # Pokemon Stats
    pokemon_hp = pokemon_soup.find("th", string = "HP").find_next("td").text
    pokemon_attack = pokemon_soup.find("th", string = "Attack").find_next("td").text
    pokemon_defense = pokemon_soup.find("th", string = "Defense").find_next("td").text
    pokemon_sp_atk = pokemon_soup.find("th", string = "Sp. Atk").find_next("td").text
    pokemon_sp_def = pokemon_soup.find("th", string = "Sp. Def").find_next("td").text
    pokemon_speed = pokemon_soup.find("th", string = "Speed").find_next("td").text
    pokemon_stats_total = pokemon_soup.find("th", string = "Total").find_next("td").text
    
    data["HP"] = pokemon_hp
    data["Attack"] = pokemon_attack
    data["Defense"] = pokemon_defense
    data["Sp. Atk"] = pokemon_sp_atk
    data["SP. Def"] = pokemon_sp_def
    data["Speed"] = pokemon_speed
    data["Total"] = pokemon_stats_total
    
    # Pokemon Image Source
    pokemon_img = pokemon_soup.find("div", class_ = "grid-col span-md-6 span-lg-4 text-center").find_next("img")["src"]
    data["Pokemon Image"] = pokemon_img
    
    pokemon_data.append(data)

print("[FETCH DATA]: DONE")

pd.DataFrame(pokemon_data).to_json("./pokemon-data.json", orient = "records")
print("[SAVE DATA]: Data saved to \"pokemon-data.json\"")
