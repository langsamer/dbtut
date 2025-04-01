from dataclasses import asdict, dataclass
import sqlite3


@dataclass
class Student:
    first_name: str
    date_of_birth: str
    student_id: int | None = None  # Primary Key, assigned by DB
    class_id: int | None = None  # Foreign Key


@dataclass
class Teacher:
    first_name: str
    subjects: list[str]
    teacher_id: int | None = None  # Primary Key, assigned by DB
    leitet_klasse_id: int | None = None  # Foreign Key


@dataclass
class Klasse:
    name: str
    grade: int
    klassenlehrer_id: int | None = None  # Foreign Key
    klassen_id: int | None = None


def create_tables(conn: sqlite3.Connection) -> None:
    with conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS students 
                     (student_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, date_of_birth TEXT, class_id INTEGER FOREIGNKEY)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS teachers 
                     (teacher_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, subjects TEXT, leitet_klasse_id INTEGER FOREIGNKEY)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS klassen 
                     (klassen_id INTEGER PRIMARY KEY, name TEXT NOT NULL, grade INTEGER NOT NULL, klassenlehrer_id INTEGER FOREIGNKEY)""")


def create_or_fetch(conn: sqlite3.Connection, student: Student) -> None:
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


def main():
    print("Hello from dbtut!")
    conn = sqlite3.connect("tutorial.db")
    create_tables(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY date_of_birth ASC")
    results = cursor.fetchall()
    for r in results:
        print(r)

    conn.close()


if __name__ == "__main__":
    main()
