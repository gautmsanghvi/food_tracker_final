from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('food_tracker.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS food (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            name TEXT,
            protein REAL,
            fat REAL,
            carbs REAL,
            calories REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        food_date = request.form['date']
        food_name = request.form['name']
        protein = float(request.form['protein'])
        fat = float(request.form['fat'])
        carbs = float(request.form['carbs'])
        calories = float(request.form['calories'])

        conn = sqlite3.connect('food_tracker.db')
        c = conn.cursor()
        c.execute('INSERT INTO food (date, name, protein, fat, carbs, calories) VALUES (?, ?, ?, ?, ?, ?)',
                  (food_date, food_name, protein, fat, carbs, calories))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = sqlite3.connect('food_tracker.db')
    c = conn.cursor()
    c.execute('SELECT * FROM food WHERE date = ?', (str(date.today()),))
    foods = c.fetchall()
    conn.close()

    total_protein = sum(food[3] for food in foods)
    total_fat = sum(food[4] for food in foods)
    total_carbs = sum(food[5] for food in foods)
    total_calories = sum(food[6] for food in foods)

    return render_template('index.html', foods=foods, total_protein=total_protein, total_fat=total_fat, total_carbs=total_carbs, total_calories=total_calories, date=date)

@app.route('/delete/<int:food_id>', methods=['POST'])
def delete(food_id):
    conn = sqlite3.connect('food_tracker.db')
    c = conn.cursor()
    c.execute('DELETE FROM food WHERE id = ?', (food_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

init_db()
if __name__ == '__main__':
    app.run(debug=True)

