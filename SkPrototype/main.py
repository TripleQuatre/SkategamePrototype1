import os
from engine.core import Player, Game
from engine.rules import GameRules, PRESET_RULES, RULES_DIR
import random

for file in os.listdir(RULES_DIR):
    if file.endswith(".json"):
        preset_name = file[:-5]  # enlever ".json"
        PRESET_RULES[preset_name] = GameRules.load(preset_name)

print("🛹 Bienvenue dans le Game of SKATE prototype ! 🛹\n")

# --- Choix du preset ou personnalisation ---
print("Choix des règles :")
preset_names = list(PRESET_RULES.keys())
for i, name in enumerate(preset_names, start=1):
    print(f"{i} - {name}")
print(f"{len(preset_names)+1} - Personnalisé")

choice = input("Votre choix : ").strip()
if choice.isdigit() and 1 <= int(choice) <= len(preset_names):
    rules = PRESET_RULES[preset_names[int(choice)-1]]
else:
    # Création d'une règle personnalisée simple (mot + essais)
    word = input("Mot pour cette partie (1-10 lettres, ENTER = SKATE) : ").upper().strip()
    if not word:
        word = "SKATE"
    while not (1 <= len(word) <= 10):
        word = input("Mot invalide. Entrez un mot 1-10 lettres : ").upper().strip()

    while True:
        tries_str = input("Nombre d'essais par défenseur (1-9, ENTER = 3) : ").strip()
        if not tries_str:
            tries = 3
            break
        if tries_str.isdigit() and 1 <= int(tries_str) <= 9:
            tries = int(tries_str)
            break
        print("Valeur invalide.")

    print("\nChoix de l'ordre des joueurs :")
    print("1 - Alphabétique (A → Z)")
    print("2 - Alphabétique inversé (Z → A)")
    print("3 - Aléatoire")
    order_choice = input("Votre choix (1/2/3, ENTER = default) : ").strip()
    if order_choice == "1":
        player_order = "alpha"
    elif order_choice == "2":
        player_order = "reverse"
    elif order_choice == "3":
        player_order = "random"
    else:
        player_order = "default"

    rules = GameRules(name="Custom", 
                      word=word, 
                      max_attempts=tries,
                      player_order=player_order
    )

    save = input("Sauvegarder cette configuration ? (o/n) : ").lower().strip() == "o"
    if save:
        filename = input("Nom du preset à sauvegarder (sans extension) : ").strip()
        if filename:
            rules.name = filename
            rules.save(filename)
            print(f"Preset sauvegardé sous rulesets/{filename}.json")

print(f"\nRègles choisies : {rules.name} — mot={rules.word} essais={rules.max_attempts}\n")
game = Game(rules=rules)

# --- Initialisation des joueurs ---
nb_players = int(input("Combien de joueurs participent ? "))
for i in range(nb_players):
    name = input(f"Nom du joueur {i+1} : ")
    game.add_player(Player(name))

# --- Appliquer l'ordre défini dans les règles ---
if game.rules.player_order == "alpha":
    game.players.sort(key=lambda p: p.name)
elif game.rules.player_order == "reverse":
    game.players.sort(key=lambda p: p.name, reverse=True)
elif game.rules.player_order == "random":
    random.shuffle(game.players)

print("\nOrdre des joueurs :")
for i, p in enumerate(game.players, start=1):
    print(f"{i} - {p.name}")

# --- Démarrage ---
game.start()

while game.is_active:
    print("\n" + "-"*40)
    attacker = game.current_attacker
    defenders = game.get_defenders()

    print(f"Tour {game.round} — {attacker.name} attaque !")
    figure = input(f"{attacker.name}, quelle figure veux-tu proposer ? ")
    print(f"\n👉 Figure : '{figure}'")

    attacker_success = input(f"{attacker.name} réussit la figure ? (o/n) : ").lower().strip() == "o"

    if not attacker_success:
        # L’attaquant rate, on saute les défenseurs
        results = game.play_turn(attacker_success, {})
        print(f"{attacker.name} rate sa figure. Le tour passe au joueur suivant.")
    else:
        # On demande les résultats des défenseurs seulement si l’attaquant a réussi
        defenders_success = {}
        for d in defenders:
            res = input(f"{d.name} réussit la figure ? (o/n) : ").lower().strip() == "o"
            defenders_success[d.name] = res

        results = game.play_turn(attacker_success, defenders_success)

        for d_name, info in results["defenders"].items():
            status = "réussit" if info["success"] else "échoue"
            print(f"{d_name} {status}, lettres : {info['letters']}")
        for eliminated in results.get("eliminated", []):
            print(f"💀 {eliminated} a été éliminé !")
        if "winner" in results:
            print(f"\n🏆 {results['winner']} remporte la partie !")

    if game.is_active:
        game.next_turn()

print("\n🏁 Fin de la partie ! Résultats :\n")
for name, letters in game.letter_map.items():
    print(f" - {name} : {letters if letters else 'Aucune lettre !'}")

print("\nMerci d’avoir joué 👋")
