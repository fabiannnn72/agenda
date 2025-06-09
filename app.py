from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3, json, os

app = Flask(__name__)
CORS(app)

def conectar():
    con = sqlite3.connect("agenda.db")
    con.row_factory = sqlite3.Row
    return con

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/agenda", methods=["GET"])
def get_agenda():
    con = conectar()
    datos = {f"{r['dia']}_{r['hora']}": json.loads(r['alumnos']) for r in con.execute("SELECT * FROM agenda")}
    return jsonify(datos)

@app.route("/api/agenda", methods=["POST"])
def save_agenda():
    agenda = request.json
    con = conectar()
    con.execute("DELETE FROM agenda")
    for clave, alumnos in agenda.items():
        dia, hora = clave.split("_")
        con.execute("INSERT INTO agenda (dia, hora, alumnos) VALUES (?, ?, ?)",
                    (dia, hora, json.dumps(alumnos)))
    con.commit()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    if not os.path.exists("agenda.db"):
        con = conectar()
        con.execute("""
        CREATE TABLE agenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dia TEXT,
            hora TEXT,
            alumnos TEXT
        )
        """)
        con.commit()
        con.close()
    app.run(debug=True)
