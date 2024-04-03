from flask import Flask, request
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect('data\dataPoint.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS markers (id INTEGER, name TEXT, description TEXT, lat REAL, lng REAL)")


@app.route('/postPlayerChoice', methods=['POST'])
def post():
    cursor.execute('SELECT * FROM player_choice')
    rows = cursor.fetchall()

    db_dict = {}
    for row in rows:
        db_dict[row[0].strip()] = row[1]

    data = request.form
    for key in data:
        if key in db_dict.keys():
            sql = f"UPDATE player_choice SET amount = {int(db_dict[key]) + int(data[key])} WHERE name = '{key}'"
            cursor.execute(sql)
        else:
            sql = f"INSERT INTO player_choice (name, amount) VALUES('{key}', {data[key]})"
            cursor.execute(sql)

        connection.commit()

    return request.form


if __name__ == '__main__':
    app.run(debug=True)