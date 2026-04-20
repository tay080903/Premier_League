from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

@app.route('/')
def index():
    return app.send_static_file('index.html')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_stats():
    conn = get_db_connection()
    c = conn.cursor()
    # Global hitmap stats (number of players per country)
    c.execute('''
        SELECT n.name, n.continent, COUNT(p.id) as player_count
        FROM nations n
        LEFT JOIN players p ON n.id = p.nation_id
        GROUP BY n.id
    ''')
    hitmap_data = [dict(row) for row in c.fetchall()]
    
    # Top performers (based on rating)
    c.execute('''
        SELECT p.id, p.name, p.club_name, p.position, p.image_url, m.rating, m.goals, m.assists, n.flag_url, n.name as nation_name
        FROM players p
        JOIN match_stats m ON p.id = m.player_id
        JOIN nations n ON p.nation_id = n.id
        ORDER BY m.rating DESC
        LIMIT 5
    ''')
    top_performers = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return jsonify({
        "hitmap": hitmap_data,
        "top_performers": top_performers
    })

@app.route('/api/nations', methods=['GET'])
def get_nations():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT n.id, n.name, n.flag_url, n.continent, 
               COUNT(p.id) as player_count,
               SUM(COALESCE(m.goals, 0)) as total_goals,
               SUM(COALESCE(m.assists, 0)) as total_assists
        FROM nations n
        LEFT JOIN players p ON n.id = p.nation_id
        LEFT JOIN match_stats m ON p.id = m.player_id
        GROUP BY n.id
    ''')
    nations = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(nations)

@app.route('/api/players', methods=['GET'])
def get_players():
    nation_id = request.args.get('nation_id')
    
    conn = get_db_connection()
    c = conn.cursor()
    
    query = '''
        SELECT p.id, p.name, p.club_name, p.position, p.birth_date, p.image_url,
               n.flag_url, n.name as nation_name,
               m.goals, m.assists, m.minutes_played, m.rating, m.season
        FROM players p
        JOIN nations n ON p.nation_id = n.id
        LEFT JOIN match_stats m ON p.id = m.player_id
    '''
    params = []
    
    if nation_id:
        query += " WHERE n.id = ?"
        params.append(nation_id)
        
    query += " ORDER BY p.name ASC"
        
    c.execute(query, params)
    players = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return jsonify(players)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
