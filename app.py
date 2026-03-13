from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_attacks():
    conn = sqlite3.connect("attacks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT ip, attack_type, timestamp FROM attacks ORDER BY id DESC")
    attacks = cursor.fetchall()

    conn.close()
    return attacks


def get_attack_stats():
    conn = sqlite3.connect("attacks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT ip, COUNT(*) FROM attacks GROUP BY ip")
    stats = cursor.fetchall()

    conn.close()
    return stats


@app.route("/")
def dashboard():

    attacks = get_attacks()
    stats = get_attack_stats()

    attack_count = len(attacks)

    labels = [row[0] for row in stats]
    values = [row[1] for row in stats]

    return render_template(
        "dashboard.html",
        attacks=attacks,
        count=attack_count,
        labels=labels,
        values=values
    )


if __name__ == "__main__":
    app.run(debug=True)
