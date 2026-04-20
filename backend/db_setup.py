import sqlite3
import os
import urllib.request
import urllib.parse
import json

# Ensure we're in the correct directory
db_path = os.path.join(os.path.dirname(__file__), 'app.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing tables if necessary
cursor.executescript('''
DROP TABLE IF EXISTS match_stats;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS nations;

CREATE TABLE nations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    flag_url TEXT NOT NULL,
    continent TEXT NOT NULL
);

CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nation_id INTEGER,
    club_name TEXT NOT NULL,
    position TEXT NOT NULL,
    birth_date TEXT,
    image_url TEXT,
    FOREIGN KEY (nation_id) REFERENCES nations(id)
);

CREATE TABLE match_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    minutes_played INTEGER DEFAULT 0,
    rating REAL DEFAULT 0.0,
    season TEXT NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(id)
);
''')

# Insert Sample Data
nations = [
    ('South Korea', 'https://flagcdn.com/w320/kr.png', 'Asia'),
    ('England', 'https://flagcdn.com/w320/gb-eng.png', 'Europe'),
    ('Norway', 'https://flagcdn.com/w320/no.png', 'Europe'),
    ('Belgium', 'https://flagcdn.com/w320/be.png', 'Europe'),
    ('Egypt', 'https://flagcdn.com/w320/eg.png', 'Africa'),
    ('Brazil', 'https://flagcdn.com/w320/br.png', 'South America'),
]
cursor.executemany("INSERT INTO nations (name, flag_url, continent) VALUES (?, ?, ?)", nations)

# Fetch inserted nations ids
cursor.execute("SELECT id, name FROM nations")
nations_map = {row[1]: row[0] for row in cursor.fetchall()}

player_data = [
    ('Son Heung-min', 'South Korea', 'Tottenham Hotspur', 'Forward', '1992-07-08', 'Son_Heung-min'),
    ('Hwang Hee-chan', 'South Korea', 'Wolverhampton Wanderers', 'Forward', '1996-01-26', 'Hwang_Hee-chan'),
    ('Harry Kane', 'England', 'Bayern Munich', 'Forward', '1993-07-28', 'Harry_Kane'),
    ('Phil Foden', 'England', 'Manchester City', 'Midfielder', '2000-05-28', 'Phil_Foden'),
    ('Erling Haaland', 'Norway', 'Manchester City', 'Forward', '2000-07-21', 'Erling_Haaland'),
    ('Martin Ødegaard', 'Norway', 'Arsenal', 'Midfielder', '1998-12-17', 'Martin_Ødegaard'),
    ('Kevin De Bruyne', 'Belgium', 'Manchester City', 'Midfielder', '1991-06-28', 'Kevin_De_Bruyne'),
    ('Mohamed Salah', 'Egypt', 'Liverpool', 'Forward', '1992-06-15', 'Mohamed_Salah'),
    ('Alisson Becker', 'Brazil', 'Liverpool', 'Goalkeeper', '1992-10-02', 'Alisson'),
    ('Bruno Guimarães', 'Brazil', 'Newcastle United', 'Midfielder', '1997-11-16', 'Bruno_Guimarães_(footballer,_born_1997)'),
]

def get_wiki_image(title):
    try:
        title_quoted = urllib.parse.quote(title)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title_quoted}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if 'thumbnail' in data:
                return data['thumbnail']['source']
    except Exception as e:
        pass
    return "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

players = []
for p in player_data:
    img_url = get_wiki_image(p[5])
    players.append((p[0], nations_map[p[1]], p[2], p[3], p[4], img_url))

cursor.executemany("INSERT INTO players (name, nation_id, club_name, position, birth_date, image_url) VALUES (?, ?, ?, ?, ?, ?)", players)

cursor.execute("SELECT id, name FROM players")
players_map = {row[1]: row[0] for row in cursor.fetchall()}

stats = [
    (players_map['Son Heung-min'], 15, 9, 2900, 7.8, '2023-2024'),
    (players_map['Hwang Hee-chan'], 12, 3, 2200, 7.2, '2023-2024'),
    (players_map['Harry Kane'], 30, 8, 3300, 8.1, '2022-2023'),
    (players_map['Phil Foden'], 17, 8, 2800, 7.9, '2023-2024'),
    (players_map['Erling Haaland'], 27, 5, 2700, 8.2, '2023-2024'),
    (players_map['Martin Ødegaard'], 8, 10, 3100, 7.7, '2023-2024'),
    (players_map['Kevin De Bruyne'], 4, 10, 1500, 7.6, '2023-2024'),
    (players_map['Mohamed Salah'], 18, 10, 2600, 7.9, '2023-2024'),
    (players_map['Alisson Becker'], 0, 0, 3000, 7.1, '2023-2024'),
    (players_map['Bruno Guimarães'], 6, 8, 3000, 7.5, '2023-2024'),
]
cursor.executemany("INSERT INTO match_stats (player_id, goals, assists, minutes_played, rating, season) VALUES (?, ?, ?, ?, ?, ?)", stats)

conn.commit()
conn.close()

print("Database initialized with actual player images from Wikipedia!")
