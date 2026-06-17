from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# ---------------- GRADE CALCULATOR ----------------

def calculate_grade(marks):

    if marks >= 90:
        return "A+"

    elif marks >= 80:
        return "A"

    elif marks >= 70:
        return "B"

    elif marks >= 60:
        return "C"

    else:
        return "F"


# ---------------- HOME PAGE ----------------

@app.route('/')
def home():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(marks) FROM students")
    avg_marks = cursor.fetchone()[0]

    if avg_marks is None:
        avg_marks = 0

    cursor.execute("""
        SELECT name, marks
        FROM students
        ORDER BY marks DESC
        LIMIT 1
    """)

    topper = cursor.fetchone()

    conn.close()

    return render_template(
        "index.html",
        total_students=total_students,
        avg_marks=round(avg_marks, 2),
        topper=topper
    )


# ---------------- ADD STUDENT ----------------

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        # Student Details
        student_id = int(request.form['id'])
        name = request.form['name']
        age = int(request.form['age'])
        university = request.form['university']
        subject = request.form['subject']
        marks = int(request.form['marks'])

        # Grade Calculation
        percentage = marks
        grade = calculate_grade(marks)

        # Fee Details
        total_fees = float(request.form['total_fees'])
        fees_paid = float(request.form['fees_paid'])

        remaining_fees = total_fees - fees_paid

        if remaining_fees <= 0:
            payment_status = "Paid"
            remaining_fees = 0
        else:
            payment_status = "Pending"

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:

            cursor.execute("""
            INSERT INTO students
            (
                id,
                name,
                age,
                university,
                subject,
                marks,
                percentage,
                grade,
                total_fees,
                fees_paid,
                remaining_fees,
                payment_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                name,
                age,
                university,
                subject,
                marks,
                percentage,
                grade,
                total_fees,
                fees_paid,
                remaining_fees,
                payment_status
            ))

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()
            return "Student ID already exists!"

        conn.close()

        return redirect('/students')

    return render_template('add_student.html')


# ---------------- VIEW STUDENTS ----------------

@app.route('/students')
def students():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY marks DESC
    """)

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'students.html',
        students=students
    )


# ---------------- SEARCH STUDENT ----------------

@app.route('/search', methods=['GET', 'POST'])
def search():

    student = None

    if request.method == 'POST':

        sid = request.form['id']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE id=?",
            (sid,)
        )

        student = cursor.fetchone()

        conn.close()

    return render_template(
        'search_student.html',
        student=student
    )


# ---------------- ANALYTICS ----------------

@app.route('/analytics')
def analytics():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(marks) FROM students")
    avg_marks = cursor.fetchone()[0]

    if avg_marks is None:
        avg_marks = 0

    cursor.execute("SELECT MAX(marks) FROM students")
    highest_marks = cursor.fetchone()[0]

    if highest_marks is None:
        highest_marks = 0

    cursor.execute("""
        SELECT name, marks
        FROM students
        ORDER BY marks DESC
        LIMIT 1
    """)

    topper = cursor.fetchone()

    conn.close()

    return render_template(
        "analytics.html",
        total_students=total_students,
        avg_marks=round(avg_marks, 2),
        highest_marks=highest_marks,
        topper=topper
    )


# ---------------- DELETE STUDENT ----------------

@app.route('/delete/<int:id>')
def delete_student(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/students')


# ---------------- RUN APP ----------------

if __name__ == '__main__':
    app.run(debug=True)
    