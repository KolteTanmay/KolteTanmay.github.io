from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT,
                  category TEXT,
                  deadline TEXT,
                  status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

init_db()

# Home Page - Read all tasks
@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add Task
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        deadline = request.form['deadline']

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title, description, category, deadline) VALUES (?, ?, ?, ?)",
                  (title, description, category, deadline))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit Task
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        deadline = request.form['deadline']
        status = request.form['status']
        
        print(status)
        
        c.execute("UPDATE tasks SET title=?, description=?, category=?, deadline=?, status=? WHERE id=?",
                  (title, description, category, deadline, status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    c.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    conn.close()
    return render_template('edit.html', task=task)

# Delete Task
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
