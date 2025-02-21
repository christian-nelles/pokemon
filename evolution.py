import json
import requests

# Function to earn XP
def gain_experience(inventory_save, player_pokemon, base_experience, lvl):
    try:
        requests.get("http://clients3.google.com/generate_204", timeout=5)
        with open('inventory.json', 'r') as f:
            inventory = json.load(f)
    except:
        with open('inventory_noco.json', 'r') as f:
            inventory = json.load(f)

    def add_xp(pokemon_id, xp_a_ajouter):
        if pokemon_id in inventory:
            inventory[pokemon_id]["exp"] = (inventory[pokemon_id]["exp"]) + xp_a_ajouter
            print(f"XP ajouté au Pokémon {pokemon_id}. Nouvelle XP: {inventory[pokemon_id]['exp']}")
        else:
            print(f"Pokémon avec l'id {pokemon_id} non trouvé.")

    # We find the Pokémon in the inventory
    for slot, pokemon in inventory_save.items():
        player_id = f"{player_pokemon.id}"
        if pokemon['id'] == player_id:
            status = slot
            # Added XP
            gained_xp = round((base_experience * lvl) / 7) # The XP the Pokémon earns

            pokemon["exp"] += gained_xp

            add_xp(f"{slot}", gained_xp)

            # Save changes to JSON file
            try:
                requests.get("http://clients3.google.com/generate_204", timeout=5)
                with open('inventory.json', 'w') as f:
                    json.dump(inventory, f, indent=4)
            except:
                with open('inventory_noco.json', 'w') as f:
                    json.dump(inventory, f, indent=4)

            print(f"{pokemon['id']} a gagné {gained_xp} XP. Total XP : {pokemon['exp']}.")

            # Define the evolution threshold
            level_up_threshold = 100  

            # Check if the Pokémon levels up
            while pokemon["exp"] >= level_up_threshold:
                pokemon["exp"] = (pokemon["exp"] or 0) + gained_xp
                pokemon["level"] += 1
                pokemon["exp"] -= level_up_threshold  # Adjust remaining XP after leveling up
                print(f"{pokemon['id']} a atteint le niveau {pokemon['level']} !")

                # Check if the Pokémon should evolve
                with open("pokemon.json", "r", encoding="utf-8") as f:
                    pokemon_data = json.load(f)
                
                evolve(pokemon, pokemon_data, inventory)

                #  Check if new attacks are learned
                try:
                    requests.get("http://clients3.google.com/generate_204", timeout=5)
                    with open("inventory.json", "r", encoding="utf-8") as file:
                        inventory_data = json.load(file)
                except:
                    with open("inventory_noco.json", "r", encoding="utf-8") as file:
                        inventory_data = json.load(file)
                learn_new_attack(pokemon_data[pokemon['id']], inventory_save, pokemon)

def evolve(pokemon, pokemon_data, inventory):
    print("Début de l'évolution")

    # Retrieve the Pokémon's ID and search for the evolution chain
    species_name = pokemon["id"]

    # Make sure you access this Pokémon's evolution chain
    evolution_chain = None
    for data in pokemon_data:
        data = pokemon_data[data]
        if f"{data["id"]}" == species_name:
            evolution_chain = data["evolution_chain"]
            break

    if not evolution_chain:
        print(f"Chaîne d'évolution pour le Pokémon {species_name} non trouvée.")
        return
    
    # Explore the evolution chain
    print(f"Recherche de la chaîne d'évolution pour {species_name}")
    chain = evolution_chain["chain"]
    print(pokemon_data[pokemon['id']]["name"])
    print(chain["species"]["name"])
    if chain["species"]["name"] != pokemon_data[pokemon['id']]["name"]:
        print(evolution_chain["chain"]["evolves_to"])
        chain = evolution_chain["chain"]["evolves_to"][0]

    # Now we have the corresponding evolution chain
    print(f"Chaîne d'évolution trouvée pour {species_name}. Vérification des conditions d'évolution...")

    # Checks if the Pokémon reaches the level needed to evolve
    for evolution in chain["evolves_to"]:
        min_level = evolution["evolution_details"][0]["min_level"]
        if pokemon["level"] >= min_level:
            new_species = evolution["species"]["name"]
            if pokemon["id"] != new_species:
                pokemon["id"] = new_species
                pokemon["exp"] = 0  # Reset XP
                print(f"Félicitations ! Votre Pokémon évolue en {new_species} !")
                for poke_id, data in pokemon_data.items():
                    if data["name"].lower() == new_species.lower():  # Ignore case
                        pokemon["id"] = poke_id
            try:
                requests.get("http://clients3.google.com/generate_204", timeout=5)
                with open('inventory.json', 'w') as f:
                    json.dump(inventory, f, indent=4)
            except:
                with open('inventory_noco.json', 'w') as f:
                    json.dump(inventory, f, indent=4)
            break

def learn_new_attack(pokemon, inventory_save, inventory):
    print(f"Vérification des attaques pour {pokemon["name"]} au niveau {inventory['level']}.")

    # Browse possible attacks
    for attack_name, attack_details in pokemon["moves"].items():
        if attack_details["level_learned_at"] == inventory["level"]:
            
            # Check if the Pokémon already knows this attack
            if attack_name in inventory["attack_list"].values():
                print(f"{pokemon['name']} connaît déjà {attack_name}.")
                continue

            print(f"{pokemon['name']} a appris {attack_name} !")

            # Add the attack to the first free space in the inventory
            for slot, poke_data in inventory_save.items():
                if poke_data["id"] == inventory["id"]:
                    for key, value in inventory["attack_list"].items():
                        if value is None:
                            poke_data["attack_list"][key] = attack_name
                            print(f"Attaque {attack_name} ajoutée dans l'emplacement {key}.")
                            return

            print(f"Pas d'emplacement libre pour apprendre {attack_name}.")

    print("Aucune nouvelle attaque à apprendre à ce niveau.")
