from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/api/games")
def get_games():
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        auth_plugin="caching_sha2_password"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Games")
    games = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(games)

if __name__ == "__main__":
    app.run(debug=True)
