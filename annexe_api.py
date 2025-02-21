import requests
import time
import json

TYPE_CHART = {
    "normal": {"weak": ["fighting"], "resist": [], "immune": ["ghost"]},
    "fire": {"weak": ["water", "ground", "rock"], "resist": ["fire", "grass", "ice", "bug", "steel", "fairy"], "immune": []},
    "water": {"weak": ["electric", "grass"], "resist": ["fire", "water", "ice", "steel"], "immune": []},
    "electric": {"weak": ["ground"], "resist": ["electric", "flying", "steel"], "immune": []},
    "grass": {"weak": ["fire", "ice", "poison", "flying", "bug"], "resist": ["water", "electric", "grass", "ground"], "immune": []},
    "ice": {"weak": ["fire", "fighting", "rock", "steel"], "resist": ["ice"], "immune": []},
    "fighting": {"weak": ["flying", "psychic", "fairy"], "resist": ["bug", "rock", "dark"], "immune": []},
    "poison": {"weak": ["ground", "psychic"], "resist": ["grass", "fighting", "poison", "bug", "fairy"], "immune": []},
    "ground": {"weak": ["water", "grass", "ice"], "resist": ["poison", "rock"], "immune": ["electric"]},
    "flying": {"weak": ["electric", "ice", "rock"], "resist": ["grass", "fighting", "bug"], "immune": ["ground"]},
    "psychic": {"weak": ["bug", "ghost", "dark"], "resist": ["fighting", "psychic"], "immune": []},
    "bug": {"weak": ["fire", "flying", "rock"], "resist": ["grass", "fighting", "ground"], "immune": []},
    "rock": {"weak": ["water", "grass", "fighting", "ground", "steel"], "resist": ["normal", "fire", "poison", "flying"], "immune": []},
    "ghost": {"weak": ["ghost", "dark"], "resist": ["poison", "bug"], "immune": ["normal", "fighting"]},
    "dragon": {"weak": ["ice", "dragon", "fairy"], "resist": ["fire", "water", "electric", "grass"], "immune": []},
    "dark": {"weak": ["fighting", "bug", "fairy"], "resist": ["ghost", "dark"], "immune": ["psychic"]},
    "steel": {"weak": ["fire", "fighting", "ground"], "resist": ["normal", "grass", "ice", "flying", "psychic", "bug", "rock", "dragon", "steel", "fairy"], "immune": ["poison"]},
    "fairy": {"weak": ["poison", "steel"], "resist": ["fighting", "bug", "dark"], "immune": ["dragon"]}
}

BASE_URL = "https://pokeapi.co/api/v2/"
START_ID = 1  # Premier Pokémon (ex: Bulbizarre)
END_ID = 386  # Modifier pour récupérer plus de Pokémon
DATA = {}

def get_type_effectiveness(types):
    weaknesses = set()
    resistances = set()
    immunities = set()

    for t in types:
        type_data = TYPE_CHART.get(t, {})
        weaknesses.update(type_data.get("weak", []))
        resistances.update(type_data.get("resist", []))
        immunities.update(type_data.get("immune", []))

    # Supprimer les résistances des faiblesses (ex: Plante et Eau)
    weaknesses -= resistances
    weaknesses -= immunities

    return list(weaknesses), list(resistances), list(immunities)

def get_evolution_chain(pokemon_id):
    """ Récupère la chaîne d’évolution du Pokémon """
    response = requests.get(f"{BASE_URL}pokemon-species/{pokemon_id}")
    if response.status_code != 200:
        return None

    species_data = response.json()
    evolution_url = species_data["evolution_chain"]["url"]
    evolution_data = requests.get(evolution_url).json()
    
    chain = evolution_data['chain']
    evolution_chain = []
    
    while chain:
        evolution_chain.append(chain['species']['name'])
        if 'evolves_to' in chain and len(chain['evolves_to']) > 0:
            chain = chain['evolves_to'][0]
        else:
            break
    
    return evolution_chain

