# Description: This file will parse the data from the players.json file and create a data.json file with the data

# Import the json module
import json

# The main function will call the parse function
def main():
    # Call the parse function
    parse()

# The parse function will read the players.json file and create a data.json file with the data
def parse():

    # Open the file and load the data
    with open('players.json') as json_file:
        players_data = json.load(json_file)

    # Create a dictionary to map the car ids to the car names
    classC = {
        "22b_acpursuit": "Impreza 22B STI",
        "370z_acp": "370Z",
        "964turbo_acp23": "964 Turbo",
        "gt86_acp23": "GT86",
        "e46acpursuit": "M3 E46",
        "is300_acp": "IS300",
        "lancerix_acpursuit": "Lancer Evo IX",
        "rx7_2_acpursuit": "RX-7",
        "s15_acp": "Silvia S15",
        "skyr34_acp2": "Skyline R34",
        "supra93_acpursuit": "Supra Mk4",
        "mustang_acp": "Mustang",
        "nsx94_acp23": "NSX",
    }
    
    h1_data_c = {}
    vv_data = {}
    stRace_data = {}
    arrests_data = {}
    theft_data = {}
    drift_data = {}
    overtake_data = {}
    getaway_data = {}
    
    # Loop through the players_data and create the data.json file
    # Each leaderboard entry/player will be represented by a dictionary with steam_id as the key
    for player_id, player_data in players_data.items():
        steam_id = player_id
        # Create the data for the H1 leaderboard
        if "Sectors" in player_data:
            if "H1" in player_data["Sectors"]:
                h1_data = {
                    "Name": player_data["Name"]
                }
                for car_id, car_data in player_data["Sectors"]["H1"].items():
                    if car_id in classC:
                        h1_data[car_id] = {
                            "Time": car_data["Time"],
                        }
                h1_data_c[steam_id] = h1_data
        # Create the data for the VV leaderboard
        if "Sectors" in player_data:
            if "VV" in player_data["Sectors"]:
                if "Car" in player_data["Sectors"]["VV"]:
                    temp_vv = {
                        "Name": player_data["Name"],
                        "Time": player_data["Sectors"]["VV"]["Time"],
                        "Car": classC[player_data["Sectors"]["VV"]["Car"]]
                    }
                else:
                    temp_vv = {
                        "Name": player_data["Name"],
                        "Time": player_data["Sectors"]["VV"]["Time"],
                        "Car": "Unknown"
                    }
                vv_data[steam_id] = temp_vv
        # Create the data for the stRace leaderboard
        if "Wins" or "Losses" in player_data:
            temp_stRace = {
                "Name": player_data["Name"],
                "Wins": player_data["Wins"],
                "Losses": player_data["Losses"]
            }
            if temp_stRace["Wins"] + temp_stRace["Losses"] > 0:
                stRace_data[steam_id] = temp_stRace
        # Create the data for the arrests leaderboard
        if "Arrests" in player_data:
            temp_arrests = {
                "Name": player_data["Name"],
                "Arrests": player_data["Arrests"]
            }
            if temp_arrests["Arrests"] > 0:
                arrests_data[steam_id] = temp_arrests
        # Create the data for the theft leaderboard
        if "Theft" in player_data:
            temp_theft = {
                "Name": player_data["Name"],
                "Theft": player_data["Theft"]
            }
            if temp_theft["Theft"] > 0:
                theft_data[steam_id] = temp_theft
        # Create the data for the drift leaderboard
        if "Drift" in player_data:
            temp_drift = {
                "Name": player_data["Name"],
                "Drift": player_data["Drift"]
            }
            if temp_drift["Drift"] > 2500:
                drift_data[steam_id] = temp_drift
        # Create the data for the overtake leaderboard
        if "Overtake" in player_data:
            temp_overtake = {
                "Name": player_data["Name"],
                "Overtake": player_data["Overtake"]
            }
            if temp_overtake["Overtake"] > 2500:
                overtake_data[steam_id] = temp_overtake
        # Create the data for the getaway leaderboard
        if "Getaway" in player_data:
            temp_getaway = {
                "Name": player_data["Name"],
                "Getaway": player_data["Getaway"]
            }
            if temp_getaway["Getaway"] > 0:
                getaway_data[steam_id] = temp_getaway
    # Create the data.json file
    data = {
        "H1": h1_data_c,
        "VV": vv_data,
        "STRace": stRace_data,
        "Arrests": arrests_data,
        "Theft": theft_data,
        "Drift": drift_data,
        "Overtake": overtake_data,
        "Getaway": getaway_data
    }
    
    # Write the data to the data.json file
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
        
    # Print a message to the console
    print("Data parsed successfully!")
    
# Call the main function
main()