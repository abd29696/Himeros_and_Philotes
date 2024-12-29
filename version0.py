import random
import time
import sys

def start_game():
    """
    Function to take input for the number of players in the game, their names, and genders.
    """
    try:
        print("Welcome!\n")
        num_players = int(input("Enter the number of players (2-6): "))
        if 2 <= num_players <= 6:
            print(f"\nGreat! {num_players} player(s) will play the game. Let's begin!\n")
            player_details = []
            for i in range(1, num_players + 1):
                name = input(f"Enter the name for Player {i}: ").strip()
                while not name:
                    print("Name cannot be empty. Please enter a valid name.")
                    name = input(f"Enter the name for Player {i}: ").strip()
                
                gender = input(f"Enter the gender for Player {i} (M/F): ").strip().upper()
                while gender not in ["M", "F"]:
                    print("Invalid input. Please enter 'M' for Male or 'F' for Female.")
                    gender = input(f"Enter the gender for Player {i} (M/F): ").strip().upper()
                
                player_details.append({"name": name, "gender": gender})
            
            print("\nPlayers:")
            for p in player_details:
                gender_label = "Male" if p['gender'] == 'M' else "Female"
                print(f"{p['name']} ({gender_label})")
            
            # Initialize all players at position 0
            player_positions = {p["name"]: 0 for p in player_details}
            print("\nAll players start at position 0.")
            return player_details, player_positions
        else:
            print("\nInvalid input. Please enter a number between 2 and 6.")
            return start_game()
    except ValueError:
        print("\nInvalid input. Please enter a valid number.")
        return start_game()

def roll_dice():
    """
    Simulates rolling a dice and returning the result.
    """
    while True:
        try:
            dice_value = int(input("Enter the number you rolled on the dice (1-6): "))
            if 1 <= dice_value <= 6:
                return dice_value
            else:
                print("Invalid input. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def generate_snakes_and_ladders():
    """
    Generates random positions for snakes and ladders within a range of +/- 10.
    """
    snakes = {}
    ladders = {}
    while len(snakes) < 5:
        start = random.randint(11, 90)
        end = start - random.randint(1, 10)
        if end > 0:
            snakes[start] = end
    while len(ladders) < 5:
        start = random.randint(1, 89)
        end = start + random.randint(1, 10)
        if end <= 99:
            ladders[start] = end
    print("\nSnakes: ", snakes)
    print("Ladders: ", ladders, "\n")
    return snakes, ladders

def load_actions(file_path):
    """
    Loads actions from an external file based on intensity stages.
    If the file is not found, returns placeholder actions.
    """
    actions = {"Flirty": [], "Teasing": [], "Erotic": [], "Positions": []}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("Flirty"):
                    actions["Flirty"].append(line.split(": ")[1])
                elif line.startswith("Teasing"):
                    actions["Teasing"].append(line.split(": ")[1])
                elif line.startswith("Erotic"):
                    actions["Erotic"].append(line.split(": ")[1])
                elif line.startswith("Positions"):
                    actions["Positions"].append(line.split(": ")[1])
    except FileNotFoundError:
        print("Warning: actions.txt file not found. Defaulting to placeholder actions.\n")
        actions = {"Flirty": ["XXX"], "Teasing": ["XXX"], "Erotic": ["XXX"], "Positions": ["XXX"]}
    return actions

def get_action(position, actions):
    """
    Returns a random action based on the player's position intensity stage.
    """
    if 0 <= position <= 25:
        return random.choice(actions["Flirty"]), random.randint(30, 90)
    elif 26 <= position <= 50:
        return random.choice(actions["Teasing"]), random.randint(60, 120)
    elif 51 <= position <= 75:
        return random.choice(actions["Erotic"]), random.randint(90, 180)
    elif 76 <= position <= 99:
        return random.choice(actions["Positions"]), random.randint(180, 360)
    return "No action available.", 0

def play_game():
    """
    Runs the game with players taking turns, handling dice rolls, and enforcing rules.
    """
    player_details, player_positions = start_game()
    snakes, ladders = generate_snakes_and_ladders()
    actions = load_actions("actions.txt")  # Load actions from external file
    current_player_idx = 0
    players_completed = []  # List of players who reached 100
    player_actions_log = {p["name"]: [] for p in player_details}  # Track actions performed

    print("\nGame starts now!\n")
    while len(players_completed) < len(player_details):
        current_player = player_details[current_player_idx]["name"]
        if current_player in players_completed:
            current_player_idx = (current_player_idx + 1) % len(player_details)
            continue

        six_count = 0
        turn_total = 0  # Accumulates the moves for the turn

        while True:
            print(f"{current_player}'s turn! (Current Position: {player_positions[current_player]})")
            dice_value = roll_dice()
            print(f"{current_player} rolled a {dice_value}!")

            if dice_value == 6:
                six_count += 1
                print("Hooray! You get another chance!")
                if six_count == 3:
                    print("Oh no! You rolled 6 three times. Your turn is skipped!\n")
                    break
            else:
                # Add the accumulated total (including all previous 6s) to the position
                turn_total += 6 * six_count + dice_value
                player_positions[current_player] += turn_total

                if player_positions[current_player] in snakes:
                    print(f"Oh no! {current_player} encountered a snake and slid down to {snakes[player_positions[current_player]]}!")
                    player_positions[current_player] = snakes[player_positions[current_player]]
                elif player_positions[current_player] in ladders:
                    print(f"Yay! {current_player} found a ladder and climbed up to {ladders[player_positions[current_player]]}!")
                    player_positions[current_player] = ladders[player_positions[current_player]]

                print(f"{current_player} is now at position {player_positions[current_player]}.")
                action, duration = get_action(player_positions[current_player], actions)
                print(f"Action for {current_player}: {action} (Duration: {duration} seconds)\n")
                player_actions_log[current_player].append(action)

                if player_positions[current_player] >= 100:
                    player_positions[current_player] = 100
                    print(f"Congratulations {current_player}! You have reached position 100 and completed the game!\n")
                    players_completed.append(current_player)
                break
        current_player_idx = (current_player_idx + 1) % len(player_details)

    print("\nAll players have reached position 100! Game Over!")
    print("Summary of actions:")
    for player, log in player_actions_log.items():
        print(f"{player}: {', '.join(log)}")

play_game()