def get_moves_with_damage(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    pokemon_name = data["name"]
    moves_with_details = {}

    for move in data["moves"]:
        for version in move["version_group_details"]:
            if version["move_learn_method"]["name"] == "level-up" and version["version_group"]["name"] == "black-white":
                move_name = move["move"]["name"]
                level = version["level_learned_at"]

                # Récupérer les détails du move
                move_response = requests.get(f"https://pokeapi.co/api/v2/move/{move_name}")
                if move_response.status_code == 200:
                    move_data = move_response.json()
                    moves_with_details[move_name] = {
                        "level_learned_at": level,
                        "type": move_data["type"]["name"],
                        "power": move_data["power"],
                        "accuracy": move_data["accuracy"],
                        "pp": move_data["pp"],
                        "priority": move_data["priority"],
                        "effect": move_data["effect_entries"][0]["effect"] if move_data["effect_entries"] else "No effect description",
                    }

    return moves_with_details

def get_pokedex_entry(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    entries = set()
    for entry in data["flavor_text_entries"]:
        if entry["language"]["name"] == "fr":
            entries.add(entry["flavor_text"].replace("\n", " ").replace("\f", " "))
    return list(entries)[:3]  # Garder 3 entrées uniques max

for pokemon_id in range(START_ID, END_ID + 1):
    print(f"Fetching Pokémon {pokemon_id}...")

    try:
        # 🔥 Récupérer les infos générales
        pokemon_data = requests.get(f"{BASE_URL}pokemon/{pokemon_id}").json()
        species_data = requests.get(f"{BASE_URL}pokemon-species/{pokemon_id}").json()

        # 🎨 Sprites (images du Pokémon)
        sprites = {
            "front_normal": pokemon_data["sprites"]["front_default"],
            "back_normal": pokemon_data["sprites"]["back_default"],
            "front_shiny": pokemon_data["sprites"]["front_shiny"],
            "back_shiny": pokemon_data["sprites"]["back_shiny"],
            "official_artwork": pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
        }

        # 🔹 Types et efficacité
        types = [t["type"]["name"] for t in pokemon_data["types"]]
        weaknesses, resistances, immunities = get_type_effectiveness(types)

        # 📜 Pokedex entries
        descriptions = get_pokedex_entry(pokemon_id)

        # 📈 Statistiques
        stats = {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]}

        # 🎮 Attaques et dégâts
        moves = get_moves_with_damage(pokemon_id)

        # ⭐ Capacités spéciales
        abilities = [a["ability"]["name"] for a in pokemon_data["abilities"]]

        # 🌱 Chaîne d’évolution
        evolution_chain_url = species_data["evolution_chain"]["url"]
        evolution_chain_id = evolution_chain_url.split("/")[-2]
        evolution_chain = requests.get(f"{BASE_URL}evolution-chain/{evolution_chain_id}").json()

        # 🏆 Stockage des données
        DATA[pokemon_id] = {
            "id": pokemon_data["id"], #oui
            "name": pokemon_data["name"], #oui
            "types": types, #oui
            "weaknesses": weaknesses, #oui
            "resistances": resistances, #oui
            "immunities": immunities, #oui
            "height": pokemon_data["height"] / 10,  # Converti en mètres oui
            "weight": pokemon_data["weight"] / 10,  # Converti en kg oui
            "stats": stats, #oui
            "base_experience": pokemon_data["base_experience"],
            "abilities": abilities, #non null
            "moves": moves, #oui
            "sprites": sprites, #oui
            "pokedex_entries": descriptions, #oui
            "color": species_data["color"]["name"], #oui
            "shape": species_data["shape"]["name"] if species_data["shape"] else None, #oui
            "habitat": species_data["habitat"]["name"] if species_data["habitat"] else None, #oui
            "capture_rate": species_data["capture_rate"], #oui
            "base_happiness": species_data["base_happiness"], #oui
            "growth_rate": species_data["growth_rate"]["name"], #oui
            "evolution_chain": evolution_chain #oui
        }

        time.sleep(0.5)  # Éviter d'être bloqué par l'API

    except Exception as e:
        print(f"❌ Erreur avec le Pokémon {pokemon_id}: {e}")

# 💾 Sauvegarde en JSON
with open("pokemon.json", "w", encoding="utf-8") as f:
    json.dump(DATA, f, indent=4, ensure_ascii=False)

print("✅ Données récupérées et enregistrées !")

































# def get_pokemon_data(pokemon_id):
#     url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
#     response = requests.get(url)
    
#     if response.status_code != 200:
#         print(f"Erreur lors de la récupération des données pour le Pokémon ID {pokemon_id}")
#         return None
    
#     data = response.json()
    
#     pokemon_data = {
#         'ID': data['id'],
#         'Nom': data['name'],
#         'Types': [type_info['type']['name'] for type_info in data['types']],
#         'Stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
#         'Abilities': [ability['ability']['name'] for ability in data['abilities']],
#         'Taille': data['height'] / 10,  # Taille en mètres
#         'Poids': data['weight'] / 10,  # Poids en kilogrammes
#         'Sprites': {
#             'Sprite normal de face': data['sprites']['front_default'],
#             'Sprite normal de dos': data['sprites']['back_default'],
#             'Sprite shiny de face': data['sprites']['front_shiny'],
#             'Sprite shiny de dos': data['sprites']['back_shiny'],
#             'Artworks officiel': data['sprites']['other']['official-artwork']['front_default']
#         },
#         'Evolution': get_evolution_chain(data['id']),
#         'Moves': [move['move']['name'] for move in data['moves']],
#         'Moveset par niveau': get_moveset_by_level(data['id']),
#         'Rarete': 'Non disponible dans l’API standard',  # Information non disponible
#         'Stats des capacites cachees': get_hidden_abilities(data['id']),
#         'Faiblesses': get_weaknesses(data['types']),
#         'Resistances': get_resistances(data['types']),
#         'Immunités': get_immunities(data['types']),
#     }
    
#     return pokemon_data

# def get_evolution_chain(pokemon_id):
#     url = f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}'
#     response = requests.get(url)
    
#     if response.status_code != 200:
#         print(f"Erreur lors de la récupération de la chaîne d’évolution pour le Pokémon ID {pokemon_id}")
#         return None
    
#     species_data = response.json()
#     evolution_url = species_data['evolution_chain']['url']
#     evolution_response = requests.get(evolution_url)
    
#     if evolution_response.status_code != 200:
#         print(f"Erreur lors de la récupération de l’évolution pour le Pokémon ID {pokemon_id}")
#         return None
    
#     evolution_data = evolution_response.json()
#     chain = evolution_data['chain']
#     evolution_chain = []
    
#     while chain:
#         evolution_chain.append(chain['species']['name'])
#         if 'evolves_to' in chain and len(chain['evolves_to']) > 0:
#             chain = chain['evolves_to'][0]
#         else:
#             break
    
#     return evolution_chain

# def get_moveset_by_level(pokemon_id):
#     url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
#     response = requests.get(url)
    
#     if response.status_code != 200:
#         print(f"Erreur lors de la récupération du moveset pour le Pokémon ID {pokemon_id}")
#         return None
    
#     data = response.json()
#     moveset_by_level = {}
    
#     for move in data['moves']:
#         if move['version_group_details'][0]['level_learned_at'] > 0:
#             level = move['version_group_details'][0]['level_learned_at']
#             if level not in moveset_by_level:
#                 moveset_by_level[level] = []
#             moveset_by_level[level].append(move['move']['name'])
    
#     return moveset_by_level

# def get_hidden_abilities(pokemon_id):
#     url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
#     response = requests.get(url)
    
#     if response.status_code != 200:
#         print(f"Erreur lors de la récupération des capacités cachées pour le Pokémon ID {pokemon_id}")
#         return None
    
#     data = response.json()
#     hidden_abilities = [ability['ability']['name'] for ability in data['abilities'] if 'hidden' in ability['ability']['name']]
    
#     return hidden_abilities

# def get_weaknesses(types):
#     weaknesses = []
#     for pokemon_type in types:
#         url = f'https://pokeapi.co/api/v2/type/{pokemon_type}'
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             type_data = response.json()
#             for weak in type_data['damage_relations']['double_damage_from']:
#                 weaknesses.append(weak['name'])
    
#     return list(set(weaknesses))

# def get_resistances(types):
#     resistances = []
#     for pokemon_type in types:
#         url = f'https://pokeapi.co/api/v2/type/{pokemon_type}'
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             type_data = response.json()
#             for resistant in type_data['damage_relations']['half_damage_from']:
#                 resistances.append(resistant['name'])
    
#     return list(set(resistances))

# def get_immunities(types):
#     immunities = []
#     for pokemon_type in types:
#         url = f'https://pokeapi.co/api/v2/type/{pokemon_type}'
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             type_data = response.json()
#             for immune in type_data['damage_relations']['no_damage_from']:
#                 immunities.append(immune['name'])
    
#     return list(set(immunities))

# def save_pokemon_data():
#     all_pokemon_data = []
#     for i in range(1, 2):  # Pour les 650 premiers Pokémon
#         pokemon_data = get_pokemon_data(i)
#         if pokemon_data:
#             all_pokemon_data.append(pokemon_data)
    
#     with open('pokemon1.json', 'w') as f:
#         json.dump(all_pokemon_data, f, indent=4)

# if __name__ == '__main__':
#     save_pokemon_data()



















# BASE_URL = "https://pokeapi.co/api/v2/"
# START_ID = 1  # Premier Pokémon (Bulbizarre)
# END_ID = 1  # Dernier Pokémon à récupérer
# DATA = {}

# def get_type_effectiveness(types):
#     """ Récupère les faiblesses, résistances et immunités du Pokémon """
#     weaknesses = set()
#     resistances = set()
#     immunities = set()

#     for type_name in types:
#         type_data = requests.get(f"{BASE_URL}type/{type_name}").json()
#         weaknesses.update([t["name"] for t in type_data["damage_relations"]["double_damage_from"]])
#         resistances.update([t["name"] for t in type_data["damage_relations"]["half_damage_from"]])
#         immunities.update([t["name"] for t in type_data["damage_relations"]["no_damage_from"]])
#         time.sleep(0.2)  # Petite pause pour ne pas spam l'API

#     # Gestion des doubles types :
#     resistances -= weaknesses  # Un type annule une faiblesse si l'autre le résiste
#     immunities -= weaknesses   # Une immunité prévaut toujours

#     return list(weaknesses), list(resistances), list(immunities)

# for pokemon_id in range(START_ID, END_ID + 1):
#     print(f"Fetching Pokémon {pokemon_id}...")

#     try:
#         # 🔥 Récupérer les infos générales
#         pokemon_data = requests.get(f"{BASE_URL}pokemon/{pokemon_id}").json()
#         species_data = requests.get(f"{BASE_URL}pokemon-species/{pokemon_id}").json()

#         # 🎨 Sprites (images du Pokémon)
#         sprites = pokemon_data["sprites"]["front_default"]

#         # 🔹 Récupérer les types
#         types = [t["type"]["name"] for t in pokemon_data["types"]]
#         weaknesses, resistances, immunities = get_type_effectiveness(types)

#         # 📜 Récupérer les descriptions du Pokédex
#         descriptions = [entry["flavor_text"] for entry in species_data["flavor_text_entries"] if entry["language"]["name"] == "fr"]

#         # 🔗 Récupérer la chaîne d'évolution
#         evolution_chain_url = species_data["evolution_chain"]["url"]
#         evolution_chain_id = evolution_chain_url.split("/")[-2]
#         evolution_chain_data = requests.get(f"{BASE_URL}evolution-chain/{evolution_chain_id}").json()

#         # 📈 Récupérer les stats
#         stats = {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]}

#         # 🎮 Récupérer toutes les attaques disponibles
#         moves = [m["move"]["name"] for m in pokemon_data["moves"]]

#         # ⭐ Récupérer les capacités spéciales
#         abilities = [a["ability"]["name"] for a in pokemon_data["abilities"]]

#         # 🏆 Stocker toutes les données
#         DATA[pokemon_id] = {
#             "id": pokemon_data["id"],
#             "name": pokemon_data["name"],
#             "types": types,
#             "weaknesses": weaknesses,
#             "resistances": resistances,
#             "immunities": immunities,
#             "height": pokemon_data["height"],
#             "weight": pokemon_data["weight"],
#             "stats": stats,
#             "abilities": abilities,
#             "moves": moves,
#             "sprite": sprites,
#             "pokedex_entries": descriptions,
#             "color": species_data["color"]["name"],
#             "shape": species_data["shape"]["name"] if species_data["shape"] else None,
#             "habitat": species_data["habitat"]["name"] if species_data["habitat"] else None,
#             "capture_rate": species_data["capture_rate"],
#             "base_happiness": species_data["base_happiness"],
#             "growth_rate": species_data["growth_rate"]["name"],
#             "evolution_chain": evolution_chain_data
#         }

#         time.sleep(0.5)  # Éviter d'être bloqué par l'API

#     except Exception as e:
#         print(f"❌ Erreur avec le Pokémon {pokemon_id}: {e}")

# # 💾 Sauvegarde en JSON
# with open("pokemon2.json", "w", encoding="utf-8") as f:
#     json.dump(DATA, f, indent=4, ensure_ascii=False)

# print("✅ Données récupérées et enregistrées !")

























#             # "id":
#             # "name":
#             # "types":
#             # "weaknesses":
#             # "resistances":
#             # "immunities":
#             # "height":
#             # "weight":
#             # "stats":
#             # "abilities":
#             # "moves":
#             # "sprites": {
#             #     "front_normal_sprite":
#             #     "back_normal_sprite":
#             #     "front_shiny_sprite":
#             #     "back_shiny_sprite":
#             #     "official_artworks":
#             # },
#             # "pokedex_entries":
#             # "color":
#             # "shape":
#             # "habitat":
#             # "capture_rate":
#             # "base_happiness":
#             # "growth_rate":
#             # "evolution_chain":
#             # "evolution":
#             # "moveset_by_level: 




















# import requests
# import time
# import json

# BASE_URL = "https://pokeapi.co/api/v2/"
# START_ID = 1  # Premier Pokémon (ex: Bulbizarre)
# END_ID = 1  # Modifier pour récupérer plus de Pokémon
# DATA = {}

# def get_type_effectiveness(types):
#     """ Récupère les faiblesses, résistances et immunités du Pokémon """
#     weaknesses, resistances, immunities = set(), set(), set()

#     for type_name in types:
#         response = requests.get(f"{BASE_URL}type/{type_name}")
#         if response.status_code == 200:
#             type_data = response.json()
#             weaknesses.update([t["name"] for t in type_data["damage_relations"]["double_damage_from"]])
#             resistances.update([t["name"] for t in type_data["damage_relations"]["half_damage_from"]])
#             immunities.update([t["name"] for t in type_data["damage_relations"]["no_damage_from"]])
#             time.sleep(0.2)

#     resistances -= weaknesses  # Une résistance annule une faiblesse
#     immunities -= weaknesses   # Une immunité prévaut toujours

#     return list(weaknesses), list(resistances), list(immunities)

# def get_evolution_chain(pokemon_id):
#     """ Récupère la chaîne d’évolution du Pokémon """
#     response = requests.get(f"{BASE_URL}pokemon-species/{pokemon_id}")
#     if response.status_code != 200:
#         return None

#     species_data = response.json()
#     evolution_url = species_data["evolution_chain"]["url"]
#     evolution_data = requests.get(evolution_url).json()
    
#     chain = evolution_data['chain']
#     evolution_chain = []
    
#     while chain:
#         evolution_chain.append(chain['species']['name'])
#         if 'evolves_to' in chain and len(chain['evolves_to']) > 0:
#             chain = chain['evolves_to'][0]
#         else:
#             break
    
#     return evolution_chain

# def get_moves_with_damage(pokemon_id):
#     """ Récupère les attaques du Pokémon avec leurs dégâts """
#     response = requests.get(f"{BASE_URL}pokemon/{pokemon_id}")
#     if response.status_code != 200:
#         return None

#     data = response.json()
#     moves_with_damage = {}

#     for move in data['moves']:
#         move_name = move['move']['name']
#         move_details = requests.get(move['move']['url']).json()

#         power = move_details.get('power', 'Inconnu')  # Certains moves n'ont pas de puissance
#         accuracy = move_details.get('accuracy', 'Inconnue')
#         pp = move_details.get('pp', 'Inconnu')
#         type_move = move_details['type']['name']

#         moves_with_damage[move_name] = {
#             "type": type_move,
#             "power": power,
#             "accuracy": accuracy,
#             "pp": pp
#         }

#         time.sleep(0.2)  # Pause pour éviter le spam API

#     return moves_with_damage

# for pokemon_id in range(START_ID, END_ID + 1):
#     print(f"Fetching Pokémon {pokemon_id}...")

#     try:
#         # 🔥 Récupérer les infos générales
#         pokemon_data = requests.get(f"{BASE_URL}pokemon/{pokemon_id}").json()
#         species_data = requests.get(f"{BASE_URL}pokemon-species/{pokemon_id}").json()

#         # 🎨 Sprites (images du Pokémon)
#         sprites = {
#             "front_normal": pokemon_data["sprites"]["front_default"],
#             "back_normal": pokemon_data["sprites"]["back_default"],
#             "front_shiny": pokemon_data["sprites"]["front_shiny"],
#             "back_shiny": pokemon_data["sprites"]["back_shiny"],
#             "official_artwork": pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
#         }

#         # 🔹 Types et efficacité
#         types = [t["type"]["name"] for t in pokemon_data["types"]]
#         weaknesses, resistances, immunities = get_type_effectiveness(types)

#         # 📜 Pokedex entries
#         descriptions = [entry["flavor_text"] for entry in species_data["flavor_text_entries"] if entry["language"]["name"] == "fr"]

#         # 📈 Statistiques
#         stats = {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]}

#         # 🎮 Attaques et dégâts
#         moves = get_moves_with_damage(pokemon_id)

#         # ⭐ Capacités spéciales
#         abilities = [a["ability"]["name"] for a in pokemon_data["abilities"]]

#         # 🌱 Chaîne d’évolution
#         evolution_chain = get_evolution_chain(pokemon_id)

#         # 🏆 Stockage des données
#         DATA[pokemon_id] = {
#             "id": pokemon_data["id"],
#             "name": pokemon_data["name"],
#             "types": types,
#             "weaknesses": weaknesses,
#             "resistances": resistances,
#             "immunities": immunities,
#             "height": pokemon_data["height"] / 10,  # Converti en mètres
#             "weight": pokemon_data["weight"] / 10,  # Converti en kg
#             "stats": stats,
#             "abilities": abilities,
#             "moves": moves,
#             "sprites": sprites,
#             "pokedex_entries": descriptions,
#             "color": species_data["color"]["name"],
#             "shape": species_data["shape"]["name"] if species_data["shape"] else None,
#             "habitat": species_data["habitat"]["name"] if species_data["habitat"] else None,
#             "capture_rate": species_data["capture_rate"],
#             "base_happiness": species_data["base_happiness"],
#             "growth_rate": species_data["growth_rate"]["name"],
#             "evolution_chain": evolution_chain
#         }

#         time.sleep(0.5)  # Éviter d'être bloqué par l'API

#     except Exception as e:
#         print(f"❌ Erreur avec le Pokémon {pokemon_id}: {e}")

# # 💾 Sauvegarde en JSON
# with open("pokemon3.json", "w", encoding="utf-8") as f:
#     json.dump(DATA, f, indent=4, ensure_ascii=False)

# print("✅ Données récupérées et enregistrées !")






























# import requests
# import json

# # Liste des types et interactions
# TYPE_CHART = {
#     "normal": {"weak": ["fighting"], "resist": [], "immune": ["ghost"]},
#     "fire": {"weak": ["water", "ground", "rock"], "resist": ["fire", "grass", "ice", "bug", "steel", "fairy"], "immune": []},
#     "water": {"weak": ["electric", "grass"], "resist": ["fire", "water", "ice", "steel"], "immune": []},
#     "electric": {"weak": ["ground"], "resist": ["electric", "flying", "steel"], "immune": []},
#     "grass": {"weak": ["fire", "ice", "poison", "flying", "bug"], "resist": ["water", "electric", "grass", "ground"], "immune": []},
#     "ice": {"weak": ["fire", "fighting", "rock", "steel"], "resist": ["ice"], "immune": []},
#     "fighting": {"weak": ["flying", "psychic", "fairy"], "resist": ["bug", "rock", "dark"], "immune": []},
#     "poison": {"weak": ["ground", "psychic"], "resist": ["grass", "fighting", "poison", "bug", "fairy"], "immune": []},
#     "ground": {"weak": ["water", "grass", "ice"], "resist": ["poison", "rock"], "immune": ["electric"]},
#     "flying": {"weak": ["electric", "ice", "rock"], "resist": ["grass", "fighting", "bug"], "immune": ["ground"]},
#     "psychic": {"weak": ["bug", "ghost", "dark"], "resist": ["fighting", "psychic"], "immune": []},
#     "bug": {"weak": ["fire", "flying", "rock"], "resist": ["grass", "fighting", "ground"], "immune": []},
#     "rock": {"weak": ["water", "grass", "fighting", "ground", "steel"], "resist": ["normal", "fire", "poison", "flying"], "immune": []},
#     "ghost": {"weak": ["ghost", "dark"], "resist": ["poison", "bug"], "immune": ["normal", "fighting"]},
#     "dragon": {"weak": ["ice", "dragon", "fairy"], "resist": ["fire", "water", "electric", "grass"], "immune": []},
#     "dark": {"weak": ["fighting", "bug", "fairy"], "resist": ["ghost", "dark"], "immune": ["psychic"]},
#     "steel": {"weak": ["fire", "fighting", "ground"], "resist": ["normal", "grass", "ice", "flying", "psychic", "bug", "rock", "dragon", "steel", "fairy"], "immune": ["poison"]},
#     "fairy": {"weak": ["poison", "steel"], "resist": ["fighting", "bug", "dark"], "immune": ["dragon"]}
# }

# # Récupérer la liste des Pokémon (jusqu'à Genesect)
# POKEMON_COUNT = 1  # Genesect est le numéro 649

# def get_pokemon_data(pokemon_id):
#     url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return None
#     return response.json()

# def get_pokedex_entry(pokemon_id):
#     url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return []
#     data = response.json()
#     entries = set()
#     for entry in data["flavor_text_entries"]:
#         if entry["language"]["name"] == "fr":
#             entries.add(entry["flavor_text"].replace("\n", " ").replace("\f", " "))
#     return list(entries)[:3]  # Garder 3 entrées uniques max

# def calculate_weaknesses_resistances(types):
#     weaknesses = set()
#     resistances = set()
#     immunities = set()

#     for t in types:
#         type_data = TYPE_CHART.get(t, {})
#         weaknesses.update(type_data.get("weak", []))
#         resistances.update(type_data.get("resist", []))
#         immunities.update(type_data.get("immune", []))

#     # Supprimer les résistances des faiblesses (ex: Plante et Eau)
#     weaknesses -= resistances
#     weaknesses -= immunities

#     return list(weaknesses), list(resistances), list(immunities)

# def get_clean_moves(moves):
#     cleaned_moves = {}
#     for move in moves:
#         move_data = move["move"]["name"]
#         move_url = move["move"]["url"]
#         response = requests.get(move_url)
#         if response.status_code != 200:
#             continue
#         move_info = response.json()
        
#         # Vérifier que l'attaque a une puissance ou un effet utile
#         power = move_info.get("power")
#         accuracy = move_info.get("accuracy")
#         move_type = move_info["type"]["name"]
#         pp = move_info.get("pp")

#         if power is not None or accuracy is not None or move_info["damage_class"]["name"] != "status":
#             cleaned_moves[move_data] = {
#                 "type": move_type,
#                 "power": power,
#                 "accuracy": accuracy,
#                 "pp": pp
#             }
    
#     return cleaned_moves

# def create_pokemon_json(pokemon_id):
#     data = get_pokemon_data(pokemon_id)
#     if not data:
#         return None

#     name = data["name"]
#     types = [t["type"]["name"] for t in data["types"]]
#     height = data["height"] / 10  # Convertir en mètres
#     weight = data["weight"] / 10  # Convertir en kg
#     abilities = [a["ability"]["name"] for a in data["abilities"]]
    
#     stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
#     moves = get_clean_moves(data["moves"])
#     pokedex_entries = get_pokedex_entry(pokemon_id)

#     weaknesses, resistances, immunities = calculate_weaknesses_resistances(types)

#     pokemon_json = {
#         "id": pokemon_id,
#         "name": name,
#         "types": types,
#         "weaknesses": weaknesses,
#         "resistances": resistances,
#         "immunities": immunities,
#         "height": height,
#         "weight": weight,
#         "stats": stats,
#         "abilities": abilities,
#         "moves": moves,
#         "pokedex_entries": pokedex_entries,
#         "sprites": {
#             "front": data["sprites"]["front_default"],
#             "back": data["sprites"]["back_default"],
#             "shiny": data["sprites"]["front_shiny"]
#         }
#     }

#     return pokemon_json

# # Générer JSON pour tous les Pokémon
# pokemon_data_list = {}
# for i in range(1, POKEMON_COUNT + 1):
#     print(f"Processing Pokémon {i}...")
#     pokemon_data_list[i] = create_pokemon_json(i)

# with open("pokemon4.json", "w", encoding="utf-8") as f:
#     json.dump(pokemon_data_list, f, indent=4, ensure_ascii=False)

# print("✅ JSON généré : 'pokemon_data.json'")




























# import requests
# import json

# def get_level_up_moves_gen5(pokemon_id):
#     url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         return None

#     data = response.json()
#     level_up_moves = {}

#     for move in data["moves"]:
#         for version in move["version_group_details"]:
#             if version["move_learn_method"]["name"] == "level-up" and version["version_group"]["name"] == "black-white":
#                 level = version["level_learned_at"]
#                 move_name = move["move"]["name"]
#                 level_up_moves[move_name] = level

#     return data["name"], level_up_moves  # Retourne aussi le nom du Pokémon

# def get_move_details(move_name):
#     url = f"https://pokeapi.co/api/v2/move/{move_name}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         return {}

#     data = response.json()
#     move_details = {
#         "name": move_name,
#         "type": data["type"]["name"],
#         "power": data["power"],
#         "accuracy": data["accuracy"],
#         "pp": data["pp"],
#         "priority": data["priority"],
#         "effect": data["effect_entries"][0]["effect"] if data["effect_entries"] else "No effect description",
#     }

#     return move_details

# # 🔥 Boucle sur les 650 premiers Pokémon
# for pokemon_id in range(1, 2):  # Génération pour les Pokémon 1 à 650
#     result = get_level_up_moves_gen5(pokemon_id)

#     if result:
#         pokemon_name, moves = result
#         moves_with_details = {}

#         for move, level in moves.items():
#             moves_with_details[move] = {
#                 "level_learned_at": level,
#                 **get_move_details(move)  # Fusionne les détails
#             }

#         # 🔹 Stocker dans un JSON
#         with open(f"pokemon5.json", "w", encoding="utf-8") as f:
#             json.dump(moves_with_details, f, indent=4, ensure_ascii=False)

#         print(f"✅ Fichier {pokemon_name.lower()}_gen5_moves.json créé avec succès !")
#     else:
#         print(f"❌ Erreur : Pokémon ID {pokemon_id} non trouvé !")
