## =========================== ##
## generate-data-v3.py
## =========================== ##

# Created by Gemini, adapted by Régis KLA
# Addition of seconds generation compared to v1

# To run 
# (...)$ cd notebooks/data/gemini-generated-data
# (...)$ python generate-data-v3.py -d1 20/03/2025 -d2 25/03/2025 

import pandas as pd
import random
import argparse
from datetime import datetime, timedelta

def generate_synthetic_data(date_str, num_records):
    """Generates synthetic business data with seconds."""

    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    data = []
    used_arrival_times = set()
    used_departure_times = set()

    for _ in range(num_records):
        camion_id = random.randint(1000, 9999)
        pcj_id = random.randint(1, 3)
        destination = random.choice(["Burkina Faso", "Togo"])
        origine = "Burkina Faso" if destination == "Togo" else "Togo"

        while True:                        
            # Weighted random choice for arrival time
            time_ranges = [
                (5, 7), (7, 8), (8, 10), (10, 14), (14, 16), (16, 21)
            ]
            weights = [1, 3, 4, 2, 2, 1]  # the highest the number, the higher the probability. 

            chosen_range = random.choices(time_ranges, weights=weights)[0]
            arrival_hour = random.randint(chosen_range[0], chosen_range[1] -1) if chosen_range[1] != 21 else 20
            arrival_minute = random.randint(0, 59)
            arrival_second = random.randint(0, 59)
            arrival_time = datetime(date_obj.year, date_obj.month, date_obj.day, arrival_hour, arrival_minute, arrival_second)
            if arrival_time.time() not in used_arrival_times:
                used_arrival_times.add(arrival_time.time())
                break

        while True:
            departure_hour = random.randint(5, 20)
            departure_minute = random.randint(0, 59)
            departure_second = random.randint(0, 59)
            departure_time = datetime(date_obj.year, date_obj.month, date_obj.day, departure_hour, departure_minute, departure_second)
            if departure_time.time() not in used_departure_times:
                used_departure_times.add(departure_time.time())
                break

        categorie = random.choice([
            "Camion plein", "Autocar de 56 à 75 places", "Camion vide",
            "Camion citerne vide", "Camion citerne plein", "Autocar de 36 à 55 places",
            "Véhicule de moins de 09 places", "Autocar de 15 à 35 places",
            "Véhicule ou autocar de 09 à 14 places"
        ])

        data.append({
            "Camion ID": camion_id,
            "PCJ ID": pcj_id,
            "Heure Arrivée": arrival_time.strftime("%d/%m/%Y %H:%M:%S"),
            "Heure Départ": departure_time.strftime("%d/%m/%Y %H:%M:%S"),
            "Destination": destination,
            "Origine": origine,
            "Categorie": categorie
        })

    return pd.DataFrame(data)

def daterange(start, end):
    assert end >= start
    return [start + timedelta(n) for n in range(int((end - start).days) + 1)]

## 
## __main__
## 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='generate-data-v3',
        description='Generate synthetic business data',
        epilog='End of help.')

    # mandatory d1
    parser.add_argument("-d1", "--date1", help="Start date, format = DD/MM/YYYY", required=True)

    # optional d2 
    parser.add_argument("-d2", "--date2", help="End date, format = DD/MM/YYYY", required=False)

    # Read cmd line
    args = parser.parse_args()

    # output file
    filename = "synthetic_business_data_v3.csv"

    start_date = datetime.strptime(args.date1, "%d/%m/%Y")
    df = None
    nb_records_generated = 0
    num_records_to_generate = random.randint(800, 1100) #Generate a random number of records within the requested range.

    if args.date2:

        end_date = datetime.strptime(args.date2, "%d/%m/%Y")
        days_between = daterange(start_date, end_date)

        sub_df = []
        for day in days_between:
            sub_df.append(generate_synthetic_data(day.strftime("%d/%m/%Y"), num_records_to_generate))
            nb_records_generated += num_records_to_generate

        df = pd.concat(sub_df)
        filename = "synthetic_business_data_v3_{}_{}.csv".format(args.date1.replace("/", "-"), args.date2.replace("/", "-"))
    
    else:      
        df = generate_synthetic_data(args.date1, num_records_to_generate)
        nb_records_generated = num_records_to_generate
        filename = "synthetic_business_data_v3_{}.csv".format(args.date1.replace("/", "-"))

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"[INFO] Generated {nb_records_generated} records and saved to {filename}")



