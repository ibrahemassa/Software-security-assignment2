from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_db():
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

def connect_db():
    return sqlite3.connect('users.db')

@app.route('/')
def home():
    with connect_db() as db:
        db_cursor = db.cursor()
        db_cursor.execute('SELECT * FROM users')
        # users_info = db_cursor.fetchall()
    return render_template('index.html', message=None)

@app.route('/<message>')
def home_message(message):
    return render_template('index.html', message=message)

@app.route('/signup', methods=['POST'])
def add():
    new_username = request.form['username']
    new_password = request.form['password']
    with connect_db() as db:
        db_cursor = db.cursor()
        db_cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (new_username, new_password))
        db.commit()
    return redirect(url_for('home_message', message='User added successfully.'))

def safe(input):
    for c in input:
        if not (c.isdigit() or c.isalpha() or c == '_'):
            return False
    return True

@app.route('/login', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if not safe(username) or not safe(password):
        return redirect(url_for('home_message', message='Invalid username or password'))
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    with connect_db() as db:
        db_cursor = db.cursor()
        db_cursor.execute(query)
        user = db_cursor.fetchone()
    if user:
        return render_template('account.html', user=user[1])
    else:
        return redirect(url_for('home_message', message='Invalid username or password!'))

if __name__ == "__main__":
    create_db()
    app.run(debug=True)
