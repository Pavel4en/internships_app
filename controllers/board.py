from app import app
from flask import render_template, request, redirect, session
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('inter.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/internships')
def internships():
    if 'user_id' in session:
        user_id = session['user_id']
        user_type = session['user_type']
        if user_type == 'customer':
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM Traineeship"
            cursor.execute(query)
            internships = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('internships.html', internships=internships)
    return redirect('/login')
