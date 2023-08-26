# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import db_fn, https_fn

# The Firebase Admin SDK to access the Firebase Realtime Database.
from firebase_admin import initialize_app, db
from operator import itemgetter

app = initialize_app()

@db_fn.on_value_updated(reference='/PlayersData')
def onUpdate(event: db_fn.Event[db_fn.Change[object]]) -> None:

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

    h1_data_c = []
    vv_data = []
    stRace_data = []
    arrests_data = []
    theft_data = [] 
    drift_data = []
    overtake_data = []
    getaway_data = []

    players_data = db.reference('/PlayersData').get()
    
    if players_data is None:  # Add a check here to ensure players_data is not None
        return
    for categories, category in players_data.items():
        if category is None:
            continue
        for player_id, player_info in category.items():
            if player_info is None:
                continue
            playerName = player_info.get('Name')
            if playerName is None:
                playerName = "Unknown"
            if categories == 'H1':
                for car_id in classC.keys():
                    time = player_info.get(car_id, {}).get('Time')
                    if time:
                        car_data = {'Time': time, 'Driver': playerName, 'Car': classC[car_id]}
                        h1_data_c.append(car_data)

            elif categories == 'VV':
                
                    time = player_info.get('Time')
                    if time:
                        car_data = {'Time': time, 'Driver': playerName, 'Car': player_info['Car']}
                        vv_data.append(car_data)
           
            elif categories == 'STRace':
                w = 3.25
                l = 2
                t = 0.5

                wins = player_info.get('Wins', 0)
                losses = player_info.get('Losses', 0)
                total_races = wins + losses
                stRace = ((w * wins)-(l * losses) + (t * total_races)) if total_races > 0 else 0
                score = round(stRace * 100)/100
                
                if score:
                    stRace_data.append({'Driver': playerName, 'Score': score, 'Wins': wins, 'Losses': losses})
                    
            elif categories == 'Arrests':
                arrests = player_info.get('Arrests')
                
                if arrests:
                    arrests_data.append({'Driver': playerName, 'Arrests': arrests})
            
            elif categories == 'Theft':
                theft = player_info.get('Theft')
                
                if theft:
                    theft_data.append({'Driver': playerName, 'Theft': theft})
            
            elif categories == 'Drift':
                drift = player_info.get('Drift')
                
                if drift:
                    drift_data.append({'Driver': playerName, 'Drift': drift})
            
            elif categories == 'Overtake':
                overtake = player_info.get('Overtake')
                
                if overtake:
                    overtake_data.append({'Driver': playerName, 'Overtake': overtake})
            
            elif categories == 'Getaway':
                getaway = player_info.get('Getaway')
                
                if getaway:
                    getaway_data.append({'Driver': playerName, 'Getaways': getaway})

    h1_data_c.sort(key=itemgetter('Time'))
    vv_data.sort(key=itemgetter('Time'))
    stRace_data.sort(key=itemgetter('Score'), reverse=True)
    arrests_data.sort(key=itemgetter('Arrests'), reverse=True)
    theft_data.sort(key=itemgetter('Theft'), reverse=True)
    drift_data.sort(key=itemgetter('Drift'), reverse=True)
    overtake_data.sort(key=itemgetter('Overtake'), reverse=True)
    getaway_data.sort(key=itemgetter('Getaways'), reverse=True)

    total_points = {}

    def calculate_points(position):
        return 400 - (position - 1) * 20 if position <= 20 else 10

    categories = [h1_data_c, vv_data, stRace_data, arrests_data, theft_data, drift_data, overtake_data, getaway_data]

    for category in categories:
        added_player_infos = set()
        leaderboard_position = 1

        for data in category:
            driver = data['Driver']
            if driver not in added_player_infos:
                points = calculate_points(leaderboard_position)
                total_points[driver] = total_points.get(driver, 0) + points
                added_player_infos.add(driver)
                leaderboard_position += 1

    leaderboard = sorted([{ 'Driver': driver, 'Points': points } for driver, points in total_points.items()], key=itemgetter('Points'), reverse=True)

    db.reference('/Leaderboards/HORIZON').set(leaderboard)
    db.reference('/Leaderboards/Class C - H1').set(h1_data_c)
    db.reference('/Leaderboards/Velocity Vendetta').set(vv_data)
    db.reference('/Leaderboards/Street Racing').set(stRace_data)
    db.reference('/Leaderboards/Arrestations').set(arrests_data)
    db.reference('/Leaderboards/Car Thefts').set(theft_data)
    db.reference('/Leaderboards/Drift').set(drift_data)
    db.reference('/Leaderboards/Overtake').set(overtake_data)
    db.reference('/Leaderboards/Most Wanted').set(getaway_data)
