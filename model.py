from dataclasses import dataclass


@dataclass
class Student:
    first_name: str
    date_of_birth: str
    student_id: int | None = None  # Primary Key, assigned by DB
    class_id: int | None = None  # Foreign Key


@dataclass
class Teacher:
    first_name: str
    date_of_birth: str
    subjects: list[str]
    teacher_id: int | None = None  # Primary Key, assigned by DB
    leitet_klasse_id: int | None = None  # Foreign Key


@dataclass
class Klasse:
    name: str
    grade: int
    klassenlehrer_id: int | None = None  # Foreign Key
    klassen_id: int | None = None
