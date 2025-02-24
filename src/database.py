import sqlite3
# import data_getter

# all_tournaments_with_data = data_getter.return_tournaments_with_data()

conn = sqlite3.connect("tournaments.db")
cursor = conn.cursor()

def create_database_tables():
    for index in range(len(all_tournaments_with_data)):
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {list(all_tournaments_with_data.keys())[index]} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                tournament_date TEXT,
                regis_start_date TEXT,
                regis_end_date TEXT,
                draw_date TEXT,
                street TEXT, 
                plz TEXT,
                link TEXT
            );
        """)

    conn.commit()


def insert_tournament_data_into_tables():
    for age_class, tournaments in all_tournaments_with_data.items():
        for tournament in tournaments:
            cursor.execute(f"""
                INSERT INTO {age_class} (title, tournament_date, regis_start_date, regis_end_date, draw_date, street, plz, link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                tournament["tournament_title"],
                tournament["tournament_dates"]["tournament_date"],
                tournament["tournament_dates"]["tournament_registration_start"],
                tournament["tournament_dates"]["tournament_registration_end"],
                tournament["tournament_dates"]["tournament_draw_date"],
                tournament["tournament_location"]["tournament_street"],
                tournament["tournament_location"]["tournament_plz"],
                tournament["tournament_link"]
            ))

    conn.commit()


def delete_already_passed_tournaments():
    tournament_dates_age_class = {     
        "M18": [],
        "M16": [],
        "M14": [],
        "M13": [],
        "M12": [],
        "M11": [],

        "W18": [],
        "W16": [],
        "W14": [],
        "W13": [],
        "W12": [],
        "W11": []
    }
    
    for age_class, age_class_array in tournament_dates_age_class.items():
        cursor.execute(f"SELECT tournament_date FROM {age_class}")
        dates = cursor.fetchall()

        for date in dates:
            age_class_array.append(str(date)[15:-3])

    conn.commit()

    
def main():
    # create_database_tables()
    delete_already_passed_tournaments()
    # insert_tournament_data_into_tables()


main()
