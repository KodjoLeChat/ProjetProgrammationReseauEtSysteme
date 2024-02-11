from flask import Flask, render_template, redirect, url_for, request, jsonify
import psycopg2
import psycopg2
import bcrypt
import secrets
 
# dbname=postgres
# user=kaiserv_user
# password=kaiserv_mdp
# host=localhost
# port=5432

class UserAuthAPI:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS player (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                token VARCHAR(255)
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        ''')

        
        self.create_user('awa', '123456')
        self.create_user('ayet', '123456')
        self.create_user('philémon', '123456')
        self.create_user('rayane', '123456')
        self.create_user('peres', '123456')

        self.create_admin('admin', 'admin_password')

    def create_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('''
            INSERT INTO player (username, password, token)
            VALUES (%s, %s, NULL)
            ON CONFLICT (username) DO NOTHING;
        ''', (username, hashed_password.decode('utf-8')))
        self.conn.commit()

    def create_admin(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('''
            INSERT INTO admin (username, password)
            VALUES (%s, %s)
            ON CONFLICT (username) DO NOTHING;
        ''', (username, hashed_password.decode('utf-8')))
        self.conn.commit()

    def check_user(self, username, password):
        self.cursor.execute("SELECT * FROM player WHERE username=%s", (username,))
        result = self.cursor.fetchone()

        if result:
            stored_password = result[2]  
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                token = secrets.token_urlsafe(32)
                self.cursor.execute("UPDATE player SET token=%s WHERE id=%s", (token, result[0]))
                self.conn.commit()
                return token

        return None
    

    def check_admin(self, username, password):
        self.cursor.execute("SELECT * FROM admin WHERE username=%s", (username,))
        result = self.cursor.fetchone()

        if result:
            stored_password = result[2] 
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True

        return False

    def check_token(self, username, token):
        self.cursor.execute("SELECT * FROM player WHERE username=%s AND token=%s", (username, token))
        result = self.cursor.fetchone()

        if result:
            return True

        return False
    
    def get_all_players(self):
        self.cursor.execute("SELECT * FROM player")
        players = self.cursor.fetchall()
        return players

    def delete_player(self, player_id):
        self.cursor.execute("DELETE FROM player WHERE id=%s", (player_id,))
        self.conn.commit()

app = Flask(__name__)
user_auth_api = UserAuthAPI(dbname="postgres", user="kaiserv_user", password="kaiserv_mdp", host="localhost", port="5432")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if user_auth_api.check_admin(username, password):
        players = user_auth_api.get_all_players()
        return render_template('admin_dashboard.html', players=players)
    else:
        return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('index'))


@app.route('/delete_player/<int:player_id>')
def delete_player(player_id):
    user_auth_api.delete_player(player_id)
    players = user_auth_api.get_all_players()
    return render_template('admin_dashboard.html', players=players)
@app.route('/check_user', methods=['POST'])
def check_user_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(username, password)

    if username and password:
        result = user_auth_api.check_user(username, password)
        return jsonify({'token': result})
    else:
        return jsonify({'token': None})

@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.form
    new_username = data.get('new_username')
    new_password = data.get('new_password')

    if new_username and new_password:
        user_auth_api.create_user(new_username, new_password)

    players = user_auth_api.get_all_players()
    return render_template('admin_dashboard.html', players=players)


@app.route('/check_token', methods=['POST'])
def check_token_route():
    data = request.get_json()
    username = data.get('username')
    token = data.get('token')

    if username and token:
        result = user_auth_api.check_token(username, token)
        return jsonify({'valid': result})
    else:
        return jsonify({'valid': False})


if __name__ == '__main__':
    app.run(debug=True)
