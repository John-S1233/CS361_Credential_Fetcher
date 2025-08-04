from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

DATABASE = 'credentials.db'

"""
fetch bobs data : 
    curl "http://localhost:8000/fetch_creds?uId=2&acc_token=token2"
fetch Alice's data:
    curl "http://localhost:8000/fetch_creds?uId=1&acc_token=token1"

"""

# ID, Token Pairs for each user
USER_TOKENS = {
    '1': 'token1',
    '2': 'token2',
}

# Admin token
ADMIN_TOKEN = 'admin-token'

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE credentials (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                account TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Dummy data
        users = [
            (1, 'Alice', 'ACCT123', 'password123'),
            (2, 'Bob', 'ACCT456', 'securePass'),
        ]

        c.executemany(
            'INSERT INTO credentials (id, name, account, password) VALUES (?, ?, ?, ?)',
            users
        )
        conn.commit()
        conn.close()

# Get a SQLite database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
CORS(app)

@app.before_request
def setup():
    init_db()

# Validate token, UID alignment
def validate_token(uId, token):
    return USER_TOKENS.get(str(uId)) == token

# Retrieve a specific user's bank credentials.
@app.route('/fetch_creds', methods=['GET'])
def fetch_creds():
    uId = request.args.get('uId')
    token = request.args.get('acc_token')
    if not uId or not token:
        return jsonify({'error': 'Missing parameters.'}), 400
    if not validate_token(uId, token):
        return jsonify({'error': 'Unauthorized.'}), 401
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        'SELECT name, account, password FROM credentials WHERE id = ?',
        (uId,)
    )
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row)), 200
    else:
        return jsonify({'error': 'User not found.'}), 404
    

# Retrieve all stored bank credentials (admin only).
@app.route('/fetch_all_creds', methods=['GET'])
def fetch_all_creds():
    token = request.args.get('acc_token')
    if not token:
        return jsonify({'error': 'Missing access token.'}), 400
    if token != ADMIN_TOKEN:
        return jsonify({'error': 'Unauthorized.'}), 401
    conn = get_db_connection()
    creds = conn.execute(
        'SELECT id, name, account, password FROM credentials'
    ).fetchall()
    conn.close()
    result = [dict(row) for row in creds]
    return jsonify(result), 200

if __name__ == '__main__':
    # Run the service
    app.run(host='0.0.0.0', port=8000, debug=False)
