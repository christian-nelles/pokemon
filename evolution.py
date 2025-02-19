import json

# Fonction pour charger les données Pokémon
def load_pokemon_data():
    with open("pokemon.json", "r") as f:
        return json.load(f)

# Fonction pour gagner de l'XP
def gain_experience(inventory, player_pokemon, base_experience, id):
    with open('inventaire.json', 'r') as f:
        inventaire = json.load(f)

    def ajouter_xp(pokemon_id, xp_a_ajouter):
        if pokemon_id in inventaire:
            inventaire[pokemon_id]["exp"] = (inventaire[pokemon_id]["exp"] or 0) + xp_a_ajouter
            print(f"XP ajouté au Pokémon {pokemon_id}. Nouvelle XP: {inventaire[pokemon_id]['exp']}")
        else:
            print(f"Pokémon avec l'id {pokemon_id} non trouvé.")

    # On trouve le Pokémon dans l'inventaire
    for slot, pokemon in inventory.items():
        if id == player_pokemon.id:
            # Ajout de l'XP
            growth_rate = "medium-slow"  # Ici on le met en dur, mais tu peux le récupérer depuis `pokemon.json`
            gained_xp = base_experience  # L'XP que le Pokémon gagne

            # pokemon["exp"] += gained_xp

            # Exemple d'utilisation : ajouter 50 XP au Pokémon avec l'id "1"
            ajouter_xp("1", gained_xp)

            # Sauvegarder les modifications dans le fichier JSON
            with open('inventaire.json', 'w') as f:
                json.dump(inventaire, f, indent=4)

            print(f"{pokemon['id']} a gagné {gained_xp} XP. Total XP : {pokemon['exp']}.")

            # Définir le seuil d'évolution en fonction du growth_rate (simplifié ici)
            level_up_threshold = 100  # Ce seuil peut varier en fonction du growth_rate

            # Vérifier si le Pokémon monte de niveau
            # while inventaire[id].get("exp") >= level_up_threshold:
            #     inventaire[id]["exp"] = (inventaire[pokemon_id]["exp"] or 0) + xp_a_ajouter
            #     pokemon["level"] += 1
            #     pokemon["exp"] -= level_up_threshold  # Ajuster l'XP restante après montée de niveau
            #     print(f"{pokemon['id']} a atteint le niveau {pokemon['level']} !")

            #     # Vérifier si le Pokémon doit évoluer
            #     evolve(pokemon)

            #     # Vérifier si de nouvelles attaques sont apprises
            #     learn_new_attack(pokemon, inventory)

def evolve(pokemon):
    with open("pokemon.json", "r") as f:
        pokemon_data = json.load(f)

    species_name = pokemon["id"]
    evolution_chain = pokemon_data["evolution_chain"]["chain"]

    # Cherche la chaîne d'évolution jusqu'à trouver l'espèce correspondante
    while evolution_chain["species"]["name"] != species_name:
        evolution_chain = evolution_chain["evolves_to"][0]

    # Vérifier si le Pokémon doit évoluer à ce niveau
    for evolution in evolution_chain["evolves_to"]:
        min_level = evolution["evolution_details"][0]["min_level"]
        if pokemon["level"] >= min_level:
            new_species = evolution["species"]["name"]
            if pokemon["id"] != new_species:
                pokemon["id"] = new_species
                print(f"Félicitations ! Votre Pokémon évolue en {new_species} !")
            break

def learn_new_attack(pokemon, inventory):
    # Vérifier les attaques que le Pokémon peut apprendre
    for attack_name, attack_details in pokemon["moves"].items():
        if attack_details["level_learned_at"] == pokemon["level"]:
            # Le Pokémon apprend cette attaque s'il ne la connaît pas déjà
            if attack_name not in pokemon["attack_list"].values():
                print(f"{pokemon['id']} a appris {attack_name} !")

                # Ajouter l'attaque à la première case vide dans l'inventaire
                for slot, poke_data in inventory.items():
                    if poke_data["id"] == pokemon["id"]:
                        attack_list = poke_data["attack_list"]
                        for key in attack_list:
                            if attack_list[key] is None:
                                attack_list[key] = attack_name
                                return
