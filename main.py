from dataclasses import asdict
import sqlite3

from model import Student, Teacher, Klasse
from populate import PersonenGenerator, read_names
import db_helpers  # noqa: F401


def create_tables(conn: sqlite3.Connection) -> None:
    with conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS students 
                     (student_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, date_of_birth TEXT, class_id INTEGER FOREIGNKEY)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS teachers 
                     (teacher_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, date_of_birth TEXT, subjects TEXT, leitet_klasse_id INTEGER FOREIGNKEY)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS klassen 
                     (klassen_id INTEGER PRIMARY KEY, name TEXT NOT NULL, grade INTEGER NOT NULL, klassenlehrer_id INTEGER FOREIGNKEY)""")


def create_or_fetch(conn: sqlite3.Connection, person: Student | Teacher) -> None:
    if isinstance(person, Student):
        _create_or_fetch_student(conn, person)
    elif isinstance(person, Teacher):
        _create_or_fetch_teacher(conn, person)


def _create_or_fetch_student(conn: sqlite3.Connection, student: Student) -> None:
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE first_name = :first_name AND date_of_birth = :date_of_birth",
            asdict(student),
        )
        db_student = cursor.fetchone()
        if db_student:
            student.student_id = db_student[0]
        else:
            cursor.execute(
                """INSERT INTO students VALUES (:student_id, :first_name, :date_of_birth, :class_id)""",
                asdict(student),
            )
            student.student_id = cursor.lastrowid


def _create_or_fetch_teacher(conn: sqlite3.Connection, teacher: Teacher) -> None:
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM teachers WHERE first_name = :first_name AND date_of_birth = :date_of_birth",
            asdict(teacher),
        )
        db_student = cursor.fetchone()
        if db_student:
            teacher.teacher_id = db_student[0]
        else:
            teacher_dict = asdict(teacher)
            teacher_dict["subjects"] = ",".join(teacher.subjects)
            cursor.execute(
                """INSERT INTO teachers VALUES (:teacher_id, :first_name, :date_of_birth, :subjects, :leitet_klasse_id)""",
                teacher_dict,
            )
            teacher.teacher_id = cursor.lastrowid


def main():
    print("Hello from dbtut!")
    conn = sqlite3.connect("tutorial.db")
    create_tables(conn)

    pg = PersonenGenerator(read_names("names.csv"))
    for _ in range(3):
        t = pg.random_person(is_student=False)
        t = Teacher(first_name=t["name"], date_of_birth=t["birthday"], subjects=[])
        create_or_fetch(conn, t)
    for _ in range(3):
        s = pg.random_person(is_student=True)
        s = Student(first_name=s["name"], date_of_birth=s["birthday"])
        create_or_fetch(conn, s)

    print("Students:")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY date_of_birth ASC")
    for r in cursor.fetchall():
        print(r)

    print()
    print("Teachers:")
    cursor.execute("SELECT * FROM teachers")
    for r in cursor.fetchall():
        print(r)

    conn.close()


if __name__ == "__main__":
    main()
