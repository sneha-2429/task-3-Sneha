from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# CREATE Student
@app.route('/students', methods=['POST'])
def add_student():

    data = request.get_json()

    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({
            "message": "Name and Age are required"
        }), 400

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students(name, age) VALUES (?, ?)",
        (name, age)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student Added Successfully"
    }), 201


# READ Students
@app.route('/students', methods=['GET'])
def get_students():

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    conn.close()

    students = []

    for row in rows:
        students.append({
            "id": row[0],
            "name": row[1],
            "age": row[2]
        })

    return jsonify(students)


# UPDATE Student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):

    data = request.get_json()

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET name=?, age=? WHERE id=?",
        (data['name'], data['age'], id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student Updated Successfully"
    })


# DELETE Student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student Deleted Successfully"
    })


if __name__ == '__main__':
    app.run(debug=True)